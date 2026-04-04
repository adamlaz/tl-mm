#!/usr/bin/env python3
"""Jira custom field discovery and Root Cause Category analysis."""

import requests
import json
import os
import sys
import time
from collections import defaultdict
from requests.auth import HTTPBasicAuth

sys.path.insert(0, os.path.dirname(__file__))
import jira_config

JIRA_URL = os.environ.get("ATLASSIAN_URL", "https://madmobile-eng.atlassian.net")
JIRA_EMAIL = os.environ.get("ATLASSIAN_EMAIL", "adam.lazarus@madmobile.com")
JIRA_TOKEN = os.environ["ATLASSIAN_TOKEN"]
AUTH = HTTPBasicAuth(JIRA_EMAIL, JIRA_TOKEN)
HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}

INTERESTING_PATTERNS = [
    'root cause', 'story points', 'sprint', 'epic', 'customer',
    'impact', 'severity', 'environment', 'team', 'component',
    'release', 'deployment', 'rca', 'category',
]

def api_get(path, params=None):
    url = f"{JIRA_URL}{path}" if path.startswith('/') else path
    resp = requests.get(url, auth=AUTH, headers={"Accept": "application/json"}, params=params)
    resp.raise_for_status()
    return resp.json()

def api_post(path, body):
    url = f"{JIRA_URL}{path}" if path.startswith('/') else path
    resp = requests.post(url, auth=AUTH, headers=HEADERS, json=body)
    resp.raise_for_status()
    return resp.json()

def search_issues(jql, fields=None, max_results=200):
    body = {"jql": jql, "maxResults": min(max_results, 100)}
    if fields:
        body["fields"] = fields
    items = []
    token = None
    while len(items) < max_results:
        if token:
            body["nextPageToken"] = token
        data = api_post('/rest/api/3/search/jql', body)
        items.extend(data.get('issues', []))
        token = data.get('nextPageToken')
        if not token:
            break
    return items[:max_results]

def main():
    os.makedirs('inventory/jira', exist_ok=True)

    print("=== Discovering Custom Fields ===", flush=True)
    all_fields = api_get('/rest/api/3/field')

    interesting_fields = []
    root_cause_field = None
    story_points_field = None

    for field in all_fields:
        fid = field.get('id', '')
        fname = field.get('name', '').lower()
        if not fid.startswith('customfield_'):
            continue
        for pattern in INTERESTING_PATTERNS:
            if pattern in fname:
                entry = {
                    'id': fid,
                    'name': field.get('name', ''),
                    'type': field.get('schema', {}).get('type', 'unknown'),
                    'custom_type': field.get('schema', {}).get('custom', ''),
                }
                interesting_fields.append(entry)
                if 'root cause' in fname and ('category' in fname or 'analysis' in fname or fname == 'root cause'):
                    root_cause_field = entry
                if fname in ('story points', 'story point estimate'):
                    story_points_field = entry
                break

    print(f"  Found {len(interesting_fields)} interesting custom fields", flush=True)
    for f in interesting_fields[:20]:
        print(f"    {f['id']}: {f['name']} ({f['type']})")

    root_cause_dist = {}
    if root_cause_field:
        print(f"\n=== Root Cause Field: {root_cause_field['name']} ({root_cause_field['id']}) ===", flush=True)
        eng_jql = jira_config.engineering_jql()
        jql = f"issuetype = Bug AND resolved >= -365d AND {eng_jql}"
        try:
            bugs = search_issues(jql, fields=[root_cause_field['id'], 'project', 'status'], max_results=500)
            counts = defaultdict(int)
            populated = 0
            for issue in bugs:
                fields = issue.get('fields', {})
                rc_val = fields.get(root_cause_field['id'])
                if rc_val:
                    populated += 1
                    if isinstance(rc_val, dict):
                        val = rc_val.get('value', rc_val.get('name', str(rc_val)))
                    else:
                        val = str(rc_val)
                    counts[val] += 1
                else:
                    counts['(not set)'] += 1

            root_cause_dist = {
                'field_id': root_cause_field['id'],
                'field_name': root_cause_field['name'],
                'total_bugs_sampled': len(bugs),
                'populated_count': populated,
                'population_rate_pct': round(populated / len(bugs) * 100, 1) if bugs else 0,
                'distribution': dict(sorted(counts.items(), key=lambda x: -x[1])),
            }
            print(f"  Sampled {len(bugs)} bugs, {populated} have root cause set ({root_cause_dist['population_rate_pct']}%)")
            for cat, count in list(root_cause_dist['distribution'].items())[:10]:
                print(f"    {cat}: {count}")
        except Exception as e:
            print(f"  Error querying root cause: {e}")
            root_cause_dist = {'error': str(e)}
    else:
        print("\n  No Root Cause Category field found")
        for f in interesting_fields:
            if 'root' in f['name'].lower() or 'cause' in f['name'].lower() or 'rca' in f['name'].lower():
                print(f"  Possible match: {f['id']}: {f['name']}")

    story_points_coverage = {}
    if story_points_field:
        print(f"\n=== Story Points: {story_points_field['name']} ({story_points_field['id']}) ===", flush=True)
        eng_jql = jira_config.engineering_jql()
        jql = f"issuetype = Story AND resolved >= -180d AND {eng_jql}"
        try:
            stories = search_issues(jql, fields=[story_points_field['id']], max_results=300)
            has_points = sum(1 for s in stories if s.get('fields', {}).get(story_points_field['id']) is not None)
            story_points_coverage = {
                'field_id': story_points_field['id'],
                'total_stories_sampled': len(stories),
                'with_points': has_points,
                'coverage_pct': round(has_points / len(stories) * 100, 1) if stories else 0,
            }
            print(f"  {has_points}/{len(stories)} stories have points ({story_points_coverage['coverage_pct']}%)")
        except Exception as e:
            print(f"  Error: {e}")
            story_points_coverage = {'error': str(e)}

    with open('inventory/jira/custom_fields.json', 'w') as f:
        json.dump({
            'total_custom_fields': len([f for f in all_fields if f.get('id', '').startswith('customfield_')]),
            'interesting_fields': interesting_fields,
            'root_cause_field': root_cause_field,
            'story_points_field': story_points_field,
            'story_points_coverage': story_points_coverage,
        }, f, indent=2)

    with open('inventory/jira/root_cause_distribution.json', 'w') as f:
        json.dump(root_cause_dist, f, indent=2)

    print("\nDone.")

if __name__ == '__main__':
    main()
