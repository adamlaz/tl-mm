#!/usr/bin/env python3
"""Extract sprint retrospective content from Confluence and build aggregated summary."""

import json
import os
import re
import sys
import time
from collections import defaultdict
from datetime import datetime
from html.parser import HTMLParser

import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv(".env.local")

CONFLUENCE_URL = os.environ.get("ATLASSIAN_URL", "https://madmobile-eng.atlassian.net")
AUTH = HTTPBasicAuth(
    os.environ.get("ATLASSIAN_EMAIL", "adam.lazarus@madmobile.com"),
    os.environ["ATLASSIAN_TOKEN"],
)
HEADERS = {"Accept": "application/json"}
API_DELAY = 0.5

OUT_DIR = "inventory/confluence"
CONTENT_DIR = os.path.join(OUT_DIR, "content")
os.makedirs(CONTENT_DIR, exist_ok=True)


class HTMLTextExtractor(HTMLParser):
    """Strip HTML tags, preserving basic structure with newlines."""

    def __init__(self):
        super().__init__()
        self._parts = []
        self._block_tags = {
            "p", "div", "br", "h1", "h2", "h3", "h4", "h5", "h6",
            "li", "tr", "table", "thead", "tbody", "blockquote", "hr",
        }

    def handle_starttag(self, tag, attrs):
        if tag in self._block_tags:
            self._parts.append("\n")
        if tag == "li":
            self._parts.append("  • ")

    def handle_endtag(self, tag):
        if tag in self._block_tags:
            self._parts.append("\n")

    def handle_data(self, data):
        self._parts.append(data)

    def get_text(self):
        text = "".join(self._parts)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()


def html_to_text(html):
    parser = HTMLTextExtractor()
    parser.feed(html or "")
    return parser.get_text()


def api_get(path, params=None):
    url = f"{CONFLUENCE_URL}{path}" if path.startswith("/") else path
    resp = requests.get(url, auth=AUTH, headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json()


def search_retros():
    """Search Confluence for retrospective pages using CQL."""
    cql = (
        '(title ~ "Review & Retrospective" '
        'OR title ~ "Review / Retrospective" '
        'OR title ~ "Sprint Retrospective") '
        'AND lastModified > "2024-01-01" '
        'AND type = "page"'
    )
    params = {
        "cql": cql,
        "limit": 50,
        "orderby": "lastModified desc",
    }
    print(f"Searching: {cql[:80]}...")
    data = api_get("/wiki/rest/api/content/search", params=params)
    results = data.get("results", [])
    print(f"  Found {len(results)} retrospective pages")
    return results


def fetch_page(page_id):
    """Fetch full page content with body, space, and version info."""
    return api_get(
        f"/wiki/rest/api/content/{page_id}",
        params={"expand": "body.storage,space,version"},
    )


def extract_section(text, heading_pattern, max_chars=2000):
    """Extract text under a heading that matches the pattern."""
    match = re.search(heading_pattern, text, re.IGNORECASE)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"\n[A-Z][A-Za-z\s/&]{2,}\n", text[start:])
    end = start + next_heading.start() if next_heading else start + max_chars
    return text[start:end].strip()


def extract_goals(text):
    """Pull sprint goals / objectives from the page text."""
    for pattern in [
        r"(?:Sprint\s+)?Goals?\s*[\n:]",
        r"Objectives?\s*[\n:]",
        r"What we(?:'re| are) working on\s*[\n:]",
        r"Commitments?\s*[\n:]",
    ]:
        section = extract_section(text, pattern, max_chars=1500)
        if section and len(section) > 10:
            return section
    return ""


def extract_sprint_name(title, text):
    """Derive sprint/PI name from the page title or overview section."""
    pi_match = re.search(r"(PI\s*\d+(?:\.\d+)?)", title, re.IGNORECASE)
    if pi_match:
        return pi_match.group(1).strip()
    sprint_match = re.search(r"(Sprint\s+\d+)", title, re.IGNORECASE)
    if sprint_match:
        return sprint_match.group(1).strip()
    overview = extract_section(text, r"Overview\s*[\n:]", max_chars=500)
    pi_match = re.search(r"(PI\s*\d+(?:\.\d+)?)", overview, re.IGNORECASE)
    if pi_match:
        return pi_match.group(1).strip()
    return ""


def extract_team(title, space_name):
    """Extract team name from title or space."""
    team_tokens = [
        "MIRA", "LEO", "Castor", "NOVA", "Apollo", "Vega", "DRAC",
        "Thor", "HULK", "Phoenix", "Taur", "Libra", "Pollux", "Maui",
        "Kenworth", "Wolverine",
    ]
    for t in team_tokens:
        if t.lower() in title.lower():
            return t.upper()
    return space_name


def extract_theme(text, goals):
    """Try to find a main sprint theme or summarize from goals."""
    for pattern in [r"Theme\s*[:\n]", r"Main\s+Theme\s*[:\n]", r"Focus\s+Area\s*[:\n]"]:
        theme = extract_section(text, pattern, max_chars=500)
        if theme and len(theme) > 5:
            return theme.split("\n")[0].strip()
    if goals:
        first_line = goals.strip().split("\n")[0]
        return first_line[:200].strip("•- ").strip()
    return ""


def common_phrases(all_goals, top_n=15):
    """Extract the most common meaningful phrases from goals text."""
    stop = {
        "the", "and", "for", "with", "this", "that", "from", "will", "are",
        "was", "has", "have", "been", "not", "but", "they", "our", "all",
        "can", "their", "into", "also", "should", "need", "get", "per",
        "new", "any", "each", "more", "some", "when", "what", "which",
    }
    words = re.findall(r"[a-zA-Z]{3,}", " ".join(all_goals).lower())
    freq = defaultdict(int)
    for w in words:
        if w not in stop:
            freq[w] += 1

    bigrams = defaultdict(int)
    for i in range(len(words) - 1):
        if words[i] not in stop and words[i + 1] not in stop:
            bigrams[f"{words[i]} {words[i+1]}"] += 1

    combined = {**freq, **bigrams}
    ranked = sorted(combined.items(), key=lambda x: -x[1])
    return [(phrase, count) for phrase, count in ranked[:top_n] if count >= 2]


def main():
    errors = []
    retros = []
    all_goals_text = []

    print("=" * 60)
    print("Confluence Retrospective Extraction")
    print("=" * 60)

    try:
        search_results = search_retros()
    except Exception as e:
        print(f"FATAL: Search failed: {e}", file=sys.stderr)
        sys.exit(1)

    to_fetch = search_results[:30]
    print(f"\nFetching content for {len(to_fetch)} pages...\n")

    for i, result in enumerate(to_fetch):
        page_id = result["id"]
        title = result.get("title", "")
        print(f"  [{i+1}/{len(to_fetch)}] {title[:70]}...")

        try:
            page = fetch_page(page_id)
            time.sleep(API_DELAY)
        except Exception as e:
            msg = f"Failed to fetch page {page_id} ({title}): {e}"
            print(f"    ERROR: {msg}")
            errors.append(msg)
            continue

        space = page.get("space", {})
        version = page.get("version", {})
        body_html = page.get("body", {}).get("storage", {}).get("value", "")
        text = html_to_text(body_html)

        content_path = os.path.join(CONTENT_DIR, f"retro_{page_id}.txt")
        with open(content_path, "w") as f:
            f.write(f"Title: {title}\n")
            f.write(f"Space: {space.get('name', '')}\n")
            f.write(f"Modified: {version.get('when', '')}\n")
            f.write(f"URL: {CONFLUENCE_URL}/wiki{result.get('_links', {}).get('webui', '')}\n")
            f.write("=" * 60 + "\n\n")
            f.write(text)

        goals = extract_goals(text)
        sprint_name = extract_sprint_name(title, text)
        team = extract_team(title, space.get("name", ""))
        theme = extract_theme(text, goals)
        modified = version.get("when", "")

        if goals:
            all_goals_text.append(goals)

        retros.append({
            "page_id": page_id,
            "title": title,
            "space_key": space.get("key", ""),
            "space_name": space.get("name", ""),
            "team": team,
            "last_modified": modified,
            "sprint_name": sprint_name,
            "theme": theme,
            "goals_snippet": goals[:500] if goals else "",
            "content_file": f"content/retro_{page_id}.txt",
            "text_length": len(text),
        })

    # --- Aggregation ---
    teams = defaultdict(list)
    for r in retros:
        teams[r["team"]].append(r)

    team_summary = {}
    for team, pages in sorted(teams.items()):
        dates = []
        for p in pages:
            if p["last_modified"]:
                try:
                    dt = datetime.fromisoformat(p["last_modified"].replace("Z", "+00:00"))
                    dates.append(dt)
                except ValueError:
                    pass
        dates.sort()
        team_summary[team] = {
            "count": len(pages),
            "most_recent": dates[-1].isoformat() if dates else "",
            "oldest": dates[0].isoformat() if dates else "",
            "titles": [p["title"] for p in pages],
        }

    phrases = common_phrases(all_goals_text)
    all_dates = []
    for r in retros:
        if r["last_modified"]:
            try:
                all_dates.append(
                    datetime.fromisoformat(r["last_modified"].replace("Z", "+00:00"))
                )
            except ValueError:
                pass
    all_dates.sort()

    output = {
        "extracted_at": datetime.now().isoformat(),
        "total_search_results": len(search_results),
        "total_fetched": len(retros),
        "date_range": {
            "earliest": all_dates[0].isoformat() if all_dates else "",
            "latest": all_dates[-1].isoformat() if all_dates else "",
        },
        "teams": team_summary,
        "common_themes": [{"phrase": p, "count": c} for p, c in phrases],
        "errors": errors,
        "retrospectives": retros,
    }

    out_path = os.path.join(OUT_DIR, "retrospectives.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nWrote {out_path}")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total retros found in search: {len(search_results)}")
    print(f"Successfully fetched:         {len(retros)}")
    if all_dates:
        print(f"Date range:                   {all_dates[0].strftime('%Y-%m-%d')} → {all_dates[-1].strftime('%Y-%m-%d')}")
    print(f"\nRetros per team:")
    for team, info in sorted(team_summary.items(), key=lambda x: -x[1]["count"]):
        recent = info["most_recent"][:10] if info["most_recent"] else "?"
        print(f"  {team:25s}  {info['count']:3d} retros  (latest: {recent})")
    if phrases:
        print(f"\nTop themes/phrases across goals:")
        for phrase, count in phrases[:10]:
            print(f"  {phrase:30s}  ({count}x)")
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
    print()


if __name__ == "__main__":
    main()
