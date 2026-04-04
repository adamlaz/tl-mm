#!/usr/bin/env python3
"""Audit Jira workflows, workflow schemes, and statuses."""

import json
import os
import sys
import time
from collections import Counter
from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv(".env.local")

BASE_URL = os.environ.get("ATLASSIAN_URL", "https://madmobile-eng.atlassian.net")
AUTH = HTTPBasicAuth(
    os.environ.get("ATLASSIAN_EMAIL", "adam.lazarus@madmobile.com"),
    os.environ["ATLASSIAN_TOKEN"],
)
HEADERS = {"Accept": "application/json"}
API_DELAY = 0.3

OUT_DIR = "inventory/jira"
os.makedirs(OUT_DIR, exist_ok=True)


def api_get(path, params=None):
    url = f"{BASE_URL}{path}"
    resp = requests.get(url, auth=AUTH, headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json()


def fetch_all_workflows():
    """Try v3 paginated search first, fall back to v2 list."""
    # v3 paginated
    try:
        workflows = []
        start = 0
        while True:
            print(f"  Fetching workflows v3 (startAt={start})...")
            data = api_get("/rest/api/3/workflow/search", params={
                "startAt": start, "maxResults": 50,
            })
            values = data.get("values", [])
            workflows.extend(values)
            if data.get("isLast", True) or not values:
                break
            start += len(values)
            time.sleep(API_DELAY)
        return workflows
    except requests.HTTPError as e:
        print(f"  v3 workflow/search returned {e.response.status_code}, trying v2...")

    # v2 flat list
    try:
        data = api_get("/rest/api/2/workflow")
        if isinstance(data, list):
            return data
        return data.get("values", data.get("workflows", []))
    except requests.HTTPError as e2:
        print(f"  v2 also failed ({e2.response.status_code}), trying /rest/api/latest/workflow...")

    # latest fallback
    data = api_get("/rest/api/latest/workflow")
    if isinstance(data, list):
        return data
    return data.get("values", data.get("workflows", []))


def fetch_workflow_schemes():
    """Try /rest/api/3/workflowscheme — may 403."""
    try:
        data = api_get("/rest/api/3/workflowscheme")
        if isinstance(data, list):
            return data
        return data.get("values", data.get("schemes", [data]))
    except requests.HTTPError as e:
        print(f"  Workflow schemes not accessible ({e.response.status_code})")
        return None
    except Exception as e:
        print(f"  Workflow schemes error: {e}")
        return None


def fetch_all_statuses():
    """GET statuses — try v3 paginated, then v2 flat list."""
    # v3 paginated
    try:
        statuses = []
        start = 0
        while True:
            data = api_get("/rest/api/3/statuses/search", params={
                "startAt": start, "maxResults": 200,
            })
            values = data.get("values", [])
            statuses.extend(values)
            if data.get("isLast", True) or not values:
                break
            start += len(values)
            time.sleep(API_DELAY)
        if statuses:
            return statuses
    except Exception:
        pass

    # v2 flat list
    try:
        data = api_get("/rest/api/2/status")
        if isinstance(data, list):
            return data
    except Exception:
        pass

    # v3 flat
    data = api_get("/rest/api/3/status")
    if isinstance(data, list):
        return data
    return data.get("values", [])


BUILTIN_STATUSES = {
    "open", "to do", "in progress", "done", "closed", "resolved",
    "reopened", "backlog",
}


def main():
    print("=" * 60)
    print("Jira Workflow & Status Audit")
    print("=" * 60)

    # --- Workflows ---
    print("\n[1/3] Fetching workflows...")
    try:
        workflows = fetch_all_workflows()
    except Exception as e:
        print(f"  Workflow fetch failed (likely permission issue): {e}")
        workflows = []
    print(f"  Total workflows: {len(workflows)}")

    workflow_summaries = []
    for wf in workflows:
        name = wf.get("id", {}).get("name", "") if isinstance(wf.get("id"), dict) else wf.get("name", "")
        entity_id = wf.get("id", {}).get("entityId", "") if isinstance(wf.get("id"), dict) else wf.get("entityId", "")
        statuses = wf.get("statuses", [])
        transitions = wf.get("transitions", [])
        workflow_summaries.append({
            "name": name,
            "entity_id": entity_id,
            "status_count": len(statuses),
            "transition_count": len(transitions),
            "statuses": [s.get("name", s.get("id", "")) for s in statuses],
        })

    # --- Workflow Schemes ---
    print("\n[2/3] Fetching workflow schemes...")
    time.sleep(API_DELAY)
    schemes_raw = fetch_workflow_schemes()
    schemes = []
    if schemes_raw:
        for s in (schemes_raw if isinstance(schemes_raw, list) else [schemes_raw]):
            schemes.append({
                "id": s.get("id", ""),
                "name": s.get("name", ""),
                "description": s.get("description", ""),
                "defaultWorkflow": s.get("defaultWorkflow", ""),
            })
        print(f"  Total workflow schemes: {len(schemes)}")
    else:
        print("  Skipped (not accessible)")

    # --- Statuses ---
    print("\n[3/3] Fetching statuses...")
    time.sleep(API_DELAY)
    try:
        statuses_raw = fetch_all_statuses()
    except Exception as e:
        print(f"  Status fetch failed: {e}")
        statuses_raw = []
    print(f"  Total statuses: {len(statuses_raw)}")

    status_details = []
    category_counts = Counter()
    custom_statuses = []
    for s in statuses_raw:
        name = s.get("name", "")
        cat = s.get("statusCategory", {}).get("name", "Unknown")
        category_counts[cat] += 1
        is_custom = name.lower().strip() not in BUILTIN_STATUSES
        entry = {
            "name": name,
            "id": s.get("id", ""),
            "category": cat,
            "is_custom": is_custom,
        }
        status_details.append(entry)
        if is_custom:
            custom_statuses.append(entry)

    # --- Output ---
    output = {
        "extracted_at": datetime.now().isoformat(),
        "workflows": {
            "total": len(workflow_summaries),
            "items": workflow_summaries,
        },
        "workflow_schemes": {
            "accessible": schemes_raw is not None,
            "total": len(schemes),
            "items": schemes,
        },
        "statuses": {
            "total": len(status_details),
            "custom_count": len(custom_statuses),
            "builtin_count": len(status_details) - len(custom_statuses),
            "by_category": dict(category_counts),
            "custom_statuses": custom_statuses,
            "all": status_details,
        },
    }

    out_path = os.path.join(OUT_DIR, "workflows.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nWrote {out_path}")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Workflows:          {len(workflow_summaries)}")
    if workflow_summaries:
        by_status_count = sorted(workflow_summaries, key=lambda w: -w["status_count"])
        print(f"\nTop workflows by status count:")
        for wf in by_status_count[:10]:
            print(f"  {wf['name'][:50]:50s}  {wf['status_count']} statuses, {wf['transition_count']} transitions")

    print(f"\nWorkflow schemes:   {'N/A (no access)' if schemes_raw is None else len(schemes)}")
    print(f"\nStatuses:           {len(status_details)} total")
    print(f"  Custom:           {len(custom_statuses)}")
    print(f"  Built-in:         {len(status_details) - len(custom_statuses)}")
    print(f"  By category:")
    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"    {cat:25s}  {count}")
    print()


if __name__ == "__main__":
    main()
