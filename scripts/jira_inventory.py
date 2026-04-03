#!/usr/bin/env python3
"""Jira inventory via REST API. Outputs JSON for projects, boards, velocity."""

import requests
import json
import os
from datetime import datetime, timedelta, timezone
from requests.auth import HTTPBasicAuth

JIRA_URL = os.environ.get("ATLASSIAN_URL", "https://madmobile-eng.atlassian.net")
JIRA_EMAIL = os.environ.get("ATLASSIAN_EMAIL", "adam.lazarus@madmobile.com")
JIRA_TOKEN = os.environ["ATLASSIAN_TOKEN"]
AUTH = HTTPBasicAuth(JIRA_EMAIL, JIRA_TOKEN)
HEADERS = {"Accept": "application/json"}
SIX_MONTHS_AGO = datetime.now(timezone.utc) - timedelta(days=180)

def api_get(path, params=None):
    url = f"{JIRA_URL}{path}" if path.startswith('/') else path
    resp = requests.get(url, auth=AUTH, headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json()

def paginate_jira(path, key='values', start_key='startAt', max_key='maxResults', total_key='total'):
    items = []
    start = 0
    while True:
        data = api_get(path, params={start_key: start, max_key: 50})
        batch = data.get(key, [])
        items.extend(batch)
        total = data.get(total_key, len(items))
        start += len(batch)
        if start >= total or not batch:
            break
    return items

def get_projects():
    projects = paginate_jira('/rest/api/3/project/search', key='values')
    return [{
        'key': p['key'],
        'name': p['name'],
        'style': p.get('style', ''),
        'type_key': p.get('projectTypeKey', ''),
        'lead': p.get('lead', {}).get('displayName', '') if p.get('lead') else '',
        'category': p.get('projectCategory', {}).get('name', '') if p.get('projectCategory') else '',
    } for p in projects]

def get_boards():
    boards = paginate_jira('/rest/agile/1.0/board')
    return [{
        'id': b['id'],
        'name': b['name'],
        'type': b.get('type', ''),
        'project_key': b.get('location', {}).get('projectKey', '') if b.get('location') else '',
        'project_name': b.get('location', {}).get('name', '') if b.get('location') else '',
    } for b in boards]

def get_sprints_for_board(board_id):
    try:
        sprints = paginate_jira(f'/rest/agile/1.0/board/{board_id}/sprint')
        recent = [s for s in sprints if s.get('completeDate') and
                  datetime.fromisoformat(s['completeDate'].replace('Z', '+00:00')) > SIX_MONTHS_AGO]
        results = []
        for s in recent[-12:]:
            try:
                velocity = api_get(f'/rest/agile/1.0/sprint/{s["id"]}/issue',
                                   params={'maxResults': 0, 'jql': 'statusCategory = Done'})
                done_count = velocity.get('total', 0)
            except Exception:
                done_count = None
            results.append({
                'id': s['id'],
                'name': s['name'],
                'state': s.get('state', ''),
                'start_date': s.get('startDate', ''),
                'end_date': s.get('endDate', ''),
                'complete_date': s.get('completeDate', ''),
                'done_issues': done_count,
            })
        return results
    except Exception as e:
        return [{'error': str(e)}]

def approximate_count(jql):
    """Use the new POST /rest/api/3/search/approximate-count endpoint."""
    url = f"{JIRA_URL}/rest/api/3/search/approximate-count"
    resp = requests.post(url, auth=AUTH, headers={**HEADERS, "Content-Type": "application/json"},
                         json={"jql": jql})
    resp.raise_for_status()
    return resp.json().get('count', 0)

def get_issue_distribution():
    distributions = {}
    jql_types = {
        'bugs': 'issuetype = Bug',
        'stories': 'issuetype = Story',
        'tasks': 'issuetype = Task',
        'epics': 'issuetype = Epic',
        'subtasks': 'issuetype in subtaskIssueTypes()',
    }
    for label, jql in jql_types.items():
        try:
            distributions[label] = approximate_count(jql)
        except Exception as e:
            distributions[label] = f"error: {e}"

    for label, jql in [
        ('total_open', 'statusCategory != Done'),
        ('open_older_than_6mo', 'statusCategory != Done AND created <= -180d'),
        ('open_older_than_1yr', 'statusCategory != Done AND created <= -365d'),
        ('resolved_last_30d', 'statusCategory = Done AND resolved >= -30d'),
        ('resolved_last_90d', 'statusCategory = Done AND resolved >= -90d'),
        ('created_last_30d', 'created >= -30d'),
        ('created_last_90d', 'created >= -90d'),
    ]:
        try:
            distributions[label] = approximate_count(jql)
        except Exception as e:
            distributions[label] = f"error: {e}"

    return distributions

def get_issue_count_by_project():
    try:
        projects = api_get('/rest/api/3/project/search', params={'maxResults': 200}).get('values', [])
        counts = {}
        for p in projects:
            try:
                counts[p['key']] = approximate_count(f'project = {p["key"]}')
            except Exception:
                counts[p['key']] = 'error'
        return counts
    except Exception as e:
        return {'error': str(e)}


if __name__ == '__main__':
    os.makedirs('inventory/jira', exist_ok=True)

    print("=== Jira Projects ===", flush=True)
    projects = get_projects()
    print(f"  Found {len(projects)} projects", flush=True)
    with open('inventory/jira/projects.json', 'w') as f:
        json.dump(projects, f, indent=2)

    print("\n=== Jira Boards ===", flush=True)
    boards = get_boards()
    print(f"  Found {len(boards)} boards", flush=True)
    with open('inventory/jira/boards.json', 'w') as f:
        json.dump(boards, f, indent=2)

    print("\n=== Sprint Velocity (last 6 months) ===", flush=True)
    scrum_boards = [b for b in boards if b['type'] == 'scrum']
    velocity = {}
    for b in scrum_boards:
        print(f"  Board: {b['name']}...", flush=True)
        velocity[b['name']] = get_sprints_for_board(b['id'])
    with open('inventory/jira/velocity.json', 'w') as f:
        json.dump(velocity, f, indent=2)

    print("\n=== Issue Distribution ===", flush=True)
    dist = get_issue_distribution()
    print(f"  {dist}", flush=True)
    with open('inventory/jira/issue_distribution.json', 'w') as f:
        json.dump(dist, f, indent=2)

    print("\n=== Issue Counts by Project ===", flush=True)
    counts = get_issue_count_by_project()
    with open('inventory/jira/project_issue_counts.json', 'w') as f:
        json.dump(counts, f, indent=2)

    print("\nDone.", flush=True)
