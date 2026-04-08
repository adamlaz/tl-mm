"""Generate ECharts from M365 analysis inventory.

Reads m365_meeting_network, m365_meeting_crossfunc, m365_org_metrics,
m365_crossorg_bridges, unified_interaction_network, and
network_divergence_findings. Produces 6 chart JSON files in
analysis/charts/ for inline rendering in the minisite.
"""

import json
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(__file__))
import tl_echarts_style as zcs

ROOT = os.path.join(os.path.dirname(__file__), os.pardir)
CHARTS_DIR = os.path.join(ROOT, "analysis", "charts")
SOURCE = "Microsoft 365 Graph API"
INV = os.path.join(ROOT, "inventory", "users")


def _load(filename):
    path = os.path.join(INV, filename)
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def _save(config, filename, generated):
    zcs.add_source_annotation(config, SOURCE)
    path = os.path.join(CHARTS_DIR, filename)
    zcs.write_echarts_json(config, path)
    generated.append(filename)


# ── 1. Meeting Co-Attendance Network (force-directed graph) ──────────────

def chart_meeting_network_force(generated):
    net = _load("m365_meeting_network.json")
    load = _load("m365_meeting_load.json")
    if not net or not load:
        return

    edges = net.get("edge_list", [])
    if not edges:
        return

    dept_map = {}
    for email, info in load.items():
        dept_map[email] = info.get("department", "Unknown")

    degree = Counter()
    for e in edges:
        degree[e["source"]] += 1
        degree[e["target"]] += 1

    sorted_edges = sorted(edges, key=lambda e: e.get("count", 0), reverse=True)
    top_edges = sorted_edges[:500]

    node_set = set()
    for e in top_edges:
        node_set.add(e["source"])
        node_set.add(e["target"])

    dept_color = {}
    for email in node_set:
        dept = dept_map.get(email, "Unknown")
        if dept not in dept_color:
            dept_color[dept] = zcs.TL_CATEGORICAL[len(dept_color) % len(zcs.TL_CATEGORICAL)]

    deg_90 = sorted(degree.values())[int(len(degree) * 0.9)] if degree else 10

    max_deg = max(degree.values()) if degree else 1
    nodes = []
    for email in node_set:
        dept = dept_map.get(email, "Unknown")
        name = load.get(email, {}).get("name", email.split("@")[0])
        d = degree.get(email, 0)
        nodes.append({
            "name": name,
            "id": email,
            "symbolSize": max(6, min(40, d / max_deg * 40)),
            "category": dept,
            "itemStyle": {"color": dept_color[dept]},
            "label": {"show": d >= deg_90},
            "value": d,
        })

    max_count = max(e.get("count", 1) for e in top_edges)
    graph_edges = []
    for e in top_edges:
        graph_edges.append({
            "source": load.get(e["source"], {}).get("name", e["source"].split("@")[0]),
            "target": load.get(e["target"], {}).get("name", e["target"].split("@")[0]),
            "value": e.get("count", 1),
            "lineStyle": {"width": max(0.5, e.get("count", 1) / max_count * 4)},
        })

    categories = [{"name": d} for d in sorted(dept_color.keys())]
    for i, cat in enumerate(categories):
        cat["itemStyle"] = {"color": dept_color[cat["name"]]}

    config = zcs.graph_config(nodes, graph_edges, title="Meeting Co-Attendance Network")

    config["legend"] = {
        "data": [c["name"] for c in categories],
        "orient": "vertical",
        "right": 10,
        "top": 40,
        "textStyle": {"fontFamily": "Noto Sans", "fontSize": 10, "color": zcs.TL_LIGHT["text_secondary"]},
    }
    config["series"][0]["categories"] = categories
    config["series"][0]["force"]["repulsion"] = 300
    config["series"][0]["force"]["gravity"] = 0.08
    config["series"][0]["force"]["edgeLength"] = [30, 150]
    config["tooltip"] = {
        "trigger": "item",
        "backgroundColor": zcs.TL_LIGHT["bg"],
        "borderColor": zcs.TL_LIGHT["zeroline"],
        "textStyle": {"fontFamily": "Noto Sans", "fontSize": 12, "color": zcs.TL_LIGHT["text"]},
    }

    _save(config, "meeting_network_force.json", generated)


# ── 2. Cross-Functional Meeting Chord Diagram ────────────────────────────

def chart_meeting_crossfunc_chord(generated):
    data = _load("m365_meeting_crossfunc.json")
    if not data:
        return

    depts = set()
    for row in data:
        depts.add(row["from"])
        depts.add(row["to"])
    labels = sorted(depts)
    idx = {d: i for i, d in enumerate(labels)}

    size = len(labels)
    matrix = [[0] * size for _ in range(size)]
    for row in data:
        i, j = idx[row["from"]], idx[row["to"]]
        matrix[i][j] = row["meetings"]
        matrix[j][i] = row["meetings"]

    config = zcs.chord_config(
        matrix, labels,
        title="Cross-Functional Meeting Flow",
    )
    _save(config, "meeting_crossfunc_chord.json", generated)


# ── 3. Manager Span of Control (horizontal bar) ─────────────────────────

def chart_org_span_of_control(generated):
    data = _load("m365_org_metrics.json")
    if not data:
        return

    metrics = data.get("metrics", [])
    managers = [m for m in metrics if m.get("direct_reports", 0) > 0]
    managers.sort(key=lambda m: m["direct_reports"])

    names = [m["name"] for m in managers]
    counts = [m["direct_reports"] for m in managers]

    colors = []
    for c in counts:
        if c > 10:
            colors.append(zcs.TL_STATUS["red"])
        elif c >= 7:
            colors.append(zcs.TL_STATUS["amber"])
        else:
            colors.append(zcs.TL_STATUS["green"])

    config = zcs.bar_config(
        names,
        [{"text": "Direct Reports", "values": counts}],
        horizontal=True,
        title="Manager Span of Control",
        x_title="Direct Reports",
    )

    config["series"][0]["data"] = [
        {"value": v, "itemStyle": {"color": c}} for v, c in zip(counts, colors)
    ]
    config["grid"]["left"] = 180

    zcs.add_reference_line(config, "x", 7, "Industry threshold (7)")

    _save(config, "org_span_of_control.json", generated)


# ── 4. Bridge Department Radar ───────────────────────────────────────────

def chart_bridge_department_radar(generated):
    bridges = _load("m365_crossorg_bridges.json")
    load_data = _load("m365_meeting_load.json")
    if not bridges:
        return

    bridges_sorted = sorted(bridges, key=lambda b: b.get("bridge_strength", 0), reverse=True)
    top = bridges_sorted[:8]

    all_depts = set()
    for b in top:
        all_depts.update(b.get("bridges_to", {}).keys())
    dept_list = sorted(all_depts)

    if not dept_list:
        return

    global_max = max(
        max(b.get("bridges_to", {}).values(), default=0) for b in top
    ) or 1

    series = []
    for b in top:
        bt = b.get("bridges_to", {})
        values = [bt.get(d, 0) for d in dept_list]
        name = b.get("email", "").split("@")[0]
        if load_data and b.get("email") in load_data:
            name = load_data[b["email"]].get("name", name)
        series.append({"text": name, "values": values})

    config = zcs.radar_config(dept_list, series, title="Cross-Org Bridge Profiles — Top 8")

    config["radar"]["indicator"] = [
        {"name": d, "max": global_max} for d in dept_list
    ]

    _save(config, "bridge_department_radar.json", generated)


# ── 5. Unified Network Sankey ────────────────────────────────────────────

def chart_unified_network_sankey(generated):
    data = _load("unified_interaction_network.json")
    if not data:
        return

    edges = data.get("edges", [])
    layers = data.get("layers_available", ["meeting", "relevance", "code_review"])

    layer_labels = {
        "meeting": "Meetings",
        "relevance": "Relevance",
        "code_review": "Code Review",
    }

    strengths = [e.get("total_strength", 0) for e in edges if e.get("total_strength", 0) > 0]
    if not strengths:
        return
    strengths.sort()
    t1 = strengths[len(strengths) // 3]
    t2 = strengths[2 * len(strengths) // 3]

    buckets = defaultdict(int)
    for e in edges:
        for layer_key in layers:
            s = e.get("layers", {}).get(layer_key, 0)
            if s <= 0:
                continue
            total = e.get("total_strength", 0)
            if total <= t1:
                band = "Weak"
            elif total <= t2:
                band = "Medium"
            else:
                band = "Strong"
            buckets[(layer_key, band)] += 1

    layer_nodes = [{"name": layer_labels.get(l, l)} for l in layers]
    band_nodes = [{"name": b} for b in ["Strong", "Medium", "Weak"]]
    all_nodes = layer_nodes + band_nodes

    links = []
    for (layer_key, band), count in buckets.items():
        links.append({
            "source": layer_labels.get(layer_key, layer_key),
            "target": band,
            "value": count,
        })

    config = zcs.sankey_config(all_nodes, links, title="Multi-Layer Interaction Composition")
    _save(config, "unified_network_sankey.json", generated)


# ── 6. Divergence Treemap ────────────────────────────────────────────────

def chart_divergence_treemap(generated):
    data = _load("network_divergence_findings.json")
    if not data:
        return

    findings = data.get("findings", [])
    if not findings:
        return

    category_counts = Counter()
    for f in findings:
        text = f.get("finding", "")
        if "meetings without" in text.lower():
            category_counts["Meetings without code interaction"] += 1
        elif "code without meeting" in text.lower() or "code review without" in text.lower():
            category_counts["Code review without meetings"] += 1
        elif "relevance without" in text.lower():
            category_counts["Relevance without meetings"] += 1
        elif "single layer" in text.lower() or "single-layer" in text.lower():
            category_counts["Single-layer only"] += 1
        else:
            category_counts["Other divergence"] += 1

    children = [
        {"name": cat, "value": count}
        for cat, count in sorted(category_counts.items(), key=lambda x: -x[1])
    ]

    config = zcs.treemap_config(children, title="Where Interaction Layers Diverge")
    _save(config, "divergence_treemap.json", generated)


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    os.makedirs(CHARTS_DIR, exist_ok=True)
    generated = []

    chart_meeting_network_force(generated)
    chart_meeting_crossfunc_chord(generated)
    chart_org_span_of_control(generated)
    chart_bridge_department_radar(generated)
    chart_unified_network_sankey(generated)
    chart_divergence_treemap(generated)

    print(f"\n{'─' * 50}")
    print(f"Generated {len(generated)} M365 charts:")
    for c in generated:
        print(f"  ✓ {c}")


if __name__ == "__main__":
    main()
