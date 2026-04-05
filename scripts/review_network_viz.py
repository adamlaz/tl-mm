#!/usr/bin/env python3
"""Build an interactive HTML chord diagram of Bitbucket code review relationships."""

import json
import os
from collections import defaultdict

import tl_echarts_style as zcs

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT = os.path.join(BASE, "inventory", "bitbucket", "review_network.json")
OUTPUT_HTML = os.path.join(BASE, "analysis", "charts", "review_network.json")
OUTPUT_JSON = os.path.join(BASE, "inventory", "bitbucket", "review_network_summary.json")

TOP_N = 40


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


def main():
    with open(INPUT) as f:
        data = json.load(f)

    edges = data["edges"]
    nodes = data["nodes"]

    node_names = {n["name"] for n in nodes if n["name"] != "Former user"}
    nodes = [n for n in nodes if n["name"] in node_names]

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

    filtered_edges = [
        e for e in edges
        if e["author"] in node_map and e["reviewer"] in node_map and e["count"] >= 5
    ]

    bridge_nodes = [
        name for name, info in node_map.items()
        if len(info["workspaces_touched"]) >= 2
    ]

    clusters = defaultdict(list)
    for name, info in node_map.items():
        clusters[info["workspace"]].append(name)

    # ── Select top N nodes by degree for a readable chord diagram ────
    degree: dict[str, int] = defaultdict(int)
    for e in filtered_edges:
        degree[e["author"]] += e["count"]
        degree[e["reviewer"]] += e["count"]

    top_names = sorted(degree, key=degree.get, reverse=True)[:TOP_N]
    top_set = set(top_names)
    name_to_idx = {name: i for i, name in enumerate(top_names)}

    # ── Build adjacency matrix (rows=author, cols=reviewer) ──────────
    n = len(top_names)
    matrix = [[0] * n for _ in range(n)]
    for e in filtered_edges:
        a, r = e["author"], e["reviewer"]
        if a in top_set and r in top_set:
            matrix[name_to_idx[a]][name_to_idx[r]] += e["count"]

    labels = top_names

    config = zcs.chord_config(
        matrix,
        labels,
        title=f"Code Review Network — Top {TOP_N} Reviewers",
        source="Bitbucket",
    )

    os.makedirs(os.path.dirname(OUTPUT_HTML), exist_ok=True)
    zcs.write_echarts_json(config, OUTPUT_HTML)
    print(f"  Wrote {OUTPUT_HTML}")

    # ── Summary JSON (unchanged) ─────────────────────────────────────
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
