#!/usr/bin/env python3
"""Jira assignee concentration — who has the most open issues."""

import requests
import json
import os
import time
from collections import defaultdict
from requests.auth import HTTPBasicAuth
import jira_config

JIRA_URL = os.environ.get("ATLASSIAN_URL", "https://madmobile-eng.atlassian.net")
JIRA_EMAIL = os.environ.get("ATLASSIAN_EMAIL", "adam.lazarus@madmobile.com")
JIRA_TOKEN = os.environ["ATLASSIAN_TOKEN"]
AUTH = HTTPBasicAuth(JIRA_EMAIL, JIRA_TOKEN)
HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}


def search_jql(jql, fields, max_results=200):
    body = {"jql": jql, "maxResults": min(max_results, 100), "fields": fields}
    items = []
    token = None
    while len(items) < max_results:
        if token:
            body["nextPageToken"] = token
        resp = requests.post(f"{JIRA_URL}/rest/api/3/search/jql",
                             auth=AUTH, headers=HEADERS, json=body)
        resp.raise_for_status()
        data = resp.json()
        items.extend(data.get('issues', []))
        token = data.get('nextPageToken')
        if not token:
            break
    return items[:max_results]


def approximate_count(jql):
    resp = requests.post(f"{JIRA_URL}/rest/api/3/search/approximate-count",
                         auth=AUTH, headers=HEADERS, json={"jql": jql})
    resp.raise_for_status()
    return resp.json().get('count', 0)


if __name__ == '__main__':
    os.makedirs('inventory/jira', exist_ok=True)

    print("=== Fetching open issues with assignees ===", flush=True)
    issues = search_jql(
        'statusCategory != Done AND assignee is not EMPTY ORDER BY assignee ASC',
        fields=["assignee", "issuetype", "project", "status"],
        max_results=1000
    )
    print(f"  Retrieved {len(issues)} assigned open issues", flush=True)

    assignee_data = defaultdict(lambda: {'total': 0, 'bugs': 0, 'stories': 0, 'tasks': 0, 'epics': 0, 'other': 0, 'projects': set()})
    for issue in issues:
        fields = issue.get('fields', {})
        assignee = fields.get('assignee', {})
        if not assignee:
            continue
        name = assignee.get('displayName', 'Unknown')
        itype = fields.get('issuetype', {}).get('name', '').lower()
        project = fields.get('project', {}).get('key', '')

        assignee_data[name]['total'] += 1
        assignee_data[name]['projects'].add(project)
        if 'bug' in itype:
            assignee_data[name]['bugs'] += 1
        elif 'story' in itype:
            assignee_data[name]['stories'] += 1
        elif 'task' in itype:
            assignee_data[name]['tasks'] += 1
        elif 'epic' in itype:
            assignee_data[name]['epics'] += 1
        else:
            assignee_data[name]['other'] += 1

    sorted_assignees = sorted(assignee_data.items(), key=lambda x: -x[1]['total'])[:30]
    output = {
        'top_30_assignees': [],
        'overloaded_count': sum(1 for _, d in sorted_assignees if d['total'] > 50),
        'total_assigned_issues_sampled': len(issues),
    }
    for name, data in sorted_assignees:
        projects_list = sorted(list(data['projects']))
        role = jira_config.classify_assignee(projects_list, {
            'total': data['total'], 'bugs': data['bugs'], 'stories': data['stories'],
            'tasks': data['tasks'], 'epics': data['epics'], 'other': data['other'],
        })
        eng_projects = [p for p in projects_list if jira_config.classify_project(p) == 'engineering']
        cs_projects = [p for p in projects_list if jira_config.classify_project(p) == 'customer_success']
        ops_projects = [p for p in projects_list if jira_config.classify_project(p) == 'operations']
        output['top_30_assignees'].append({
            'name': name,
            'open_issues': data['total'],
            'bugs': data['bugs'],
            'stories': data['stories'],
            'tasks': data['tasks'],
            'epics': data['epics'],
            'other': data['other'],
            'project_count': len(projects_list),
            'projects': projects_list,
            'role_classification': role,
            'primary_category': 'engineering' if len(eng_projects) >= len(cs_projects) and len(eng_projects) >= len(ops_projects) else 'customer_success' if len(cs_projects) > len(ops_projects) else 'operations',
            'engineering_projects': len(eng_projects),
            'customer_success_projects': len(cs_projects),
            'operations_projects': len(ops_projects),
            'is_overloaded': data['total'] > 50,
        })

    with open('inventory/jira/assignee_concentration.json', 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\n-> {output['overloaded_count']} overloaded assignees (>50 open)")
    print("Done.", flush=True)
