#!/usr/bin/env python3
"""Confluence deep analysis — page creation trends and post-mortem catalog."""

import requests
import json
import os
import time
from datetime import datetime, timedelta, timezone
from requests.auth import HTTPBasicAuth

CONFLUENCE_URL = os.environ.get("ATLASSIAN_URL", "https://madmobile-eng.atlassian.net")
CONFLUENCE_EMAIL = os.environ.get("ATLASSIAN_EMAIL", "adam.lazarus@madmobile.com")
CONFLUENCE_TOKEN = os.environ["ATLASSIAN_TOKEN"]
AUTH = HTTPBasicAuth(CONFLUENCE_EMAIL, CONFLUENCE_TOKEN)
HEADERS = {"Accept": "application/json"}


def api_get(path, params=None):
    url = f"{CONFLUENCE_URL}{path}" if path.startswith('/') else path
    resp = requests.get(url, auth=AUTH, headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json()


def get_page_creation_trend():
    """Weekly page creation over 6 months."""
    trend = []
    now = datetime.now(timezone.utc)
    for weeks_ago in range(26, -1, -1):
        week_start = now - timedelta(weeks=weeks_ago + 1)
        week_end = now - timedelta(weeks=weeks_ago)
        start_str = week_start.strftime('%Y-%m-%d')
        end_str = week_end.strftime('%Y-%m-%d')
        try:
            cql = f'type=page AND created >= "{start_str}" AND created < "{end_str}"'
            data = api_get('/wiki/rest/api/search', params={'cql': cql, 'limit': 0})
            count = data.get('totalSize', data.get('size', 0))
            trend.append({'week_start': start_str, 'week_end': end_str, 'pages_created': count})
        except Exception as e:
            trend.append({'week_start': start_str, 'error': str(e)})
        time.sleep(0.3)
    return trend


def get_postmortem_catalog():
    """Search for post-mortem and incident documentation."""
    search_queries = [
        'title ~ "RCA"',
        'title ~ "root cause"',
        'title ~ "post-mortem"',
        'title ~ "postmortem"',
        'title ~ "incident report"',
        'title ~ "outage"',
        'title ~ "retrospective"',
    ]
    all_results = {}
    seen_ids = set()
    unique_results = []

    for query in search_queries:
        try:
            data = api_get('/wiki/rest/api/search', params={'cql': query, 'limit': 50})
            results = data.get('results', [])
            all_results[query] = len(results)
            for r in results:
                rid = r.get('content', {}).get('id', r.get('title', ''))
                if rid not in seen_ids:
                    seen_ids.add(rid)
                    unique_results.append({
                        'title': r.get('title', ''),
                        'space': r.get('resultGlobalContainer', {}).get('title', ''),
                        'last_modified': r.get('lastModified', ''),
                        'url': r.get('url', ''),
                        'excerpt': (r.get('excerpt', '') or '')[:200],
                    })
        except Exception as e:
            all_results[query] = f"error: {e}"
        time.sleep(0.3)

    return {
        'query_counts': all_results,
        'unique_documents': unique_results,
        'total_unique': len(unique_results),
    }


if __name__ == '__main__':
    os.makedirs('inventory/confluence', exist_ok=True)

    print("=== Page Creation Trend (26 weeks) ===", flush=True)
    trend = get_page_creation_trend()
    valid = [t for t in trend if 'error' not in t]
    total = sum(t['pages_created'] for t in valid)
    print(f"  {total} pages created over {len(valid)} weeks", flush=True)
    with open('inventory/confluence/creation_trend.json', 'w') as f:
        json.dump(trend, f, indent=2)

    print("\n=== Post-Mortem / RCA Catalog ===", flush=True)
    catalog = get_postmortem_catalog()
    print(f"  {catalog['total_unique']} unique documents found", flush=True)
    with open('inventory/confluence/postmortem_catalog.json', 'w') as f:
        json.dump(catalog, f, indent=2)

    print("\nDone.", flush=True)
