#!/usr/bin/env python3
"""Jira people collector — extracts user records with activity metrics."""

import json
import os
import time

import requests
from requests.auth import HTTPBasicAuth

from collectors import PersonRecord

ENV_FILE = os.path.join(os.path.dirname(__file__), '..', '..', '.env.local')
BASE_URL = "https://madmobile-eng.atlassian.net"
EMAIL = "adam.lazarus@madmobile.com"
HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}


def _load_token():
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line.startswith("ATLASSIAN_TOKEN="):
                return line.split("=", 1)[1].strip('"').strip("'")
    raise RuntimeError("ATLASSIAN_TOKEN not found in .env.local")


def _auth():
    return HTTPBasicAuth(EMAIL, _load_token())


def _get_assignable_users(auth):
    """Enumerate all assignable users via multiProjectSearch."""
    resp = requests.get(
        f"{BASE_URL}/rest/api/3/user/assignable/multiProjectSearch",
        params={"projectKeys": "REST", "maxResults": 200},
        auth=auth, headers=HEADERS,
    )
    resp.raise_for_status()
    return resp.json()


def _get_user_activity(auth, account_id):
    """Get 90-day activity counts for a single user."""
    queries = {
        "issues_created_90d": f'reporter = "{account_id}" AND created >= -90d',
        "issues_resolved_90d": f'assignee = "{account_id}" AND resolved >= -90d',
        "open_assigned": f'assignee = "{account_id}" AND statusCategory != Done',
        "bugs_created_90d": f'reporter = "{account_id}" AND issuetype = Bug AND created >= -90d',
    }
    activity = {}
    for label, jql in queries.items():
        try:
            resp = requests.post(
                f"{BASE_URL}/rest/api/3/search/approximate-count",
                auth=auth, headers=HEADERS, json={"jql": jql},
            )
            activity[label] = resp.json().get("count", 0) if resp.status_code == 200 else None
        except Exception:
            activity[label] = None
        time.sleep(0.15)
    return activity


def _get_project_assignments(auth):
    """Fetch recent issues to build user -> project/role mapping."""
    users = {}
    token = None
    total_fetched = 0

    while total_fetched < 500:
        body = {
            "jql": "updated >= -90d ORDER BY updated DESC",
            "maxResults": 100,
            "fields": ["reporter", "assignee", "project"],
        }
        if token:
            body["nextPageToken"] = token

        resp = requests.post(
            f"{BASE_URL}/rest/api/3/search/jql",
            auth=auth, headers=HEADERS, json=body,
        )
        if resp.status_code != 200:
            break

        data = resp.json()
        for issue in data.get("issues", []):
            fields = issue.get("fields", {})
            for role in ("reporter", "assignee"):
                person = fields.get(role)
                if not person or not person.get("accountId"):
                    continue
                aid = person["accountId"]
                if aid not in users:
                    users[aid] = {"projects": set(), "roles": set()}
                proj_key = fields.get("project", {}).get("key", "")
                if proj_key:
                    users[aid]["projects"].add(proj_key)
                users[aid]["roles"].add(role)

        total_fetched += len(data.get("issues", []))
        token = data.get("nextPageToken")
        if not token:
            break
        time.sleep(0.15)

    return {aid: {"projects": sorted(v["projects"]), "roles": sorted(v["roles"])}
            for aid, v in users.items()}


def collect() -> list[PersonRecord]:
    auth = _auth()

    print("Jira: fetching assignable users...", flush=True)
    raw_users = _get_assignable_users(auth)
    humans = [u for u in raw_users if u.get("accountType") != "app"]
    print(f"Jira: {len(humans)} human users (filtered from {len(raw_users)} total)", flush=True)
    time.sleep(0.15)

    print("Jira: fetching project assignments...", flush=True)
    assignments = _get_project_assignments(auth)
    time.sleep(0.15)

    print("Jira: fetching per-user activity...", flush=True)
    records = []
    for i, user in enumerate(humans):
        aid = user.get("accountId", "")
        name = user.get("displayName", "")

        if (i + 1) % 20 == 0:
            print(f"  [{i + 1}/{len(humans)}] {name}...", flush=True)

        activity = _get_user_activity(auth, aid)
        user_assignments = assignments.get(aid, {"projects": [], "roles": []})

        records.append(PersonRecord(
            source="jira",
            canonical_name=name,
            email=user.get("emailAddress"),
            account_id=aid,
            status="active" if user.get("active") else "inactive",
            metadata={
                "projects": user_assignments["projects"],
                "roles": user_assignments["roles"],
                "issues_created_90d": activity.get("issues_created_90d"),
                "issues_resolved_90d": activity.get("issues_resolved_90d"),
                "open_assigned": activity.get("open_assigned"),
                "bugs_created_90d": activity.get("bugs_created_90d"),
                "timeZone": user.get("timeZone"),
                "active": user.get("active", True),
            },
        ))

    print(f"Jira: collected {len(records)} person records", flush=True)
    return records


if __name__ == "__main__":
    people = collect()
    print(json.dumps([{"name": p.canonical_name, "email": p.email, **p.metadata}
                       for p in people[:5]], indent=2))
