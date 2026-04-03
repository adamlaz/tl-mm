#!/usr/bin/env python3
"""Jira delivery health metrics: issue counts, cycle time, created-vs-resolved trends."""

import requests
import json
import os
import time
from datetime import datetime, timedelta, timezone
from requests.auth import HTTPBasicAuth
import jira_config

JIRA_URL = os.environ.get("ATLASSIAN_URL", "https://madmobile-eng.atlassian.net")
JIRA_EMAIL = os.environ.get("ATLASSIAN_EMAIL", "adam.lazarus@madmobile.com")
JIRA_TOKEN = os.environ["ATLASSIAN_TOKEN"]
AUTH = HTTPBasicAuth(JIRA_EMAIL, JIRA_TOKEN)
HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}
SIX_MONTHS_AGO = datetime.now(timezone.utc) - timedelta(days=180)

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

def search_issues_jql(jql, fields=None, max_results=100):
    """Use the new POST /rest/api/3/search/jql endpoint with token pagination."""
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

def paginate_agile(path):
    items = []
    start = 0
    while True:
        data = api_get(path, params={'startAt': start, 'maxResults': 50})
        batch = data.get('values', [])
        items.extend(batch)
        total = data.get('total', len(items))
        start += len(batch)
        if start >= total or not batch:
            break
    return items

def get_all_velocity():
    """Sprint velocity for ALL scrum boards."""
    boards = paginate_agile('/rest/agile/1.0/board')
    scrum_boards = [b for b in boards if b.get('type') == 'scrum']
    print(f"  Found {len(scrum_boards)} scrum boards", flush=True)

    velocity = {}
    for i, b in enumerate(scrum_boards):
        name = b['name']
        bid = b['id']
        print(f"  [{i+1}/{len(scrum_boards)}] {name}...", flush=True)
        try:
            sprints = paginate_agile(f'/rest/agile/1.0/board/{bid}/sprint')
            recent = [s for s in sprints if s.get('completeDate') and
                      datetime.fromisoformat(s['completeDate'].replace('Z', '+00:00')) > SIX_MONTHS_AGO]
            results = []
            for s in recent[-12:]:
                try:
                    v = api_get(f'/rest/agile/1.0/sprint/{s["id"]}/issue',
                                params={'maxResults': 0, 'jql': 'statusCategory = Done'})
                    done = v.get('total', 0)
                except Exception:
                    done = None
                total_in_sprint = None
                try:
                    t = api_get(f'/rest/agile/1.0/sprint/{s["id"]}/issue',
                                params={'maxResults': 0})
                    total_in_sprint = t.get('total', 0)
                except Exception:
                    pass
                results.append({
                    'id': s['id'], 'name': s['name'], 'state': s.get('state', ''),
                    'start_date': s.get('startDate', ''), 'end_date': s.get('endDate', ''),
                    'complete_date': s.get('completeDate', ''),
                    'done_issues': done, 'total_issues': total_in_sprint,
                    'completion_rate': round(done / total_in_sprint * 100, 1) if done and total_in_sprint else None,
                })
            if results:
                velocity[name] = {
                    'board_id': bid,
                    'project_key': b.get('location', {}).get('projectKey', ''),
                    'sprints': results,
                }
        except Exception as e:
            velocity[name] = {'error': str(e)}
        if (i + 1) % 10 == 0:
            time.sleep(1)

    return velocity

def get_created_vs_resolved_trend():
    """Weekly created vs resolved counts over 6 months, segmented."""
    result = {}
    now = datetime.now(timezone.utc)
    for seg_name, seg_fn in [('overall', None), ('engineering', jira_config.engineering_jql)]:
        prefix = f" AND {seg_fn()}" if seg_fn else ""
        trend = []
        print(f"    Segment: {seg_name}...", flush=True)
        for weeks_ago in range(26, -1, -1):
            week_start = now - timedelta(weeks=weeks_ago + 1)
            week_end = now - timedelta(weeks=weeks_ago)
            start_str = week_start.strftime('%Y-%m-%d')
            end_str = week_end.strftime('%Y-%m-%d')
            try:
                created = approximate_count(f'created >= "{start_str}" AND created < "{end_str}"{prefix}')
                resolved = approximate_count(f'resolved >= "{start_str}" AND resolved < "{end_str}"{prefix}')
                trend.append({
                    'week_start': start_str, 'week_end': end_str,
                    'created': created, 'resolved': resolved,
                    'net': resolved - created,
                })
            except Exception as e:
                trend.append({'week_start': start_str, 'error': str(e)})
            time.sleep(0.2)
        result[seg_name] = trend
    return result

def get_backlog_age_distribution():
    """Open issues bucketed by age, segmented."""
    result = {}
    age_ranges = [
        ('0-30d', 'statusCategory != Done AND created >= -30d'),
        ('30-90d', 'statusCategory != Done AND created >= -90d AND created < -30d'),
        ('90-180d', 'statusCategory != Done AND created >= -180d AND created < -90d'),
        ('180-365d', 'statusCategory != Done AND created >= -365d AND created < -180d'),
        ('365d+', 'statusCategory != Done AND created < -365d'),
    ]
    for seg_name, seg_fn in jira_config.SEGMENTS.items():
        prefix = f" AND {seg_fn()}" if seg_fn else ""
        buckets = {}
        print(f"    Segment: {seg_name}...", flush=True)
        for label, jql_base in age_ranges:
            try:
                buckets[label] = approximate_count(f'{jql_base}{prefix}')
            except Exception as e:
                buckets[label] = f"error: {e}"
        result[seg_name] = buckets
    return result

def get_cycle_time_sample():
    """Sample resolved issues from engineering projects and compute cycle time."""
    eng_filter = f" AND {jira_config.engineering_jql()}"
    issues = search_issues_jql(
        f'statusCategory = Done AND resolved >= -90d{eng_filter} ORDER BY resolved DESC',
        fields=["key", "summary", "issuetype", "project", "created", "resolutiondate", "status"],
        max_results=200
    )
    results = []
    for idx, issue in enumerate(issues):
        key = issue['key']
        fields = issue.get('fields', {})
        created = fields.get('created', '')
        resolved = fields.get('resolutiondate', '')
        if not created or not resolved:
            continue
        created_dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
        resolved_dt = datetime.fromisoformat(resolved.replace('Z', '+00:00'))
        total_days = (resolved_dt - created_dt).total_seconds() / 86400

        in_progress_dt = None
        try:
            changelog = api_get(f'/rest/api/3/issue/{key}/changelog', params={'maxResults': 50})
            for history in changelog.get('values', []):
                for item in history.get('items', []):
                    if item.get('field') == 'status' and item.get('toString', '').lower() in ('in progress', 'in development', 'in review'):
                        in_progress_dt = datetime.fromisoformat(history['created'].replace('Z', '+00:00'))
                        break
                if in_progress_dt:
                    break
        except Exception:
            pass

        cycle_days = None
        if in_progress_dt:
            cycle_days = round((resolved_dt - in_progress_dt).total_seconds() / 86400, 1)

        results.append({
            'key': key,
            'project': fields.get('project', {}).get('key', ''),
            'type': fields.get('issuetype', {}).get('name', ''),
            'created': created,
            'resolved': resolved,
            'total_lead_time_days': round(total_days, 1),
            'cycle_time_days': cycle_days,
        })
        if (idx + 1) % 20 == 0:
            print(f"    Changelog {idx+1}/{len(issues)}...", flush=True)
            time.sleep(0.5)
    return results


if __name__ == '__main__':
    os.makedirs('inventory/jira', exist_ok=True)

    print("=== Full Sprint Velocity (all scrum boards) ===", flush=True)
    velocity = get_all_velocity()
    boards_with_data = sum(1 for v in velocity.values() if isinstance(v, dict) and v.get('sprints'))
    print(f"  {boards_with_data} boards with sprint data", flush=True)
    with open('inventory/jira/velocity_full.json', 'w') as f:
        json.dump(velocity, f, indent=2)

    print("\n=== Backlog Age Distribution ===", flush=True)
    age = get_backlog_age_distribution()
    print(f"  {age}", flush=True)
    with open('inventory/jira/backlog_age.json', 'w') as f:
        json.dump(age, f, indent=2)

    print("\n=== Created vs Resolved Trend (26 weeks) ===", flush=True)
    trend = get_created_vs_resolved_trend()
    with open('inventory/jira/created_vs_resolved.json', 'w') as f:
        json.dump(trend, f, indent=2)

    print("\n=== Cycle Time Sample (200 recent issues) ===", flush=True)
    cycle = get_cycle_time_sample()
    print(f"  {len(cycle)} issues with cycle time data", flush=True)
    with open('inventory/jira/cycle_time.json', 'w') as f:
        json.dump(cycle, f, indent=2)

    print("\nDone.", flush=True)
