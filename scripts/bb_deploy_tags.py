#!/usr/bin/env python3
"""Bitbucket deployment tag frequency analysis."""

import requests
import json
import os
import time
import re
from collections import defaultdict
from datetime import datetime, timedelta, timezone

BB_API = "https://api.bitbucket.org/2.0"
BB_USER = os.environ.get("BB_USER", "adam.lazarus@madmobile.com")
BB_TOKEN = os.environ["BB_TOKEN"]
AUTH = (BB_USER, BB_TOKEN)
SIX_MONTHS_AGO = datetime.now(timezone.utc) - timedelta(days=180)


def get_tags(workspace, repo_slug):
    tags = []
    url = f"{BB_API}/repositories/{workspace}/{repo_slug}/refs/tags"
    params = {"pagelen": 100, "sort": "-target.date"}
    page = 0
    while url and page < 3:
        resp = requests.get(url, auth=AUTH, params=params)
        if resp.status_code in (404, 403):
            return []
        if resp.status_code == 429:
            time.sleep(5)
            continue
        resp.raise_for_status()
        data = resp.json()
        tags.extend(data.get('values', []))
        url = data.get('next')
        params = None
        page += 1
    return tags


def classify_tag(name):
    if re.match(r'^v?\d+\.\d+\.\d+', name):
        return 'semver'
    if re.match(r'^v?\d+\.\d+', name):
        return 'major.minor'
    if re.match(r'^\d{4}[-.]?\d{2}[-.]?\d{2}', name):
        return 'date-based'
    if re.match(r'^release', name, re.I):
        return 'release-prefix'
    return 'other'


if __name__ == '__main__':
    os.makedirs('inventory/bitbucket', exist_ok=True)

    metrics = json.load(open('inventory/bitbucket/metrics.json'))
    repos = [(m['workspace'], m['repo']) for m in metrics]

    results = []
    for i, (ws, repo) in enumerate(repos):
        print(f"[{i+1}/{len(repos)}] {ws}/{repo}...", flush=True)
        tags = get_tags(ws, repo)

        monthly = defaultdict(int)
        patterns = defaultdict(int)
        recent_tags = []
        for t in tags:
            target = t.get('target', {})
            date_str = target.get('date', '')
            if not date_str:
                continue
            try:
                dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            except ValueError:
                continue
            if dt < SIX_MONTHS_AGO:
                break
            month = dt.strftime('%Y-%m')
            monthly[month] += 1
            patterns[classify_tag(t.get('name', ''))] += 1
            if len(recent_tags) < 5:
                recent_tags.append({'name': t.get('name', ''), 'date': date_str})

        results.append({
            'workspace': ws,
            'repo': repo,
            'total_tags_6mo': sum(monthly.values()),
            'monthly_tags': dict(monthly),
            'tag_patterns': dict(patterns),
            'recent_tags': recent_tags,
            'has_releases': sum(monthly.values()) > 0,
        })
        time.sleep(0.3)

    no_tags = [r for r in results if not r['has_releases']]
    with open('inventory/bitbucket/deploy_tags.json', 'w') as f:
        json.dump({
            'repos': results,
            'repos_with_tags': len(results) - len(no_tags),
            'repos_without_tags': len(no_tags),
        }, f, indent=2)
    print(f"\n-> {len(results) - len(no_tags)} repos with tags, {len(no_tags)} without")
    print("Done.", flush=True)
