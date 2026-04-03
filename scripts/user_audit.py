#!/usr/bin/env python3
"""Cross-system user audit: enumerate users + activity from BB, Jira, Confluence, AWS."""

import requests
import json
import os
import sys
import time
import glob
import boto3
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from requests.auth import HTTPBasicAuth
from botocore.exceptions import ClientError

BB_API = "https://api.bitbucket.org/2.0"
BB_USER = os.environ.get("BB_USER", "adam.lazarus@madmobile.com")
BB_TOKEN = os.environ["BB_TOKEN"]
BB_AUTH = (BB_USER, BB_TOKEN)

JIRA_URL = os.environ.get("ATLASSIAN_URL", "https://madmobile-eng.atlassian.net")
JIRA_EMAIL = os.environ.get("ATLASSIAN_EMAIL", "adam.lazarus@madmobile.com")
JIRA_TOKEN = os.environ["ATLASSIAN_TOKEN"]
JIRA_AUTH = HTTPBasicAuth(JIRA_EMAIL, JIRA_TOKEN)
JIRA_HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}

NINETY_DAYS_AGO = datetime.now(timezone.utc) - timedelta(days=90)
OUTPUT_DIR = "inventory/users"

sys.path.insert(0, os.path.dirname(__file__))
import jira_config


# ─── BITBUCKET ──────────────────────────────────────────────────────────

def get_bb_members():
    """Get all workspace members across all 4 workspaces."""
    workspaces = ['madmobile', 'syscolabs', 'madpayments', 'syscolabsconf']
    all_members = {}
    for ws in workspaces:
        print(f"  BB workspace: {ws}...", flush=True)
        url = f"{BB_API}/workspaces/{ws}/members"
        params = {"pagelen": 100}
        while url:
            resp = requests.get(url, auth=BB_AUTH, params=params)
            if resp.status_code != 200:
                print(f"    Error: {resp.status_code}", flush=True)
                break
            data = resp.json()
            for m in data.get('values', []):
                u = m.get('user', {})
                uid = u.get('account_id', u.get('uuid', ''))
                name = u.get('display_name', '')
                if uid not in all_members:
                    all_members[uid] = {
                        'account_id': uid, 'display_name': name,
                        'nickname': u.get('nickname', ''),
                        'type': u.get('type', ''),
                        'workspaces': [],
                    }
                all_members[uid]['workspaces'].append(ws)
            url = data.get('next')
            params = None
            time.sleep(0.2)
    return list(all_members.values())


def get_bb_commit_authors():
    """Get commit authors from top 30 repos (existing metrics data)."""
    authors = defaultdict(lambda: {'commits': 0, 'repos': set()})
    metrics = json.load(open('inventory/bitbucket/metrics.json'))
    for m in metrics:
        for pr in m.get('pr_cycle_times', []):
            author = pr.get('author', '')
            if author:
                authors[author]['repos'].add(f"{m['workspace']}/{m['repo']}")
        # Commit authors -- we need to collect from the commit data
        # The weekly_unique_authors has counts, not names
        # We'll use PR authors as a proxy for now
    return {k: {'commits_proxy': 0, 'prs_authored': len([p for p in sum([m2.get('pr_cycle_times', []) for m2 in metrics], []) if p.get('author') == k]),
                 'repos': list(v['repos'])} for k, v in authors.items()}


def get_bb_pr_authors_and_reviewers():
    """Extract PR authors and reviewers from existing metrics and reviewer data."""
    pr_authors = defaultdict(int)
    pr_reviewers = defaultdict(int)

    metrics = json.load(open('inventory/bitbucket/metrics.json'))
    for m in metrics:
        for pr in m.get('pr_cycle_times', []):
            author = pr.get('author', '')
            if author:
                pr_authors[author] += 1

    try:
        reviewers = json.load(open('inventory/bitbucket/reviewer_concentration.json'))
        for r in reviewers.get('global_top_20_reviewers', []):
            pr_reviewers[r['name']] = r['total_reviews']
        for repo_data in reviewers.get('per_repo', []):
            for rev in repo_data.get('top_reviewers', []):
                if rev['name'] not in pr_reviewers:
                    pr_reviewers[rev['name']] = rev['count']
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    return dict(pr_authors), dict(pr_reviewers)


# ─── JIRA ───────────────────────────────────────────────────────────────

def get_jira_users_from_issues():
    """Get unique users from recent Jira issues (reporters + assignees)."""
    users = {}
    eng_filter = jira_config.engineering_jql()
    token = None
    total_fetched = 0

    while total_fetched < 500:
        body = {
            "jql": f"updated >= -90d AND {eng_filter} ORDER BY updated DESC",
            "maxResults": 100,
            "fields": ["reporter", "assignee", "project"],
        }
        if token:
            body["nextPageToken"] = token
        resp = requests.post(f"{JIRA_URL}/rest/api/3/search/jql",
                            auth=JIRA_AUTH, headers=JIRA_HEADERS, json=body)
        if resp.status_code != 200:
            break
        data = resp.json()
        for issue in data.get('issues', []):
            fields = issue.get('fields', {})
            for role in ['reporter', 'assignee']:
                person = fields.get(role)
                if person and person.get('accountId'):
                    aid = person['accountId']
                    if aid not in users:
                        users[aid] = {
                            'account_id': aid,
                            'display_name': person.get('displayName', ''),
                            'active': person.get('active', True),
                            'account_type': person.get('accountType', ''),
                            'projects': set(),
                            'roles': set(),
                        }
                    users[aid]['projects'].add(fields.get('project', {}).get('key', ''))
                    users[aid]['roles'].add(role)
        total_fetched += len(data.get('issues', []))
        token = data.get('nextPageToken')
        if not token:
            break
        time.sleep(0.2)

    # Add project leads
    try:
        projects = json.load(open('inventory/jira/projects.json'))
        for p in projects:
            lead = p.get('lead', '')
            if lead:
                for uid, u in users.items():
                    if u['display_name'] == lead:
                        u['roles'].add('project_lead')
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    for u in users.values():
        u['projects'] = sorted(list(u['projects']))
        u['roles'] = sorted(list(u['roles']))
    return list(users.values())


def get_jira_user_activity(account_id):
    """Get activity counts for a single Jira user."""
    activity = {}
    queries = {
        'issues_created_90d': f'reporter = "{account_id}" AND created >= -90d',
        'issues_resolved_90d': f'assignee = "{account_id}" AND resolved >= -90d',
        'open_assigned': f'assignee = "{account_id}" AND statusCategory != Done',
        'bugs_created_90d': f'reporter = "{account_id}" AND issuetype = Bug AND created >= -90d',
    }
    for label, jql in queries.items():
        try:
            resp = requests.post(f"{JIRA_URL}/rest/api/3/search/approximate-count",
                                auth=JIRA_AUTH, headers=JIRA_HEADERS, json={"jql": jql})
            if resp.status_code == 200:
                activity[label] = resp.json().get('count', 0)
            else:
                activity[label] = None
        except Exception:
            activity[label] = None
        time.sleep(0.15)
    return activity


# ─── CONFLUENCE ─────────────────────────────────────────────────────────

def get_confluence_author_activity():
    """Aggregate page creation/edit activity by author from existing page index."""
    try:
        pages = json.load(open('inventory/confluence/page_index.json'))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

    authors = defaultdict(lambda: {'pages_total': 0, 'pages_90d': 0, 'spaces': set()})
    for p in pages:
        aid = p.get('author', '')
        if not aid:
            continue
        authors[aid]['pages_total'] += 1
        authors[aid]['spaces'].add(p.get('space_key', ''))
        version_date = p.get('version_created_at', '')
        if version_date:
            try:
                dt = datetime.fromisoformat(version_date.replace('Z', '+00:00'))
                if dt > NINETY_DAYS_AGO:
                    authors[aid]['pages_90d'] += 1
            except (ValueError, TypeError):
                pass

    return {k: {'pages_total': v['pages_total'], 'pages_90d': v['pages_90d'],
                'spaces': sorted(list(v['spaces']))} for k, v in authors.items()}


# ─── AWS IAM ────────────────────────────────────────────────────────────

def get_aws_iam_users():
    """Get IAM users from all accounts."""
    all_users = []
    profiles_with_users = ['mm-cake-development', 'mm-retail-prod-us', 'mm-retail-prod-eu',
                           'mm-retail-prod-apac', 'mm-customer-analytics', 'mm-mm-archive', 'mm-security']
    for profile in profiles_with_users:
        try:
            session = boto3.Session(profile_name=profile)
            iam = session.client('iam')
            users = iam.list_users()['Users']
            for u in users:
                is_service = any(kw in u['UserName'].lower() for kw in
                    ['pipeline', 'bitbucket', 'deploy', 'monitoring', 'api', 'service',
                     'lambda', 'ecr', 'analytics', 's3', 'prometheus', 'gitlab', 'doc-gen',
                     'terraform', 'ci-', 'cd-', 'bot', 'automation', 'system'])
                all_users.append({
                    'username': u['UserName'],
                    'profile': profile,
                    'created': u['CreateDate'].isoformat(),
                    'is_service_account': is_service,
                })
        except Exception as e:
            print(f"    {profile}: {e}", flush=True)
    return all_users


# ─── MAIN ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=== Phase 1: Enumerate Users ===\n", flush=True)

    print("Bitbucket workspace members...", flush=True)
    bb_members = get_bb_members()
    print(f"  {len(bb_members)} unique members across workspaces", flush=True)
    with open(f'{OUTPUT_DIR}/bitbucket_members.json', 'w') as f:
        json.dump(bb_members, f, indent=2)

    print("\nBitbucket PR authors & reviewers...", flush=True)
    pr_authors, pr_reviewers = get_bb_pr_authors_and_reviewers()
    print(f"  {len(pr_authors)} PR authors, {len(pr_reviewers)} PR reviewers", flush=True)

    print("\nJira users from recent issues...", flush=True)
    jira_users = get_jira_users_from_issues()
    print(f"  {len(jira_users)} unique Jira users", flush=True)
    with open(f'{OUTPUT_DIR}/jira_users.json', 'w') as f:
        json.dump(jira_users, f, indent=2)

    print("\nConfluence author activity...", flush=True)
    confluence_authors = get_confluence_author_activity()
    print(f"  {len(confluence_authors)} unique Confluence authors", flush=True)
    with open(f'{OUTPUT_DIR}/confluence_authors.json', 'w') as f:
        json.dump(confluence_authors, f, indent=2)

    print("\nAWS IAM users...", flush=True)
    aws_users = get_aws_iam_users()
    service = [u for u in aws_users if u['is_service_account']]
    human = [u for u in aws_users if not u['is_service_account']]
    print(f"  {len(aws_users)} total ({len(service)} service, {len(human)} possibly human)", flush=True)
    with open(f'{OUTPUT_DIR}/aws_iam_users.json', 'w') as f:
        json.dump(aws_users, f, indent=2)

    # ─── Phase 2: Jira per-user activity ────────────────────────────────

    print("\n=== Phase 2: Per-User Activity ===\n", flush=True)

    print("Jira activity per user...", flush=True)
    jira_activity = {}
    for i, user in enumerate(jira_users):
        if user.get('account_type') == 'app':
            continue
        aid = user['account_id']
        name = user['display_name']
        if (i + 1) % 20 == 0:
            print(f"  [{i+1}/{len(jira_users)}] {name}...", flush=True)
        jira_activity[aid] = get_jira_user_activity(aid)

    # ─── Phase 3: Cross-reference ───────────────────────────────────────

    print("\n=== Phase 3: Cross-Reference ===\n", flush=True)

    unified = {}

    for member in bb_members:
        name = member['display_name']
        if not name or name.lower() in ('', 'unknown'):
            continue
        unified[name] = {
            'display_name': name,
            'bitbucket': {
                'workspaces': member['workspaces'],
                'workspace_count': len(member['workspaces']),
                'prs_authored_90d': pr_authors.get(name, 0),
                'prs_reviewed_90d': pr_reviewers.get(name, 0),
            },
            'jira': None,
            'confluence': None,
            'aws_iam': [],
        }

    for user in jira_users:
        if user.get('account_type') == 'app':
            continue
        name = user['display_name']
        aid = user['account_id']
        activity = jira_activity.get(aid, {})
        classification = jira_config.classify_assignee(
            user.get('projects', []),
            {'total': activity.get('open_assigned', 0), 'bugs': activity.get('bugs_created_90d', 0),
             'stories': 0, 'tasks': 0, 'epics': 0, 'other': 0}
        )
        jira_data = {
            'account_id': aid,
            'projects': user.get('projects', []),
            'roles': user.get('roles', []),
            'issues_created_90d': activity.get('issues_created_90d', 0),
            'issues_resolved_90d': activity.get('issues_resolved_90d', 0),
            'open_assigned': activity.get('open_assigned', 0),
            'bugs_created_90d': activity.get('bugs_created_90d', 0),
            'role_classification': classification,
        }
        if name in unified:
            unified[name]['jira'] = jira_data
        else:
            unified[name] = {
                'display_name': name,
                'bitbucket': None,
                'jira': jira_data,
                'confluence': None,
                'aws_iam': [],
            }

    for aid, activity in confluence_authors.items():
        # Author IDs are opaque -- match where possible via existing Jira mapping
        for name, record in unified.items():
            if record.get('jira') and record['jira'].get('account_id') == aid:
                record['confluence'] = activity
                break

    for iam_user in aws_users:
        username = iam_user['username']
        for name, record in unified.items():
            if name.lower().replace(' ', '.') in username.lower() or username.lower() in name.lower().replace(' ', '.'):
                record['aws_iam'].append(iam_user)
                break

    # Compute activity scores
    for name, record in unified.items():
        total_activity = 0
        systems_active = 0
        bb = record.get('bitbucket')
        if bb and (bb.get('prs_authored_90d', 0) > 0 or bb.get('prs_reviewed_90d', 0) > 0):
            systems_active += 1
            total_activity += bb.get('prs_authored_90d', 0) + bb.get('prs_reviewed_90d', 0)
        jira = record.get('jira')
        if jira and (jira.get('issues_created_90d', 0) > 0 or jira.get('issues_resolved_90d', 0) > 0):
            systems_active += 1
            total_activity += jira.get('issues_created_90d', 0) + jira.get('issues_resolved_90d', 0)
        conf = record.get('confluence')
        if conf and conf.get('pages_90d', 0) > 0:
            systems_active += 1
            total_activity += conf.get('pages_90d', 0)

        record['systems_active_90d'] = systems_active
        record['total_activity_90d'] = total_activity
        if total_activity > 50:
            record['activity_level'] = 'high'
        elif total_activity > 10:
            record['activity_level'] = 'medium'
        elif total_activity > 0:
            record['activity_level'] = 'low'
        else:
            record['activity_level'] = 'inactive'

    with open(f'{OUTPUT_DIR}/unified_user_map.json', 'w') as f:
        json.dump(unified, f, indent=2)

    # ─── Audit Findings ─────────────────────────────────────────────────

    inactive = [n for n, r in unified.items() if r['activity_level'] == 'inactive']
    high_activity = sorted([(n, r['total_activity_90d']) for n, r in unified.items() if r['activity_level'] == 'high'],
                           key=lambda x: -x[1])
    multi_system = [(n, r['systems_active_90d']) for n, r in unified.items() if r['systems_active_90d'] >= 2]
    bb_only = [n for n, r in unified.items() if r.get('bitbucket') and not r.get('jira') and r['activity_level'] == 'inactive']

    findings = {
        'total_unique_users': len(unified),
        'activity_breakdown': {
            'high': sum(1 for r in unified.values() if r['activity_level'] == 'high'),
            'medium': sum(1 for r in unified.values() if r['activity_level'] == 'medium'),
            'low': sum(1 for r in unified.values() if r['activity_level'] == 'low'),
            'inactive': len(inactive),
        },
        'systems_coverage': {
            'bb_only': sum(1 for r in unified.values() if r.get('bitbucket') and not r.get('jira')),
            'jira_only': sum(1 for r in unified.values() if r.get('jira') and not r.get('bitbucket')),
            'both': sum(1 for r in unified.values() if r.get('bitbucket') and r.get('jira')),
        },
        'top_20_contributors': [{'name': n, 'activity': a} for n, a in high_activity[:20]],
        'inactive_with_access': inactive[:30],
        'multi_system_active': len(multi_system),
        'aws_service_accounts': len(service),
        'aws_human_accounts': len(human),
    }

    with open(f'{OUTPUT_DIR}/audit_findings.json', 'w') as f:
        json.dump(findings, f, indent=2)

    print(f"Total unique users: {len(unified)}", flush=True)
    print(f"Activity: {findings['activity_breakdown']}", flush=True)
    print(f"Systems: BB-only={findings['systems_coverage']['bb_only']}, "
          f"Jira-only={findings['systems_coverage']['jira_only']}, "
          f"Both={findings['systems_coverage']['both']}", flush=True)
    print(f"Top contributor: {high_activity[0] if high_activity else 'none'}", flush=True)
    print(f"Inactive with access: {len(inactive)}", flush=True)

    print("\nDone.", flush=True)
