"""Generate additional ECharts JSON for untapped inventory data.

People: m365_teams_heatmap, m365_discrepancy_bar, people_source_coverage
Infra/Cross: aws_account_cost_treemap, bus_factor_risk, deploy_lead_time
"""

import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
import tl_echarts_style as zcs

OUT = "analysis/charts"


def m365_teams_heatmap():
    with open("inventory/users/m365_teams_analysis.json") as f:
        teams = json.load(f)

    teams_sorted = sorted(teams, key=lambda t: t.get("member_count", 0), reverse=True)[:20]
    team_names = [t["name"][:30] for t in teams_sorted]
    metrics = ["Members", "Channels", "Departments", "Cross-Functional"]

    matrix = []
    for t in teams_sorted:
        matrix.append([
            t.get("member_count", 0),
            t.get("channel_count", 0),
            len(t.get("departments", [])),
            1 if t.get("cross_functional") else 0,
        ])

    config = zcs.heatmap_config(
        matrix, metrics, team_names,
        title="M365 Teams Overview",
        source="M365 Teams API",
    )
    zcs.add_source_annotation(config, "M365 Teams API")
    zcs.write_echarts_json(config, f"{OUT}/m365_teams_heatmap.json")


def m365_discrepancy_bar():
    with open("inventory/users/m365_discrepancies.json") as f:
        data = json.load(f)

    items = data.get("items", [])
    type_counts = Counter(item["type"] for item in items)

    labels_map = {
        "manager_mismatch": "Manager Mismatch",
        "title_mismatch": "Title Mismatch",
        "missing_from_directory": "Missing from Directory",
        "missing_from_org_chart": "Missing from Org Chart",
    }

    categories = [labels_map.get(t, t) for t in type_counts.keys()]
    values = list(type_counts.values())

    config = zcs.bar_config(
        categories,
        [{"text": "Discrepancies", "values": values}],
        horizontal=True,
        title="Org Chart vs Directory Discrepancies",
        source="M365 Directory / Org Chart",
    )
    zcs.add_source_annotation(config, "M365 Directory / Org Chart")
    zcs.write_echarts_json(config, f"{OUT}/m365_discrepancy_bar.json")


def people_source_coverage():
    with open("inventory/users/people_master.json") as f:
        data = json.load(f)

    all_sources = set()
    for person in data.values():
        srcs = person.get("sources", {})
        all_sources.update(srcs.keys())

    source_list = sorted(all_sources)
    coverage = {}
    for src in source_list:
        count = sum(1 for p in data.values() if src in p.get("sources", {}))
        coverage[src] = count

    categories = [s.replace("_", " ").title() for s in source_list]
    values = [coverage[s] for s in source_list]

    config = zcs.bar_config(
        categories,
        [{"text": "People", "values": values}],
        horizontal=True,
        title="People Coverage by Data Source",
        source="People Master",
    )
    zcs.add_source_annotation(config, "People Master (cross-system)")
    zcs.write_echarts_json(config, f"{OUT}/people_source_coverage.json")


def bus_factor_risk():
    with open("inventory/cross_system/bus_factor.json") as f:
        data = json.load(f)

    reviewers = data.get("heavy_reviewers_100plus", [])[:15]
    if not reviewers:
        return

    categories = [r["name"] for r in reviewers]
    given = [r.get("reviews_given", 0) for r in reviewers]
    received = [r.get("reviews_received", 0) for r in reviewers]

    config = zcs.bar_config(
        categories,
        [
            {"text": "Reviews Given", "values": given},
            {"text": "Reviews Received", "values": received},
        ],
        horizontal=True,
        title="Bus Factor — Top Code Reviewers",
        source="Bitbucket",
    )
    zcs.add_source_annotation(config, "Bitbucket Review Data")
    zcs.write_echarts_json(config, f"{OUT}/bus_factor_risk.json")


def deploy_lead_time():
    with open("inventory/cross_system/deploy_lead_time.json") as f:
        data = json.load(f)

    worst = data.get("worst_build_reliability", [])[:15]
    if not worst:
        return

    categories = [r["repo"].split("/")[-1][:25] for r in worst]
    success_rates = [r.get("success_rate_pct", 0) for r in worst]

    config = zcs.bar_config(
        categories,
        [{"text": "Success Rate %", "values": success_rates}],
        horizontal=True,
        title="Worst Build Reliability — Bottom 15 Repos",
        source="Bitbucket Pipelines",
    )
    zcs.add_source_annotation(config, "Bitbucket Pipelines")
    zcs.write_echarts_json(config, f"{OUT}/deploy_lead_time.json")


def aws_account_cost_treemap():
    aws_dir = "inventory/aws"
    children = []

    files = [f for f in os.listdir(aws_dir) if f.startswith("mm-") and f.endswith(".json")]
    for fn in files:
        with open(os.path.join(aws_dir, fn)) as f:
            try:
                acct = json.load(f)
            except Exception:
                continue

        name = acct.get("account_name", fn.replace(".json", ""))
        cost = acct.get("monthly_cost_usd") or acct.get("total_monthly_cost") or 0
        if isinstance(cost, str):
            cost = float(cost.replace(",", "").replace("$", "")) if cost else 0
        if cost > 0:
            children.append({"name": name, "value": round(cost)})

    if not children:
        return

    config = zcs.treemap_config(
        children,
        title="AWS Cost by Account",
        source="AWS Cost Explorer",
    )
    zcs.add_source_annotation(config, "AWS Cost Explorer, March 2026")
    zcs.write_echarts_json(config, f"{OUT}/aws_account_cost_treemap.json")


if __name__ == "__main__":
    m365_teams_heatmap()
    m365_discrepancy_bar()
    people_source_coverage()
    bus_factor_risk()
    deploy_lead_time()
    aws_account_cost_treemap()
    print("Generated new charts")
