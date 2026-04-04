#!/usr/bin/env python3
"""Extract structured incident/RCA data from Confluence postmortem documents."""

import requests
import json
import os
import re
import time
from datetime import datetime
from collections import Counter, defaultdict
from requests.auth import HTTPBasicAuth
from html.parser import HTMLParser

CONFLUENCE_URL = os.environ.get("ATLASSIAN_URL", "https://madmobile-eng.atlassian.net")
CONFLUENCE_EMAIL = os.environ.get("ATLASSIAN_EMAIL", "adam.lazarus@madmobile.com")
CONFLUENCE_TOKEN = os.environ["ATLASSIAN_TOKEN"]
AUTH = HTTPBasicAuth(CONFLUENCE_EMAIL, CONFLUENCE_TOKEN)
HEADERS = {"Accept": "application/json"}

CATALOG_PATH = "inventory/confluence/postmortem_catalog.json"
OUTPUT_DIR = "inventory/confluence"


class HTMLTableExtractor(HTMLParser):
    """Extract text and table structures from Confluence HTML."""

    def __init__(self):
        super().__init__()
        self.result = []
        self.tables = []
        self._current_table = None
        self._current_row = None
        self._current_cell = []
        self._in_cell = False
        self._tag_stack = []

    def handle_starttag(self, tag, attrs):
        self._tag_stack.append(tag)
        if tag == "table":
            self._current_table = []
        elif tag == "tr" and self._current_table is not None:
            self._current_row = []
        elif tag in ("td", "th") and self._current_row is not None:
            self._in_cell = True
            self._current_cell = []
        elif tag == "br":
            if self._in_cell:
                self._current_cell.append(" ")
            self.result.append(" ")

    def handle_endtag(self, tag):
        if self._tag_stack and self._tag_stack[-1] == tag:
            self._tag_stack.pop()
        if tag in ("td", "th") and self._in_cell:
            self._in_cell = False
            cell_text = " ".join(self._current_cell).strip()
            cell_text = re.sub(r"\s+", " ", cell_text)
            if self._current_row is not None:
                self._current_row.append(cell_text)
        elif tag == "tr" and self._current_row is not None and self._current_table is not None:
            self._current_table.append(self._current_row)
            self._current_row = None
        elif tag == "table" and self._current_table is not None:
            if self._current_table:
                self.tables.append(self._current_table)
            self._current_table = None

    def handle_data(self, data):
        if self._in_cell:
            self._current_cell.append(data)
        self.result.append(data)

    def get_text(self):
        return re.sub(r"\s+", " ", " ".join(self.result)).strip()


def parse_html(html):
    parser = HTMLTableExtractor()
    parser.feed(html or "")
    return parser.get_text(), parser.tables


def api_get(path, params=None):
    url = f"{CONFLUENCE_URL}{path}" if path.startswith("/") else path
    resp = requests.get(url, auth=AUTH, headers=HEADERS, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def extract_page_id(url):
    m = re.search(r"/pages/(\d+)/", url)
    if m:
        return m.group(1)
    m = re.search(r"pageId=(\d+)", url)
    if m:
        return m.group(1)
    return None


INCLUDE_PATTERNS = [
    re.compile(r"\bRCA\b", re.IGNORECASE),
    re.compile(r"POST\s*MORT", re.IGNORECASE),
    re.compile(r"\boutage\b", re.IGNORECASE),
    re.compile(r"\bincident\s+report\b", re.IGNORECASE),
]

EXCLUDE_PATTERNS = [
    re.compile(r"guideline", re.IGNORECASE),
    re.compile(r"\bprocess\b", re.IGNORECASE),
    re.compile(r"retrospective", re.IGNORECASE),
    re.compile(r"\bsprint\b", re.IGNORECASE),
    re.compile(r"\.(mp4|png|pdf|jpg)$", re.IGNORECASE),
    re.compile(r"Root Cause Analysis for Bug", re.IGNORECASE),
    re.compile(r"Bug Root Cause Analysis", re.IGNORECASE),
    re.compile(r"Defect Classification", re.IGNORECASE),
    re.compile(r"Root Cause Analysis For.*Bugs", re.IGNORECASE),
    re.compile(r"Fixes and Root cause$", re.IGNORECASE),
    re.compile(r"root cause detection", re.IGNORECASE),
    re.compile(r"RCA Creation", re.IGNORECASE),
    re.compile(r"Importance of.*RCA", re.IGNORECASE),
    re.compile(r"Hosting a RCA Call", re.IGNORECASE),
    re.compile(r"How to unblock", re.IGNORECASE),
    re.compile(r"Patch Releases.*Root Cause", re.IGNORECASE),
    re.compile(r"Root Cause Classification", re.IGNORECASE),
    re.compile(r"Root Cause Analysis for Bug Tickets", re.IGNORECASE),
    re.compile(r"didn.*identify root cause", re.IGNORECASE),
]

EXCLUDE_URL_PATTERNS = [
    "viewpageattachments",
    "/blog/",
    "/plugins/servlet/",
]

SYSTEM_KEYWORDS = {
    "Payments": ["payment", "payout", "funding", "ach", "vantiv", "worldpay", "express", "litle", "gateway", "batch notification", "ndf", "sdf", "2cp"],
    "Menu": ["menu", "menucore", "menu core", "menu admin", "ems"],
    "Reports": ["report", "timesheet", "report sync", "timesheets"],
    "OLO": ["olo", "online order", "paytronix", "px order", "omnivore"],
    "Guest Manager": ["guest manager", "gm ", "buzztable", "floor map"],
    "Admin Portal": ["admin portal", "admin.cake"],
    "Pulse": ["pulse"],
    "POS": [" pos ", "pos "],
    "Cloud/Infrastructure": ["cloud", "infrastructure", "aws", "rds", "database", "bitbucket", "502", "500 error", "cpu", "esb"],
    "Security": ["security", "twilio", "breach"],
    "Platform": ["platform", "api", "communicator"],
}

TEAM_ALIASES = {
    "Payments": ["payments", "cake payments", "cake payment"],
    "Cloud Services": ["cloud services", "cloud-services", "cs team"],
    "CAKEAPP DC": ["cakeapp dc", "cake apps dc", "cake apps - dc"],
    "CAKEAPP DU": ["cakeapp du", "cake apps du"],
    "CAKEAPP GPS": ["cakeapp gps", "cake apps gps", "cake-gps"],
    "Platform": ["platform", "plat"],
    "DBE": ["dbe", "dba"],
    "Stark": ["stark"],
    "Cloud Engineering": ["cloud engineering", "cce"],
    "Application Support": ["application support", "app support"],
}


def is_incident_doc(doc):
    title = doc.get("title", "")
    url = doc.get("url", "")

    for pat in EXCLUDE_URL_PATTERNS:
        if pat in url:
            return False

    for pat in EXCLUDE_PATTERNS:
        if pat.search(title):
            return False

    for pat in INCLUDE_PATTERNS:
        if pat.search(title):
            return True

    return False


def extract_date_from_title(title):
    """Try to extract an incident date from the title."""
    m = re.search(r"(\d{1,2})[/\-](\d{1,2})[/\-](\d{4})", title)
    if m:
        a, b, year = m.group(1), m.group(2), m.group(3)
        a, b = int(a), int(b)
        if a > 12:
            return f"{year}-{b:02d}-{a:02d}"
        elif b > 12:
            return f"{year}-{a:02d}-{b:02d}"
        return f"{year}-{a:02d}-{b:02d}"

    m = re.search(r"(\d{4})\s*[-/]\s*(\w{3,})\s*[-/]\s*(\d{1,2})", title)
    if m:
        try:
            dt = datetime.strptime(f"{m.group(1)} {m.group(2)} {m.group(3)}", "%Y %b %d")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            pass

    m = re.search(r"(\d{4})\s*-\s*(\d{2})\s*-\s*(\d{2})", title)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"

    return None


def extract_date_from_body(text):
    """Try to extract incident start date from body text."""
    patterns = [
        r"Incident Start Date.*?(\d{1,2})[/\-](\d{1,2})[/\-](\d{4})",
        r"effective as of\s+(\d{4})-(\d{2})-(\d{2})",
        r"Start Time[:\s]*(\d{1,2})[/\-](\d{1,2})[/\-](\d{4})",
        r"Date of the Incident[:\s]*(\d{4})-(\d{2})-(\d{2})",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            groups = m.groups()
            if len(groups[0]) == 4:
                return f"{groups[0]}-{groups[1]}-{groups[2]}"
            a, b, year = int(groups[0]), int(groups[1]), groups[2]
            if a > 12:
                return f"{year}-{b:02d}-{a:02d}"
            elif b > 12:
                return f"{year}-{a:02d}-{b:02d}"
            return f"{year}-{a:02d}-{b:02d}"
    return None


def classify_system(title, text=""):
    combined = (title + " " + text[:500]).lower()
    matches = []
    for system, keywords in SYSTEM_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in combined:
                matches.append(system)
                break
    if not matches:
        return "Unknown"
    if "Payments" in matches:
        return "Payments"
    return matches[0]


def normalize_team(raw_team):
    raw_lower = raw_team.lower().strip()
    for canonical, aliases in TEAM_ALIASES.items():
        for alias in aliases:
            if alias in raw_lower:
                return canonical
    if raw_lower and raw_lower not in ("", " "):
        return raw_team.strip()
    return "Unknown"


def extract_structured_from_tables(tables, text):
    """Extract structured fields from table data or raw text.
    
    Confluence RCA tables use a header-row / value-row layout:
      Row N:   [Ticket Id, Team Assigned, RCA Completed by]
      Row N+1: [DE-98436,  Payments,      Altaaf Anver    ]
    """
    fields = {
        "ticket_id": "",
        "team_assigned": "",
        "rca_completed_by": "",
        "incident_start": "",
        "resolution_end": "",
        "elapsed_time": "",
        "priority": "",
        "incident_summary": "",
    }

    field_map = {
        "ticket id": "ticket_id",
        "team assigned": "team_assigned",
        "rca completed by": "rca_completed_by",
        "incident start": "incident_start",
        "resolution date": "resolution_end",
        "elapsed time": "elapsed_time",
        "priority": "priority",
        "incident summary": "incident_summary",
    }

    for table in tables:
        for row_idx in range(len(table) - 1):
            header_row = table[row_idx]
            value_row = table[row_idx + 1]
            for col_idx, cell in enumerate(header_row):
                cell_lower = cell.lower().strip()
                for key_fragment, field_name in field_map.items():
                    if key_fragment in cell_lower:
                        if col_idx < len(value_row):
                            val = value_row[col_idx].strip()
                            is_another_label = any(
                                k in val.lower() for k in field_map
                            )
                            if val and not fields[field_name] and not is_another_label:
                                fields[field_name] = val

    if not any(fields.values()):
        for key_fragment, field_name in field_map.items():
            m = re.search(
                re.escape(key_fragment) + r"[:\s]*([^\n]{3,80})",
                text,
                re.IGNORECASE,
            )
            if m and not fields[field_name]:
                val = m.group(1).strip()
                is_label = any(k in val.lower() for k in field_map)
                if not is_label:
                    fields[field_name] = val

    return fields


def extract_rca_summary(text):
    """Extract first meaningful sentence from an RCA or root cause section."""
    patterns = [
        r"(?:Root\s*Cause|RCA)[:\s]*(.+?)(?:\.|$)",
        r"(?:What\s+(?:happened|caused))[:\s]*(.+?)(?:\.|$)",
        r"(?:Summary|Description)[:\s]*(.+?)(?:\.|$)",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            summary = m.group(1).strip()
            summary = re.sub(r"\s+", " ", summary)
            if len(summary) > 15 and len(summary) < 500:
                return summary[:300]
    return ""


def extract_year(date_str, last_modified):
    """Get year from incident date or fall back to last_modified."""
    if date_str:
        m = re.search(r"(\d{4})", date_str)
        if m:
            y = int(m.group(1))
            if 2014 <= y <= 2026:
                return y
    if last_modified:
        m = re.search(r"(\d{4})", last_modified)
        if m:
            return int(m.group(1))
    return None


def classify_root_cause_theme(title, rca_summary, text_snippet):
    """Classify into broad root cause theme buckets."""
    combined = (title + " " + rca_summary + " " + text_snippet[:300]).lower()
    themes = {
        "Database / RDS": ["rds", "database", "mysql", "replication", "cpu utilization", "connection", "db ", "shard"],
        "Payment Provider": ["vantiv", "worldpay", "express", "litle", "hsm", "payment gateway", "batch notification"],
        "Deployment / Config": ["deploy", "config", "release", "version", "migration", "upgrade"],
        "Infrastructure / Cloud": ["aws", "cloud", "ec2", "alb", "cloudflare", "esb", "load balancer", "infrastructure"],
        "Application Bug": ["bug", "code", "null", "exception", "error", "overflow", "timeout", "memory", "int32"],
        "Sync / Data Flow": ["sync", "syncing", "replicat", "sqs", "queue", "retry", "kafka"],
        "Third-party / External": ["twilio", "omnivore", "paytronix", "third party", "external"],
        "ACH / Funding": ["ach", "funding", "payout", "ndf", "sdf", "ledger"],
        "Capacity / Performance": ["capacity", "performance", "cpu", "memory", "throughput", "slow", "loading time"],
    }
    for theme, keywords in themes.items():
        for kw in keywords:
            if kw in combined:
                return theme
    return "Other"


def fetch_page_content(page_id):
    """Fetch page body via v1 API."""
    try:
        data = api_get(f"/wiki/rest/api/content/{page_id}", params={"expand": "body.storage"})
        html = data.get("body", {}).get("storage", {}).get("value", "")
        return html
    except Exception as e:
        return f"[Error: {e}]"


def fetch_summary_page(space_key, title_query):
    """Search for a specific summary page and return its parsed content."""
    try:
        cql = f'space="{space_key}" AND title="{title_query}"'
        data = api_get("/wiki/rest/api/content/search", params={"cql": cql, "limit": 1, "expand": "body.storage"})
        results = data.get("results", [])
        if results:
            html = results[0].get("body", {}).get("storage", {}).get("value", "")
            text, tables = parse_html(html)
            return {
                "title": results[0].get("title", title_query),
                "page_id": results[0].get("id", ""),
                "text_preview": text[:500],
                "table_count": len(tables),
                "tables": tables[:5],
            }
    except Exception as e:
        print(f"  Error fetching summary page '{title_query}': {e}", flush=True)
    return None


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=== Loading Postmortem Catalog ===", flush=True)
    with open(CATALOG_PATH) as f:
        catalog = json.load(f)

    docs = catalog.get("unique_documents", [])
    print(f"Total documents in catalog: {len(docs)}", flush=True)

    filtered = [d for d in docs if is_incident_doc(d)]
    filtered.sort(key=lambda d: d.get("last_modified", ""), reverse=True)
    print(f"Filtered to {len(filtered)} incident docs (excluded {len(docs) - len(filtered)} non-incident docs)", flush=True)

    top_n = filtered[:50]
    print(f"\n=== Fetching Content for Top {len(top_n)} Most Recent Docs ===", flush=True)

    incidents = []
    errors = []

    for i, doc in enumerate(top_n):
        title = doc["title"]
        page_id = extract_page_id(doc["url"])
        if not page_id:
            errors.append({"title": title, "error": "Could not extract page ID", "url": doc["url"]})
            print(f"  [{i+1}/{len(top_n)}] SKIP (no page ID): {title[:60]}", flush=True)
            continue

        print(f"  [{i+1}/{len(top_n)}] Fetching: {title[:65]}...", flush=True)
        html = fetch_page_content(page_id)

        if html.startswith("[Error"):
            errors.append({"title": title, "page_id": page_id, "error": html})
            print(f"    -> {html}", flush=True)
            time.sleep(0.5)
            continue

        text, tables = parse_html(html)
        structured = extract_structured_from_tables(tables, text)

        incident_date = extract_date_from_title(title)
        if not incident_date:
            incident_date = extract_date_from_body(text)

        affected_system = classify_system(title, text)
        team = normalize_team(structured["team_assigned"])
        rca_summary = extract_rca_summary(text)
        year = extract_year(incident_date, doc.get("last_modified"))
        theme = classify_root_cause_theme(title, rca_summary, text)

        record = {
            "title": title,
            "page_id": page_id,
            "space": doc.get("space", ""),
            "last_modified": doc.get("last_modified", ""),
            "url": doc.get("url", ""),
            "incident_date": incident_date or "",
            "year": year,
            "affected_system": affected_system,
            "team_assigned": team,
            "priority": structured["priority"],
            "elapsed_time": structured["elapsed_time"],
            "ticket_id": structured["ticket_id"],
            "rca_completed_by": structured["rca_completed_by"],
            "incident_summary": structured["incident_summary"][:300] if structured["incident_summary"] else "",
            "rca_summary": rca_summary,
            "root_cause_theme": theme,
            "content_length": len(text),
        }
        incidents.append(record)
        time.sleep(0.5)

    print(f"\n=== Fetching Summary Pages ===", flush=True)
    summary_pages = []
    summary_queries = [
        ("POAI", "CAKE Payments Outages - 2018"),
        ("POAI", "CAKE Payments Outages - 2017"),
        ("PS", "POST MORTEMS"),
    ]
    for space_key, title_q in summary_queries:
        print(f"  Searching: {title_q} (space {space_key})...", flush=True)
        result = fetch_summary_page(space_key, title_q)
        if result:
            summary_pages.append(result)
            print(f"    -> Found: {result['title']} (tables: {result['table_count']})", flush=True)
        else:
            print(f"    -> Not found", flush=True)
        time.sleep(0.5)

    print(f"\n=== Building Aggregations ===", flush=True)

    by_year = Counter()
    by_system = Counter()
    by_team = Counter()
    by_theme = Counter()

    for inc in incidents:
        if inc["year"]:
            by_year[inc["year"]] += 1
        by_system[inc["affected_system"]] += 1
        by_team[inc["team_assigned"]] += 1
        by_theme[inc["root_cause_theme"]] += 1

    timeline = {
        "generated_at": datetime.now().astimezone().isoformat(),
        "total_incidents_parsed": len(incidents),
        "total_filtered_docs": len(filtered),
        "fetch_errors": len(errors),
        "incidents_by_year": dict(sorted(by_year.items())),
        "incidents_by_system": dict(by_system.most_common()),
        "incidents_by_team": dict(by_team.most_common()),
        "root_cause_themes": dict(by_theme.most_common()),
        "summary_pages": summary_pages,
        "errors": errors,
    }

    out_structured = os.path.join(OUTPUT_DIR, "rca_structured.json")
    out_timeline = os.path.join(OUTPUT_DIR, "rca_timeline.json")

    with open(out_structured, "w") as f:
        json.dump(incidents, f, indent=2)
    print(f"\nWrote {len(incidents)} incidents -> {out_structured}", flush=True)

    with open(out_timeline, "w") as f:
        json.dump(timeline, f, indent=2)
    print(f"Wrote aggregations -> {out_timeline}", flush=True)

    print("\n" + "=" * 60)
    print(f"TOTAL INCIDENTS PARSED: {len(incidents)}")
    print(f"FETCH ERRORS: {len(errors)}")

    print(f"\nINCIDENTS BY YEAR:")
    for year, count in sorted(by_year.items()):
        print(f"  {year}: {count}")

    print(f"\nTOP AFFECTED SYSTEMS:")
    for system, count in by_system.most_common(10):
        print(f"  {system}: {count}")

    print(f"\nTOP TEAMS:")
    for team, count in by_team.most_common(10):
        print(f"  {team}: {count}")

    print(f"\nROOT CAUSE THEMES:")
    for theme, count in by_theme.most_common():
        print(f"  {theme}: {count}")

    if errors:
        print(f"\nERRORS:")
        for e in errors:
            print(f"  {e['title'][:50]}: {e.get('error', 'unknown')}")

    print("\nDone.", flush=True)


if __name__ == "__main__":
    main()
