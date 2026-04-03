#!/usr/bin/env python3
"""Confluence content extraction -- page index for key spaces + body content for top relevant pages."""

import requests
import json
import os
import re
import time
from datetime import datetime, timezone
from requests.auth import HTTPBasicAuth
from html.parser import HTMLParser

CONFLUENCE_URL = os.environ.get("ATLASSIAN_URL", "https://madmobile-eng.atlassian.net")
CONFLUENCE_EMAIL = os.environ.get("ATLASSIAN_EMAIL", "adam.lazarus@madmobile.com")
CONFLUENCE_TOKEN = os.environ["ATLASSIAN_TOKEN"]
AUTH = HTTPBasicAuth(CONFLUENCE_EMAIL, CONFLUENCE_TOKEN)
HEADERS = {"Accept": "application/json"}

TARGET_SPACES = {
    'MMA': 'Mad Mobile Architecture',
    'ES': 'CAKE Engineering Excellence',
    'PROD': 'Product',
    'LP': 'Leapset Platform',
    'TT': 'Team Tesla',
    'SWAT': 'SWAT',
    'DEP': 'Cloud Services Home',
    'CR': 'Cake Reports',
    'DB': 'Data & Analytics',
    'PT': 'Concierge Team',
    'CCE': 'Cloud Engineering',
    'AI': 'AI',
    'AIMM': 'AI at Mad Mobile',
    'P': 'Payments',
    'CA': 'Cake Apps',
}

CONTENT_KEYWORDS = [
    'architecture', 'design', 'topology', 'system diagram', 'c4',
    'rca', 'root cause', 'code red', 'outage', 'incident', 'post-mortem', 'postmortem',
    'deployment', 'release', 'pipeline', 'ci/cd', 'build flow', 'runbook',
    'roadmap', 'strategy', 'vision', 'initiative',
    'cursor', 'ai tool', 'agentic', 'lovable', 'neo platform', 'llm', 'prompt',
    'tool inventory', 'license', 'vendor', 'saas',
]


class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []
    def handle_data(self, data):
        self.result.append(data)
    def get_text(self):
        return ' '.join(self.result)


def strip_html(html):
    s = HTMLStripper()
    s.feed(html or '')
    text = s.get_text()
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def api_get(path, params=None):
    url = f"{CONFLUENCE_URL}{path}" if path.startswith('/') else path
    resp = requests.get(url, auth=AUTH, headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json()


def get_space_id(space_key):
    """Get the numeric space ID from a space key."""
    spaces = json.load(open('inventory/confluence/spaces.json'))
    for s in spaces:
        if s['key'] == space_key:
            return s['id']
    return None


def get_all_pages_for_space(space_id, space_key, max_pages=2000):
    """Get all page metadata for a space using v2 API."""
    pages = []
    url = f'/wiki/api/v2/pages'
    params = {"space-id": space_id, "sort": "-modified-date", "limit": 250, "status": "current"}
    while url and len(pages) < max_pages:
        try:
            data = api_get(url, params=params)
        except Exception as e:
            print(f"    Error fetching pages: {e}", flush=True)
            break
        batch = data.get('results', [])
        for p in batch:
            pages.append({
                'id': p['id'],
                'title': p.get('title', ''),
                'space_key': space_key,
                'status': p.get('status', ''),
                'created_at': p.get('createdAt', ''),
                'version_number': p.get('version', {}).get('number', 0) if isinstance(p.get('version'), dict) else 0,
                'version_created_at': p.get('version', {}).get('createdAt', '') if isinstance(p.get('version'), dict) else '',
                'author': p.get('version', {}).get('authorId', '') if isinstance(p.get('version'), dict) else '',
            })
        next_link = data.get('_links', {}).get('next', '')
        if next_link and batch:
            url = next_link if next_link.startswith('http') else f"{CONFLUENCE_URL}{next_link}"
            params = None
        else:
            break
        time.sleep(0.2)
    return pages


def matches_keywords(title):
    title_lower = title.lower()
    return any(kw in title_lower for kw in CONTENT_KEYWORDS)


def get_page_content(page_id):
    """Get page body content and convert to plain text."""
    try:
        data = api_get(f'/wiki/api/v2/pages/{page_id}', params={"body-format": "storage"})
        body_html = data.get('body', {}).get('storage', {}).get('value', '')
        return strip_html(body_html)
    except Exception as e:
        return f"[Error fetching content: {e}]"


if __name__ == '__main__':
    os.makedirs('inventory/confluence/content', exist_ok=True)

    all_pages = []
    print("=== Building Page Index ===", flush=True)
    for space_key, space_name in TARGET_SPACES.items():
        space_id = get_space_id(space_key)
        if not space_id:
            print(f"  {space_key}: space ID not found, skipping", flush=True)
            continue
        print(f"  {space_key} ({space_name})...", flush=True)
        pages = get_all_pages_for_space(space_id, space_key)
        all_pages.extend(pages)
        print(f"    -> {len(pages)} pages indexed", flush=True)
        time.sleep(0.3)

    print(f"\nTotal pages indexed: {len(all_pages)}", flush=True)
    with open('inventory/confluence/page_index.json', 'w') as f:
        json.dump(all_pages, f, indent=2)

    relevant = [p for p in all_pages if matches_keywords(p['title'])]
    relevant.sort(key=lambda p: p.get('version_created_at', ''), reverse=True)
    relevant = relevant[:100]
    print(f"\n=== Extracting Content for {len(relevant)} Relevant Pages ===", flush=True)

    content_index = []
    for i, page in enumerate(relevant):
        pid = page['id']
        title = page['title']
        print(f"  [{i+1}/{len(relevant)}] {page['space_key']}: {title[:60]}...", flush=True)
        text = get_page_content(pid)
        if len(text) > 50:
            filepath = f"inventory/confluence/content/{pid}.txt"
            with open(filepath, 'w') as f:
                f.write(f"# {title}\n# Space: {page['space_key']}\n# Page ID: {pid}\n\n{text}")
            content_index.append({
                'id': pid, 'title': title, 'space_key': page['space_key'],
                'file': filepath, 'content_length': len(text),
                'version_created_at': page.get('version_created_at', ''),
            })
        time.sleep(0.3)

    with open('inventory/confluence/content_index.json', 'w') as f:
        json.dump(content_index, f, indent=2)
    print(f"\n-> Extracted {len(content_index)} pages to inventory/confluence/content/")
    print("Done.", flush=True)
