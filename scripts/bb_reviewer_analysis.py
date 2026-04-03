#!/usr/bin/env python3
"""Bitbucket PR reviewer concentration analysis."""

import requests
import json
import os
import time
from collections import defaultdict

BB_API = "https://api.bitbucket.org/2.0"
BB_USER = os.environ.get("BB_USER", "adam.lazarus@madmobile.com")
BB_TOKEN = os.environ["BB_TOKEN"]
AUTH = (BB_USER, BB_TOKEN)


def get_merged_prs(workspace, repo_slug, max_pages=5):
    items = []
    url = f"{BB_API}/repositories/{workspace}/{repo_slug}/pullrequests"
    params = {"state": "MERGED", "pagelen": 50, "sort": "-updated_on"}
    page = 0
    while url and page < max_pages:
        resp = requests.get(url, auth=AUTH, params=params)
        if resp.status_code == 429:
            time.sleep(5)
            continue
        resp.raise_for_status()
        data = resp.json()
        items.extend(data.get('values', []))
        url = data.get('next')
        params = None
        page += 1
    return items


def analyze_reviewers(prs):
    reviewer_counts = defaultdict(int)
    for pr in prs:
        reviewers = set()
        for p in pr.get('participants', []):
            if p.get('role') in ('REVIEWER',) and p.get('approved', False):
                name = p.get('user', {}).get('display_name', 'Unknown')
                reviewers.add(name)
        if not reviewers:
            for p in pr.get('participants', []):
                if p.get('role') == 'REVIEWER':
                    name = p.get('user', {}).get('display_name', 'Unknown')
                    reviewers.add(name)
        for r in reviewers:
            reviewer_counts[r] += 1
    total = len(prs)
    top = sorted(reviewer_counts.items(), key=lambda x: -x[1])[:5]
    top_pct = round(top[0][1] / total * 100, 1) if top and total else 0
    return {
        'total_prs': total,
        'top_reviewers': [{'name': n, 'count': c, 'pct': round(c/total*100, 1)} for n, c in top],
        'top_reviewer_pct': top_pct,
        'is_bottleneck': top_pct > 60,
    }


if __name__ == '__main__':
    os.makedirs('inventory/bitbucket', exist_ok=True)

    metrics = json.load(open('inventory/bitbucket/metrics.json'))
    repos = [(m['workspace'], m['repo']) for m in metrics]

    results = []
    global_reviewers = defaultdict(int)

    for i, (ws, repo) in enumerate(repos):
        print(f"[{i+1}/{len(repos)}] {ws}/{repo}...", flush=True)
        prs = get_merged_prs(ws, repo)
        analysis = analyze_reviewers(prs)
        analysis['workspace'] = ws
        analysis['repo'] = repo
        results.append(analysis)
        for r in analysis['top_reviewers']:
            global_reviewers[r['name']] += r['count']
        time.sleep(0.5)

    global_top = sorted(global_reviewers.items(), key=lambda x: -x[1])[:20]
    bottleneck_repos = [r for r in results if r['is_bottleneck']]

    output = {
        'per_repo': results,
        'global_top_20_reviewers': [{'name': n, 'total_reviews': c} for n, c in global_top],
        'bottleneck_repos': [{'workspace': r['workspace'], 'repo': r['repo'],
                              'top_reviewer': r['top_reviewers'][0]['name'] if r['top_reviewers'] else '',
                              'pct': r['top_reviewer_pct']} for r in bottleneck_repos],
    }

    with open('inventory/bitbucket/reviewer_concentration.json', 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\n-> {len(bottleneck_repos)} bottleneck repos (>60% single reviewer)")
    print("Done.", flush=True)
