#!/usr/bin/env python3
"""Build an interactive HTML network graph of Bitbucket code review relationships."""

import json
import math
import os
from collections import defaultdict

import plotly.graph_objects as go

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT = os.path.join(BASE, "inventory", "bitbucket", "review_network.json")
OUTPUT_HTML = os.path.join(BASE, "analysis", "charts", "review_network.html")
OUTPUT_JSON = os.path.join(BASE, "inventory", "bitbucket", "review_network_summary.json")

WORKSPACE_COLORS = {
    "madmobile": "#3B82F6",
    "syscolabs": "#22C55E",
    "madpayments": "#F97316",
    "mixed": "#A855F7",
    "unknown": "#6B7280",
}


def classify_workspace(repos: list[str]) -> str:
    """Determine primary workspace from repo list."""
    ws_counts: dict[str, int] = defaultdict(int)
    for r in repos:
        org = r.split("/")[0].lower() if "/" in r else r.lower()
        if "madpayment" in org:
            ws_counts["madpayments"] += 1
        elif "syscolab" in org:
            ws_counts["syscolabs"] += 1
        elif "madmobile" in org:
            ws_counts["madmobile"] += 1
        else:
            ws_counts["unknown"] += 1
    if not ws_counts:
        return "unknown"
    top = max(ws_counts, key=ws_counts.get)
    total = sum(ws_counts.values())
    if ws_counts[top] / total < 0.6 and len(ws_counts) > 1:
        return "mixed"
    return top


def workspace_set(repos: list[str]) -> set[str]:
    """Return set of workspaces a person touches."""
    ws = set()
    for r in repos:
        org = r.split("/")[0].lower() if "/" in r else r.lower()
        if "madpayment" in org:
            ws.add("madpayments")
        elif "syscolab" in org:
            ws.add("syscolabs")
        elif "madmobile" in org:
            ws.add("madmobile")
    return ws


def spring_layout(nodes, edges, iterations=80, k=2.0):
    """Simple force-directed layout."""
    import random
    random.seed(42)
    n = len(nodes)
    names = [nd["name"] for nd in nodes]
    idx = {name: i for i, name in enumerate(names)}

    pos_x = [random.uniform(-10, 10) for _ in range(n)]
    pos_y = [random.uniform(-10, 10) for _ in range(n)]

    ws_map = {nd["name"]: classify_workspace(nd["repos"]) for nd in nodes}

    # group by workspace for initial positioning
    ws_centers = {"madmobile": (-6, 0), "syscolabs": (6, 0), "madpayments": (0, 6), "mixed": (0, -3), "unknown": (0, 0)}
    for i, nd in enumerate(nodes):
        ws = ws_map[nd["name"]]
        cx, cy = ws_centers.get(ws, (0, 0))
        pos_x[i] += cx
        pos_y[i] += cy

    edge_map: dict[tuple[int, int], float] = {}
    for e in edges:
        a, b = idx.get(e["author"]), idx.get(e["reviewer"])
        if a is not None and b is not None:
            key = (min(a, b), max(a, b))
            edge_map[key] = edge_map.get(key, 0) + e["count"]

    max_weight = max(edge_map.values()) if edge_map else 1

    for _ in range(iterations):
        fx = [0.0] * n
        fy = [0.0] * n

        # repulsion
        for i in range(n):
            for j in range(i + 1, n):
                dx = pos_x[i] - pos_x[j]
                dy = pos_y[i] - pos_y[j]
                dist = max(math.sqrt(dx * dx + dy * dy), 0.1)
                force = k * k / dist
                fx[i] += force * dx / dist
                fy[i] += force * dy / dist
                fx[j] -= force * dx / dist
                fy[j] -= force * dy / dist

        # attraction along edges
        for (i, j), w in edge_map.items():
            dx = pos_x[i] - pos_x[j]
            dy = pos_y[i] - pos_y[j]
            dist = max(math.sqrt(dx * dx + dy * dy), 0.1)
            strength = (w / max_weight) * 0.5
            force = dist / k * strength
            fx[i] -= force * dx / dist
            fy[i] -= force * dy / dist
            fx[j] += force * dx / dist
            fy[j] += force * dy / dist

        temp = 0.3 * (1 - _ / iterations)
        for i in range(n):
            disp = math.sqrt(fx[i] ** 2 + fy[i] ** 2)
            if disp > 0:
                pos_x[i] += fx[i] / disp * min(disp, temp * 5)
                pos_y[i] += fy[i] / disp * min(disp, temp * 5)

    return pos_x, pos_y


def main():
    with open(INPUT) as f:
        data = json.load(f)

    edges = data["edges"]
    nodes = data["nodes"]

    # filter out "Former user" and very low-activity nodes
    node_names = {n["name"] for n in nodes if n["name"] != "Former user"}
    nodes = [n for n in nodes if n["name"] in node_names]

    # compute per-node stats
    node_map = {}
    for nd in nodes:
        total = nd["reviews_given"] + nd["reviews_received"]
        ws = classify_workspace(nd["repos"])
        ws_set = workspace_set(nd["repos"])
        node_map[nd["name"]] = {
            "total_reviews": total,
            "given": nd["reviews_given"],
            "received": nd["reviews_received"],
            "prs_authored": nd["prs_authored"],
            "workspace": ws,
            "workspaces_touched": ws_set,
            "repos": nd["repos"],
        }

    # filter edges to known nodes, top relationships
    filtered_edges = [
        e for e in edges
        if e["author"] in node_map and e["reviewer"] in node_map and e["count"] >= 5
    ]

    # bridge nodes: people reviewing across 2+ workspaces
    bridge_nodes = [
        name for name, info in node_map.items()
        if len(info["workspaces_touched"]) >= 2
    ]

    # cluster summary
    clusters = defaultdict(list)
    for name, info in node_map.items():
        clusters[info["workspace"]].append(name)

    # layout
    pos_x, pos_y = spring_layout(nodes, filtered_edges)
    name_to_pos = {nd["name"]: (pos_x[i], pos_y[i]) for i, nd in enumerate(nodes)}

    # build edge traces (grouped by cross-workspace vs intra-workspace)
    edge_traces = []
    for is_cross, color, opacity, label in [
        (True, "#F59E0B", 0.6, "Cross-workspace"),
        (False, "#94A3B8", 0.25, "Intra-workspace"),
    ]:
        ex, ey, hover = [], [], []
        for e in filtered_edges:
            a_ws = node_map[e["author"]]["workspace"]
            r_ws = node_map[e["reviewer"]]["workspace"]
            cross = a_ws != r_ws
            if cross != is_cross:
                continue
            ax, ay = name_to_pos.get(e["author"], (0, 0))
            rx, ry = name_to_pos.get(e["reviewer"], (0, 0))
            ex += [ax, rx, None]
            ey += [ay, ry, None]

        edge_traces.append(go.Scatter(
            x=ex, y=ey, mode="lines",
            line=dict(width=1 if not is_cross else 1.5, color=color),
            opacity=opacity,
            hoverinfo="skip",
            name=label,
        ))

    # node traces, one per workspace for legend
    node_traces = []
    for ws, color in WORKSPACE_COLORS.items():
        ws_nodes = [n for n in nodes if node_map[n["name"]]["workspace"] == ws]
        if not ws_nodes:
            continue
        nx = [name_to_pos[n["name"]][0] for n in ws_nodes]
        ny = [name_to_pos[n["name"]][1] for n in ws_nodes]
        sizes = [
            max(8, min(45, math.sqrt(node_map[n["name"]]["total_reviews"]) * 1.5))
            for n in ws_nodes
        ]
        texts = [n["name"] for n in ws_nodes]
        hovers = [
            f"<b>{n['name']}</b><br>"
            f"Reviews given: {node_map[n['name']]['given']}<br>"
            f"Reviews received: {node_map[n['name']]['received']}<br>"
            f"PRs authored: {node_map[n['name']]['prs_authored']}<br>"
            f"Repos: {len(node_map[n['name']]['repos'])}<br>"
            f"{'🌉 Bridge node' if n['name'] in bridge_nodes else ''}"
            for n in ws_nodes
        ]

        is_bridge = [n["name"] in bridge_nodes for n in ws_nodes]
        borders = [2.5 if b else 0.5 for b in is_bridge]
        border_colors = ["#FBBF24" if b else "rgba(255,255,255,0.6)" for b in is_bridge]

        node_traces.append(go.Scatter(
            x=nx, y=ny, mode="markers+text",
            marker=dict(
                size=sizes,
                color=color,
                line=dict(width=borders, color=border_colors),
                opacity=0.9,
            ),
            text=texts,
            textposition="top center",
            textfont=dict(size=8, color="#1E293B"),
            hovertext=hovers,
            hoverinfo="text",
            name=ws,
        ))

    fig = go.Figure(data=edge_traces + node_traces)

    fig.update_layout(
        title=dict(
            text="<b>Bitbucket Code Review Network</b><br>"
                 "<sup>Node size = total reviews | Gold border = bridge node (cross-workspace reviewer)</sup>",
            font=dict(size=16),
        ),
        showlegend=True,
        legend=dict(
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#E2E8F0",
            borderwidth=1,
            font=dict(size=11),
        ),
        hovermode="closest",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, visible=False),
        plot_bgcolor="#F8FAFC",
        paper_bgcolor="#FFFFFF",
        margin=dict(l=20, r=20, t=80, b=20),
        width=1200,
        height=900,
    )

    os.makedirs(os.path.dirname(OUTPUT_HTML), exist_ok=True)
    fig.write_html(OUTPUT_HTML, include_plotlyjs="cdn")
    print(f"  Wrote {OUTPUT_HTML}")

    # summary stats
    top_reviewers = sorted(
        node_map.items(), key=lambda x: x[1]["given"], reverse=True
    )[:10]
    top_authors = sorted(
        node_map.items(), key=lambda x: x[1]["received"], reverse=True
    )[:10]
    strongest_pairs = sorted(filtered_edges, key=lambda e: e["count"], reverse=True)[:10]

    summary = {
        "total_nodes": len(nodes),
        "total_edges": len(filtered_edges),
        "clusters": {ws: {"count": len(members), "members": members} for ws, members in clusters.items()},
        "bridge_nodes": {
            "count": len(bridge_nodes),
            "people": [
                {"name": n, "workspaces": sorted(node_map[n]["workspaces_touched"])}
                for n in sorted(bridge_nodes)
            ],
        },
        "top_reviewers": [
            {"name": n, "reviews_given": info["given"], "workspace": info["workspace"]}
            for n, info in top_reviewers
        ],
        "top_review_recipients": [
            {"name": n, "reviews_received": info["received"], "workspace": info["workspace"]}
            for n, info in top_authors
        ],
        "strongest_review_pairs": [
            {"author": e["author"], "reviewer": e["reviewer"], "count": e["count"]}
            for e in strongest_pairs
        ],
    }

    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"  Wrote {OUTPUT_JSON}")
    print(f"\n  Summary: {len(nodes)} nodes, {len(filtered_edges)} edges, {len(bridge_nodes)} bridge nodes")
    for ws, members in clusters.items():
        print(f"    {ws}: {len(members)} people")


if __name__ == "__main__":
    main()
