#!/usr/bin/env python3
"""Jira Flow Framework distribution — features vs defects vs debt vs risk."""

import requests
import json
import os
from requests.auth import HTTPBasicAuth
import jira_config

JIRA_URL = os.environ.get("ATLASSIAN_URL", "https://madmobile-eng.atlassian.net")
JIRA_EMAIL = os.environ.get("ATLASSIAN_EMAIL", "adam.lazarus@madmobile.com")
JIRA_TOKEN = os.environ["ATLASSIAN_TOKEN"]
AUTH = HTTPBasicAuth(JIRA_EMAIL, JIRA_TOKEN)
HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}


def approximate_count(jql):
    resp = requests.post(f"{JIRA_URL}/rest/api/3/search/approximate-count",
                         auth=AUTH, headers=HEADERS, json={"jql": jql})
    resp.raise_for_status()
    return resp.json().get('count', 0)


def run_flow_queries(prefix=""):
    """Run flow distribution queries with an optional JQL prefix."""
    base_queries = {
        'resolved_90d': {
            'features': f'issuetype = Story AND resolved >= -90d{prefix}',
            'defects': f'issuetype = Bug AND resolved >= -90d{prefix}',
            'tasks': f'issuetype = Task AND resolved >= -90d{prefix}',
            'epics': f'issuetype = Epic AND resolved >= -90d{prefix}',
            'subtasks': f'issuetype in subtaskIssueTypes() AND resolved >= -90d{prefix}',
        },
        'created_90d': {
            'features': f'issuetype = Story AND created >= -90d{prefix}',
            'defects': f'issuetype = Bug AND created >= -90d{prefix}',
            'tasks': f'issuetype = Task AND created >= -90d{prefix}',
            'epics': f'issuetype = Epic AND created >= -90d{prefix}',
            'subtasks': f'issuetype in subtaskIssueTypes() AND created >= -90d{prefix}',
        },
        'open': {
            'features': f'issuetype = Story AND statusCategory != Done{prefix}',
            'defects': f'issuetype = Bug AND statusCategory != Done{prefix}',
            'tasks': f'issuetype = Task AND statusCategory != Done{prefix}',
            'epics': f'issuetype = Epic AND statusCategory != Done{prefix}',
        },
    }
    result = {}
    for category, jqls in base_queries.items():
        result[category] = {}
        for label, jql in jqls.items():
            try:
                result[category][label] = approximate_count(jql)
            except Exception as e:
                result[category][label] = f"error: {e}"

    resolved = result.get('resolved_90d', {})
    total_resolved = sum(v for v in resolved.values() if isinstance(v, int))
    if total_resolved:
        result['resolved_90d_percentages'] = {
            k: round(v / total_resolved * 100, 1)
            for k, v in resolved.items() if isinstance(v, int)
        }
        result['resolved_90d_total'] = total_resolved
    return result


if __name__ == '__main__':
    os.makedirs('inventory/jira', exist_ok=True)
    output = {}

    for seg_name, seg_fn in [('overall', None), ('engineering', jira_config.engineering_jql)]:
        prefix = f" AND {seg_fn()}" if seg_fn else ""
        print(f"=== {seg_name} ===", flush=True)
        output[seg_name] = run_flow_queries(prefix)
        for cat, vals in output[seg_name].items():
            if isinstance(vals, dict) and not cat.endswith('_percentages') and not cat.endswith('_total'):
                for label, count in vals.items():
                    print(f"  {cat}/{label}: {count}", flush=True)

    with open('inventory/jira/flow_distribution.json', 'w') as f:
        json.dump(output, f, indent=2)
    print("\nDone.", flush=True)
