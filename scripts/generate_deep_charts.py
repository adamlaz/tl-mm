#!/usr/bin/env python3
"""Generate new charts from previously untapped inventory data.

Covers AWS deep inventory, Jira workflow/epic/priority/blocking data,
Confluence RCA/retro/postmortem data, cross-system bus factor and deploy
lead time, people network communities, and DORA-aligned gauge dashboards.
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


# ── AWS Deep Charts ─────────────────────────────────────────────────────

def generate_aws_security_posture():
    data = _load("inventory/aws/security_posture.json")
    if not data or not data.get("accounts"):
        return
    print("  radar: aws_security_posture.json")

    accounts = data["accounts"]
    if isinstance(accounts, dict):
        accounts = list(accounts.values())

    axes = ["IAM Health", "Network Security", "Encryption", "Logging", "Public Exposure", "Patch Status"]
    series = []
    for acct in accounts[:4]:
        name = acct.get("account_alias", acct.get("account_id", "Unknown"))
        scores = acct.get("scores", acct.get("summary", {}))
        vals = [
            scores.get("iam_health", scores.get("iam", 50)),
            scores.get("network_security", scores.get("network", 50)),
            scores.get("encryption", scores.get("encryption_at_rest", 50)),
            scores.get("logging", scores.get("cloudtrail", 50)),
            scores.get("public_exposure", scores.get("public", 50)),
            scores.get("patch_status", scores.get("patching", 50)),
        ]
        vals = [v if isinstance(v, (int, float)) else 50 for v in vals]
        series.append({"text": str(name)[:20], "values": vals})

    if not series:
        return
    config = zcs.radar_config(axes, series, title="AWS Security Posture by Account", source="AWS Security Hub")
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "aws_security_posture.json"))


def generate_aws_tagging_compliance():
    data = _load("inventory/aws/tagging_compliance.json")
    if not data:
        return
    print("  bar: aws_tagging_compliance.json")

    per_account = data.get("per_account", {})
    if isinstance(per_account, list):
        categories = [a.get("account", a.get("profile", "?"))[:20] for a in per_account[:15]]
        values = [a.get("compliance_pct", a.get("tagged_pct", 0)) for a in per_account[:15]]
    elif isinstance(per_account, dict):
        categories = [str(k)[:20] for k in list(per_account.keys())[:15]]
        values = [v.get("compliance_pct", v.get("tagged_pct", 0)) if isinstance(v, dict) else 0
                  for v in list(per_account.values())[:15]]
    else:
        return

    config = zcs.bar_config(categories, [{"text": "Tagging Compliance %", "values": values}],
                            horizontal=True, title="AWS Resource Tagging Compliance by Account",
                            source="AWS Config", y_title="Account", x_title="Compliance %")
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "aws_tagging_compliance.json"))


def generate_aws_instance_audit():
    data = _load("inventory/aws/instance_audit.json")
    if not data:
        return
    print("  bar: aws_instance_audit.json")

    by_type = data.get("by_type", {})
    if not by_type:
        return

    categories = list(by_type.keys())[:20]
    running_vals = []
    stopped_vals = []
    for t in categories:
        info = by_type[t]
        if isinstance(info, dict):
            running_vals.append(info.get("running", info.get("count", 0)))
            stopped_vals.append(info.get("stopped", 0))
        else:
            running_vals.append(info if isinstance(info, (int, float)) else 0)
            stopped_vals.append(0)

    config = zcs.bar_config(categories,
                            [{"text": "Running", "values": running_vals},
                             {"text": "Stopped", "values": stopped_vals}],
                            stacked=True, horizontal=True,
                            title="EC2/RDS Instance Types — Running vs Stopped",
                            source="AWS EC2/RDS", y_title="Instance Type")
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "aws_instance_audit.json"))


def generate_aws_deploy_frequency():
    data = _load("inventory/aws/cloudtrail_deployments.json")
    if not data:
        return
    print("  line: aws_deploy_frequency.json")

    aggs = data.get("aggregations", {})
    daily = aggs.get("daily", aggs.get("by_day", {}))
    if isinstance(daily, dict):
        dates = sorted(daily.keys())
        counts = [daily[d] if isinstance(daily[d], (int, float)) else daily[d].get("count", 0) for d in dates]
    elif isinstance(daily, list):
        dates = [d.get("date", str(i)) for i, d in enumerate(daily)]
        counts = [d.get("count", 0) for d in daily]
    else:
        return

    if not dates:
        return

    config = zcs.line_config(dates, [{"text": "Deploy Events", "values": counts}],
                             title="Deployment Frequency — CloudTrail Events",
                             source="AWS CloudTrail", x_title="Date", y_title="Events")
    zcs.add_zoom_preview(config)
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "aws_deploy_frequency.json"))


# ── Jira Deep Charts ────────────────────────────────────────────────────

def generate_jira_epic_completion():
    data = _load("inventory/jira/epic_completion.json")
    if not data:
        return
    print("  bar: jira_epic_completion.json")

    projects = data.get("all_projects", data.get("top_10_by_count", []))
    if not projects:
        return

    projects_sorted = sorted(projects, key=lambda p: p.get("total", p.get("count", 0)), reverse=True)[:15]
    categories = [p.get("project", p.get("key", "?")) for p in projects_sorted]
    resolved = [p.get("resolved", p.get("done", 0)) for p in projects_sorted]
    unresolved = [p.get("unresolved", p.get("total", 0)) - p.get("resolved", p.get("done", 0))
                  for p in projects_sorted]

    config = zcs.bar_config(categories,
                            [{"text": "Resolved", "values": resolved},
                             {"text": "Unresolved", "values": unresolved}],
                            stacked=True, horizontal=True,
                            title=f"Epic Completion by Project — {data.get('overall_resolution_rate_pct', '?')}% Overall",
                            source="Jira", y_title="Project")
    rate = data.get("overall_resolution_rate_pct")
    if rate is not None:
        zcs.add_reference_line(config, "x", rate, f"Overall: {rate}%")
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "jira_epic_completion.json"))


def generate_jira_priority_inflation():
    data = _load("inventory/jira/priority_distribution.json")
    if not data:
        return
    print("  bar: jira_priority_inflation.json")

    dist = data.get("distribution", {})
    if isinstance(dist, list):
        categories = [d.get("priority", "?") for d in dist]
        values = [d.get("count", 0) for d in dist]
    elif isinstance(dist, dict):
        categories = list(dist.keys())
        values = [v if isinstance(v, (int, float)) else v.get("count", 0) for v in dist.values()]
    else:
        return

    flag = data.get("priority_inflation_flag", False)
    title = "Jira Priority Distribution"
    if flag:
        pct = data.get("critical_or_higher_pct", "")
        title += f" — {pct}% High or Above" if pct else " — Priority Inflation Detected"

    config = zcs.bar_config(categories, [{"text": "Open Issues", "values": values}],
                            title=title, source="Jira", x_title="Priority", y_title="Count")
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "jira_priority_inflation.json"))


def generate_jira_blocking_chains():
    data = _load("inventory/jira/blocking_chains.json")
    if not data:
        return
    print("  bar: jira_blocking_chains.json")

    top_blockers = data.get("top_blockers", [])
    if not top_blockers:
        return

    categories = [b.get("key", b.get("issue", "?")) for b in top_blockers[:15]]
    blocked_count = [b.get("blocks_count", b.get("blocked_issues", 0)) for b in top_blockers[:15]]

    config = zcs.bar_config(categories, [{"text": "Issues Blocked", "values": blocked_count}],
                            horizontal=True,
                            title=f"Top Blocking Issues — {data.get('issues_blocking_others', '?')} Blockers Total",
                            source="Jira", y_title="Blocker Issue", x_title="Downstream Blocked")
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "jira_blocking_chains.json"))


def generate_jira_root_cause():
    data = _load("inventory/jira/root_cause_distribution.json")
    if not data:
        return
    print("  treemap: jira_root_cause.json")

    dist = data.get("distribution", {})
    if isinstance(dist, dict):
        children = [{"text": k, "value": v if isinstance(v, (int, float)) else v.get("count", 0)}
                    for k, v in dist.items() if k and v]
    elif isinstance(dist, list):
        children = [{"text": d.get("value", d.get("name", "?")),
                     "value": d.get("count", d.get("total", 0))} for d in dist if d]
    else:
        return

    if not children:
        return

    rate = data.get("population_rate_pct", "?")
    config = zcs.treemap_config(children,
                                title=f"Root Cause Distribution — {rate}% Population Rate",
                                source="Jira Custom Fields")
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "jira_root_cause.json"))


def generate_jira_workflow_states():
    data = _load("inventory/jira/workflows.json")
    if not data:
        return

    statuses = data.get("statuses", {})
    by_cat = statuses.get("by_category", {})
    if not by_cat:
        return
    print("  bar: jira_workflow_states.json")

    categories = list(by_cat.keys())
    values = [len(v) if isinstance(v, list) else v for v in by_cat.values()]

    custom = statuses.get("custom_statuses", [])
    title = f"Jira Status Categories — {len(custom)} Custom Statuses"

    config = zcs.bar_config(categories, [{"text": "Status Count", "values": values}],
                            title=title, source="Jira Workflows", x_title="Category", y_title="Count")
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "jira_workflow_states.json"))


# ── Confluence Deep Charts ──────────────────────────────────────────────

def generate_confluence_rca_timeline():
    data = _load("inventory/confluence/rca_timeline.json")
    if not data:
        return
    print("  line: confluence_rca_timeline.json")

    by_year = data.get("incidents_by_year", {})
    if isinstance(by_year, dict) and by_year:
        years = sorted(by_year.keys())
        counts = [by_year[y] if isinstance(by_year[y], (int, float)) else len(by_year[y]) for y in years]
        config = zcs.line_config(years, [{"text": "Incidents", "values": counts}],
                                 title=f"RCA Incident Frequency — {data.get('total_incidents_parsed', '?')} Total",
                                 source="Confluence", x_title="Year", y_title="Incidents")
        zcs.add_zoom_preview(config)
        zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "confluence_rca_timeline.json"))


def generate_confluence_retro_themes():
    data = _load("inventory/confluence/retrospectives.json")
    if not data:
        return

    themes = data.get("common_themes", [])
    if not themes:
        return
    print("  wordcloud: confluence_retro_themes.json")

    if isinstance(themes, dict):
        words = [[k, v] for k, v in themes.items()]
    elif isinstance(themes, list) and themes and isinstance(themes[0], dict):
        words = [[t.get("theme", t.get("text", "?")), t.get("count", t.get("mentions", 1))] for t in themes]
    elif isinstance(themes, list) and themes and isinstance(themes[0], (list, tuple)):
        words = themes
    else:
        words = [[str(t), 1] for t in themes]

    config = zcs.wordcloud_config(words[:80],
                                  title=f"Retrospective Themes — {data.get('total_fetched', '?')} Retros Analyzed",
                                  source="Confluence Retrospectives")
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "confluence_retro_themes.json"))


def generate_confluence_postmortem_funnel():
    data = _load("inventory/confluence/postmortem_catalog.json")
    if not data:
        return
    print("  funnel: confluence_postmortem_funnel.json")

    total = data.get("total_unique", 0)
    docs = data.get("unique_documents", [])
    query_counts = data.get("query_counts", {})

    rca_count = query_counts.get("rca", query_counts.get("root cause", total))
    postmortem_count = query_counts.get("postmortem", query_counts.get("post-mortem", total))
    documented = len(docs) if docs else total

    stages = [
        {"text": "Incidents Detected", "values": [max(total, rca_count, postmortem_count)]},
        {"text": "RCA Documented", "values": [documented]},
        {"text": "Unique RCAs", "values": [total]},
    ]

    config = zcs.funnel_config(stages, title="Postmortem Documentation Coverage", source="Confluence")
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "confluence_postmortem_funnel.json"))


# ── Cross-System Charts ─────────────────────────────────────────────────

def generate_bus_factor():
    data = _load("inventory/cross_system/bus_factor.json")
    if not data:
        return
    print("  bar: bus_factor_risk.json")

    risks = data.get("key_person_risks", data.get("heavy_reviewers_100plus", []))
    if not risks:
        return

    if isinstance(risks, list) and risks and isinstance(risks[0], dict):
        categories = [r.get("name", r.get("person", "?"))[:25] for r in risks[:15]]
        values = [r.get("risk_score", r.get("reviews", r.get("total", 0))) for r in risks[:15]]
    elif isinstance(risks, dict):
        categories = list(risks.keys())[:15]
        values = [v if isinstance(v, (int, float)) else 0 for v in list(risks.values())[:15]]
    else:
        return

    config = zcs.bar_config(categories, [{"text": "Risk Score", "values": values}],
                            horizontal=True,
                            title="Bus Factor — Key Person Risk",
                            source="Bitbucket + Jira", y_title="Person", x_title="Risk Score")
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "bus_factor_risk.json"))


def generate_deploy_lead_time():
    data = _load("inventory/cross_system/deploy_lead_time.json")
    if not data:
        return
    print("  scatter: deploy_lead_time.json")

    repos = data.get("per_repo", [])
    if not repos:
        return

    scatter_data = []
    for r in repos:
        build_s = r.get("median_build_seconds", r.get("build_seconds"))
        deploy_d = r.get("deploy_frequency_days", r.get("frequency_days"))
        if build_s is not None and deploy_d is not None:
            scatter_data.append([float(deploy_d), float(build_s) / 60.0])

    if not scatter_data:
        return

    config = zcs.scatter_config([{"text": "Repos", "values": scatter_data}],
                                title=f"Deploy Lead Time — {data.get('repos_with_pipeline_data', '?')} Repos",
                                source="Bitbucket + CloudTrail",
                                x_title="Deploy Frequency (days)", y_title="Build Time (minutes)")
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "deploy_lead_time.json"))


def generate_identity_match_quality():
    data = _load("inventory/users/match_report.json")
    if not data:
        return
    print("  sunburst: identity_match_quality.json")

    match_types = data.get("match_types", {})
    if not match_types:
        return

    children = [{"text": k.replace("_", " ").title(), "value": v}
                for k, v in match_types.items() if v]

    total = data.get("total_records_processed", sum(v for v in match_types.values()))
    config = zcs.sunburst_config(children,
                                 title=f"Identity Resolution Quality — {total} Records",
                                 source="People Registry")
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "identity_match_quality.json"))


def generate_network_communities():
    data = _load("inventory/users/network_metrics.json")
    if not data:
        return
    print("  bar: network_communities.json")

    communities = data.get("communities", [])
    if not communities:
        return

    if isinstance(communities, list):
        categories = [f"Community {i+1}" for i in range(len(communities))]
        values = [len(c) if isinstance(c, list) else c.get("size", c.get("count", 0))
                  for c in communities]
    elif isinstance(communities, dict):
        categories = list(communities.keys())
        values = [len(v) if isinstance(v, list) else v for v in communities.values()]
    else:
        return

    config = zcs.bar_config(categories, [{"text": "Members", "values": values}],
                            title=f"Network Community Sizes — {data.get('community_count', len(categories))} Communities",
                            source="Bitbucket + Jira", x_title="Community", y_title="Members")
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "network_communities.json"))


def generate_centrality_beeswarm():
    data = _load("inventory/users/network_metrics.json")
    if not data:
        return

    pr_data = data.get("all_pagerank", data.get("pagerank_top20", []))
    if not pr_data:
        return
    print("  scatter: centrality_beeswarm.json")

    if isinstance(pr_data, dict):
        scatter_points = [[i, v] for i, (k, v) in enumerate(pr_data.items())]
    elif isinstance(pr_data, list) and pr_data and isinstance(pr_data[0], dict):
        scatter_points = [[i, p.get("score", p.get("pagerank", 0))] for i, p in enumerate(pr_data)]
    elif isinstance(pr_data, list):
        scatter_points = [[i, v] for i, v in enumerate(pr_data)]
    else:
        return

    config = zcs.scatter_config([{"text": "PageRank", "values": scatter_points}],
                                title="PageRank Distribution Across Network",
                                source="Bitbucket Review Network",
                                x_title="Person Index", y_title="PageRank Score")
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "centrality_beeswarm.json"))


# ── Gauge Showcase Charts ───────────────────────────────────────────────

def generate_kpi_gauges():
    pipeline = _load("inventory/bitbucket/pipeline_history.json") or {}
    velocity = _load("inventory/jira/velocity.json") or _load("inventory/jira/velocity_full.json") or {}
    metrics = _load("inventory/bitbucket/metrics.json") or []
    epic = _load("inventory/jira/epic_completion.json") or {}

    print("  gauge: kpi_gauges.json")

    pipeline_rate = pipeline.get("overall_success_rate_pct", 0)
    epic_rate = epic.get("overall_resolution_rate_pct", 0)

    pr_cycles = []
    if isinstance(metrics, list):
        for m in metrics:
            for pr in m.get("pr_cycle_times", []):
                if isinstance(pr, dict) and pr.get("cycle_hours"):
                    pr_cycles.append(pr["cycle_hours"])
    avg_cycle = round(sum(pr_cycles) / len(pr_cycles), 1) if pr_cycles else 0

    sprint_completion = 0
    if isinstance(velocity, dict):
        all_sprints = []
        for board_name, sprints in velocity.items():
            if isinstance(sprints, list):
                for sp in sprints:
                    done = sp.get("done_issues", sp.get("completedIssues", 0))
                    total = sp.get("total_issues", sp.get("allIssues", done))
                    if total > 0:
                        all_sprints.append(done / total * 100)
        if all_sprints:
            sprint_completion = round(sum(all_sprints) / len(all_sprints), 1)

    gauges = [
        {"label": "Pipeline Success", "value": round(pipeline_rate, 1), "max": 100, "unit": "%",
         "thresholds": [[0.5, zcs.TL_STATUS["red"]], [0.8, zcs.TL_STATUS["amber"]], [1.0, zcs.TL_STATUS["green"]]]},
        {"label": "Avg PR Cycle", "value": min(avg_cycle, 200), "max": 200, "unit": "h",
         "thresholds": [[0.12, zcs.TL_STATUS["green"]], [0.42, zcs.TL_STATUS["amber"]], [1.0, zcs.TL_STATUS["red"]]]},
        {"label": "Sprint Completion", "value": round(sprint_completion, 1), "max": 100, "unit": "%",
         "thresholds": [[0.5, zcs.TL_STATUS["red"]], [0.75, zcs.TL_STATUS["amber"]], [1.0, zcs.TL_STATUS["green"]]]},
        {"label": "Epic Completion", "value": round(epic_rate, 1), "max": 100, "unit": "%",
         "thresholds": [[0.3, zcs.TL_STATUS["red"]], [0.6, zcs.TL_STATUS["amber"]], [1.0, zcs.TL_STATUS["green"]]]},
    ]

    config = zcs.gauge_multi_config(gauges, title="DORA-Aligned KPI Dashboard")
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "kpi_gauges.json"))


def generate_pipeline_health_gauge():
    pipeline = _load("inventory/bitbucket/pipeline_history.json")
    if not pipeline:
        return
    print("  gauge: pipeline_health_gauge.json")

    rate = pipeline.get("overall_success_rate_pct", 0)
    total = pipeline.get("total_pipeline_runs", 0)

    config = zcs.gauge_config(
        round(rate, 1),
        title="Pipeline Health",
        unit="%",
        thresholds=[[0.5, zcs.TL_STATUS["red"]], [0.8, zcs.TL_STATUS["amber"]], [1.0, zcs.TL_STATUS["green"]]],
        delta=f"{total:,} total runs",
        source="Bitbucket Pipelines",
    )
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "pipeline_health_gauge.json"))


def generate_dora_lead_time_gauge():
    data = _load("inventory/cross_system/deploy_lead_time.json")
    if not data:
        return
    print("  gauge: dora_lead_time_gauge.json")

    median_build = data.get("overall_median_build_seconds", 0)
    median_freq = data.get("overall_median_deploy_frequency_days", 0)

    build_minutes = round(median_build / 60, 1) if median_build else 0

    config = zcs.gauge_config(
        build_minutes,
        title="DORA Lead Time — Median Build",
        min_val=0,
        max_val=max(60, build_minutes * 1.5),
        unit=" min",
        thresholds=[
            [0.17, zcs.TL_STATUS["green"]],
            [0.5, zcs.TL_STATUS["amber"]],
            [1.0, zcs.TL_STATUS["red"]],
        ],
        delta=f"Deploy freq: {median_freq:.0f}d median" if median_freq else None,
        source="Bitbucket + CloudTrail",
    )
    zcs.write_echarts_json(config, os.path.join(CHARTS_DIR, "dora_lead_time_gauge.json"))


# ── Main ────────────────────────────────────────────────────────────────

def main():
    print("=== Deep Charts (ECharts v6) ===")

    print("\n--- AWS ---")
    generate_aws_security_posture()
    generate_aws_tagging_compliance()
    generate_aws_instance_audit()
    generate_aws_deploy_frequency()

    print("\n--- Jira ---")
    generate_jira_epic_completion()
    generate_jira_priority_inflation()
    generate_jira_blocking_chains()
    generate_jira_root_cause()
    generate_jira_workflow_states()

    print("\n--- Confluence ---")
    generate_confluence_rca_timeline()
    generate_confluence_retro_themes()
    generate_confluence_postmortem_funnel()

    print("\n--- Cross-System ---")
    generate_bus_factor()
    generate_deploy_lead_time()
    generate_identity_match_quality()
    generate_network_communities()
    generate_centrality_beeswarm()

    print("\n--- Gauge Showcase ---")
    generate_kpi_gauges()
    generate_pipeline_health_gauge()
    generate_dora_lead_time_gauge()

    chart_count = len([f for f in os.listdir(CHARTS_DIR) if f.endswith(".json")])
    print(f"\n=== Done. Total charts: {chart_count} ===")


if __name__ == "__main__":
    main()
