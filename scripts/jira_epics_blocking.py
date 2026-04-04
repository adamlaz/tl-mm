#!/usr/bin/env python3
"""Jira epic completion, priority distribution, blocking chains, and status transition analysis."""

import requests
import json
import os
import time
from datetime import datetime, timedelta, timezone
from collections import defaultdict
from statistics import median
from requests.auth import HTTPBasicAuth
import jira_config

JIRA_URL = os.environ.get("ATLASSIAN_URL", "https://madmobile-eng.atlassian.net")
JIRA_EMAIL = os.environ.get("ATLASSIAN_EMAIL", "adam.lazarus@madmobile.com")
JIRA_TOKEN = os.environ["ATLASSIAN_TOKEN"]
AUTH = HTTPBasicAuth(JIRA_EMAIL, JIRA_TOKEN)
HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}


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


def approximate_count(jql):
    return api_post('/rest/api/3/search/approximate-count', {"jql": jql}).get('count', 0)


def search_issues_jql(jql, fields=None, max_results=100, expand=None):
    body = {"jql": jql, "maxResults": min(max_results, 100)}
    if fields:
        body["fields"] = fields
    if expand:
        body["expand"] = expand
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


# ---------------------------------------------------------------------------
# 1. Epic Completion
# ---------------------------------------------------------------------------
def get_epic_completion():
    eng = jira_config.engineering_jql()
    twelve_months_ago = (datetime.now(timezone.utc) - timedelta(days=365)).strftime('%Y-%m-%d')

    base_jql = f'issuetype = Epic AND created >= "{twelve_months_ago}" AND {eng}'
    total = approximate_count(base_jql)
    resolved = approximate_count(f'{base_jql} AND statusCategory = Done')
    unresolved = total - resolved

    print(f"  Total epics (12mo): {total}, Resolved: {resolved}, Unresolved: {unresolved}", flush=True)

    issues = search_issues_jql(
        f'{base_jql} ORDER BY project ASC',
        fields=["project", "status", "statusCategory", "resolution"],
        max_results=1000
    )

    by_project = defaultdict(lambda: {"total": 0, "resolved": 0})
    for issue in issues:
        f = issue.get('fields', {})
        pkey = f.get('project', {}).get('key', 'UNKNOWN')
        by_project[pkey]["total"] += 1
        status_cat = f.get('status', {}).get('statusCategory', {}).get('name', '')
        if status_cat == 'Done':
            by_project[pkey]["resolved"] += 1

    projects = []
    for pkey, counts in sorted(by_project.items(), key=lambda x: x[1]["total"], reverse=True):
        rate = round(counts["resolved"] / counts["total"] * 100, 1) if counts["total"] else 0
        projects.append({
            "project": pkey,
            "total_epics": counts["total"],
            "resolved": counts["resolved"],
            "unresolved": counts["total"] - counts["resolved"],
            "resolution_rate_pct": rate,
        })

    overall_rate = round(resolved / total * 100, 1) if total else 0
    return {
        "period": f"{twelve_months_ago} to today",
        "total_epics": total,
        "resolved": resolved,
        "unresolved": unresolved,
        "overall_resolution_rate_pct": overall_rate,
        "top_10_by_count": projects[:10],
        "all_projects": projects,
    }


# ---------------------------------------------------------------------------
# 2. Priority Distribution
# ---------------------------------------------------------------------------
def get_priority_distribution():
    eng = jira_config.engineering_jql()
    base_jql = f'statusCategory != Done AND {eng}'

    issues = search_issues_jql(
        f'{base_jql} ORDER BY priority DESC',
        fields=["priority"],
        max_results=1000
    )

    total_approx = approximate_count(base_jql)

    counts = defaultdict(int)
    for issue in issues:
        pri = issue.get('fields', {}).get('priority')
        pname = pri.get('name', 'None') if isinstance(pri, dict) else 'None'
        counts[pname] += 1

    sampled = sum(counts.values())
    priorities = []
    for pname, cnt in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        priorities.append({
            "priority": pname,
            "count": cnt,
            "pct_of_sample": round(cnt / sampled * 100, 1) if sampled else 0,
        })

    critical_and_above = sum(
        c for p, c in counts.items()
        if p.lower() in ('blocker', 'critical', 'highest')
    )
    inflation = critical_and_above / sampled > 0.5 if sampled else False

    return {
        "total_open_approx": total_approx,
        "sample_size": sampled,
        "distribution": priorities,
        "critical_or_higher_pct": round(critical_and_above / sampled * 100, 1) if sampled else 0,
        "priority_inflation_flag": inflation,
    }


# ---------------------------------------------------------------------------
# 3. Blocking Analysis
# ---------------------------------------------------------------------------
def get_blocking_chains():
    eng = jira_config.engineering_jql()

    print("  Fetching open issues with issuelinks...", flush=True)
    issues = search_issues_jql(
        f'statusCategory != Done AND {eng} ORDER BY updated DESC',
        fields=["issuelinks", "status", "priority", "project", "summary"],
        max_results=500
    )
    print(f"  Fetched {len(issues)} issues, analyzing links...", flush=True)

    blocking_others = []  # issues that block something
    blocked_by = []       # issues blocked by something
    link_type_counts = defaultdict(int)

    for issue in issues:
        key = issue['key']
        f = issue.get('fields', {})
        links = f.get('issuelinks', []) or []

        is_blocker = False
        is_blocked = False

        for link in links:
            ltype = link.get('type', {}).get('name', '')
            link_type_counts[ltype] += 1

            if link.get('outwardIssue') and 'block' in link.get('type', {}).get('outward', '').lower():
                is_blocker = True
            if link.get('inwardIssue') and 'block' in link.get('type', {}).get('inward', '').lower():
                is_blocked = True

        info = {
            "key": key,
            "project": f.get('project', {}).get('key', ''),
            "priority": f.get('priority', {}).get('name', ''),
            "status": f.get('status', {}).get('name', ''),
            "summary": (f.get('summary') or '')[:80],
            "link_count": len(links),
        }
        if is_blocker:
            blocking_others.append(info)
        if is_blocked:
            blocked_by.append(info)

    return {
        "sample_size": len(issues),
        "issues_blocking_others": len(blocking_others),
        "issues_blocked": len(blocked_by),
        "link_type_distribution": dict(link_type_counts),
        "top_blockers": sorted(blocking_others, key=lambda x: x["link_count"], reverse=True)[:15],
        "top_blocked": sorted(blocked_by, key=lambda x: x["link_count"], reverse=True)[:15],
    }


# ---------------------------------------------------------------------------
# 4. Status Transitions
# ---------------------------------------------------------------------------
def get_status_transitions():
    eng = jira_config.engineering_jql()

    print("  Fetching recently resolved issues...", flush=True)
    issues = search_issues_jql(
        f'statusCategory = Done AND resolved >= -90d AND {eng} ORDER BY resolved DESC',
        fields=["key", "project", "status", "resolutiondate"],
        max_results=100
    )
    print(f"  Got {len(issues)} issues, fetching changelogs...", flush=True)

    status_durations = defaultdict(list)  # status_name -> [hours]
    errors = 0

    for idx, issue in enumerate(issues):
        key = issue['key']
        try:
            changelog = api_get(f'/rest/api/3/issue/{key}/changelog', params={'maxResults': 100})
        except Exception as e:
            errors += 1
            continue

        transitions = []
        for history in changelog.get('values', []):
            ts = history.get('created', '')
            for item in history.get('items', []):
                if item.get('field') == 'status':
                    transitions.append({
                        'timestamp': ts,
                        'from': item.get('fromString', ''),
                        'to': item.get('toString', ''),
                    })

        transitions.sort(key=lambda t: t['timestamp'])

        for i, tr in enumerate(transitions):
            from_status = tr['from']
            if not from_status:
                continue
            entered = transitions[i - 1]['timestamp'] if i > 0 else issue.get('fields', {}).get('created', '')
            if not entered:
                continue
            try:
                entered_dt = datetime.fromisoformat(entered.replace('Z', '+00:00'))
                exited_dt = datetime.fromisoformat(tr['timestamp'].replace('Z', '+00:00'))
                hours = (exited_dt - entered_dt).total_seconds() / 3600
                if 0 < hours < 10000:
                    status_durations[from_status].append(hours)
            except (ValueError, TypeError):
                pass

        if (idx + 1) % 20 == 0:
            print(f"    Changelog {idx+1}/{len(issues)}...", flush=True)
            time.sleep(0.5)

    statuses = []
    for name, hours_list in sorted(status_durations.items(), key=lambda x: -len(x[1])):
        med = round(median(hours_list), 1)
        statuses.append({
            "status": name,
            "sample_count": len(hours_list),
            "median_hours": med,
            "median_days": round(med / 24, 1),
        })

    bottleneck = max(statuses, key=lambda s: s["median_hours"]) if statuses else None

    return {
        "issues_analyzed": len(issues),
        "changelog_errors": errors,
        "status_durations": statuses,
        "bottleneck": bottleneck,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    os.makedirs('inventory/jira', exist_ok=True)

    print("=== 1. Epic Completion (12 months) ===", flush=True)
    epic_data = get_epic_completion()
    print(f"  Overall rate: {epic_data['overall_resolution_rate_pct']}%", flush=True)
    with open('inventory/jira/epic_completion.json', 'w') as f:
        json.dump(epic_data, f, indent=2)

    print("\n=== 2. Priority Distribution ===", flush=True)
    priority_data = get_priority_distribution()
    print(f"  Inflation flag: {priority_data['priority_inflation_flag']}", flush=True)
    for p in priority_data['distribution'][:5]:
        print(f"    {p['priority']}: {p['count']} ({p['pct_of_sample']}%)", flush=True)
    with open('inventory/jira/priority_distribution.json', 'w') as f:
        json.dump(priority_data, f, indent=2)

    print("\n=== 3. Blocking Analysis ===", flush=True)
    blocking_data = get_blocking_chains()
    print(f"  Blocking others: {blocking_data['issues_blocking_others']}", flush=True)
    print(f"  Blocked: {blocking_data['issues_blocked']}", flush=True)
    with open('inventory/jira/blocking_chains.json', 'w') as f:
        json.dump(blocking_data, f, indent=2)

    print("\n=== 4. Status Transitions ===", flush=True)
    transition_data = get_status_transitions()
    if transition_data['bottleneck']:
        bn = transition_data['bottleneck']
        print(f"  Bottleneck: {bn['status']} (median {bn['median_hours']}h / {bn['median_days']}d)", flush=True)
    with open('inventory/jira/status_transitions.json', 'w') as f:
        json.dump(transition_data, f, indent=2)

    print("\n=== Summary ===", flush=True)
    print(f"  Epics: {epic_data['total_epics']} total, {epic_data['overall_resolution_rate_pct']}% resolved", flush=True)
    print(f"  Priority inflation: {priority_data['priority_inflation_flag']} ({priority_data['critical_or_higher_pct']}% critical+)", flush=True)
    print(f"  Blocking: {blocking_data['issues_blocking_others']} blockers, {blocking_data['issues_blocked']} blocked", flush=True)
    if transition_data['bottleneck']:
        print(f"  Bottleneck status: {transition_data['bottleneck']['status']} @ {transition_data['bottleneck']['median_days']}d median", flush=True)
    print("\nDone. Files written to inventory/jira/", flush=True)
