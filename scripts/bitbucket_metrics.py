#!/usr/bin/env python3
"""Bitbucket DORA-adjacent metrics: commit frequency, PR cycle time, contributors."""

import requests
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from collections import defaultdict

BB_API = "https://api.bitbucket.org/2.0"
BB_USER = os.environ.get("BB_USER", "adam.lazarus@madmobile.com")
BB_TOKEN = os.environ["BB_TOKEN"]
AUTH = (BB_USER, BB_TOKEN)
SIX_MONTHS_AGO = datetime.now(timezone.utc) - timedelta(days=180)
NINETY_DAYS_AGO = datetime.now(timezone.utc) - timedelta(days=90)

def paginate(url, params=None, max_pages=50):
    items = []
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
        if page % 5 == 0:
            time.sleep(0.5)
    return items

def get_top_active_repos(workspaces, top_n=30):
    """Find the most recently active repos across all workspaces."""
    all_repos = []
    for ws in workspaces:
        try:
            with open(f'inventory/bitbucket/{ws}.json') as f:
                data = json.load(f)
            for r in data.get('repos', []):
                if r.get('is_active'):
                    r['_workspace'] = ws
                    all_repos.append(r)
        except FileNotFoundError:
            pass
    all_repos.sort(key=lambda r: r.get('updated_on', ''), reverse=True)
    return all_repos[:top_n]

def get_commit_frequency(workspace, repo_slug):
    """Weekly commit counts over 6 months."""
    commits = paginate(
        f"{BB_API}/repositories/{workspace}/{repo_slug}/commits",
        max_pages=30
    )
    weekly = defaultdict(int)
    authors = defaultdict(set)
    for c in commits:
        date_str = c.get('date', '')
        if not date_str:
            continue
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        if dt < SIX_MONTHS_AGO:
            break
        week = dt.strftime('%Y-W%W')
        weekly[week] += 1
        author = c.get('author', {})
        author_name = author.get('user', {}).get('display_name', '') or author.get('raw', '')
        if author_name:
            authors[week].add(author_name)
    return {
        'weekly_commits': dict(weekly),
        'weekly_unique_authors': {k: len(v) for k, v in authors.items()},
        'total_commits_6mo': sum(weekly.values()),
    }

def get_pr_cycle_times(workspace, repo_slug):
    """PR cycle time for merged PRs in last 90 days."""
    merged_prs = paginate(
        f"{BB_API}/repositories/{workspace}/{repo_slug}/pullrequests",
        params={"state": "MERGED", "pagelen": 50,
                "sort": "-updated_on"},
        max_pages=5
    )
    results = []
    for pr in merged_prs:
        created = pr.get('created_on', '')
        merged = pr.get('updated_on', '')
        if not created or not merged:
            continue
        created_dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
        if created_dt < NINETY_DAYS_AGO:
            continue
        merged_dt = datetime.fromisoformat(merged.replace('Z', '+00:00'))
        cycle_hours = (merged_dt - created_dt).total_seconds() / 3600
        results.append({
            'id': pr.get('id'),
            'title': pr.get('title', ''),
            'author': pr.get('author', {}).get('display_name', ''),
            'created': created,
            'merged': merged,
            'cycle_hours': round(cycle_hours, 1),
        })
    return results


if __name__ == '__main__':
    workspaces = ['madmobile', 'syscolabs', 'madpayments', 'syscolabsconf']
    os.makedirs('inventory/bitbucket', exist_ok=True)

    top_repos = get_top_active_repos(workspaces, top_n=30)
    print(f"Analyzing top {len(top_repos)} most active repos", flush=True)

    metrics = []
    for i, repo in enumerate(top_repos):
        ws = repo['_workspace']
        slug = repo['slug']
        print(f"\n[{i+1}/{len(top_repos)}] {ws}/{slug}...", flush=True)

        print(f"  Commits...", flush=True)
        commit_data = get_commit_frequency(ws, slug)

        print(f"  PRs...", flush=True)
        pr_data = get_pr_cycle_times(ws, slug)

        metrics.append({
            'workspace': ws,
            'repo': slug,
            'language': repo.get('language', ''),
            'project': repo.get('project', ''),
            'commits': commit_data,
            'pr_cycle_times': pr_data,
            'pr_count_90d': len(pr_data),
            'avg_pr_cycle_hours': round(sum(p['cycle_hours'] for p in pr_data) / len(pr_data), 1) if pr_data else None,
            'median_pr_cycle_hours': round(sorted(p['cycle_hours'] for p in pr_data)[len(pr_data)//2], 1) if pr_data else None,
        })
        time.sleep(0.5)

    with open('inventory/bitbucket/metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2, default=str)
    print(f"\n-> Wrote inventory/bitbucket/metrics.json", flush=True)
    print("Done.", flush=True)
