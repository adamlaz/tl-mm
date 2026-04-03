#!/usr/bin/env python3
"""Bitbucket workspace inventory via REST API v2. Outputs JSON per workspace."""

import requests
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone

BB_API = "https://api.bitbucket.org/2.0"
BB_USER = os.environ.get("BB_USER", "adam.lazarus@madmobile.com")
BB_TOKEN = os.environ["BB_TOKEN"]
AUTH = (BB_USER, BB_TOKEN)
ACTIVE_THRESHOLD = datetime.now(timezone.utc) - timedelta(days=90)
PR_WINDOW = datetime.now(timezone.utc) - timedelta(days=30)

def paginate(url, params=None):
    items = []
    while url:
        resp = requests.get(url, auth=AUTH, params=params)
        resp.raise_for_status()
        data = resp.json()
        items.extend(data.get('values', []))
        url = data.get('next')
        params = None
    return items

def get_repo_list(workspace):
    repos = paginate(f"{BB_API}/repositories/{workspace}", params={"pagelen": 100})
    results = []
    for r in repos:
        updated = r.get('updated_on', '')
        is_active = updated and datetime.fromisoformat(updated.replace('Z', '+00:00')) > ACTIVE_THRESHOLD
        results.append({
            'slug': r['slug'],
            'name': r.get('name', r['slug']),
            'language': r.get('language', ''),
            'size': r.get('size', 0),
            'updated_on': updated,
            'created_on': r.get('created_on', ''),
            'default_branch': r.get('mainbranch', {}).get('name', '') if r.get('mainbranch') else '',
            'is_active': is_active,
            'project': r.get('project', {}).get('name', '') if r.get('project') else '',
            'has_pipelines': r.get('has_pipelines', False) if 'has_pipelines' in r else None,
        })
    return results

def get_pr_summary(workspace, repo_slug):
    try:
        open_prs = requests.get(
            f"{BB_API}/repositories/{workspace}/{repo_slug}/pullrequests",
            auth=AUTH, params={"state": "OPEN", "pagelen": 1}
        ).json()
        merged_prs = requests.get(
            f"{BB_API}/repositories/{workspace}/{repo_slug}/pullrequests",
            auth=AUTH, params={
                "state": "MERGED", "pagelen": 50,
                "q": f'updated_on > {PR_WINDOW.strftime("%Y-%m-%dT%H:%M:%S")}'
            }
        ).json()
        return {
            'open_count': open_prs.get('size', 0),
            'merged_last_30d': merged_prs.get('size', 0),
        }
    except Exception as e:
        return {'error': str(e)}

def check_pipelines_config(workspace, repo_slug):
    try:
        resp = requests.get(
            f"{BB_API}/repositories/{workspace}/{repo_slug}/src/HEAD/bitbucket-pipelines.yml",
            auth=AUTH
        )
        return resp.status_code == 200
    except Exception:
        return False

def inventory_workspace(workspace):
    print(f"\n=== {workspace} ===", flush=True)
    repos = get_repo_list(workspace)
    print(f"  Found {len(repos)} repos", flush=True)

    active_repos = [r for r in repos if r['is_active']]
    stale_repos = [r for r in repos if not r['is_active']]

    languages = {}
    projects = {}
    for r in repos:
        lang = r['language'] or 'unknown'
        languages[lang] = languages.get(lang, 0) + 1
        proj = r['project'] or 'No Project'
        projects[proj] = projects.get(proj, 0) + 1

    pipeline_count = 0
    for i, r in enumerate(active_repos):
        print(f"  [{i+1}/{len(active_repos)}] {r['slug']}...", flush=True)
        has_pipeline = check_pipelines_config(workspace, r['slug'])
        r['has_pipeline_config'] = has_pipeline
        if has_pipeline:
            pipeline_count += 1
        r['pr_summary'] = get_pr_summary(workspace, r['slug'])
        if (i + 1) % 20 == 0:
            time.sleep(1)

    return {
        'workspace': workspace,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'total_repos': len(repos),
        'active_repos': len(active_repos),
        'stale_repos': len(stale_repos),
        'languages': languages,
        'projects': projects,
        'pipeline_count_in_active': pipeline_count,
        'repos': repos,
    }


if __name__ == '__main__':
    workspaces = sys.argv[1:] or ['madmobile', 'syscolabs', 'syscolabsconf', 'madpayments']
    os.makedirs('inventory/bitbucket', exist_ok=True)
    for ws in workspaces:
        try:
            data = inventory_workspace(ws)
            outfile = f"inventory/bitbucket/{ws}.json"
            with open(outfile, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            print(f"  -> Wrote {outfile}")
        except Exception as e:
            print(f"  ERROR on {ws}: {e}")
