#!/usr/bin/env python3
"""Interaction Analysis & Network Science

Builds interaction graphs from Jira comments and Bitbucket review data,
computes network metrics (centrality, PageRank, communities), calculates
key-person risk scores, and detects cross-team communication gaps.

Usage:
    python3 scripts/people_interactions.py [--skip-api]

    --skip-api   Skip Jira API calls, use cached comment data only
"""

import sys
import os
import json
import time
from collections import defaultdict
from datetime import datetime, timezone

import requests
from requests.auth import HTTPBasicAuth
import networkx as nx

# ─── Configuration ───────────────────────────────────────────────────────

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(ROOT, ".env.local")
PEOPLE_FILE = os.path.join(ROOT, "inventory/users/people_master.json")
REVIEW_NET_FILE = os.path.join(ROOT, "inventory/bitbucket/review_network.json")
REVIEW_SUMMARY_FILE = os.path.join(ROOT, "inventory/bitbucket/review_network_summary.json")
OUTPUT_DIR = os.path.join(ROOT, "inventory/users")

JIRA_BASE = "https://madmobile-eng.atlassian.net"
JIRA_EMAIL = "adam.lazarus@madmobile.com"
JIRA_SEARCH_URL = f"{JIRA_BASE}/rest/api/3/search/jql"
JIRA_ISSUE_COMMENT_URL = f"{JIRA_BASE}/rest/api/3/issue/{{key}}/comment"

ENGINEERING_PROJECTS = ("REST", "OS", "DSO", "CE", "DR", "BO", "PAY", "CLOUD", "NEO", "CLD", "MP", "POS")
MAX_ISSUES = 300
RATE_LIMIT_DELAY = 0.15

SKIP_API = "--skip-api" in sys.argv


def load_env():
    creds = {}
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    creds[k.strip()] = v.strip().strip('"').strip("'")
    return creds


def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    print(f"  Saved {path}")


# ─── People Lookup Helpers ───────────────────────────────────────────────

def build_lookup_tables(people):
    """Build fast lookup dicts: account_id -> person key, display name -> person key."""
    by_account_id = {}
    by_name_lower = {}
    by_alias = {}

    for pkey, person in people.items():
        canonical = person.get("canonical_name", "").lower().strip()
        if canonical:
            by_name_lower[canonical] = pkey

        for alias in person.get("aliases", []):
            by_alias[alias.lower().strip()] = pkey

        for source_data in person.get("sources", {}).values():
            aid = source_data.get("account_id")
            if aid:
                by_account_id[aid] = pkey

    return by_account_id, by_name_lower, by_alias


def resolve_account_id(account_id, by_account_id):
    return by_account_id.get(account_id)


def resolve_display_name(name, by_name_lower, by_alias):
    if not name:
        return None
    n = name.lower().strip()
    result = by_name_lower.get(n) or by_alias.get(n)
    if result:
        return result
    parts = n.split()
    if len(parts) >= 2:
        first_last = f"{parts[0]} {parts[-1]}"
        return by_name_lower.get(first_last) or by_alias.get(first_last)
    return None


def person_team(people, pkey):
    if not pkey or pkey not in people:
        return "Unknown"
    return people[pkey].get("team") or people[pkey].get("division") or "Unknown"


def person_geo(people, pkey):
    if not pkey or pkey not in people:
        return "Unknown"
    return people[pkey].get("geography") or "Unknown"


def person_name(people, pkey):
    if not pkey or pkey not in people:
        return pkey or "Unknown"
    return people[pkey].get("canonical_name", pkey)


# ═══════════════════════════════════════════════════════════════════════════
# PHASE 1: Jira Comment Network
# ═══════════════════════════════════════════════════════════════════════════

def fetch_jira_comments(auth):
    print("\n╔══════════════════════════════════════════════╗")
    print("║  Phase 1: Jira Comment Network               ║")
    print("╚══════════════════════════════════════════════╝")

    jql = (
        'updated >= -90d AND project in ("REST","OS","DSO","CE","DR","BO","PAY","CLOUD","NEO","CLD","MP","POS") '
        'ORDER BY updated DESC'
    )

    issues = []
    next_token = None
    page = 0

    while len(issues) < MAX_ISSUES:
        payload = {
            "jql": jql,
            "maxResults": 100,
            "fields": ["key", "assignee", "reporter", "comment"],
        }
        if next_token:
            payload["nextPageToken"] = next_token

        try:
            resp = requests.post(JIRA_SEARCH_URL, json=payload, auth=auth, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            print(f"  API error on page {page}: {e}")
            break

        batch = data.get("issues", [])
        if not batch:
            break

        issues.extend(batch)
        page += 1
        print(f"  Fetched page {page}: {len(batch)} issues (total: {len(issues)})")

        next_token = data.get("nextPageToken")
        if not next_token:
            break

        time.sleep(RATE_LIMIT_DELAY)

    print(f"  Total issues fetched: {len(issues)}")

    comment_edges = defaultdict(int)
    cowork_edges = defaultdict(int)
    issues_with_comments = 0
    total_comments = 0

    comments_in_fields = True
    if issues:
        sample_fields = issues[0].get("fields", {})
        if "comment" not in sample_fields:
            comments_in_fields = False
            print("  Comments not in fields response, will fetch separately for top 100 issues")

    for i, issue in enumerate(issues):
        if (i + 1) % 50 == 0:
            print(f"  Processing issue {i + 1}/{len(issues)}...")

        fields = issue.get("fields", {})
        key = issue.get("key", "")

        assignee_id = None
        reporter_id = None
        if fields.get("assignee"):
            assignee_id = fields["assignee"].get("accountId")
        if fields.get("reporter"):
            reporter_id = fields["reporter"].get("accountId")

        if assignee_id and reporter_id and assignee_id != reporter_id:
            pair = tuple(sorted([assignee_id, reporter_id]))
            cowork_edges[pair] += 1

        comments = []
        if comments_in_fields:
            comment_field = fields.get("comment", {})
            if isinstance(comment_field, dict):
                comments = comment_field.get("comments", [])
            elif isinstance(comment_field, list):
                comments = comment_field
        elif i < 100:
            try:
                url = JIRA_ISSUE_COMMENT_URL.format(key=key)
                cr = requests.get(url, auth=auth, timeout=15)
                cr.raise_for_status()
                cdata = cr.json()
                comments = cdata.get("comments", [])
                time.sleep(RATE_LIMIT_DELAY)
            except requests.RequestException:
                pass

        if comments:
            issues_with_comments += 1
            total_comments += len(comments)

        for comment in comments:
            author = comment.get("author", {})
            commenter_id = author.get("accountId")
            if not commenter_id:
                continue

            if assignee_id and commenter_id != assignee_id:
                comment_edges[(commenter_id, assignee_id)] += 1
            if reporter_id and commenter_id != reporter_id:
                comment_edges[(commenter_id, reporter_id)] += 1

    print(f"  Issues with comments: {issues_with_comments}")
    print(f"  Total comments processed: {total_comments}")
    print(f"  Comment edges: {len(comment_edges)}")
    print(f"  Co-work edges: {len(cowork_edges)}")

    comment_edge_list = [
        {"from": f, "to": t, "count": c, "type": "jira_comment"}
        for (f, t), c in sorted(comment_edges.items(), key=lambda x: -x[1])
    ]
    cowork_edge_list = [
        {"from": pair[0], "to": pair[1], "count": c, "type": "jira_cowork"}
        for pair, c in sorted(cowork_edges.items(), key=lambda x: -x[1])
    ]

    return comment_edge_list, cowork_edge_list


def load_cached_jira_comments():
    path = os.path.join(OUTPUT_DIR, "interactions_jira_comments.json")
    data = load_json(path)
    if data:
        print(f"  Loaded cached Jira comment data: {len(data.get('comment_edges', []))} comment edges")
        return data.get("comment_edges", []), data.get("cowork_edges", [])
    return [], []


# ═══════════════════════════════════════════════════════════════════════════
# PHASE 2: Review Network Enrichment
# ═══════════════════════════════════════════════════════════════════════════

def enrich_review_network(people, by_account_id, by_name_lower, by_alias):
    print("\n╔══════════════════════════════════════════════╗")
    print("║  Phase 2: Review Network Enrichment           ║")
    print("╚══════════════════════════════════════════════╝")

    review_data = load_json(REVIEW_NET_FILE)
    if not review_data:
        print("  review_network.json not found, skipping")
        return [], {}

    edges = review_data.get("edges") or review_data.get("data") or []
    if isinstance(review_data, list):
        edges = review_data

    summary_data = load_json(REVIEW_SUMMARY_FILE)
    clusters = summary_data.get("clusters", {}) if summary_data else {}

    print(f"  Loaded {len(edges)} review edges")

    enriched = []
    team_review_counts = defaultdict(lambda: {"within": 0, "cross": 0, "total": 0})
    cross_team_pairs = defaultdict(int)

    for edge in edges:
        author_name = edge.get("author", "")
        reviewer_name = edge.get("reviewer", "")
        count = edge.get("count", 1)
        repos = edge.get("repos", [])

        author_key = resolve_display_name(author_name, by_name_lower, by_alias)
        reviewer_key = resolve_display_name(reviewer_name, by_name_lower, by_alias)

        author_team = person_team(people, author_key)
        reviewer_team = person_team(people, reviewer_key)
        author_geo = person_geo(people, author_key)
        reviewer_geo = person_geo(people, reviewer_key)

        same_team = author_team == reviewer_team and author_team != "Unknown"
        cross_geography = author_geo != reviewer_geo and author_geo != "Unknown" and reviewer_geo != "Unknown"

        enriched_edge = {
            "author": author_name,
            "reviewer": reviewer_name,
            "author_key": author_key,
            "reviewer_key": reviewer_key,
            "count": count,
            "repos": repos,
            "author_team": author_team,
            "reviewer_team": reviewer_team,
            "same_team": same_team,
            "cross_geography": cross_geography,
        }
        if not same_team and author_team != "Unknown" and reviewer_team != "Unknown":
            enriched_edge["cross_team"] = f"{author_team} <-> {reviewer_team}"

        enriched.append(enriched_edge)

        if same_team and author_team != "Unknown":
            team_review_counts[author_team]["within"] += count
            team_review_counts[author_team]["total"] += count
        else:
            if author_team != "Unknown":
                team_review_counts[author_team]["cross"] += count
                team_review_counts[author_team]["total"] += count
            if reviewer_team != "Unknown" and reviewer_team != author_team:
                team_review_counts[reviewer_team]["cross"] += count
                team_review_counts[reviewer_team]["total"] += count

            if author_team != "Unknown" and reviewer_team != "Unknown":
                pair = tuple(sorted([author_team, reviewer_team]))
                cross_team_pairs[pair] += count

    concentration = {}
    for team, counts in team_review_counts.items():
        total = counts["total"]
        if total > 0:
            concentration[team] = {
                "within_count": counts["within"],
                "cross_count": counts["cross"],
                "total": total,
                "within_pct": round(counts["within"] / total * 100, 1),
                "cross_pct": round(counts["cross"] / total * 100, 1),
            }

    review_summary = {
        "total_edges": len(enriched),
        "team_review_concentration": concentration,
        "cross_team_pairs": {
            f"{a} <-> {b}": c for (a, b), c in sorted(cross_team_pairs.items(), key=lambda x: -x[1])
        },
        "clusters": clusters,
    }

    print(f"  Enriched {len(enriched)} edges")
    print(f"  Teams with reviews: {len(concentration)}")
    top_cross = sorted(cross_team_pairs.items(), key=lambda x: -x[1])[:5]
    for (a, b), c in top_cross:
        print(f"    {a} <-> {b}: {c} reviews")

    return enriched, review_summary


# ═══════════════════════════════════════════════════════════════════════════
# PHASE 3: Unified Interaction Graph
# ═══════════════════════════════════════════════════════════════════════════

def build_unified_graph(people, comment_edges, cowork_edges, review_edges, by_account_id, by_name_lower, by_alias):
    print("\n╔══════════════════════════════════════════════╗")
    print("║  Phase 3: Unified Interaction Graph            ║")
    print("╚══════════════════════════════════════════════╝")

    G = nx.DiGraph()

    def ensure_node(pkey):
        if pkey and pkey not in G:
            G.add_node(pkey,
                       name=person_name(people, pkey),
                       team=person_team(people, pkey),
                       geo=person_geo(people, pkey))

    for edge in comment_edges:
        from_key = resolve_account_id(edge["from"], by_account_id)
        to_key = resolve_account_id(edge["to"], by_account_id)
        if from_key and to_key and from_key != to_key:
            ensure_node(from_key)
            ensure_node(to_key)
            if G.has_edge(from_key, to_key):
                G[from_key][to_key]["weight"] += edge["count"]
                if "jira_comment" not in G[from_key][to_key]["channels"]:
                    G[from_key][to_key]["channels"].append("jira_comment")
            else:
                G.add_edge(from_key, to_key, weight=edge["count"], channels=["jira_comment"])

    for edge in cowork_edges:
        a_key = resolve_account_id(edge["from"], by_account_id)
        b_key = resolve_account_id(edge["to"], by_account_id)
        if a_key and b_key and a_key != b_key:
            ensure_node(a_key)
            ensure_node(b_key)
            for u, v in [(a_key, b_key), (b_key, a_key)]:
                if G.has_edge(u, v):
                    G[u][v]["weight"] += edge["count"]
                    if "jira_cowork" not in G[u][v]["channels"]:
                        G[u][v]["channels"].append("jira_cowork")
                else:
                    G.add_edge(u, v, weight=edge["count"], channels=["jira_cowork"])

    for edge in review_edges:
        reviewer_key = edge.get("reviewer_key")
        author_key = edge.get("author_key")
        count = edge.get("count", 1)
        if reviewer_key and author_key and reviewer_key != author_key:
            ensure_node(reviewer_key)
            ensure_node(author_key)
            if G.has_edge(reviewer_key, author_key):
                G[reviewer_key][author_key]["weight"] += count
                if "code_review" not in G[reviewer_key][author_key]["channels"]:
                    G[reviewer_key][author_key]["channels"].append("code_review")
            else:
                G.add_edge(reviewer_key, author_key, weight=count, channels=["code_review"])

    print(f"  Nodes: {G.number_of_nodes()}")
    print(f"  Edges: {G.number_of_edges()}")

    channel_counts = defaultdict(int)
    for u, v, d in G.edges(data=True):
        for ch in d.get("channels", []):
            channel_counts[ch] += 1
    for ch, cnt in sorted(channel_counts.items()):
        print(f"    {ch}: {cnt} edges")

    return G


def graph_to_json(G, people):
    nodes = []
    for n, d in G.nodes(data=True):
        nodes.append({
            "id": n,
            "name": d.get("name", n),
            "team": d.get("team", "Unknown"),
            "geo": d.get("geo", "Unknown"),
            "degree_in": G.in_degree(n),
            "degree_out": G.out_degree(n),
        })

    edges = []
    for u, v, d in G.edges(data=True):
        edges.append({
            "from": u,
            "to": v,
            "weight": d.get("weight", 1),
            "channels": d.get("channels", []),
        })

    return {"nodes": nodes, "edges": edges, "node_count": len(nodes), "edge_count": len(edges)}


# ═══════════════════════════════════════════════════════════════════════════
# PHASE 4: Network Science Metrics
# ═══════════════════════════════════════════════════════════════════════════

def compute_network_metrics(G, people):
    print("\n╔══════════════════════════════════════════════╗")
    print("║  Phase 4: Network Science Metrics              ║")
    print("╚══════════════════════════════════════════════╝")

    if G.number_of_nodes() == 0:
        print("  Empty graph, skipping metrics")
        return {}

    G_undirected = G.to_undirected()

    print("  Computing betweenness centrality...")
    betweenness = nx.betweenness_centrality(G, weight="weight")
    top_betweenness = sorted(betweenness.items(), key=lambda x: -x[1])[:20]

    print("  Computing PageRank...")
    try:
        pagerank = nx.pagerank(G, weight="weight")
    except nx.PowerIterationFailedConvergence:
        pagerank = nx.pagerank(G, weight="weight", max_iter=500)
    top_pagerank = sorted(pagerank.items(), key=lambda x: -x[1])[:20]

    print("  Computing degree centrality...")
    degree_cent = nx.degree_centrality(G)
    top_degree = sorted(degree_cent.items(), key=lambda x: -x[1])[:20]

    print("  Detecting communities...")
    try:
        communities = nx.community.louvain_communities(G_undirected, weight="weight", seed=42)
    except (AttributeError, Exception):
        try:
            communities = nx.community.greedy_modularity_communities(G_undirected, weight="weight")
        except Exception:
            communities = []
            print("  Warning: community detection failed")

    community_data = []
    for i, comm in enumerate(communities):
        members = []
        team_counts = defaultdict(int)
        for node in comm:
            name = person_name(people, node)
            team = person_team(people, node)
            members.append({"id": node, "name": name, "team": team})
            team_counts[team] += 1

        dominant_team = max(team_counts, key=team_counts.get) if team_counts else "Unknown"
        total = sum(team_counts.values())
        alignment = team_counts[dominant_team] / total if total > 0 else 0

        community_data.append({
            "community_id": i,
            "size": len(comm),
            "members": sorted(members, key=lambda m: m["name"]),
            "team_distribution": dict(team_counts),
            "dominant_team": dominant_team,
            "team_alignment_pct": round(alignment * 100, 1),
        })

    community_data.sort(key=lambda c: -c["size"])

    def format_top(items):
        return [
            {"id": k, "name": person_name(people, k), "team": person_team(people, k), "score": round(v, 6)}
            for k, v in items
        ]

    print(f"\n  Top 5 Betweenness (bridge people):")
    for k, v in top_betweenness[:5]:
        print(f"    {person_name(people, k):30s} [{person_team(people, k):15s}] {v:.4f}")

    print(f"\n  Top 5 PageRank (most depended-on):")
    for k, v in top_pagerank[:5]:
        print(f"    {person_name(people, k):30s} [{person_team(people, k):15s}] {v:.4f}")

    print(f"\n  Communities found: {len(community_data)}")
    for c in community_data[:5]:
        print(f"    Community {c['community_id']}: {c['size']} members, dominant team: {c['dominant_team']} ({c['team_alignment_pct']}% aligned)")

    metrics = {
        "betweenness_top20": format_top(top_betweenness),
        "pagerank_top20": format_top(top_pagerank),
        "degree_centrality_top20": format_top(top_degree),
        "communities": community_data,
        "community_count": len(community_data),
        "graph_stats": {
            "nodes": G.number_of_nodes(),
            "edges": G.number_of_edges(),
            "density": round(nx.density(G), 6),
        },
        "all_betweenness": {k: round(v, 6) for k, v in betweenness.items()},
        "all_pagerank": {k: round(v, 6) for k, v in pagerank.items()},
    }

    return metrics


# ═══════════════════════════════════════════════════════════════════════════
# PHASE 5: Key Person Risk Scoring
# ═══════════════════════════════════════════════════════════════════════════

def compute_risk_scores(people, review_edges, metrics):
    print("\n╔══════════════════════════════════════════════╗")
    print("║  Phase 5: Key Person Risk Scoring              ║")
    print("╚══════════════════════════════════════════════╝")

    all_pagerank = metrics.get("all_pagerank", {})
    max_pr = max(all_pagerank.values()) if all_pagerank else 1

    team_review_totals = defaultdict(int)
    person_review_counts = defaultdict(int)
    for edge in review_edges:
        reviewer_key = edge.get("reviewer_key")
        if reviewer_key:
            person_review_counts[reviewer_key] += edge.get("count", 1)
            team = person_team(people, reviewer_key)
            team_review_totals[team] += edge.get("count", 1)

    team_confluence_totals = defaultdict(int)
    person_confluence = {}
    for pkey, person in people.items():
        conf = person.get("sources", {}).get("confluence", {})
        pages = conf.get("pages_total", 0)
        if pages > 0:
            person_confluence[pkey] = pages
            team = person_team(people, pkey)
            team_confluence_totals[team] += pages

    risk_scores = {}
    for pkey, person in people.items():
        if person.get("status") != "active" and person.get("activity", {}).get("level") == "inactive":
            continue

        score = 0.0
        breakdown = {}

        team = person_team(people, pkey)
        reviews = person_review_counts.get(pkey, 0)
        team_total_reviews = team_review_totals.get(team, 0)
        if team_total_reviews > 0:
            review_share = reviews / team_total_reviews
            if review_share > 0.10:
                pts = min(30, review_share * 100)
                score += pts
                breakdown["review_bottleneck"] = round(pts, 1)
                breakdown["review_share_pct"] = round(review_share * 100, 1)

        pr = all_pagerank.get(pkey, 0)
        if max_pr > 0:
            pts = (pr / max_pr) * 25
            score += pts
            breakdown["code_centrality"] = round(pts, 1)

        conf_pages = person_confluence.get(pkey, 0)
        team_conf = team_confluence_totals.get(team, 0)
        if team_conf > 0:
            conf_share = conf_pages / team_conf
            if conf_share > 0.15:
                pts = min(20, conf_share * 40)
                score += pts
                breakdown["knowledge_monopoly"] = round(pts, 1)
                breakdown["confluence_share_pct"] = round(conf_share * 100, 1)

        systems = person.get("activity", {}).get("systems_active_90d", 0)
        pts = min(25, systems * 5)
        score += pts
        breakdown["cross_system_breadth"] = round(pts, 1)
        breakdown["systems_active"] = systems

        score = min(100, score)

        if score > 0:
            risk_scores[pkey] = {
                "name": person_name(people, pkey),
                "team": team,
                "score": round(score, 1),
                "breakdown": breakdown,
            }

    team_risk = defaultdict(list)
    for pkey, rdata in risk_scores.items():
        team_risk[rdata["team"]].append(rdata["score"])

    team_aggregate = {}
    for team, scores in team_risk.items():
        scores_sorted = sorted(scores, reverse=True)
        top3 = scores_sorted[:3]
        team_aggregate[team] = {
            "avg_top3_risk": round(sum(top3) / len(top3), 1) if top3 else 0,
            "max_risk": round(scores_sorted[0], 1) if scores_sorted else 0,
            "people_at_risk": len([s for s in scores if s >= 30]),
            "total_scored": len(scores),
        }

    top_risk = sorted(risk_scores.items(), key=lambda x: -x[1]["score"])[:10]
    print(f"  People scored: {len(risk_scores)}")
    print(f"\n  Top 10 Key Person Risk:")
    for pkey, rd in top_risk:
        print(f"    {rd['name']:30s} [{rd['team']:15s}] risk={rd['score']:.0f}")

    high_risk_teams = sorted(team_aggregate.items(), key=lambda x: -x[1]["avg_top3_risk"])[:5]
    print(f"\n  Highest team aggregate risk:")
    for team, td in high_risk_teams:
        print(f"    {team:20s} avg_top3={td['avg_top3_risk']:.1f}  max={td['max_risk']:.1f}  at_risk={td['people_at_risk']}")

    return {
        "people": risk_scores,
        "teams": team_aggregate,
    }


# ═══════════════════════════════════════════════════════════════════════════
# PHASE 6: Cross-Team Interaction Heatmap
# ═══════════════════════════════════════════════════════════════════════════

def build_team_interaction_matrix(G, people):
    print("\n╔══════════════════════════════════════════════╗")
    print("║  Phase 6: Cross-Team Interaction Heatmap       ║")
    print("╚══════════════════════════════════════════════╝")

    teams = set()
    for pkey, person in people.items():
        t = person.get("team")
        if t:
            teams.add(t)
    teams = sorted(teams)

    directed = defaultdict(int)
    undirected = defaultdict(int)

    for u, v, d in G.edges(data=True):
        t_u = person_team(people, u)
        t_v = person_team(people, v)
        if t_u == "Unknown" or t_v == "Unknown":
            continue
        weight = d.get("weight", 1)
        directed[(t_u, t_v)] += weight
        pair = tuple(sorted([t_u, t_v]))
        undirected[pair] += weight

    matrix = {}
    for t1 in teams:
        row = {}
        for t2 in teams:
            row[t2] = directed.get((t1, t2), 0)
        matrix[t1] = row

    symmetric = {}
    for t1 in teams:
        row = {}
        for t2 in teams:
            pair = tuple(sorted([t1, t2]))
            row[t2] = undirected.get(pair, 0)
        symmetric[t1] = row

    nonzero = [(k, v) for k, v in undirected.items() if k[0] != k[1] and v > 0]
    nonzero.sort(key=lambda x: -x[1])

    print(f"  Teams: {len(teams)}")
    print(f"  Non-zero cross-team pairs: {len(nonzero)}")
    print(f"\n  Top cross-team interactions:")
    for (t1, t2), count in nonzero[:10]:
        print(f"    {t1:20s} <-> {t2:20s}: {count}")

    return {
        "teams": teams,
        "directed_matrix": matrix,
        "symmetric_matrix": symmetric,
        "top_cross_team": [{"team_a": a, "team_b": b, "count": c} for (a, b), c in nonzero[:30]],
    }


# ═══════════════════════════════════════════════════════════════════════════
# PHASE 7: Communication Gap Detection
# ═══════════════════════════════════════════════════════════════════════════

def detect_communication_gaps(people, team_matrix, G):
    print("\n╔══════════════════════════════════════════════╗")
    print("║  Phase 7: Communication Gap Detection          ║")
    print("╚══════════════════════════════════════════════╝")

    team_projects = defaultdict(set)
    for pkey, person in people.items():
        team = person.get("team")
        if not team:
            continue
        jira = person.get("sources", {}).get("jira", {})
        for proj in jira.get("projects", []):
            team_projects[team].add(proj)

    shared_projects = defaultdict(set)
    teams_list = sorted(team_projects.keys())
    for i, t1 in enumerate(teams_list):
        for t2 in teams_list[i + 1:]:
            overlap = team_projects[t1] & team_projects[t2]
            if overlap:
                pair = tuple(sorted([t1, t2]))
                shared_projects[pair] = overlap

    symmetric = team_matrix.get("symmetric_matrix", {})

    gaps = []
    for (t1, t2), projects in shared_projects.items():
        interaction_count = symmetric.get(t1, {}).get(t2, 0)
        if interaction_count <= 2:
            gaps.append({
                "team_a": t1,
                "team_b": t2,
                "shared_projects": sorted(projects),
                "interaction_count": interaction_count,
                "severity": "high" if interaction_count == 0 else "medium",
            })

    gaps.sort(key=lambda g: (0 if g["severity"] == "high" else 1, -len(g["shared_projects"])))

    print(f"  Team pairs sharing projects: {len(shared_projects)}")
    print(f"  Communication gaps found: {len(gaps)}")
    for gap in gaps[:10]:
        print(f"    [{gap['severity']:6s}] {gap['team_a']:20s} <-> {gap['team_b']:20s}  "
              f"projects={gap['shared_projects']}  interactions={gap['interaction_count']}")

    return {
        "gaps": gaps,
        "team_project_map": {t: sorted(p) for t, p in team_projects.items()},
        "shared_project_pairs": {f"{a} <-> {b}": sorted(p) for (a, b), p in shared_projects.items()},
    }


# ═══════════════════════════════════════════════════════════════════════════
# Update People Master
# ═══════════════════════════════════════════════════════════════════════════

def update_people_master(people, risk_data, metrics, G):
    print("\n  Updating people_master.json with interaction data...")

    all_pagerank = metrics.get("all_pagerank", {})
    all_betweenness = metrics.get("all_betweenness", {})

    community_map = {}
    for comm in metrics.get("communities", []):
        for member in comm.get("members", []):
            community_map[member["id"]] = comm["community_id"]

    updated = 0
    for pkey, person in people.items():
        interactions = {
            "in_degree": G.in_degree(pkey) if pkey in G else 0,
            "out_degree": G.out_degree(pkey) if pkey in G else 0,
            "pagerank": all_pagerank.get(pkey, 0),
            "betweenness": all_betweenness.get(pkey, 0),
            "community_id": community_map.get(pkey),
        }

        channels = set()
        if pkey in G:
            for _, _, d in G.edges(pkey, data=True):
                channels.update(d.get("channels", []))
            for _, _, d in G.in_edges(pkey, data=True):
                channels.update(d.get("channels", []))
        interactions["channels"] = sorted(channels)

        person["interactions"] = interactions

        risk_entry = risk_data.get("people", {}).get(pkey)
        if risk_entry:
            person["risk_scores"] = {
                "total": risk_entry["score"],
                "breakdown": risk_entry["breakdown"],
            }
            updated += 1

    print(f"  Updated {updated} people with risk scores")
    return people


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    start = time.time()
    print("=" * 60)
    print("  Interaction Analysis & Network Science")
    print("=" * 60)

    creds = load_env()
    people = load_json(PEOPLE_FILE)
    if not people:
        print("ERROR: people_master.json not found")
        sys.exit(1)

    print(f"  People registry: {len(people)} records")

    by_account_id, by_name_lower, by_alias = build_lookup_tables(people)
    print(f"  Lookup tables: {len(by_account_id)} account IDs, {len(by_name_lower)} names")

    # Phase 1: Jira Comments
    if SKIP_API:
        print("\n  --skip-api: loading cached Jira data")
        comment_edges, cowork_edges = load_cached_jira_comments()
    else:
        token = creds.get("ATLASSIAN_TOKEN")
        if not token:
            print("  WARNING: No ATLASSIAN_TOKEN, skipping Jira phase")
            comment_edges, cowork_edges = load_cached_jira_comments()
        else:
            auth = HTTPBasicAuth(JIRA_EMAIL, token)
            comment_edges, cowork_edges = fetch_jira_comments(auth)
            save_json(os.path.join(OUTPUT_DIR, "interactions_jira_comments.json"), {
                "comment_edges": comment_edges,
                "cowork_edges": cowork_edges,
                "fetched_at": datetime.now(timezone.utc).isoformat(),
            })

    # Phase 2: Review Network Enrichment
    review_edges, review_summary = enrich_review_network(people, by_account_id, by_name_lower, by_alias)
    save_json(os.path.join(OUTPUT_DIR, "interactions_review_enriched.json"), {
        "edges": review_edges,
        "summary": review_summary,
        "enriched_at": datetime.now(timezone.utc).isoformat(),
    })

    # Phase 3: Unified Graph
    G = build_unified_graph(people, comment_edges, cowork_edges, review_edges, by_account_id, by_name_lower, by_alias)
    unified_data = graph_to_json(G, people)
    save_json(os.path.join(OUTPUT_DIR, "interactions_unified.json"), unified_data)

    # Phase 4: Network Metrics
    metrics = compute_network_metrics(G, people)
    save_json(os.path.join(OUTPUT_DIR, "network_metrics.json"), metrics)

    # Phase 5: Risk Scoring
    risk_data = compute_risk_scores(people, review_edges, metrics)
    save_json(os.path.join(OUTPUT_DIR, "people_risk.json"), risk_data)

    # Phase 6: Team Interaction Matrix
    team_matrix = build_team_interaction_matrix(G, people)
    save_json(os.path.join(OUTPUT_DIR, "team_interactions.json"), team_matrix)

    # Phase 7: Communication Gaps
    gap_data = detect_communication_gaps(people, team_matrix, G)
    save_json(os.path.join(OUTPUT_DIR, "communication_gaps.json"), gap_data)

    # Update people_master.json
    people = update_people_master(people, risk_data, metrics, G)
    save_json(PEOPLE_FILE, people)

    elapsed = time.time() - start
    print("\n" + "=" * 60)
    print("  Summary")
    print("=" * 60)
    print(f"  Jira comment edges:     {len(comment_edges)}")
    print(f"  Jira co-work edges:     {len(cowork_edges)}")
    print(f"  Review edges enriched:  {len(review_edges)}")
    print(f"  Unified graph:          {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    print(f"  Communities detected:   {metrics.get('community_count', 0)}")
    print(f"  People with risk score: {len(risk_data.get('people', {}))}")
    print(f"  Communication gaps:     {len(gap_data.get('gaps', []))}")
    print(f"  Elapsed: {elapsed:.1f}s")
    print("=" * 60)


if __name__ == "__main__":
    main()
