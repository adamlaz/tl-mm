#!/usr/bin/env python3
"""Confluence inventory via REST API. Outputs JSON for spaces and content search."""

import requests
import json
import os
from datetime import datetime, timedelta, timezone
from requests.auth import HTTPBasicAuth
from urllib.parse import quote

CONFLUENCE_URL = os.environ.get("ATLASSIAN_URL", "https://madmobile-eng.atlassian.net")
CONFLUENCE_EMAIL = os.environ.get("ATLASSIAN_EMAIL", "adam.lazarus@madmobile.com")
CONFLUENCE_TOKEN = os.environ["ATLASSIAN_TOKEN"]
AUTH = HTTPBasicAuth(CONFLUENCE_EMAIL, CONFLUENCE_TOKEN)
HEADERS = {"Accept": "application/json"}
NINETY_DAYS_AGO = datetime.now(timezone.utc) - timedelta(days=90)

SEARCH_TERMS = [
    "architecture", "runbook", "post-mortem", "postmortem", "incident",
    "deployment", "CI/CD", "onboarding", "infrastructure", "SLA",
    "disaster recovery", "monitoring", "alerting", "release process",
]

def api_get(path, params=None):
    url = f"{CONFLUENCE_URL}{path}" if path.startswith('/') else path
    resp = requests.get(url, auth=AUTH, headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json()

def get_spaces():
    spaces = []
    cursor = None
    while True:
        params = {"limit": 250}
        if cursor:
            params["cursor"] = cursor
        data = api_get('/wiki/api/v2/spaces', params=params)
        batch = data.get('results', [])
        spaces.extend(batch)
        next_link = data.get('_links', {}).get('next', '')
        if not next_link or not batch:
            break
        cursor = next_link.split('cursor=')[-1].split('&')[0] if 'cursor=' in next_link else None
        if not cursor:
            break
    return [{
        'id': s['id'],
        'key': s['key'],
        'name': s['name'],
        'type': s.get('type', ''),
        'status': s.get('status', ''),
    } for s in spaces]

def get_page_count(space_key):
    """Use CQL search to get accurate total page count for a space."""
    try:
        cql = f'type=page AND space="{space_key}"'
        data = api_get('/wiki/rest/api/search', params={'cql': cql, 'limit': 0})
        return data.get('totalSize', data.get('size', 0))
    except Exception:
        try:
            data = api_get('/wiki/rest/api/content', params={
                'spaceKey': space_key, 'type': 'page', 'limit': 0
            })
            return data.get('size', 0)
        except Exception:
            return 'unknown'

def get_recent_pages(space_key, limit=10):
    try:
        cql = f'space = "{space_key}" AND lastModified > now("-90d") ORDER BY lastModified DESC'
        data = api_get('/wiki/rest/api/search', params={'cql': cql, 'limit': limit})
        return [{
            'title': r.get('title', ''),
            'last_modified': r.get('lastModified', ''),
            'url': r.get('url', ''),
        } for r in data.get('results', [])]
    except Exception as e:
        return [{'error': str(e)}]

def search_content(term, limit=15):
    try:
        cql = f'text ~ "{term}" ORDER BY lastModified DESC'
        data = api_get('/wiki/rest/api/search', params={'cql': cql, 'limit': limit})
        return [{
            'title': r.get('title', ''),
            'space': r.get('resultGlobalContainer', {}).get('title', ''),
            'last_modified': r.get('lastModified', ''),
            'url': r.get('url', ''),
            'excerpt': r.get('excerpt', '')[:200],
        } for r in data.get('results', [])]
    except Exception as e:
        return [{'error': str(e)}]


if __name__ == '__main__':
    os.makedirs('inventory/confluence', exist_ok=True)

    print("=== Confluence Spaces ===", flush=True)
    spaces = get_spaces()
    print(f"  Found {len(spaces)} spaces", flush=True)

    for s in spaces:
        print(f"  Space: {s['key']} ({s['name']})...", flush=True)
        s['page_count'] = get_page_count(s['key'])
        s['recent_pages'] = get_recent_pages(s['key'], limit=5)

    with open('inventory/confluence/spaces.json', 'w') as f:
        json.dump(spaces, f, indent=2)

    print(f"\n=== Content Search ({len(SEARCH_TERMS)} terms) ===", flush=True)
    search_results = {}
    for term in SEARCH_TERMS:
        print(f"  Searching: '{term}'...", flush=True)
        search_results[term] = search_content(term)
        count = len([r for r in search_results[term] if 'error' not in r])
        print(f"    Found {count} results", flush=True)

    with open('inventory/confluence/search_results.json', 'w') as f:
        json.dump(search_results, f, indent=2)

    print("\nDone.", flush=True)
