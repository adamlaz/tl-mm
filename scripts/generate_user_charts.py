#!/usr/bin/env python3
"""Generate user-centric and cross-system charts from user_audit and Jira data.

Covers the 5 charts that previously had no generating script:
  - user_activity_levels.json
  - user_contribution_top20.json
  - user_cross_system.json
  - user_workload_distribution.json
  - jira_issue_distribution.json

Plus:
  - user_system_venn.json  (cross-system coverage Venn diagram)
"""

import json
import os

import pandas as pd

import tl_echarts_style as zcs

CHARTS_DIR = "analysis/charts"
os.makedirs(CHARTS_DIR, exist_ok=True)


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def generate_user_activity_levels(df):
    """Horizontal bar: users grouped by activity level."""
    counts = df["activity_level"].value_counts().sort_values()
    config = zcs.bar_config(
        counts.index.tolist(),
        [{"text": "Users", "values": counts.values.tolist()}],
        horizontal=True,
        title="User Activity Levels -- Cross-System (90 Days)",
        source="Bitbucket, Jira, Confluence",
    )
    zcs.write_echarts_json(config, f"{CHARTS_DIR}/user_activity_levels.json")
    print(f"  -> {CHARTS_DIR}/user_activity_levels.json")


def generate_user_contribution_top20(df):
    """Horizontal bar: top 20 contributors by total cross-system activity."""
    df["total_activity_90d"] = pd.to_numeric(df["total_activity_90d"], errors="coerce").fillna(0)
    top = df.nlargest(20, "total_activity_90d").sort_values("total_activity_90d")
    config = zcs.bar_config(
        top["display_name"].tolist(),
        [{"text": "Total Activity Events", "values": top["total_activity_90d"].tolist()}],
        horizontal=True,
        title="Top 20 Contributors by Cross-System Activity (90 Days)",
        source="Bitbucket, Jira, Confluence",
    )
    zcs.write_echarts_json(config, f"{CHARTS_DIR}/user_contribution_top20.json")
    print(f"  -> {CHARTS_DIR}/user_contribution_top20.json")


def generate_user_cross_system(df):
    """Vertical bar: users by number of systems active in."""
    df["systems_active_90d"] = pd.to_numeric(df["systems_active_90d"], errors="coerce").fillna(0).astype(int)
    sys_counts = df["systems_active_90d"].value_counts().sort_index()
    config = zcs.bar_config(
        sys_counts.index.astype(str).tolist(),
        [{"text": "Users", "values": sys_counts.values.tolist()}],
        horizontal=False,
        title="Users by Number of Systems Active In (90 Days)",
        source="Bitbucket, Jira, Confluence",
    )
    zcs.write_echarts_json(config, f"{CHARTS_DIR}/user_cross_system.json")
    print(f"  -> {CHARTS_DIR}/user_cross_system.json")


def generate_user_workload(df):
    """Horizontal bar: workload distribution by role classification."""
    if "jira_role" not in df.columns:
        return
    role_counts = df["jira_role"].value_counts().sort_values()
    config = zcs.bar_config(
        role_counts.index.tolist(),
        [{"text": "Users", "values": role_counts.values.tolist()}],
        horizontal=True,
        title="User Workload Distribution by Jira Role",
        source="Jira",
    )
    zcs.write_echarts_json(config, f"{CHARTS_DIR}/user_workload_distribution.json")
    print(f"  -> {CHARTS_DIR}/user_workload_distribution.json")


def generate_jira_issue_distribution(issue_dist):
    """Horizontal bar: combined issue type distribution (all segments)."""
    all_types = {}
    for seg_name in ["overall", "engineering", "customer_success", "operations"]:
        seg_data = issue_dist.get(seg_name, {})
        for k, v in seg_data.items():
            if isinstance(v, (int, float)) and k in ("bugs", "stories", "tasks", "epics", "subtasks"):
                all_types[k] = all_types.get(k, 0) + v

    if not all_types:
        return

    sorted_items = sorted(all_types.items(), key=lambda x: x[1])
    labels = [k.title() for k, _ in sorted_items]
    values = [v for _, v in sorted_items]
    config = zcs.bar_config(
        labels,
        [{"text": "Issues", "values": values}],
        horizontal=True,
        title="Jira Issue Distribution by Type (All Segments)",
        source="Jira",
    )
    zcs.write_echarts_json(config, f"{CHARTS_DIR}/jira_issue_distribution.json")
    print(f"  -> {CHARTS_DIR}/jira_issue_distribution.json")


def generate_user_system_venn():
    """Venn diagram: cross-system user coverage from people_master.json."""
    people = load_json("inventory/users/people_master.json")
    if not people:
        print("  ! inventory/users/people_master.json not found, skipping user_system_venn")
        return

    bb_set = set()
    jira_set = set()
    conf_set = set()

    for pid, person in people.items():
        sources = person.get("sources", {})
        if "bitbucket" in sources:
            bb_set.add(pid)
        if "jira" in sources:
            jira_set.add(pid)
        if "confluence" in sources:
            conf_set.add(pid)

    bb_jira = len(bb_set & jira_set)
    bb_conf = len(bb_set & conf_set)
    jira_conf = len(jira_set & conf_set)
    all_three = len(bb_set & jira_set & conf_set)

    sets = [
        {"text": "Bitbucket", "values": [len(bb_set)]},
        {"text": "Jira", "values": [len(jira_set)]},
        {"text": "Confluence", "values": [len(conf_set)]},
        {"text": "BB+Jira", "values": [bb_jira]},
        {"text": "BB+Conf", "values": [bb_conf]},
        {"text": "Jira+Conf", "values": [jira_conf]},
        {"text": "All Three", "values": [all_three]},
    ]

    config = zcs.venn_config(
        sets,
        title="Cross-System User Coverage — Bitbucket, Jira, Confluence",
        source="People Registry",
    )
    zcs.write_echarts_json(config, f"{CHARTS_DIR}/user_system_venn.json")
    print(f"  -> {CHARTS_DIR}/user_system_venn.json")


def main():
    print("=== User & Cross-System Charts ===", flush=True)

    user_csv = "analysis/user_audit.csv"
    if os.path.exists(user_csv):
        df = pd.read_csv(user_csv, dtype=str)
        generate_user_activity_levels(df)
        generate_user_contribution_top20(df)
        generate_user_cross_system(df)
        generate_user_workload(df)
    else:
        print(f"  ! {user_csv} not found, skipping user charts")

    issue_dist = load_json("inventory/jira/issue_distribution.json")
    if issue_dist:
        generate_jira_issue_distribution(issue_dist)
    else:
        print("  ! inventory/jira/issue_distribution.json not found, skipping jira_issue_distribution")

    generate_user_system_venn()

    print("Done.", flush=True)


if __name__ == "__main__":
    main()
