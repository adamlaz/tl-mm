#!/usr/bin/env python3
"""Microsoft Graph organizational intelligence.

Subcommands:
  directory  - Pull full directory, build org tree, cross-reference people_master
  meetings   - Pull full 2026 YTD calendar data, build meeting interaction network
  people     - Pull People API relevance scores, detect clusters
  teams      - Pull Teams/Groups membership
  network    - Merge all layers into unified interaction network
  all        - Run everything in sequence

Usage:
  python scripts/m365_directory.py directory
  python scripts/m365_directory.py meetings
  python scripts/m365_directory.py all
"""

import sys
import json
import os
import time
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

sys.stdout.reconfigure(line_buffering=True)

sys.path.insert(0, str(Path(__file__).parent))
from m365_auth import get_app_token, graph_get, GRAPH_BASE

import requests

ROOT = Path(__file__).parent.parent
INV = ROOT / "inventory" / "users"
SRC = INV / "sources"
CHARTS = ROOT / "analysis" / "charts"

for d in [INV, SRC, CHARTS]:
    d.mkdir(parents=True, exist_ok=True)


def save(path, data):
    Path(path).write_text(json.dumps(data, indent=2, default=str))
    print(f"  Saved -> {path}")


def load(path):
    p = Path(path)
    if p.exists():
        return json.loads(p.read_text())
    return None


# ─── DIRECTORY ────────────────────────────────────────────────

def cmd_directory(token):
    print("\n" + "=" * 60)
    print("STEP 1: FULL DIRECTORY PULL")
    print("=" * 60)

    select = "id,displayName,mail,userPrincipalName,jobTitle,department,officeLocation,accountEnabled,createdDateTime,employeeType"
    headers = {"Authorization": f"Bearer {token}"}

    print("\n  Pulling active users...")
    url = f"{GRAPH_BASE}/users?$top=999&$select={select}&$expand=manager($select=id,displayName,mail)&$filter=accountEnabled eq true"
    active = []
    page = 0
    while url:
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            print(f"  ERROR {r.status_code}: {r.text[:200]}")
            break
        data = r.json()
        batch = data.get("value", [])
        active.extend(batch)
        page += 1
        print(f"    Page {page}: {len(batch)} users (total: {len(active)})")
        url = data.get("@odata.nextLink")
    print(f"  Active users: {len(active)}")

    print("\n  Pulling disabled/departed accounts...")
    url = f"{GRAPH_BASE}/users?$top=999&$select={select}&$filter=accountEnabled eq false"
    disabled = []
    while url:
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            break
        data = r.json()
        disabled.extend(data.get("value", []))
        url = data.get("@odata.nextLink")
    print(f"  Disabled accounts: {len(disabled)}")

    save(SRC / "m365_directory.json", active)
    save(SRC / "m365_disabled.json", disabled)

    real_people = [u for u in active if not _is_service_account(u)]
    print(f"  Real people (filtered): {len(real_people)}")
    print(f"  Service/shared accounts filtered: {len(active) - len(real_people)}")

    print("\n  Building org tree...")
    tree, metrics, orphans = _build_org_tree(real_people)
    save(INV / "m365_org_tree.json", tree)
    save(INV / "m365_org_metrics.json", {
        "total_people": len(real_people),
        "orphan_nodes": len(orphans),
        "orphans": orphans,
        "metrics": metrics,
    })
    print(f"  Org tree built. Orphan nodes: {len(orphans)}")

    print("\n  Cross-referencing people_master...")
    discrepancies = _cross_reference_people_master(real_people)
    save(INV / "m365_discrepancies.json", discrepancies)
    print(f"  Discrepancies flagged: {len(discrepancies.get('items', []))}")

    print("\n  Summary:")
    dept_counts = defaultdict(int)
    for u in real_people:
        dept_counts[u.get("department") or "No Department"] += 1
    for dept, count in sorted(dept_counts.items(), key=lambda x: -x[1])[:15]:
        print(f"    {dept}: {count}")


def _is_service_account(user):
    name = (user.get("displayName") or "").lower()
    mail = (user.get("mail") or "").lower()
    upn = (user.get("userPrincipalName") or "").lower()
    markers = ["shared", "service", "test", "backstage", "noreply", "room", "conference", "admin@", "sync"]
    if "(shared)" in name or "(unlicensed)" in name:
        return True
    if any(m in mail for m in markers) or any(m in upn for m in markers):
        return True
    if not user.get("jobTitle") and not user.get("department") and "(shared)" not in name.lower():
        if "@" in name or "." not in name:
            return True
    return False


def _build_org_tree(users):
    by_id = {}
    by_email = {}
    by_name = {}
    for u in users:
        uid = u.get("id")
        by_id[uid] = u
        if u.get("mail"):
            by_email[u["mail"].lower()] = u
        by_name[u.get("displayName", "").lower()] = u

    children = defaultdict(list)
    orphans = []
    for u in users:
        mgr = u.get("manager")
        if mgr and mgr.get("id"):
            children[mgr["id"]].append(u)
        else:
            orphans.append({"name": u.get("displayName"), "email": u.get("mail"), "title": u.get("jobTitle")})

    def build_node(user, depth=0):
        uid = user.get("id")
        reports = children.get(uid, [])
        subtree = len(reports)
        child_nodes = []
        for r in sorted(reports, key=lambda x: x.get("displayName", "")):
            cn = build_node(r, depth + 1)
            subtree += cn.get("subtree_size", 0)
            child_nodes.append(cn)
        return {
            "name": user.get("displayName"),
            "email": user.get("mail"),
            "title": user.get("jobTitle"),
            "department": user.get("department"),
            "office": user.get("officeLocation"),
            "depth": depth,
            "direct_reports": len(reports),
            "subtree_size": subtree,
            "reports": child_nodes,
        }

    metrics = []
    for u in users:
        uid = u.get("id")
        dr = len(children.get(uid, []))
        if dr > 0:
            metrics.append({
                "name": u.get("displayName"),
                "email": u.get("mail"),
                "title": u.get("jobTitle"),
                "direct_reports": dr,
            })
    metrics.sort(key=lambda x: -x["direct_reports"])

    roots = [u for u in users if not u.get("manager") or not u.get("manager", {}).get("id")]
    don = None
    for r in roots:
        if "salama" in (r.get("displayName") or "").lower() or "don" in (r.get("displayName") or "").lower():
            don = r
            break

    if don:
        tree = build_node(don)
    else:
        tree = {"name": "ROOT (Don not found)", "reports": [build_node(r) for r in roots[:10]]}

    return tree, metrics, orphans


def _cross_reference_people_master(directory_users):
    pm_path = INV / "people_master.json"
    if not pm_path.exists():
        return {"items": [], "note": "people_master.json not found"}

    pm = json.loads(pm_path.read_text())
    dir_by_email = {}
    dir_by_name = {}
    for u in directory_users:
        if u.get("mail"):
            dir_by_email[u["mail"].lower()] = u
        dir_by_name[u.get("displayName", "").lower().strip()] = u

    discrepancies = []
    emails_filled = 0
    updated = 0

    for key, person in pm.items():
        pm_email = (person.get("email") or "").lower()
        pm_name = person.get("canonical_name", "").lower().strip()

        match = None
        if pm_email and pm_email in dir_by_email:
            match = dir_by_email[pm_email]
        elif pm_name in dir_by_name:
            match = dir_by_name[pm_name]
        else:
            for dname, duser in dir_by_name.items():
                pm_parts = set(pm_name.split())
                d_parts = set(dname.split())
                if len(pm_parts & d_parts) >= 2:
                    match = duser
                    break

        if not match:
            continue

        if not person.get("email") and match.get("mail"):
            person["email"] = match["mail"]
            emails_filled += 1

        dir_title = match.get("jobTitle", "")
        dir_dept = match.get("department", "")
        dir_mgr = match.get("manager", {})
        dir_mgr_name = dir_mgr.get("displayName", "") if isinstance(dir_mgr, dict) else ""

        if "sources" not in person:
            person["sources"] = {}
        person["sources"]["m365_directory"] = {
            "mail": match.get("mail"),
            "title": dir_title,
            "department": dir_dept,
            "office": match.get("officeLocation"),
            "manager": dir_mgr_name,
            "accountEnabled": match.get("accountEnabled"),
            "createdDateTime": match.get("createdDateTime"),
        }
        updated += 1

        pm_manager = person.get("manager", "")
        if dir_mgr_name and pm_manager and dir_mgr_name.lower() != pm_manager.lower():
            discrepancies.append({
                "person": person.get("canonical_name"),
                "type": "manager_mismatch",
                "org_chart_manager": pm_manager,
                "directory_manager": dir_mgr_name,
            })

        pm_title = person.get("title", "")
        if dir_title and pm_title and dir_title.lower() != pm_title.lower():
            discrepancies.append({
                "person": person.get("canonical_name"),
                "type": "title_mismatch",
                "org_chart_title": pm_title,
                "directory_title": dir_title,
            })

    pm_path.write_text(json.dumps(pm, indent=2, default=str))
    print(f"  Emails filled: {emails_filled}")
    print(f"  Records updated: {updated}")
    print(f"  Discrepancies: {len(discrepancies)}")
    return {"items": discrepancies, "emails_filled": emails_filled, "records_updated": updated}


# ─── MEETINGS ─────────────────────────────────────────────────

def cmd_meetings(token):
    print("\n" + "=" * 60)
    print("STEP 2: MEETING INTERACTION NETWORK (Full Org, 2026 YTD)")
    print("=" * 60)

    dir_data = load(SRC / "m365_directory.json")
    if not dir_data:
        print("  ERROR: Run 'directory' first")
        return

    users = [u for u in dir_data if not _is_service_account(u)]
    print(f"  Users to process: {len(users)}")

    headers = {"Authorization": f"Bearer {token}"}
    start_dt = "2026-01-01T00:00:00Z"
    end_dt = "2026-04-07T00:00:00Z"
    reorg_date = "2026-04-03"

    all_events = {}
    meeting_edges = defaultdict(lambda: {"count": 0, "total_minutes": 0, "pre_reorg": 0, "post_reorg": 0})
    per_person = {}
    errors = 0

    for i, user in enumerate(users):
        uid = user.get("id")
        email = (user.get("mail") or "").lower()
        name = user.get("displayName", "")
        if not uid or not email:
            continue

        url = f"{GRAPH_BASE}/users/{uid}/calendarView?$top=250&startDateTime={start_dt}&endDateTime={end_dt}&$select=start,end,attendees,isAllDay,type"
        events = []
        retries = 0
        while url and retries < 3:
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                data = r.json()
                events.extend(data.get("value", []))
                url = data.get("@odata.nextLink")
                retries = 0
            elif r.status_code == 429:
                retry_after = int(r.headers.get("Retry-After", "5"))
                time.sleep(retry_after)
                retries += 1
            elif r.status_code in (403, 404):
                break
            else:
                errors += 1
                break

        non_allday = [e for e in events if not e.get("isAllDay")]
        all_events[email] = len(non_allday)

        total_mins = 0
        meeting_days = defaultdict(float)
        recurring_count = 0
        sizes = []

        for evt in non_allday:
            s = evt.get("start", {}).get("dateTime", "")[:10]
            e_start = evt.get("start", {}).get("dateTime", "")
            e_end = evt.get("end", {}).get("dateTime", "")
            attendees = [a.get("emailAddress", {}).get("address", "").lower() for a in evt.get("attendees", []) if a.get("emailAddress")]
            is_post = s >= reorg_date if s else False

            dur = 0
            try:
                t1 = datetime.fromisoformat(e_start.replace("Z", "+00:00"))
                t2 = datetime.fromisoformat(e_end.replace("Z", "+00:00"))
                dur = (t2 - t1).total_seconds() / 60
            except Exception:
                dur = 30

            if dur > 480:
                continue

            total_mins += dur
            if s:
                meeting_days[s] += dur / 60
            if evt.get("type") == "occurrence":
                recurring_count += 1
            sizes.append(len(attendees))

            att_emails = set(a for a in attendees if a and a != email)
            for att in att_emails:
                edge_key = tuple(sorted([email, att]))
                meeting_edges[edge_key]["count"] += 1
                meeting_edges[edge_key]["total_minutes"] += dur
                if is_post:
                    meeting_edges[edge_key]["post_reorg"] += 1
                else:
                    meeting_edges[edge_key]["pre_reorg"] += 1

        days_with_meetings = len(meeting_days)
        avg_hrs = (total_mins / 60) / max(days_with_meetings, 1)

        per_person[email] = {
            "name": name,
            "title": user.get("jobTitle"),
            "department": user.get("department"),
            "total_events": len(non_allday),
            "total_hours": round(total_mins / 60, 1),
            "days_with_meetings": days_with_meetings,
            "avg_hours_per_meeting_day": round(avg_hrs, 2),
            "recurring_pct": round(recurring_count / max(len(non_allday), 1) * 100, 1),
            "avg_meeting_size": round(sum(sizes) / max(len(sizes), 1), 1),
        }

        if (i + 1) % 25 == 0 or (i + 1) == len(users):
            print(f"    Processed {i+1}/{len(users)} users ({errors} errors, {len(meeting_edges)} edges so far)")
        time.sleep(0.05)

    print(f"  Processed {len(users)} users ({errors} errors)")
    print(f"  Total meeting edges: {len(meeting_edges)}")

    edges_list = []
    for (a, b), data in meeting_edges.items():
        edges_list.append({"source": a, "target": b, **data})
    edges_list.sort(key=lambda x: -x["count"])

    save(INV / "m365_meeting_network.json", {
        "nodes": len(per_person),
        "edges": len(edges_list),
        "edge_list": edges_list[:5000],
    })
    save(INV / "m365_meeting_load.json", per_person)

    _build_meeting_charts(per_person, edges_list, users)


def _build_meeting_charts(per_person, edges, users):
    dept_load = defaultdict(list)
    for email, stats in per_person.items():
        dept = stats.get("department") or "Unknown"
        dept_load[dept].append(stats.get("avg_hours_per_meeting_day", 0))

    func_data = []
    for dept, hours_list in sorted(dept_load.items(), key=lambda x: -sum(x[1]) / max(len(x[1]), 1)):
        avg = sum(hours_list) / max(len(hours_list), 1)
        func_data.append({"department": dept, "avg_hours_per_day": round(avg, 2), "people": len(hours_list)})

    save(CHARTS / "meeting_load_by_function.json", {
        "option": {
            "title": {"text": "Meeting Load by Department", "subtext": "Avg hours/day in meetings (2026 YTD)"},
            "tooltip": {"trigger": "axis"},
            "grid": {"left": 180, "right": 40, "top": 60, "bottom": 30},
            "xAxis": {"type": "value", "name": "Avg Hours/Day"},
            "yAxis": {"type": "category", "data": [d["department"] for d in func_data[:20]], "inverse": True},
            "series": [{"type": "bar", "data": [d["avg_hours_per_day"] for d in func_data[:20]]}],
        }
    })

    cross_func = defaultdict(int)
    user_dept = {}
    for u in users:
        if u.get("mail"):
            user_dept[u["mail"].lower()] = u.get("department") or "Unknown"
    for e in edges:
        d1 = user_dept.get(e["source"], "External")
        d2 = user_dept.get(e["target"], "External")
        if d1 != d2 and d1 != "External" and d2 != "External":
            key = tuple(sorted([d1, d2]))
            cross_func[key] += e["count"]

    crossfunc_list = [{"from": k[0], "to": k[1], "meetings": v} for k, v in sorted(cross_func.items(), key=lambda x: -x[1])[:50]]
    save(INV / "m365_meeting_crossfunc.json", crossfunc_list)

    print(f"  Meeting charts generated")


# ─── PEOPLE RELEVANCE ─────────────────────────────────────────

def cmd_people(token):
    print("\n" + "=" * 60)
    print("STEP 3: PEOPLE API RELEVANCE MAP (Full Org)")
    print("=" * 60)

    dir_data = load(SRC / "m365_directory.json")
    if not dir_data:
        print("  ERROR: Run 'directory' first")
        return

    users = [u for u in dir_data if not _is_service_account(u) and u.get("id")]
    print(f"  Users to process: {len(users)}")

    headers = {"Authorization": f"Bearer {token}"}
    relevance_edges = []
    errors = 0

    for i, user in enumerate(users):
        uid = user.get("id")
        email = (user.get("mail") or "").lower()
        if not email:
            continue

        r = requests.get(f"{GRAPH_BASE}/users/{uid}/people?$top=25", headers=headers)
        if r.status_code == 200:
            people = r.json().get("value", [])
            for rank, p in enumerate(people):
                p_emails = p.get("scoredEmailAddresses", [])
                p_email = p_emails[0].get("address", "").lower() if p_emails else ""
                if p_email and p_email != email:
                    relevance_edges.append({
                        "source": email,
                        "target": p_email,
                        "rank": rank + 1,
                        "target_name": p.get("displayName"),
                        "target_title": p.get("jobTitle"),
                        "target_department": p.get("department"),
                    })
        else:
            errors += 1

        if (i + 1) % 50 == 0:
            print(f"    Processed {i+1}/{len(users)} ({errors} errors)")
        time.sleep(0.1)

    print(f"  Processed {len(users)} users ({errors} errors)")
    print(f"  Total relevance edges: {len(relevance_edges)}")

    save(INV / "m365_people_relevance.json", {
        "total_edges": len(relevance_edges),
        "edges": relevance_edges,
    })

    bridges = _find_bridges(relevance_edges, users)
    save(INV / "m365_crossorg_bridges.json", bridges)

    _build_relevance_charts(relevance_edges, users)


def _find_bridges(edges, users):
    user_dept = {}
    for u in users:
        if u.get("mail"):
            user_dept[u["mail"].lower()] = u.get("department") or "Unknown"

    cross_dept_mentions = defaultdict(lambda: defaultdict(int))
    for e in edges:
        src_dept = user_dept.get(e["source"], "Unknown")
        tgt_dept = e.get("target_department") or user_dept.get(e["target"], "Unknown")
        if src_dept != tgt_dept and src_dept != "Unknown" and tgt_dept != "Unknown":
            cross_dept_mentions[e["source"]][tgt_dept] += 1

    bridges = []
    for email, depts in cross_dept_mentions.items():
        if len(depts) >= 2:
            bridges.append({
                "email": email,
                "own_department": user_dept.get(email, "Unknown"),
                "bridges_to": dict(depts),
                "bridge_strength": sum(depts.values()),
            })
    bridges.sort(key=lambda x: -x["bridge_strength"])
    return bridges[:50]


def _build_relevance_charts(edges, users):
    user_dept = {}
    for u in users:
        if u.get("mail"):
            user_dept[u["mail"].lower()] = u.get("department") or "Unknown"

    func_matrix = defaultdict(lambda: defaultdict(int))
    for e in edges:
        d1 = user_dept.get(e["source"], "Unknown")
        d2 = e.get("target_department") or user_dept.get(e["target"], "Unknown")
        if d1 != "Unknown" and d2 != "Unknown":
            func_matrix[d1][d2] += 1

    depts = sorted(set(list(func_matrix.keys()) + [d for row in func_matrix.values() for d in row.keys()]))[:20]
    heatmap_data = []
    for i, d1 in enumerate(depts):
        for j, d2 in enumerate(depts):
            val = func_matrix.get(d1, {}).get(d2, 0)
            if val > 0:
                heatmap_data.append([i, j, val])

    save(CHARTS / "relevance_function_heatmap.json", {
        "option": {
            "title": {"text": "Cross-Department Relevance", "subtext": "Microsoft 365 collaboration signal strength"},
            "tooltip": {"position": "top"},
            "grid": {"left": 180, "top": 60, "right": 40, "bottom": 120},
            "xAxis": {"type": "category", "data": depts, "axisLabel": {"rotate": 45}},
            "yAxis": {"type": "category", "data": depts},
            "visualMap": {"min": 0, "max": max((d[2] for d in heatmap_data), default=1), "calculable": True, "orient": "horizontal", "left": "center", "bottom": 10},
            "series": [{"type": "heatmap", "data": heatmap_data, "label": {"show": False}}],
        }
    })
    print(f"  Relevance charts generated")


# ─── TEAMS ────────────────────────────────────────────────────

def cmd_teams(token):
    print("\n" + "=" * 60)
    print("STEP 4: TEAMS & GROUPS MAPPING")
    print("=" * 60)

    headers = {"Authorization": f"Bearer {token}"}

    print("  Pulling groups...")
    result = graph_get(token, "/groups?$top=999&$select=id,displayName,groupTypes,mailEnabled,description,createdDateTime,resourceProvisioningOptions")
    groups = result.get("values", [])
    print(f"  Total groups: {len(groups)}")

    teams_groups = [g for g in groups if "Team" in (g.get("resourceProvisioningOptions") or [])]
    print(f"  Teams-enabled groups: {len(teams_groups)}")

    teams_detail = []
    for i, team in enumerate(teams_groups):
        tid = team.get("id")
        entry = {
            "id": tid,
            "name": team.get("displayName"),
            "description": team.get("description"),
            "created": team.get("createdDateTime"),
            "members": [],
            "channels": [],
        }

        r = requests.get(f"{GRAPH_BASE}/groups/{tid}/members?$top=999&$select=id,displayName,mail,jobTitle", headers=headers)
        if r.status_code == 200:
            entry["members"] = [{"name": m.get("displayName"), "email": m.get("mail"), "title": m.get("jobTitle")} for m in r.json().get("value", [])]

        r = requests.get(f"{GRAPH_BASE}/teams/{tid}/channels?$select=id,displayName,membershipType", headers=headers)
        if r.status_code == 200:
            entry["channels"] = [{"name": c.get("displayName"), "type": c.get("membershipType")} for c in r.json().get("value", [])]

        entry["member_count"] = len(entry["members"])
        entry["channel_count"] = len(entry["channels"])
        teams_detail.append(entry)

        if (i + 1) % 20 == 0:
            print(f"    Processed {i+1}/{len(teams_groups)} teams")
        time.sleep(0.1)

    save(SRC / "m365_teams_detail.json", teams_detail)

    dir_data = load(SRC / "m365_directory.json")
    user_dept = {}
    if dir_data:
        for u in dir_data:
            if u.get("mail"):
                user_dept[u["mail"].lower()] = u.get("department") or "Unknown"

    analysis = []
    for t in teams_detail:
        depts = set()
        for m in t["members"]:
            dept = user_dept.get((m.get("email") or "").lower(), "Unknown")
            if dept != "Unknown":
                depts.add(dept)
        analysis.append({
            "name": t["name"],
            "member_count": t["member_count"],
            "channel_count": t["channel_count"],
            "departments": list(depts),
            "cross_functional": len(depts) > 1,
            "created": t["created"],
        })

    save(INV / "m365_teams_analysis.json", analysis)
    print(f"  Teams analyzed: {len(analysis)}")
    print(f"  Cross-functional teams: {sum(1 for a in analysis if a['cross_functional'])}")


# ─── UNIFIED NETWORK ──────────────────────────────────────────

def cmd_network(token):
    print("\n" + "=" * 60)
    print("STEP 5: UNIFIED MULTI-LAYER NETWORK")
    print("=" * 60)

    layers = {}

    meeting_net = load(INV / "m365_meeting_network.json")
    if meeting_net:
        edges = {}
        for e in meeting_net.get("edge_list", []):
            key = tuple(sorted([e["source"], e["target"]]))
            edges[key] = e["count"]
        layers["meeting"] = edges
        print(f"  Meeting layer: {len(edges)} edges")

    relevance = load(INV / "m365_people_relevance.json")
    if relevance:
        edges = {}
        for e in relevance.get("edges", []):
            key = tuple(sorted([e["source"], e["target"]]))
            edges[key] = edges.get(key, 0) + (26 - e.get("rank", 25))
        layers["relevance"] = edges
        print(f"  Relevance layer: {len(edges)} edges")

    unified_path = INV / "interactions_unified.json"
    if unified_path.exists():
        uni_data = json.loads(unified_path.read_text())
        uni_edges = uni_data.get("edges", [])
        code_edges = {}
        jira_edges = {}
        for e in uni_edges:
            src = (e.get("from") or "").lower().strip()
            tgt = (e.get("to") or "").lower().strip()
            channel = e.get("channel", "")
            weight = e.get("weight", 1)
            if not src or not tgt:
                continue
            key = tuple(sorted([src, tgt]))
            if "review" in channel.lower() or "pr" in channel.lower() or "bitbucket" in channel.lower():
                code_edges[key] = code_edges.get(key, 0) + weight
            elif "jira" in channel.lower() or "comment" in channel.lower():
                jira_edges[key] = jira_edges.get(key, 0) + weight
            else:
                code_edges[key] = code_edges.get(key, 0) + weight
        if code_edges:
            layers["code_review"] = code_edges
            print(f"  Code review layer: {len(code_edges)} edges")
        if jira_edges:
            layers["jira"] = jira_edges
            print(f"  Jira layer: {len(jira_edges)} edges")
        if not code_edges and not jira_edges and uni_edges:
            all_edges = {}
            for e in uni_edges:
                src = (e.get("from") or "").lower().strip()
                tgt = (e.get("to") or "").lower().strip()
                if src and tgt:
                    key = tuple(sorted([src, tgt]))
                    all_edges[key] = all_edges.get(key, 0) + e.get("weight", 1)
            layers["code_and_work"] = all_edges
            print(f"  Code+work layer (combined): {len(all_edges)} edges")

    all_pairs = set()
    for layer_edges in layers.values():
        all_pairs.update(layer_edges.keys())
    print(f"\n  Total unique pairs across all layers: {len(all_pairs)}")

    unified = []
    for pair in all_pairs:
        entry = {"source": pair[0], "target": pair[1], "layers": {}}
        for layer_name, layer_edges in layers.items():
            if pair in layer_edges:
                entry["layers"][layer_name] = layer_edges[pair]
        entry["layer_count"] = len(entry["layers"])
        entry["total_strength"] = sum(entry["layers"].values())
        unified.append(entry)

    unified.sort(key=lambda x: -x["layer_count"])

    multi_layer = [e for e in unified if e["layer_count"] >= 2]
    single_layer = [e for e in unified if e["layer_count"] == 1]

    divergences = []
    for e in unified:
        present = set(e["layers"].keys())
        if "meeting" in present and "code_review" not in present and "jira" not in present:
            divergences.append({**e, "finding": "Meets frequently but no code/work interaction -- meetings without output?"})
        elif "code_review" in present and "meeting" not in present:
            divergences.append({**e, "finding": "Code collaboration without meetings -- async-heavy or timezone split?"})
        elif e["layer_count"] >= 3:
            divergences.append({**e, "finding": f"Strong multi-layer connection ({e['layer_count']} layers) -- key organizational connector"})

    save(INV / "unified_interaction_network.json", {
        "total_pairs": len(unified),
        "multi_layer_pairs": len(multi_layer),
        "single_layer_pairs": len(single_layer),
        "layers_available": list(layers.keys()),
        "edges": unified[:3000],
    })

    save(INV / "network_divergence_findings.json", {
        "total_findings": len(divergences),
        "findings": divergences[:500],
    })

    print(f"  Multi-layer connections: {len(multi_layer)}")
    print(f"  Single-layer connections: {len(single_layer)}")
    print(f"  Divergence findings: {len(divergences)}")

    layer_counts = defaultdict(int)
    for e in unified:
        for l in e["layers"]:
            layer_counts[l] += 1
    for l, c in sorted(layer_counts.items(), key=lambda x: -x[1]):
        print(f"    {l}: {c} edges")


# ─── MAIN ─────────────────────────────────────────────────────

COMMANDS = {
    "directory": cmd_directory,
    "meetings": cmd_meetings,
    "people": cmd_people,
    "teams": cmd_teams,
    "network": cmd_network,
}

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in [*COMMANDS.keys(), "all"]:
        print(f"Usage: {sys.argv[0]} <{'|'.join([*COMMANDS.keys(), 'all'])}>")
        sys.exit(1)

    cmd = sys.argv[1]
    token = get_app_token()
    print(f"App token acquired")

    if cmd == "all":
        for name, func in COMMANDS.items():
            func(token)
    else:
        COMMANDS[cmd](token)

    print(f"\n{'='*60}")
    print("COMPLETE")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
