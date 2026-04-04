#!/usr/bin/env python3
"""Bitbucket PR reviewer concentration analysis + review network builder."""

import requests
import json
import os
import sys
import time
from collections import defaultdict

BB_API = "https://api.bitbucket.org/2.0"
BB_USER = os.environ.get("BB_USER", "adam.lazarus@madmobile.com")
BB_TOKEN = os.environ["BB_TOKEN"]
AUTH = (BB_USER, BB_TOKEN)

REQUEST_DELAY = 0.3
RATE_LIMIT_SLEEP = 10
MAX_RETRIES = 3


def bb_get(url, params=None):
    """GET with rate-limit retry and inter-request delay."""
    for attempt in range(MAX_RETRIES):
        resp = requests.get(url, auth=AUTH, params=params)
        if resp.status_code == 429:
            wait = RATE_LIMIT_SLEEP * (attempt + 1)
            print(f"  429 rate-limited, sleeping {wait}s...", flush=True)
            time.sleep(wait)
            continue
        resp.raise_for_status()
        time.sleep(REQUEST_DELAY)
        return resp.json()
    raise RuntimeError(f"Rate-limited after {MAX_RETRIES} retries: {url}")


def get_merged_prs(workspace, repo_slug, max_pages=5):
    """Fetch merged PRs with participant data via fields expansion."""
    items = []
    url = f"{BB_API}/repositories/{workspace}/{repo_slug}/pullrequests"
    params = {
        "state": "MERGED",
        "pagelen": 50,
        "sort": "-updated_on",
        "fields": "+values.participants,+values.author",
    }
    page = 0
    while url and page < max_pages:
        data = bb_get(url, params=params)
        items.extend(data.get("values", []))
        url = data.get("next")
        params = None
        page += 1
    return items


def get_pr_detail(workspace, repo_slug, pr_id):
    """Fetch a single PR's full detail (includes participants)."""
    url = f"{BB_API}/repositories/{workspace}/{repo_slug}/pullrequests/{pr_id}"
    return bb_get(url)


def extract_author(pr):
    author = pr.get("author", {})
    return author.get("display_name") or author.get("nickname") or "Unknown"


def extract_reviewers(pr):
    """Extract reviewer names from participants. Returns set of display names."""
    reviewers = set()
    for p in pr.get("participants", []):
        if p.get("role") == "REVIEWER":
            name = p.get("user", {}).get("display_name") or p.get("user", {}).get("nickname") or "Unknown"
            reviewers.add(name)
    return reviewers


def process_repo(workspace, repo_slug):
    """Fetch PRs and enrich with participants if needed. Returns list of (author, reviewers, pr_id) tuples."""
    prs = get_merged_prs(workspace, repo_slug)
    if not prs:
        return [], 0

    has_participants = any(pr.get("participants") for pr in prs[:5])

    results = []
    detail_fetches = 0

    for pr in prs:
        pr_id = pr.get("id")
        author = extract_author(pr)
        participants = pr.get("participants", [])

        if not participants and not has_participants:
            try:
                detail = get_pr_detail(workspace, repo_slug, pr_id)
                participants = detail.get("participants", [])
                pr["participants"] = participants
                detail_fetches += 1
            except Exception as e:
                print(f"    Warning: couldn't fetch PR #{pr_id} detail: {e}", flush=True)

        reviewers = extract_reviewers(pr)
        results.append((author, reviewers, pr_id))

    return results, detail_fetches


def build_outputs(all_repo_data):
    """Build both reviewer_concentration and review_network outputs."""
    per_repo = []
    global_reviewer_counts = defaultdict(int)
    edge_map = defaultdict(lambda: {"count": 0, "repos": set()})
    node_map = defaultdict(lambda: {"reviews_given": 0, "reviews_received": 0, "prs_authored": 0, "repos": set()})
    errors = []

    for workspace, repo, pr_data in all_repo_data:
        repo_reviewer_counts = defaultdict(int)
        total_prs = len(pr_data)

        for author, reviewers, pr_id in pr_data:
            node_map[author]["prs_authored"] += 1
            node_map[author]["repos"].add(f"{workspace}/{repo}")

            for reviewer in reviewers:
                repo_reviewer_counts[reviewer] += 1
                global_reviewer_counts[reviewer] += 1

                edge_key = (author, reviewer)
                edge_map[edge_key]["count"] += 1
                edge_map[edge_key]["repos"].add(f"{workspace}/{repo}")

                node_map[reviewer]["reviews_given"] += 1
                node_map[reviewer]["repos"].add(f"{workspace}/{repo}")
                node_map[author]["reviews_received"] += 1

        top = sorted(repo_reviewer_counts.items(), key=lambda x: -x[1])[:5]
        top_pct = round(top[0][1] / total_prs * 100, 1) if top and total_prs else 0
        per_repo.append({
            "workspace": workspace,
            "repo": repo,
            "total_prs": total_prs,
            "top_reviewers": [{"name": n, "count": c, "pct": round(c / total_prs * 100, 1)} for n, c in top],
            "top_reviewer_pct": top_pct,
            "is_bottleneck": top_pct > 60,
        })

    global_top = sorted(global_reviewer_counts.items(), key=lambda x: -x[1])[:20]
    bottleneck_repos = [r for r in per_repo if r["is_bottleneck"]]

    concentration = {
        "per_repo": per_repo,
        "global_top_20_reviewers": [{"name": n, "total_reviews": c} for n, c in global_top],
        "bottleneck_repos": [
            {
                "workspace": r["workspace"],
                "repo": r["repo"],
                "top_reviewer": r["top_reviewers"][0]["name"] if r["top_reviewers"] else "",
                "pct": r["top_reviewer_pct"],
            }
            for r in bottleneck_repos
        ],
    }

    edges = sorted(
        [
            {"author": a, "reviewer": r, "count": d["count"], "repos": sorted(d["repos"])}
            for (a, r), d in edge_map.items()
        ],
        key=lambda x: -x["count"],
    )

    nodes = sorted(
        [
            {
                "name": name,
                "reviews_given": d["reviews_given"],
                "reviews_received": d["reviews_received"],
                "prs_authored": d["prs_authored"],
                "repos": sorted(d["repos"]),
            }
            for name, d in node_map.items()
        ],
        key=lambda x: -(x["reviews_given"] + x["reviews_received"]),
    )

    workspace_repos = defaultdict(set)
    for name, d in node_map.items():
        for repo_path in d["repos"]:
            ws = repo_path.split("/")[0]
            workspace_repos[name].add(ws)

    cross_ws = [
        {"name": name, "workspaces": sorted(wss)}
        for name, wss in workspace_repos.items()
        if len(wss) > 1
    ]

    all_reviewers = {r for (_, r), _ in edge_map.items()}
    all_authors = {a for (a, _), _ in edge_map.items()}
    isolated = sorted(all_authors - all_reviewers)

    network = {
        "edges": edges,
        "nodes": nodes,
        "cross_workspace_reviews": cross_ws,
        "isolated_authors": isolated,
    }

    return concentration, network


if __name__ == "__main__":
    os.makedirs("inventory/bitbucket", exist_ok=True)

    metrics = json.load(open("inventory/bitbucket/metrics.json"))
    repos = [(m["workspace"], m["repo"]) for m in metrics[:50]]

    all_repo_data = []
    total_prs_with_reviewers = 0
    total_detail_fetches = 0
    errors = []

    for i, (ws, repo) in enumerate(repos):
        print(f"[{i+1}/{len(repos)}] {ws}/{repo}...", flush=True)
        try:
            pr_data, detail_fetches = process_repo(ws, repo)
            prs_with_reviewers = sum(1 for _, revs, _ in pr_data if revs)
            total_prs_with_reviewers += prs_with_reviewers
            total_detail_fetches += detail_fetches
            all_repo_data.append((ws, repo, pr_data))
            if detail_fetches:
                print(f"  -> {len(pr_data)} PRs, {prs_with_reviewers} with reviewers (fetched {detail_fetches} details)", flush=True)
            else:
                print(f"  -> {len(pr_data)} PRs, {prs_with_reviewers} with reviewers", flush=True)
        except Exception as e:
            errors.append(f"{ws}/{repo}: {e}")
            print(f"  ERROR: {e}", flush=True)

    concentration, network = build_outputs(all_repo_data)

    with open("inventory/bitbucket/reviewer_concentration.json", "w") as f:
        json.dump(concentration, f, indent=2)

    with open("inventory/bitbucket/review_network.json", "w") as f:
        json.dump(network, f, indent=2)

    print(f"\n{'='*60}")
    print(f"Repos processed: {len(all_repo_data)}/{len(repos)}")
    print(f"Total PRs with reviewer data: {total_prs_with_reviewers}")
    print(f"Detail fetches needed: {total_detail_fetches}")
    print(f"Review network edges: {len(network['edges'])}")
    print(f"Review network nodes: {len(network['nodes'])}")
    if errors:
        print(f"Errors ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
    top5 = concentration["global_top_20_reviewers"][:5]
    if top5:
        print(f"\nTop 5 reviewers:")
        for r in top5:
            print(f"  {r['name']}: {r['total_reviews']} reviews")
    print(f"\nBottleneck repos (>60% single reviewer): {len(concentration['bottleneck_repos'])}")
    print("Done.", flush=True)
