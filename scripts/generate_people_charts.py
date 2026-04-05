"""Generate interactive ECharts charts from the People Registry.

Reads people_master.json and optional enrichment files, then produces
chart JSON files in analysis/charts/.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import networkx as nx
import pandas as pd

import tl_echarts_style as zcs

ROOT = os.path.join(os.path.dirname(__file__), os.pardir)
CHARTS_DIR = os.path.join(ROOT, "analysis", "charts")
SOURCE = "Cross-System People Registry"

PEOPLE_PATH = os.path.join(ROOT, "inventory", "users", "people_master.json")
TEAM_INTERACTIONS_PATH = os.path.join(ROOT, "inventory", "users", "team_interactions.json")
NETWORK_METRICS_PATH = os.path.join(ROOT, "inventory", "users", "network_metrics.json")
RISK_PATH = os.path.join(ROOT, "inventory", "users", "people_risk.json")
REVIEW_NET_PATH = os.path.join(ROOT, "inventory", "bitbucket", "review_network_summary.json")
LABELS_PATH = os.path.join(ROOT, "inventory", "confluence", "labels.json")


def _load_json(path):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def _save(config, filename, generated, source=SOURCE):
    zcs.add_source_annotation(config, source)
    path = os.path.join(CHARTS_DIR, filename)
    zcs.write_echarts_json(config, path)
    generated.append(filename)


def _people_df(people):
    rows = []
    for p in people.values():
        src = p.get("sources", {})
        act = p.get("activity", {})
        rows.append({
            "name": p.get("canonical_name", p.get("id", "")),
            "team": p.get("team") or "Unassigned",
            "division": p.get("division") or "Unknown",
            "geography": p.get("geography") or "unknown",
            "status": p.get("status", "unknown"),
            "activity_level": act.get("level", "inactive"),
            "total_activity": act.get("total_activity_90d", 0),
            "systems_active": act.get("systems_active_90d", 0),
            "has_org_chart": "org_chart" in src,
            "has_jira": "jira" in src,
            "has_bitbucket": "bitbucket" in src,
            "has_confluence": "confluence" in src,
            "has_aws": "aws" in src,
            "prs_reviewed": src.get("bitbucket", {}).get("prs_reviewed", 0),
            "confluence_pages": src.get("confluence", {}).get("pages_total", 0),
            "jira_open": src.get("jira", {}).get("open_assigned", 0),
        })
    return pd.DataFrame(rows)


def _box_summary(values):
    """Return [min, q1, median, q3, max] for a list of numbers."""
    s = sorted(values)
    n = len(s)
    if n == 0:
        return [0, 0, 0, 0, 0]

    def _pct(data, p):
        k = (len(data) - 1) * p / 100
        f = int(k)
        c = min(f + 1, len(data) - 1)
        return data[f] + (k - f) * (data[c] - data[f])

    return [s[0], _pct(s, 25), _pct(s, 50), _pct(s, 75), s[-1]]


# ── Chart 1: People Network (Chord) ─────────────────────────────────────

def chart_people_org_map(people, review_net, generated):
    df = _people_df(people)
    active = df[(df["status"] == "active") & (df["total_activity"] > 0)].copy()
    if active.empty:
        return

    G = nx.Graph()
    for _, row in active.iterrows():
        G.add_node(row["name"], team=row["team"], activity=row["total_activity"],
                    level=row["activity_level"])

    node_set = set(G.nodes())
    lower_to_canonical = {n.lower(): n for n in node_set}

    def _resolve(name):
        if name in node_set:
            return name
        return lower_to_canonical.get(name.lower())

    unified_path = os.path.join(ROOT, "inventory", "users", "interactions_unified.json")
    unified = _load_json(unified_path)
    if unified and "edges" in unified:
        for edge in unified["edges"]:
            src = _resolve(edge.get("from", edge.get("source", "")))
            tgt = _resolve(edge.get("to", edge.get("target", "")))
            if src and tgt and src != tgt:
                w = (G[src][tgt]["weight"] + edge.get("weight", 1)
                     if G.has_edge(src, tgt) else edge.get("weight", 1))
                G.add_edge(src, tgt, weight=w)

    full_review_path = os.path.join(ROOT, "inventory", "bitbucket", "review_network.json")
    full_review = _load_json(full_review_path)
    if full_review and "edges" in full_review:
        for edge in full_review["edges"]:
            a = _resolve(edge.get("author", ""))
            r = _resolve(edge.get("reviewer", ""))
            if a and r and a != r:
                w = (G[a][r]["weight"] + edge.get("count", 1)
                     if G.has_edge(a, r) else edge.get("count", 1))
                G.add_edge(a, r, weight=w)

    top_n = 30
    nodes_with_edges = [n for n in G.nodes() if G.degree(n) > 0]
    if len(nodes_with_edges) > top_n:
        top_nodes = sorted(nodes_with_edges,
                           key=lambda n: G.degree(n, weight="weight"),
                           reverse=True)[:top_n]
    else:
        top_nodes = nodes_with_edges if nodes_with_edges else list(G.nodes())[:top_n]

    if not top_nodes:
        return

    labels = sorted(top_nodes)
    idx = {name: i for i, name in enumerate(labels)}
    size = len(labels)
    matrix = [[0] * size for _ in range(size)]
    for u, v, d in G.edges(data=True):
        if u in idx and v in idx:
            w = d.get("weight", 1)
            matrix[idx[u]][idx[v]] = w
            matrix[idx[v]][idx[u]] = w

    config = zcs.chord_config(
        matrix, labels,
        title="Mad Mobile People Network — Active Contributors (90 Days)",
    )
    _save(config, "people_org_map.json", generated)


# ── Chart 2: Cross-Team Interaction Heatmap ──────────────────────────────

def chart_team_interaction_heatmap(generated):
    data = _load_json(TEAM_INTERACTIONS_PATH)
    mat_key = next((k for k in ("symmetric_matrix", "directed_matrix", "matrix")
                     if data and k in data), None)
    if data and mat_key:
        mat = data[mat_key]
        teams = data.get("teams", sorted(mat.keys()))
        active_teams = [t for t in teams
                        if any(mat.get(t, {}).get(t2, 0) > 0 for t2 in teams)]
        if len(active_teams) > 15:
            totals = {t: sum(mat.get(t, {}).get(t2, 0) for t2 in teams)
                      for t in active_teams}
            active_teams = sorted(totals, key=totals.get, reverse=True)[:15]
        matrix = []
        for t in active_teams:
            row = mat.get(t, {})
            matrix.append([row.get(t2, 0) for t2 in active_teams])
        teams = active_teams

        config = zcs.heatmap_config(
            matrix, teams, teams,
            title="Cross-Team Interaction Heatmap",
        )
    else:
        config = zcs.bar_config(
            ["No Data"],
            [{"text": "Interactions", "values": [0]}],
            title="Cross-Team Interaction Heatmap — Run people_interactions.py first",
        )
    _save(config, "team_interaction_heatmap.json", generated)


# ── Chart 3: Team Composition by Geography ───────────────────────────────

def chart_team_composition(people, generated):
    df = _people_df(people)
    team_counts = df.groupby("team").size()
    valid_teams = team_counts[team_counts >= 2].index
    df = df[df["team"].isin(valid_teams)]

    geo_order = ["US", "SL", "unknown"]
    geo_labels = {"US": "US", "SL": "Sri Lanka", "unknown": "Unknown"}

    pivot = df.groupby(["team", "geography"]).size().unstack(fill_value=0)
    for g in geo_order:
        if g not in pivot.columns:
            pivot[g] = 0
    pivot = pivot[geo_order]
    pivot["total"] = pivot.sum(axis=1)
    pivot = pivot.sort_values("total", ascending=True)

    teams = pivot.index.tolist()
    series = [
        {"text": geo_labels[geo], "values": [int(x) for x in pivot[geo].tolist()]}
        for geo in geo_order
    ]

    config = zcs.bar_config(
        teams, series,
        stacked=True, horizontal=True,
        title="Team Composition by Geography",
        x_title="Number of People",
    )
    _save(config, "team_composition.json", generated)


# ── Chart 4: People Coverage (Chord) ────────────────────────────────────

def chart_people_coverage_sankey(people, generated):
    df = _people_df(people)
    levels = ["High", "Medium", "Low", "Inactive"]
    systems = ["Bitbucket", "Jira", "Confluence", "AWS", "Org Chart Only"]
    sys_cols = {
        "Bitbucket": "has_bitbucket", "Jira": "has_jira",
        "Confluence": "has_confluence", "AWS": "has_aws",
    }

    labels = levels + systems
    n = len(labels)
    label_idx = {l: i for i, l in enumerate(labels)}

    matrix = [[0] * n for _ in range(n)]
    for lvl in levels:
        subset = df[df["activity_level"] == lvl.lower()]
        for sys_name, col in sys_cols.items():
            count = int(subset[col].sum())
            if count > 0:
                matrix[label_idx[lvl]][label_idx[sys_name]] = count
                matrix[label_idx[sys_name]][label_idx[lvl]] = count
        org_only = subset[
            subset["has_org_chart"]
            & ~subset["has_jira"]
            & ~subset["has_bitbucket"]
            & ~subset["has_confluence"]
            & ~subset["has_aws"]
        ].shape[0]
        if org_only > 0:
            matrix[label_idx[lvl]][label_idx["Org Chart Only"]] = org_only
            matrix[label_idx["Org Chart Only"]][label_idx[lvl]] = org_only

    config = zcs.chord_config(
        matrix, labels,
        title="People Coverage — Activity Level to System Access",
    )
    _save(config, "people_coverage_sankey.json", generated)


# ── Chart 5: Key Person Risk ────────────────────────────────────────────

def chart_key_person_risk(people, generated):
    risk_data = _load_json(RISK_PATH)
    risk_people = risk_data.get("people", {}) if risk_data else {}

    if risk_people:
        items = sorted(risk_people.items(),
                       key=lambda x: x[1].get("score", 0), reverse=True)[:20]
        names = [v.get("name", k) for k, v in items]
        scores = [v.get("score", 0) for _, v in items]
    else:
        df = _people_df(people)
        active = df[df["status"] == "active"].copy()
        active["risk"] = (
            active["prs_reviewed"] * 0.3
            + active["confluence_pages"] * 0.2
            + active["jira_open"] * 0.5
        )
        max_risk = active["risk"].max()
        if max_risk > 0:
            active["risk"] = (active["risk"] / max_risk * 100).round(1)
        top = active.nlargest(20, "risk")
        names = top["name"].tolist()
        scores = top["risk"].tolist()

    names = names[::-1]
    scores = scores[::-1]

    config = zcs.bar_config(
        names,
        [{"text": "Risk Score", "values": scores}],
        horizontal=True,
        title="Key Person Risk — Top 20",
        x_title="Risk Score",
    )
    _save(config, "key_person_risk.json", generated, source="People Registry (heuristic)")


# ── Chart 6: Activity Distribution by Team ───────────────────────────────

def chart_activity_trends(people, generated):
    df = _people_df(people)
    active = df[df["status"] == "active"].copy()
    team_counts = active.groupby("team").size()
    valid_teams = team_counts[team_counts >= 3].index
    active = active[active["team"].isin(valid_teams)]

    if active.empty:
        return

    team_order = (active.groupby("team")["total_activity"]
                  .median().sort_values(ascending=False).index.tolist())

    datasets = []
    for team in team_order:
        vals = active[active["team"] == team]["total_activity"].tolist()
        datasets.append({"text": team, "values": [_box_summary(vals)]})

    config = zcs.boxplot_config(
        datasets, team_order,
        title="Activity Distribution by Team (90 Days)",
    )
    _save(config, "activity_trends.json", generated)


# ── Chart 7: Org Chart vs System Activity ────────────────────────────────

def chart_communication_gaps(people, generated):
    df = _people_df(people)
    team_stats = df.groupby("team").agg(
        org_count=("has_org_chart", "sum"),
        sys_active=("systems_active", lambda x: (x > 0).sum()),
    ).reset_index()
    team_stats = team_stats[team_stats["org_count"] >= 2]
    team_stats["gap"] = team_stats["org_count"] - team_stats["sys_active"]
    team_stats = team_stats.sort_values("gap", ascending=True)

    teams = team_stats["team"].tolist()
    series = [
        {"text": "In Org Chart", "values": [int(x) for x in team_stats["org_count"].tolist()]},
        {"text": "Active in Systems", "values": [int(x) for x in team_stats["sys_active"].tolist()]},
    ]

    config = zcs.bar_config(
        teams, series,
        horizontal=True,
        title="Org Chart vs System Activity by Team",
        x_title="Number of People",
    )
    _save(config, "communication_gaps.json", generated)


# ── Chart 8: Geography Sunburst ──────────────────────────────────────────

def chart_geography_activity(people, generated):
    df = _people_df(people)
    geo_labels = {"US": "United States", "SL": "Sri Lanka", "unknown": "Unknown"}
    df["geo_label"] = df["geography"].map(geo_labels).fillna("Unknown")
    df["level_label"] = df["activity_level"].str.capitalize()

    grouped = (df.groupby(["geo_label", "level_label"]).size()
               .reset_index(name="count"))

    sun_data = []
    for geo in sorted(grouped["geo_label"].unique()):
        subset = grouped[grouped["geo_label"] == geo]
        children = [
            {"text": row["level_label"], "value": int(row["count"])}
            for _, row in subset.iterrows()
        ]
        sun_data.append({"text": geo, "children": children})

    config = zcs.sunburst_config(
        sun_data,
        title="People Distribution — Geography and Activity",
    )
    _save(config, "geography_activity.json", generated)


# ── Chart 9: Confluence Documentation Word Cloud ─────────────────────────

def chart_confluence_wordcloud(generated):
    labels_data = _load_json(LABELS_PATH)
    if not labels_data:
        return

    words = []
    if isinstance(labels_data, list):
        for item in labels_data:
            if isinstance(item, dict):
                name = item.get("name", item.get("label", ""))
                count = item.get("count", item.get("pages", 1))
            elif isinstance(item, str):
                name, count = item, 1
            else:
                continue
            if name:
                words.append([name, count])
    elif isinstance(labels_data, dict):
        for name, val in labels_data.items():
            if isinstance(val, (int, float)):
                words.append([name, val])
            elif isinstance(val, dict):
                words.append([name, val.get("count", val.get("pages", 1))])

    if not words:
        return

    words.sort(key=lambda x: x[1], reverse=True)
    words = words[:100]

    config = zcs.wordcloud_config(
        words,
        title="Confluence Documentation Topics",
    )
    _save(config, "confluence_wordcloud.json", generated, source="Confluence")


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    os.makedirs(CHARTS_DIR, exist_ok=True)

    people = _load_json(PEOPLE_PATH)
    if not people:
        print("ERROR: people_master.json not found — cannot generate charts.")
        return

    review_net = _load_json(REVIEW_NET_PATH)
    generated = []

    chart_people_org_map(people, review_net, generated)
    chart_team_interaction_heatmap(generated)
    chart_team_composition(people, generated)
    chart_people_coverage_sankey(people, generated)
    chart_key_person_risk(people, generated)
    chart_activity_trends(people, generated)
    chart_communication_gaps(people, generated)
    chart_geography_activity(people, generated)
    chart_confluence_wordcloud(generated)

    print(f"\n{'─' * 50}")
    print(f"Generated {len(generated)} people charts:")
    for c in generated:
        print(f"  ✓ {c}")


if __name__ == "__main__":
    main()
