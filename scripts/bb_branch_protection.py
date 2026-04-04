#!/usr/bin/env python3
"""Bitbucket branch protection rules and open PR aging analysis."""

import requests
import json
import os
import time
from datetime import datetime, timezone

BB_API = "https://api.bitbucket.org/2.0"
BB_USER = os.environ.get("BB_USER", "adam.lazarus@madmobile.com")
BB_TOKEN = os.environ["BB_TOKEN"]
AUTH = (BB_USER, BB_TOKEN)
MAX_REPOS = 50


def bb_get(url, params=None, max_retries=3):
    for attempt in range(max_retries):
        resp = requests.get(url, auth=AUTH, params=params)
        if resp.status_code == 429:
            wait = int(resp.headers.get("Retry-After", 5))
            print(f"  Rate limited, sleeping {wait}s...", flush=True)
            time.sleep(wait)
            continue
        return resp
    return resp


def fetch_branch_restrictions(workspace, repo_slug):
    url = f"{BB_API}/repositories/{workspace}/{repo_slug}/branch-restrictions"
    restrictions = []
    params = {"pagelen": 100}
    page = 0
    while url and page < 5:
        resp = bb_get(url, params=params)
        if resp.status_code in (404, 403):
            return None
        resp.raise_for_status()
        data = resp.json()
        restrictions.extend(data.get("values", []))
        url = data.get("next")
        params = None
        page += 1
    return restrictions


def fetch_open_prs(workspace, repo_slug):
    url = f"{BB_API}/repositories/{workspace}/{repo_slug}/pullrequests"
    params = {
        "state": "OPEN",
        "pagelen": 50,
        "fields": ",".join([
            "next", "values.id", "values.title", "values.author",
            "values.created_on", "values.updated_on", "values.comment_count",
            "values.participants", "values.reviewers", "values.state",
        ]),
    }
    prs = []
    page = 0
    while url and page < 3:
        resp = bb_get(url, params=params)
        if resp.status_code in (404, 403):
            return []
        resp.raise_for_status()
        data = resp.json()
        prs.extend(data.get("values", []))
        url = data.get("next")
        params = None
        page += 1
    return prs


def parse_datetime(s):
    if not s:
        return None
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


if __name__ == "__main__":
    os.makedirs("inventory/bitbucket", exist_ok=True)
    now = datetime.now(timezone.utc)

    metrics = json.load(open("inventory/bitbucket/metrics.json"))
    repos_sorted = sorted(metrics, key=lambda m: m["commits"]["total_commits_6mo"], reverse=True)
    repos = [(m["workspace"], m["repo"]) for m in repos_sorted[:MAX_REPOS]]
    print(f"Scanning {len(repos)} repos...\n")

    # --- Branch Restrictions ---
    restriction_results = []
    errors = []
    for i, (ws, repo) in enumerate(repos):
        print(f"[{i+1}/{len(repos)}] restrictions: {ws}/{repo}...", flush=True)
        try:
            raw = fetch_branch_restrictions(ws, repo)
        except Exception as e:
            errors.append({"repo": f"{ws}/{repo}", "error": str(e)})
            print(f"  ERROR: {e}", flush=True)
            time.sleep(0.3)
            continue

        if raw is None:
            restriction_results.append({
                "workspace": ws,
                "repo": repo,
                "status": "no_restrictions_found",
                "restrictions": [],
            })
        else:
            parsed = []
            for r in raw:
                parsed.append({
                    "kind": r.get("kind", ""),
                    "pattern": r.get("pattern", ""),
                    "value": r.get("value"),
                })
            restriction_results.append({
                "workspace": ws,
                "repo": repo,
                "status": "ok",
                "restrictions": parsed,
            })
        time.sleep(0.3)

    repos_no_restrictions = [r for r in restriction_results if not r["restrictions"]]
    repos_with_approvals = [
        r for r in restriction_results
        if any(x["kind"] == "require_approvals_to_merge" for x in r["restrictions"])
    ]
    repos_with_builds = [
        r for r in restriction_results
        if any(x["kind"] == "require_passing_builds_to_merge" for x in r["restrictions"])
    ]
    approval_values = [
        x["value"] for r in restriction_results
        for x in r["restrictions"]
        if x["kind"] == "require_approvals_to_merge" and x["value"] is not None
    ]
    avg_min_approvals = round(sum(approval_values) / len(approval_values), 1) if approval_values else None

    restrictions_output = {
        "scanned_repos": len(restriction_results),
        "summary": {
            "repos_with_no_restrictions": len(repos_no_restrictions),
            "repos_requiring_approvals": len(repos_with_approvals),
            "repos_requiring_passing_builds": len(repos_with_builds),
            "avg_min_approvals": avg_min_approvals,
        },
        "repos": restriction_results,
        "errors": errors,
    }
    with open("inventory/bitbucket/branch_restrictions.json", "w") as f:
        json.dump(restrictions_output, f, indent=2)

    print(f"\n--- Branch Restrictions Summary ---")
    print(f"  No restrictions: {len(repos_no_restrictions)}")
    print(f"  Require approvals: {len(repos_with_approvals)}")
    print(f"  Require passing builds: {len(repos_with_builds)}")
    print(f"  Avg min approvals: {avg_min_approvals}")

    # --- Open PR Aging ---
    print(f"\n--- Fetching Open PRs ---")
    all_prs = []
    pr_errors = []
    for i, (ws, repo) in enumerate(repos):
        print(f"[{i+1}/{len(repos)}] open PRs: {ws}/{repo}...", flush=True)
        try:
            raw_prs = fetch_open_prs(ws, repo)
        except Exception as e:
            pr_errors.append({"repo": f"{ws}/{repo}", "error": str(e)})
            print(f"  ERROR: {e}", flush=True)
            time.sleep(0.3)
            continue

        for pr in raw_prs:
            created = parse_datetime(pr.get("created_on", ""))
            updated = parse_datetime(pr.get("updated_on", ""))
            age_days = (now - created).days if created else None
            reviewer_count = len(pr.get("reviewers", []) or [])
            if reviewer_count == 0:
                reviewer_count = len([
                    p for p in (pr.get("participants") or [])
                    if p.get("role") == "REVIEWER"
                ])
            all_prs.append({
                "workspace": ws,
                "repo": repo,
                "id": pr.get("id"),
                "title": pr.get("title", ""),
                "author": (pr.get("author") or {}).get("display_name", ""),
                "created_on": pr.get("created_on", ""),
                "updated_on": pr.get("updated_on", ""),
                "age_days": age_days,
                "comment_count": pr.get("comment_count", 0),
                "reviewer_count": reviewer_count,
            })
        if raw_prs:
            print(f"  -> {len(raw_prs)} open PRs", flush=True)
        time.sleep(0.3)

    older_7 = [p for p in all_prs if p["age_days"] is not None and p["age_days"] > 7]
    older_30 = [p for p in all_prs if p["age_days"] is not None and p["age_days"] > 30]
    no_reviewers = [p for p in all_prs if p["reviewer_count"] == 0]
    no_comments = [p for p in all_prs if p["comment_count"] == 0]
    oldest_20 = sorted(all_prs, key=lambda p: p["age_days"] or 0, reverse=True)[:20]

    prs_output = {
        "scanned_repos": len(repos),
        "summary": {
            "total_open_prs": len(all_prs),
            "prs_older_than_7_days": len(older_7),
            "prs_older_than_30_days": len(older_30),
            "prs_with_0_reviewers": len(no_reviewers),
            "prs_with_0_comments": len(no_comments),
        },
        "oldest_20_prs": oldest_20,
        "all_open_prs": all_prs,
        "errors": pr_errors,
    }
    with open("inventory/bitbucket/open_prs.json", "w") as f:
        json.dump(prs_output, f, indent=2)

    print(f"\n--- Open PR Summary ---")
    print(f"  Total open PRs: {len(all_prs)}")
    print(f"  Older than 7 days: {len(older_7)}")
    print(f"  Older than 30 days: {len(older_30)}")
    print(f"  With 0 reviewers: {len(no_reviewers)}")
    print(f"  With 0 comments: {len(no_comments)}")
    if pr_errors:
        print(f"  Errors: {len(pr_errors)}")

    print("\nDone.", flush=True)
