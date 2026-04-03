#!/usr/bin/env python3
"""Confluence searches for AI tooling docs and tooling/expense documentation."""

import requests
import json
import os
import time
from requests.auth import HTTPBasicAuth

CONFLUENCE_URL = os.environ.get("ATLASSIAN_URL", "https://madmobile-eng.atlassian.net")
CONFLUENCE_EMAIL = os.environ.get("ATLASSIAN_EMAIL", "adam.lazarus@madmobile.com")
CONFLUENCE_TOKEN = os.environ["ATLASSIAN_TOKEN"]
AUTH = HTTPBasicAuth(CONFLUENCE_EMAIL, CONFLUENCE_TOKEN)
HEADERS = {"Accept": "application/json"}


def search_cql(cql, limit=25):
    try:
        resp = requests.get(f"{CONFLUENCE_URL}/wiki/rest/api/search",
                           auth=AUTH, headers=HEADERS,
                           params={'cql': cql, 'limit': limit})
        resp.raise_for_status()
        data = resp.json()
        return [{
            'title': r.get('title', ''),
            'space': r.get('resultGlobalContainer', {}).get('title', ''),
            'space_key': r.get('resultGlobalContainer', {}).get('key', ''),
            'last_modified': r.get('lastModified', ''),
            'url': r.get('url', ''),
            'excerpt': (r.get('excerpt', '') or '')[:300],
            'content_id': r.get('content', {}).get('id', ''),
        } for r in data.get('results', [])]
    except Exception as e:
        return [{'error': str(e)}]


if __name__ == '__main__':
    os.makedirs('inventory/confluence', exist_ok=True)

    # AI tooling searches
    ai_queries = {
        'cursor_title': 'title ~ "cursor"',
        'cursor_text': 'text ~ "cursor IDE" OR text ~ "cursor ai"',
        'copilot': 'title ~ "copilot" OR text ~ "github copilot"',
        'ai_tooling': 'title ~ "AI tooling" OR title ~ "AI tools" OR title ~ "AI workflow"',
        'agentic': 'text ~ "agentic" OR title ~ "agentic"',
        'lovable': 'text ~ "lovable" OR title ~ "lovable"',
        'llm_prompt': 'title ~ "prompt" OR title ~ "LLM" OR title ~ "GPT" OR title ~ "Claude"',
        'ai_strategy': 'title ~ "AI strategy" OR title ~ "AI roadmap" OR title ~ "Neo platform"',
    }

    print("=== AI Tooling Documentation ===", flush=True)
    ai_results = {}
    for label, cql in ai_queries.items():
        print(f"  {label}...", flush=True)
        results = search_cql(cql)
        clean = [r for r in results if 'error' not in r]
        ai_results[label] = clean
        print(f"    {len(clean)} results", flush=True)
        time.sleep(0.3)

    with open('inventory/confluence/ai_tooling_docs.json', 'w') as f:
        json.dump(ai_results, f, indent=2)

    # Tooling/expense searches
    expense_queries = {
        'tool_inventory': 'title ~ "tool inventory" OR title ~ "tools list" OR title ~ "software inventory" OR title ~ "engineering tools"',
        'licenses': 'title ~ "license" OR title ~ "licensing" OR title ~ "subscription"',
        'vendors': 'title ~ "vendor" OR title ~ "SaaS" OR title ~ "procurement"',
        'budget_cost': 'title ~ "budget" OR title ~ "cost" OR title ~ "expense"',
        'per_seat': 'text ~ "per seat" OR text ~ "annual license" OR text ~ "monthly cost"',
        'specific_tools': 'text ~ "Datadog" OR text ~ "New Relic" OR text ~ "Snyk" OR text ~ "Wiz" OR text ~ "PagerDuty"',
    }

    print("\n=== Tooling & Expense Documentation ===", flush=True)
    expense_results = {}
    for label, cql in expense_queries.items():
        print(f"  {label}...", flush=True)
        results = search_cql(cql)
        clean = [r for r in results if 'error' not in r]
        expense_results[label] = clean
        print(f"    {len(clean)} results", flush=True)
        time.sleep(0.3)

    with open('inventory/confluence/tooling_expense_docs.json', 'w') as f:
        json.dump(expense_results, f, indent=2)

    print("\nDone.", flush=True)
