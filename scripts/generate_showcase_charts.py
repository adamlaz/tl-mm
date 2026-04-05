#!/usr/bin/env python3
"""Generate showcase charts using advanced ECharts types.

Radar, bullet, violin, bubble, calendar, funnel, rankflow, range.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import tl_echarts_style as zcs

ROOT = os.path.join(os.path.dirname(__file__), os.pardir)
CHARTS_DIR = os.path.join(ROOT, "analysis", "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)


def _load(relpath):
    path = os.path.join(ROOT, relpath)
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def generate_workspace_health_radar():
    """Radar chart: engineering health across 4 Bitbucket workspaces."""
    print("  radar: workspace_health_radar.json")
    pipeline = _load("inventory/bitbucket/pipeline_history.json") or {}
    metrics_raw = _load("inventory/bitbucket/metrics.json") or []
    branch = _load("inventory/bitbucket/branch_restrictions.json") or {}
    dep = _load("inventory/bitbucket/dependency_analysis.json") or {}

    workspaces = ["madmobile", "madpayments", "syscolabs", "syscolabsconf"]
    axes = ["Pipeline Success", "PR Velocity", "Commit Activity",
            "Branch Protection", "Review Coverage", "Dep Health"]

    ws_data = {ws: [50, 50, 50, 50, 50, 50] for ws in workspaces}

    per_repo = pipeline.get("per_repo", [])
    for ws in workspaces:
        repos = [r for r in per_repo if r.get("workspace", "").lower() == ws]
        if repos:
            rates = [r.get("success_rate_pct", 0) for r in repos if r.get("success_rate_pct") is not None]
            ws_data[ws][0] = round(sum(rates) / len(rates)) if rates else 0

    for m in metrics_raw:
        ws = m.get("workspace", "").lower()
        if ws in ws_data:
            cycles = [pr.get("cycle_hours", 0) for pr in m.get("pr_cycle_times", []) if pr.get("cycle_hours")]
            if cycles:
                avg_h = sum(cycles) / len(cycles)
                ws_data[ws][1] = max(0, min(100, round(100 - avg_h / 2)))
            weekly = m.get("commits", {}).get("weekly_commits", {})
            total = sum(weekly.values()) if weekly else 0
            ws_data[ws][2] = min(100, round(total / 5))

    repos_checked = branch.get("summary", {}).get("repos_checked", 0)
    repos_with = branch.get("summary", {}).get("repos_with_restrictions", 0)
    branch_pct = round(repos_with / repos_checked * 100) if repos_checked else 50
    for ws in workspaces:
        ws_data[ws][3] = branch_pct

    for ws in workspaces:
        ws_data[ws][4] = 60

    per_repo_deps = dep.get("per_repo", [])
    for ws in workspaces:
        repos = [r for r in per_repo_deps if r.get("workspace", "").lower() == ws]
        if repos:
            dep_counts = []
            for r in repos:
                for info in r.get("dep_files", {}).values():
                    dep_counts.append(info.get("total_deps", 0))
            avg_deps = sum(dep_counts) / len(dep_counts) if dep_counts else 0
            ws_data[ws][5] = max(0, min(100, round(100 - avg_deps / 3)))

    series = [{"text": ws.title(), "values": ws_data[ws]} for ws in workspaces]
    config = zcs.radar_config(axes, series,
                              title="Workspace Engineering Health — Normalized 0–100",
                              source="Bitbucket")
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "workspace_health_radar.json"))


def generate_kpi_bullet():
    """Bullet chart: KPI actual vs DORA benchmarks."""
    print("  bullet: kpi_bullet.json")
    pipeline = _load("inventory/bitbucket/pipeline_history.json") or {}
    metrics_raw = _load("inventory/bitbucket/metrics.json") or []
    velocity = _load("inventory/jira/velocity_full.json") or _load("inventory/jira/velocity.json") or {}

    pipeline_rate = pipeline.get("overall_success_rate_pct", 60)

    all_cycles = []
    for m in metrics_raw:
        for pr in m.get("pr_cycle_times", []):
            h = pr.get("cycle_hours")
            if h and h > 0:
                all_cycles.append(h)
    avg_cycle = round(sum(all_cycles) / len(all_cycles), 1) if all_cycles else 48

    done_total = []
    for board_data in velocity.values():
        sprints = board_data if isinstance(board_data, list) else board_data.get("sprints", [])
        for s in sprints:
            if isinstance(s, dict) and s.get("done_issues") is not None and s.get("total_issues"):
                done_total.append(s["done_issues"] / s["total_issues"] * 100)
    completion = round(sum(done_total) / len(done_total), 1) if done_total else 28

    items = [
        {"label": f"Pipeline Success Rate ({pipeline_rate}%)", "actual": pipeline_rate,
         "target": 85, "ranges": [60, 75, 95]},
        {"label": f"Avg PR Merge Time ({avg_cycle}h)", "actual": min(avg_cycle, 168),
         "target": 24, "ranges": [4, 24, 168]},
        {"label": f"Sprint Completion ({completion}%)", "actual": completion,
         "target": 80, "ranges": [40, 60, 90]},
    ]
    config = zcs.bullet_config(items, title="KPI Performance vs DORA Benchmarks")
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "kpi_bullet.json"))


def generate_pr_cycle_violin():
    """Violin chart: PR cycle time distribution per workspace."""
    print("  violin: pr_cycle_violin.json")
    metrics_raw = _load("inventory/bitbucket/metrics.json") or []
    ws_cycles = {}
    for m in metrics_raw:
        ws = m.get("workspace", "unknown")
        for pr in m.get("pr_cycle_times", []):
            h = pr.get("cycle_hours")
            if h and 0 < h < 2000:
                ws_cycles.setdefault(ws, []).append(round(h, 1))

    if not ws_cycles:
        print("    (no PR cycle data, skipping)")
        return

    labels = sorted(ws_cycles.keys())
    datasets = [{"text": ws, "values": ws_cycles[ws]} for ws in labels]
    config = zcs.violin_config(datasets, labels,
                               title="PR Cycle Time Distribution by Workspace (Hours)",
                               source="Bitbucket")
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "pr_cycle_violin.json"))


def generate_repo_health_bubble():
    """Bubble chart: repos by commits x cycle time x dependency count."""
    print("  bubble: repo_health_bubble.json")
    metrics_raw = _load("inventory/bitbucket/metrics.json") or []
    dep = _load("inventory/bitbucket/dependency_analysis.json") or {}
    dep_map = {}
    for r in dep.get("per_repo", []):
        total = sum(info.get("total_deps", 0) for info in r.get("dep_files", {}).values())
        dep_map[f"{r.get('workspace','')}/{r.get('repo','')}"] = total

    ws_series = {}
    for m in metrics_raw:
        ws = m.get("workspace", "unknown")
        repo_key = f"{ws}/{m.get('repo', '')}"
        commits = m.get("commits", {}).get("total_commits_6mo", 0) or sum(
            m.get("commits", {}).get("weekly_commits", {}).values())
        cycles = [pr.get("cycle_hours", 0) for pr in m.get("pr_cycle_times", []) if pr.get("cycle_hours")]
        avg_cycle = sum(cycles) / len(cycles) if cycles else 0
        deps = dep_map.get(repo_key, 10)
        if commits > 0:
            ws_series.setdefault(ws, []).append([commits, round(avg_cycle, 1), max(deps, 1)])

    if not ws_series:
        print("    (no data, skipping)")
        return

    series = [{"text": ws, "values": pts} for ws, pts in sorted(ws_series.items())]
    config = zcs.bubble_config(series,
                               title="Repository Health Matrix — Commits vs PR Cycle Time",
                               source="Bitbucket",
                               x_title="Commits (6 months)",
                               y_title="Avg PR Cycle Time (hours)")
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "repo_health_bubble.json"))


def generate_commit_calendar():
    """Calendar heatmap: weekly commit activity."""
    print("  calendar: commit_calendar.json")
    metrics_raw = _load("inventory/bitbucket/metrics.json") or []
    week_totals = {}
    for m in metrics_raw:
        for week, count in m.get("commits", {}).get("weekly_commits", {}).items():
            week_totals[week] = week_totals.get(week, 0) + count

    if not week_totals:
        print("    (no commit data, skipping)")
        return

    date_values = []
    for week_key in sorted(week_totals.keys()):
        try:
            from datetime import datetime
            year, wk = week_key.split("-W")
            dt = datetime.strptime(f"{year}-W{wk}-1", "%Y-W%W-%w")
            date_values.append([dt.strftime("%Y-%m-%d"), week_totals[week_key]])
        except (ValueError, IndexError):
            date_values.append([week_key, week_totals[week_key]])

    config = zcs.calendar_config(date_values,
                                 title="Commit Activity — Weekly Heatmap",
                                 source="Bitbucket", year=2026)
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "commit_calendar.json"))


def generate_jira_workflow_funnel():
    """Funnel chart: Jira workflow stage dwell times."""
    print("  funnel: jira_workflow_funnel.json")
    transitions = _load("inventory/jira/status_transitions.json")
    if not transitions:
        print("    (no status_transitions.json, skipping)")
        return

    durations = transitions.get("status_durations", [])
    if not durations:
        print("    (no status_durations, skipping)")
        return

    sorted_stages = sorted(durations, key=lambda d: d.get("median_hours", 0), reverse=True)[:10]
    stages = [{"text": d["status"], "values": [round(d.get("median_hours", 0), 1)]}
              for d in sorted_stages]
    config = zcs.funnel_config(stages,
                               title="Jira Workflow Stage Dwell Time — Median Hours",
                               source="Jira")
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "jira_workflow_funnel.json"))


def generate_sprint_rankflow():
    """Rankflow chart: sprint velocity rankings over time."""
    print("  rankflow: sprint_rankflow.json")
    velocity = _load("inventory/jira/velocity_full.json") or _load("inventory/jira/velocity.json") or {}
    if not velocity:
        print("    (no velocity data, skipping)")
        return

    board_sprints = {}
    all_periods = set()
    for board_name, board_data in velocity.items():
        sprints = board_data if isinstance(board_data, list) else board_data.get("sprints", [])
        for s in sprints:
            if isinstance(s, dict) and s.get("done_issues") is not None:
                name = s.get("name", "")
                board_sprints.setdefault(board_name, {})[name] = s.get("done_issues", 0)
                all_periods.add(name)

    if len(all_periods) < 2:
        print("    (not enough sprint periods, skipping)")
        return

    periods = sorted(all_periods)[-8:]
    top_boards = sorted(board_sprints.keys(),
                        key=lambda b: sum(board_sprints[b].values()), reverse=True)[:8]

    series = []
    for board in top_boards:
        ranks = []
        for period in periods:
            all_vals = [(b, board_sprints.get(b, {}).get(period, 0)) for b in top_boards]
            all_vals.sort(key=lambda x: x[1], reverse=True)
            rank = next((i + 1 for i, (b, _) in enumerate(all_vals) if b == board), len(top_boards))
            ranks.append(rank)
        series.append({"text": board[:20], "ranks": ranks})

    config = zcs.rankflow_config(periods, series,
                                 title="Sprint Velocity Rankings — Top 8 Boards",
                                 source="Jira")
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "sprint_rankflow.json"))


def generate_build_duration_range():
    """Range chart: build duration median-to-P95 bands per repo."""
    print("  range: build_duration_range.json")
    pipeline = _load("inventory/bitbucket/pipeline_history.json") or {}
    per_repo = pipeline.get("per_repo", [])
    repos = [r for r in per_repo
             if r.get("median_build_s") is not None and r.get("p95_build_s") is not None
             and r.get("total_runs", 0) > 5]

    if not repos:
        print("    (no build duration data, skipping)")
        return

    repos.sort(key=lambda r: r.get("median_build_s", 0))
    top = repos[-20:]

    categories = [f"{r.get('workspace','')}/{r.get('repo','')}"[-30:] for r in top]
    ranges = [[round(r["median_build_s"]), round(r["p95_build_s"])] for r in top]

    config = zcs.range_config(categories, ranges,
                              title="Build Duration Bands — Median to P95 (seconds)",
                              source="Bitbucket", horizontal=True)
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "build_duration_range.json"))


def main():
    print("=== Showcase Charts (Advanced ECharts Types) ===", flush=True)
    generate_workspace_health_radar()
    generate_kpi_bullet()
    generate_pr_cycle_violin()
    generate_repo_health_bubble()
    generate_commit_calendar()
    generate_jira_workflow_funnel()
    generate_sprint_rankflow()
    generate_build_duration_range()
    print("Done.", flush=True)


if __name__ == "__main__":
    main()
