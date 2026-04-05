#!/usr/bin/env python3
"""Bitbucket people collector — extracts workspace members with PR/review metrics."""

import json
import os
import time
from collections import defaultdict

import requests

from collectors import PersonRecord

ENV_FILE = os.path.join(os.path.dirname(__file__), '..', '..', '.env.local')
BB_API = "https://api.bitbucket.org/2.0"
BB_USER = "adam.lazarus@madmobile.com"
WORKSPACES = ["madmobile", "syscolabs", "madpayments", "syscolabsconf"]
INVENTORY_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'inventory', 'bitbucket')


def _load_token():
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line.startswith("BB_TOKEN="):
                return line.split("=", 1)[1].strip('"').strip("'")
    raise RuntimeError("BB_TOKEN not found in .env.local")


def _auth():
    return (BB_USER, _load_token())


def _enumerate_members(auth):
    """Get all workspace members across all workspaces."""
    all_members = {}
    for ws in WORKSPACES:
        print(f"  Bitbucket workspace: {ws}...", flush=True)
        url = f"{BB_API}/workspaces/{ws}/members"
        params = {"pagelen": 100}
        while url:
            resp = requests.get(url, auth=auth, params=params)
            if resp.status_code != 200:
                print(f"    Error {resp.status_code} for {ws}", flush=True)
                break
            data = resp.json()
            for m in data.get("values", []):
                u = m.get("user", {})
                uid = u.get("account_id", u.get("uuid", ""))
                name = u.get("display_name", "")
                if uid not in all_members:
                    all_members[uid] = {
                        "account_id": uid,
                        "display_name": name,
                        "nickname": u.get("nickname", ""),
                        "workspaces": [],
                    }
                all_members[uid]["workspaces"].append(ws)
            url = data.get("next")
            params = None
            time.sleep(0.2)
    return all_members


def _load_json(filename):
    path = os.path.join(INVENTORY_DIR, filename)
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def _load_pr_authors():
    """Count PRs authored per display_name from metrics.json."""
    metrics = _load_json("metrics.json")
    if not metrics:
        return {}
    counts = defaultdict(int)
    for repo_data in metrics:
        for pr in repo_data.get("pr_cycle_times", []):
            author = pr.get("author", "")
            if author:
                counts[author] += 1
    return dict(counts)


def _load_reviewer_counts():
    """Get review counts per person from reviewer_concentration.json."""
    data = _load_json("reviewer_concentration.json")
    if not data:
        return {}
    counts = {}
    for r in data.get("global_top_20_reviewers", []):
        counts[r["name"]] = r["total_reviews"]
    for repo_data in data.get("per_repo", []):
        for rev in repo_data.get("top_reviewers", []):
            if rev["name"] not in counts:
                counts[rev["name"]] = rev["count"]
    return counts


def _load_review_clusters():
    """Map person -> cluster from review_network_summary.json."""
    data = _load_json("review_network_summary.json")
    if not data:
        return {}
    mapping = {}
    for cluster_name, cluster_info in data.get("clusters", {}).items():
        for member in cluster_info.get("members", []):
            mapping[member] = cluster_name
    return mapping


def collect() -> list[PersonRecord]:
    auth = _auth()

    print("Bitbucket: enumerating workspace members...", flush=True)
    members = _enumerate_members(auth)
    print(f"Bitbucket: {len(members)} unique members across {len(WORKSPACES)} workspaces", flush=True)

    pr_authors = _load_pr_authors()
    reviewer_counts = _load_reviewer_counts()
    review_clusters = _load_review_clusters()

    records = []
    for uid, info in members.items():
        name = info["display_name"]
        records.append(PersonRecord(
            source="bitbucket",
            canonical_name=name,
            account_id=info["account_id"],
            metadata={
                "workspaces": info["workspaces"],
                "nickname": info["nickname"],
                "prs_authored": pr_authors.get(name, 0),
                "prs_reviewed": reviewer_counts.get(name, 0),
                "review_cluster": review_clusters.get(name),
            },
        ))

    print(f"Bitbucket: collected {len(records)} person records", flush=True)
    return records


if __name__ == "__main__":
    people = collect()
    active = [p for p in people if p.metadata.get("prs_authored", 0) > 0 or p.metadata.get("prs_reviewed", 0) > 0]
    print(f"\n{len(active)} members with PR activity:")
    for p in sorted(active, key=lambda x: x.metadata.get("prs_authored", 0), reverse=True)[:10]:
        print(f"  {p.canonical_name}: {p.metadata['prs_authored']} PRs authored, "
              f"{p.metadata['prs_reviewed']} reviews, cluster={p.metadata['review_cluster']}")
