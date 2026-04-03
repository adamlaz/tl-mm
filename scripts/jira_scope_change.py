#!/usr/bin/env python3
"""Jira sprint scope change detection — issues added/removed mid-sprint."""

import requests
import json
import os
import time
from datetime import datetime, timezone
from requests.auth import HTTPBasicAuth

JIRA_URL = os.environ.get("ATLASSIAN_URL", "https://madmobile-eng.atlassian.net")
JIRA_EMAIL = os.environ.get("ATLASSIAN_EMAIL", "adam.lazarus@madmobile.com")
JIRA_TOKEN = os.environ["ATLASSIAN_TOKEN"]
AUTH = HTTPBasicAuth(JIRA_EMAIL, JIRA_TOKEN)
HEADERS = {"Accept": "application/json"}


def api_get(path, params=None):
    url = f"{JIRA_URL}{path}" if path.startswith('/') else path
    resp = requests.get(url, auth=AUTH, headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json()


def get_sprint_issues(sprint_id):
    items = []
    start = 0
    while True:
        data = api_get(f'/rest/agile/1.0/sprint/{sprint_id}/issue',
                       params={'startAt': start, 'maxResults': 50, 'fields': 'key,summary,status,issuetype'})
        items.extend(data.get('issues', []))
        total = data.get('total', len(items))
        start += len(items)
        if start >= total or not data.get('issues'):
            break
    return items


def check_issue_sprint_timing(issue_key, sprint_name, sprint_start):
    """Check if issue was added after sprint started."""
    try:
        changelog = api_get(f'/rest/api/3/issue/{issue_key}/changelog', params={'maxResults': 100})
        for history in changelog.get('values', []):
            for item in history.get('items', []):
                if item.get('field') == 'Sprint' and sprint_name in (item.get('toString') or ''):
                    change_date = datetime.fromisoformat(history['created'].replace('Z', '+00:00'))
                    if change_date > sprint_start:
                        return 'added_mid_sprint'
        return 'original_scope'
    except Exception:
        return 'unknown'


if __name__ == '__main__':
    os.makedirs('inventory/jira', exist_ok=True)

    velocity = json.load(open('inventory/jira/velocity_full.json'))
    results = []

    boards_with_sprints = {k: v for k, v in velocity.items()
                          if isinstance(v, dict) and v.get('sprints') and len(v['sprints']) >= 2}

    print(f"Analyzing scope change for {len(boards_with_sprints)} boards", flush=True)

    for board_name, board_data in boards_with_sprints.items():
        sprints = board_data['sprints']
        recent = sprints[-3:]
        for sprint in recent:
            sid = sprint['id']
            sname = sprint['name']
            start_str = sprint.get('start_date', '')
            if not start_str:
                continue
            sprint_start = datetime.fromisoformat(start_str.replace('Z', '+00:00'))

            print(f"  {sname}...", flush=True)
            issues = get_sprint_issues(sid)

            original = 0
            added = 0
            unknown = 0
            sampled = min(len(issues), 30)
            for issue in issues[:sampled]:
                timing = check_issue_sprint_timing(issue['key'], sname, sprint_start)
                if timing == 'original_scope':
                    original += 1
                elif timing == 'added_mid_sprint':
                    added += 1
                else:
                    unknown += 1
                time.sleep(0.3)

            results.append({
                'board': board_name,
                'sprint': sname,
                'sprint_id': sid,
                'start_date': start_str,
                'total_issues': len(issues),
                'sampled': sampled,
                'original_scope': original,
                'added_mid_sprint': added,
                'unknown': unknown,
                'scope_change_pct': round(added / sampled * 100, 1) if sampled else 0,
                'done_issues': sprint.get('done_issues', 0),
            })

    with open('inventory/jira/scope_change.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n-> {len(results)} sprints analyzed")
    print("Done.", flush=True)
