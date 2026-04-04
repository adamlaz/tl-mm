#!/usr/bin/env python3
"""Bitbucket pipeline build history collection for technology diagnostic."""

import requests
import json
import os
import time
import statistics
from collections import defaultdict
from datetime import datetime

BB_API = "https://api.bitbucket.org/2.0"
BB_USER = os.environ.get("BB_USER", "adam.lazarus@madmobile.com")
BB_TOKEN = os.environ["BB_TOKEN"]
AUTH = (BB_USER, BB_TOKEN)

REQUEST_DELAY = 0.3
MAX_RETRIES = 5


def fetch_with_backoff(url, params=None):
    for attempt in range(MAX_RETRIES):
        resp = requests.get(url, auth=AUTH, params=params)
        if resp.status_code == 429:
            wait = 2 ** attempt + 1
            print(f"  Rate limited, waiting {wait}s...", flush=True)
            time.sleep(wait)
            continue
        return resp
    return resp


def get_pipelines(workspace, repo_slug, max_results=100):
    runs = []
    url = f"{BB_API}/repositories/{workspace}/{repo_slug}/pipelines/"
    params = {"sort": "-created_on", "pagelen": 50}
    pages_fetched = 0
    max_pages = (max_results + 49) // 50

    while url and pages_fetched < max_pages:
        time.sleep(REQUEST_DELAY)
        resp = fetch_with_backoff(url, params=params)

        if resp.status_code == 404:
            return None  # no pipelines configured
        if resp.status_code >= 400:
            print(f"  HTTP {resp.status_code} for {workspace}/{repo_slug}", flush=True)
            return runs

        data = resp.json()
        for p in data.get("values", []):
            state = p.get("state", {})
            result_name = state.get("result", {}).get("name") if state.get("result") else state.get("name", "PENDING")
            target = p.get("target", {})

            runs.append({
                "uuid": p.get("uuid"),
                "result": result_name,
                "build_seconds": p.get("build_seconds_used"),
                "created_on": p.get("created_on"),
                "completed_on": p.get("completed_on"),
                "trigger_type": p.get("trigger", {}).get("type"),
                "ref_name": target.get("ref_name"),
            })

        url = data.get("next")
        params = None
        pages_fetched += 1

    return runs


def compute_build_seconds(run):
    if run["build_seconds"] and run["build_seconds"] > 0:
        return run["build_seconds"]
    if run["created_on"] and run["completed_on"]:
        try:
            c = datetime.fromisoformat(run["created_on"].replace("Z", "+00:00"))
            d = datetime.fromisoformat(run["completed_on"].replace("Z", "+00:00"))
            return max(0, (d - c).total_seconds())
        except (ValueError, TypeError):
            return None
    return None


def aggregate_repo(runs):
    total = len(runs)
    if total == 0:
        return {"total_runs": 0, "success": 0, "failed": 0, "error": 0, "stopped": 0,
                "success_rate_pct": 0, "median_build_s": None, "p95_build_s": None}

    success = sum(1 for r in runs if r["result"] == "SUCCESSFUL")
    failed = sum(1 for r in runs if r["result"] == "FAILED")
    error = sum(1 for r in runs if r["result"] == "ERROR")
    stopped = sum(1 for r in runs if r["result"] == "STOPPED")

    build_times = [s for s in (compute_build_seconds(r) for r in runs if r["result"] == "SUCCESSFUL") if s and s > 0]

    median_t = round(statistics.median(build_times), 1) if build_times else None
    p95_t = round(sorted(build_times)[int(len(build_times) * 0.95)] , 1) if len(build_times) >= 2 else median_t

    return {
        "total_runs": total,
        "success": success,
        "failed": failed,
        "error": error,
        "stopped": stopped,
        "success_rate_pct": round(success / total * 100, 1) if total else 0,
        "median_build_s": median_t,
        "p95_build_s": p95_t,
    }


def main():
    os.makedirs("inventory/bitbucket", exist_ok=True)

    with open("inventory/bitbucket/metrics.json") as f:
        metrics = json.load(f)

    repos = [(m["workspace"], m["repo"]) for m in metrics[:50]]
    print(f"Collecting pipeline history for {len(repos)} repos...\n", flush=True)

    per_repo = []
    workspace_agg = defaultdict(lambda: {"total": 0, "success": 0})
    no_pipelines = []
    errors = []
    total_runs_collected = 0

    for i, (ws, repo) in enumerate(repos):
        print(f"[{i+1}/{len(repos)}] {ws}/{repo}...", end=" ", flush=True)
        try:
            runs = get_pipelines(ws, repo)
        except Exception as e:
            errors.append({"workspace": ws, "repo": repo, "error": str(e)})
            print(f"ERROR: {e}", flush=True)
            continue

        if runs is None:
            no_pipelines.append(f"{ws}/{repo}")
            print("no pipelines (404)", flush=True)
            continue

        agg = aggregate_repo(runs)
        agg["workspace"] = ws
        agg["repo"] = repo
        per_repo.append(agg)

        workspace_agg[ws]["total"] += agg["total_runs"]
        workspace_agg[ws]["success"] += agg["success"]
        total_runs_collected += agg["total_runs"]

        print(f"{agg['total_runs']} runs, {agg['success_rate_pct']}% success", flush=True)

    ws_summary = {}
    for ws, counts in workspace_agg.items():
        ws_summary[ws] = {
            "total_runs": counts["total"],
            "success_rate_pct": round(counts["success"] / counts["total"] * 100, 1) if counts["total"] else 0,
        }

    repos_with_runs = [r for r in per_repo if r["total_runs"] >= 5]
    worst_10 = sorted(repos_with_runs, key=lambda r: r["success_rate_pct"])[:10]

    overall_total = sum(r["total_runs"] for r in per_repo)
    overall_success = sum(r["success"] for r in per_repo)
    overall_rate = round(overall_success / overall_total * 100, 1) if overall_total else 0

    output = {
        "generated_at": datetime.now(tz=__import__('datetime').timezone.utc).isoformat(),
        "repos_checked": len(repos),
        "repos_with_pipelines": len(per_repo),
        "repos_no_pipelines": no_pipelines,
        "total_pipeline_runs": total_runs_collected,
        "overall_success_rate_pct": overall_rate,
        "per_repo": per_repo,
        "per_workspace": ws_summary,
        "worst_10_by_failure_rate": [{
            "workspace": r["workspace"],
            "repo": r["repo"],
            "total_runs": r["total_runs"],
            "success_rate_pct": r["success_rate_pct"],
            "failed": r["failed"],
            "error": r["error"],
        } for r in worst_10],
        "errors": errors,
    }

    with open("inventory/bitbucket/pipeline_history.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n{'='*60}")
    print(f"Repos checked:        {len(repos)}")
    print(f"Repos with pipelines: {len(per_repo)}")
    print(f"No pipelines (404):   {len(no_pipelines)}")
    print(f"Total runs collected:  {total_runs_collected}")
    print(f"Overall success rate:  {overall_rate}%")
    print(f"\nWorst 10 repos by failure rate:")
    for r in worst_10:
        print(f"  {r['workspace']}/{r['repo']}: {r['success_rate_pct']}% ({r['total_runs']} runs)")
    if errors:
        print(f"\nErrors: {len(errors)}")
        for e in errors:
            print(f"  {e['workspace']}/{e['repo']}: {e['error']}")
    print(f"\nSaved to inventory/bitbucket/pipeline_history.json")


if __name__ == "__main__":
    main()
