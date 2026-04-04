#!/usr/bin/env python3
"""Search Confluence for architecture diagram attachments and architecture pages."""

import json
import os
import sys
import time
from datetime import datetime

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
API_DELAY = 0.3

OUT_DIR = "inventory/confluence"
os.makedirs(OUT_DIR, exist_ok=True)

TARGET_SPACES = "MMA, ES, LP, CCE, PT, POAI, CG, TS"


def api_get(path, params=None):
    url = f"{CONFLUENCE_URL}{path}" if path.startswith("/") else path
    resp = requests.get(url, auth=AUTH, headers=HEADERS, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def paginated_search(cql, limit=50, max_results=200, expand="space,version"):
    """Run a CQL search with pagination."""
    all_results = []
    start = 0
    while start < max_results:
        params = {"cql": cql, "limit": limit, "start": start}
        if expand:
            params["expand"] = expand
        data = api_get("/wiki/rest/api/content/search", params=params)
        results = data.get("results", [])
        all_results.extend(results)
        if len(results) < limit:
            break
        start += limit
        time.sleep(API_DELAY)
    return all_results


def search_diagram_attachments():
    """Try multiple CQL queries for diagram attachments. Confluence Cloud can be finicky."""
    all_results = []
    queries = [
        f'type=attachment AND filename ~ "drawio" AND space in ({TARGET_SPACES})',
        f'type=attachment AND filename ~ "gliffy" AND space in ({TARGET_SPACES})',
        f'type=attachment AND filename ~ "diagram" AND space in ({TARGET_SPACES})',
    ]
    for cql in queries:
        print(f"  Attachment search: {cql[:80]}...")
        try:
            results = paginated_search(cql, expand="space,version,container")
            print(f"    -> {len(results)} results")
            all_results.extend(results)
        except Exception as e:
            print(f"    -> Failed: {e}")
        time.sleep(API_DELAY)

    seen = set()
    deduped = []
    for r in all_results:
        rid = r.get("id", "")
        if rid not in seen:
            seen.add(rid)
            deduped.append(r)

    print(f"  Total unique attachment results: {len(deduped)}")
    return deduped


def search_architecture_pages():
    cql = (
        'type=page AND title ~ "architecture" '
        f'AND space in ({TARGET_SPACES})'
    )
    print(f"Search 2 (pages): {cql[:90]}...")
    results = paginated_search(cql)
    print(f"  Found {len(results)} architecture page results")
    return results


def get_page_attachments(page_id):
    """Fetch attachment list for a page."""
    try:
        data = api_get(
            f"/wiki/rest/api/content/{page_id}/child/attachment",
            params={"limit": 50},
        )
        return data.get("results", [])
    except Exception:
        return []


def process_attachment_results(results):
    """Extract diagram info from attachment search results."""
    diagrams = []
    for att in results:
        container = att.get("container", {}) or att.get("_expandable", {})
        page_title = container.get("title", "")
        space_key = att.get("space", {}).get("key", "")

        if not space_key:
            extensions = att.get("extensions", {})
            space_key = extensions.get("space", {}).get("key", "")
            if not space_key and container:
                space_key = container.get("space", {}).get("key", "")

        version = att.get("version", {})
        diagrams.append({
            "type": "attachment",
            "filename": att.get("title", ""),
            "page_title": page_title,
            "page_id": container.get("id", ""),
            "space_key": space_key,
            "last_modified": version.get("when", ""),
            "file_size": att.get("extensions", {}).get("fileSize", 0),
            "media_type": att.get("extensions", {}).get("mediaType", ""),
        })
    return diagrams


def process_page_results(results):
    """Extract info from architecture page search results and fetch their attachments."""
    pages = []
    for page in results:
        page_id = page.get("id", "")
        space = page.get("space", {})
        version = page.get("version", {})

        time.sleep(API_DELAY)
        attachments = get_page_attachments(page_id)
        att_names = [a.get("title", "") for a in attachments]
        diagram_atts = [
            n for n in att_names
            if any(ext in n.lower() for ext in [".drawio", ".gliffy", ".png", ".svg", "diagram", "arch"])
        ]

        pages.append({
            "type": "architecture_page",
            "page_title": page.get("title", ""),
            "page_id": page_id,
            "space_key": space.get("key", ""),
            "space_name": space.get("name", ""),
            "last_modified": version.get("when", ""),
            "total_attachments": len(att_names),
            "diagram_attachments": diagram_atts,
            "all_attachments": att_names,
        })
    return pages


def main():
    errors = []

    print("=" * 60)
    print("Confluence Architecture Diagram Search")
    print("=" * 60)
    print(f"Spaces: {TARGET_SPACES}\n")

    attachment_results = []
    try:
        attachment_results = search_diagram_attachments()
    except Exception as e:
        msg = f"Attachment search failed: {e}"
        print(f"  ERROR: {msg}")
        errors.append(msg)

    time.sleep(API_DELAY)

    page_results = []
    try:
        page_results = search_architecture_pages()
    except Exception as e:
        msg = f"Page search failed: {e}"
        print(f"  ERROR: {msg}")
        errors.append(msg)

    print(f"\nProcessing {len(attachment_results)} attachment results...")
    diagrams = process_attachment_results(attachment_results)

    print(f"Processing {len(page_results)} architecture pages (fetching attachments)...")
    arch_pages = process_page_results(page_results)

    seen_page_ids = {d["page_id"] for d in diagrams if d.get("page_id")}
    unique_arch_pages = [p for p in arch_pages if p["page_id"] not in seen_page_ids]

    by_space = {}
    for item in diagrams + unique_arch_pages:
        sk = item.get("space_key", "UNKNOWN")
        by_space.setdefault(sk, []).append(item)

    file_types = {}
    for d in diagrams:
        ext = os.path.splitext(d.get("filename", ""))[1].lower() or "unknown"
        file_types[ext] = file_types.get(ext, 0) + 1

    output = {
        "extracted_at": datetime.now().isoformat(),
        "target_spaces": TARGET_SPACES,
        "summary": {
            "total_diagram_attachments": len(diagrams),
            "total_architecture_pages": len(arch_pages),
            "unique_architecture_pages_without_diagram_attachments": len(unique_arch_pages),
            "spaces_with_results": sorted(by_space.keys()),
            "file_types": dict(sorted(file_types.items(), key=lambda x: -x[1])),
        },
        "by_space": {
            space: {
                "count": len(items),
                "items": sorted(items, key=lambda x: x.get("last_modified", ""), reverse=True),
            }
            for space, items in sorted(by_space.items())
        },
        "diagram_attachments": sorted(diagrams, key=lambda x: x.get("last_modified", ""), reverse=True),
        "architecture_pages": sorted(arch_pages, key=lambda x: x.get("last_modified", ""), reverse=True),
        "errors": errors,
    }

    out_path = os.path.join(OUT_DIR, "architecture_diagrams.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nWrote {out_path}")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Diagram attachments found:     {len(diagrams)}")
    print(f"Architecture pages found:      {len(arch_pages)}")
    print(f"Spaces with results:           {', '.join(sorted(by_space.keys())) or 'none'}")

    if file_types:
        print(f"\nFile types:")
        for ext, count in sorted(file_types.items(), key=lambda x: -x[1]):
            print(f"  {ext:20s}  {count}")

    print(f"\nBy space:")
    for space, items in sorted(by_space.items(), key=lambda x: -len(x[1])):
        print(f"  {space:10s}  {len(items):3d} items")

    if arch_pages:
        print(f"\nArchitecture pages:")
        for p in arch_pages[:15]:
            atts = f" ({len(p['diagram_attachments'])} diagram files)" if p["diagram_attachments"] else ""
            print(f"  [{p['space_key']}] {p['page_title'][:60]}{atts}")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
    print()


if __name__ == "__main__":
    main()
