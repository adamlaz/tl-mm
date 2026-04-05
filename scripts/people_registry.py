#!/usr/bin/env python3
"""People Registry: orchestrate all collectors, merge via identity resolution,
produce people_master.json and match_report.json.

Usage:
    python3 scripts/people_registry.py [--skip-api]

    --skip-api  Use cached collector data only (no API calls)
"""

import sys
import os
import json
import time
from collections import defaultdict
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from collectors import PersonRecord, KNOWN_BOTS

try:
    from rapidfuzz import fuzz, process as rfprocess
except ImportError:
    fuzz = None

OUTPUT_DIR = "inventory/users"
SOURCES_DIR = "inventory/users/sources"
PROFILES_DIR = "inventory/users/profiles"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(SOURCES_DIR, exist_ok=True)
os.makedirs(PROFILES_DIR, exist_ok=True)


# ─── Name Normalization ─────────────────────────────────────────────────

def normalize_name(name: str) -> str:
    """Lowercase, strip extra whitespace, remove trailing dots/parens."""
    n = name.strip().lower()
    n = " ".join(n.split())
    n = n.rstrip(".")
    return n


def name_tokens(name: str) -> set:
    """Extract first/last name tokens, ignoring middle initials."""
    parts = normalize_name(name).split()
    if len(parts) >= 2:
        return {parts[0], parts[-1]}
    return set(parts)


MANUAL_OVERRIDES = {
    "dulanjan w.": "dulanjan wengappuliarachchi",
    "dulanjan w": "dulanjan wengappuliarachchi",
    "miru s.": "mirunaaliny somasunthara iyer",
    "miru s": "mirunaaliny somasunthara iyer",
    "wing hung peter wu": "peter wu",
    "paul.roberts": "paul robert",
    "gayan k": "gayan karunarathna",
    "susampath m": "susampath madarasinghe",
    "danika m (sl)": "danika m",
    "altaaf a (sl)": "altaaf a",
    "kanchana a (sl)": "kanchana a",
    "matias riglos": "matias lopez riglos",
    "dhanushka_k": "dhanushka k",
    "siva.golla": "siva ganesh",
}


def resolve_name(name: str) -> str:
    """Resolve known aliases to canonical names."""
    n = normalize_name(name)
    return MANUAL_OVERRIDES.get(n, n)


# ─── Identity Resolution ────────────────────────────────────────────────

class IdentityResolver:
    def __init__(self):
        self.people = {}
        self.match_log = []

    def _key(self, name: str) -> str:
        return resolve_name(name)

    def _find_match(self, name: str, account_id: str = None, email: str = None):
        """Find existing person by account_id, email, exact name, or fuzzy match."""
        key = self._key(name)

        if account_id:
            for pid, person in self.people.items():
                for sid, sdata in person.get("sources", {}).items():
                    if sdata.get("account_id") == account_id:
                        return pid, "account_id", 1.0

        if email:
            email_lower = email.lower()
            for pid, person in self.people.items():
                p_email = person.get("email") or ""
                if p_email and p_email.lower() == email_lower:
                    return pid, "email", 1.0
                for sid, sdata in person.get("sources", {}).items():
                    s_email = sdata.get("email") or ""
                    if s_email and s_email.lower() == email_lower:
                        return pid, "email", 1.0

        if key in self.people:
            return key, "exact", 1.0

        for existing_key, person in self.people.items():
            all_names = [existing_key] + [resolve_name(a) for a in person.get("aliases", [])]
            for alias in all_names:
                if key == alias:
                    return existing_key, "alias", 0.95
                if name_tokens(key) == name_tokens(alias) and len(name_tokens(key)) >= 2:
                    return existing_key, "token", 0.9

        if fuzz and len(key) > 3:
            candidates = list(self.people.keys())
            if candidates:
                match = rfprocess.extractOne(key, candidates, scorer=fuzz.ratio, score_cutoff=82)
                if match:
                    return match[0], "fuzzy", match[1] / 100.0

        return None, "unmatched", 0.0

    def add_person(self, record: PersonRecord):
        """Add a PersonRecord, merging with existing if matched."""
        key = self._key(record.canonical_name)
        is_bot = record.canonical_name in KNOWN_BOTS or key in {b.lower() for b in KNOWN_BOTS}

        match_key, match_type, confidence = self._find_match(
            record.canonical_name,
            account_id=record.account_id,
            email=record.email,
        )

        self.match_log.append({
            "name": record.canonical_name,
            "source": record.source,
            "match_type": match_type,
            "matched_to": match_key,
            "confidence": confidence,
        })

        if match_key and match_type != "unmatched":
            person = self.people[match_key]
        else:
            match_key = key
            person = {
                "id": key.replace(" ", "-").replace(".", "-"),
                "canonical_name": record.canonical_name,
                "aliases": [],
                "email": None,
                "title": None,
                "team": None,
                "manager": None,
                "division": None,
                "executive": None,
                "geography": None,
                "status": "bot" if is_bot else "active",
                "match_confidence": confidence,
                "sources": {},
            }
            self.people[match_key] = person

        if record.canonical_name != person["canonical_name"]:
            if record.canonical_name not in person["aliases"]:
                person["aliases"].append(record.canonical_name)

        for alias in record.aliases:
            if alias not in person["aliases"] and alias != person["canonical_name"]:
                person["aliases"].append(alias)

        if record.email and not person.get("email"):
            person["email"] = record.email

        if record.source == "org_chart":
            person["title"] = record.title or person.get("title")
            person["team"] = record.team or person.get("team")
            person["manager"] = record.manager or person.get("manager")
            person["division"] = record.division or person.get("division")
            person["executive"] = record.executive or person.get("executive")
            person["geography"] = record.geography or person.get("geography")
            if record.status and record.status != "active":
                person["status"] = record.status
        else:
            if not person.get("title") and record.title:
                person["title"] = record.title
            if not person.get("team") and record.team:
                person["team"] = record.team
            if not person.get("geography") and record.geography:
                person["geography"] = record.geography

        person["sources"][record.source] = {
            "account_id": record.account_id,
            "email": record.email,
            **record.metadata,
        }

        if is_bot:
            person["status"] = "bot"

    def get_all(self):
        return dict(self.people)

    def get_match_report(self):
        report = {
            "total_records_processed": len(self.match_log),
            "match_types": defaultdict(int),
            "unmatched": [],
            "ambiguous": [],
            "confident": [],
        }
        for entry in self.match_log:
            report["match_types"][entry["match_type"]] += 1
            if entry["match_type"] == "unmatched":
                report["unmatched"].append(entry)
            elif entry["confidence"] < 0.9:
                report["ambiguous"].append(entry)
            else:
                report["confident"].append(entry)

        report["match_types"] = dict(report["match_types"])
        return report


# ─── Collector Runner ────────────────────────────────────────────────────

def run_collector(name, collect_fn, skip_api=False):
    """Run a collector and cache results."""
    cache_file = os.path.join(SOURCES_DIR, f"{name}_cache.json")

    if skip_api and os.path.exists(cache_file):
        print(f"  {name}: loading from cache")
        with open(cache_file) as f:
            records_data = json.load(f)
        return [PersonRecord(**r) for r in records_data]

    print(f"  {name}: collecting...", flush=True)
    try:
        records = collect_fn()
        records_data = []
        for r in records:
            records_data.append({
                "source": r.source,
                "canonical_name": r.canonical_name,
                "email": r.email,
                "account_id": r.account_id,
                "title": r.title,
                "team": r.team,
                "manager": r.manager,
                "division": r.division,
                "executive": r.executive,
                "geography": r.geography,
                "status": r.status,
                "aliases": r.aliases,
                "metadata": r.metadata,
            })
        with open(cache_file, "w") as f:
            json.dump(records_data, f, indent=2, default=str)
        print(f"  {name}: {len(records)} records (cached)")
        return records
    except Exception as e:
        print(f"  {name}: ERROR - {e}")
        if os.path.exists(cache_file):
            print(f"  {name}: falling back to cache")
            with open(cache_file) as f:
                records_data = json.load(f)
            return [PersonRecord(**r) for r in records_data]
        return []


# ─── Enrichment ──────────────────────────────────────────────────────────

def enrich(people: dict):
    """Post-merge enrichment: infer team, geography, status for unresolved people."""
    from collectors.org_chart import get_team_for_project, get_division_for_workspace

    for key, person in people.items():
        jira = person["sources"].get("jira", {})
        bb = person["sources"].get("bitbucket", {})

        if not person.get("team") and jira.get("projects"):
            projects = jira["projects"]
            team_votes = defaultdict(int)
            for proj in projects:
                t = get_team_for_project(proj)
                if t != "Unknown":
                    team_votes[t] += 1
            if team_votes:
                person["team"] = max(team_votes, key=team_votes.get)

        if not person.get("division") and bb.get("review_cluster"):
            cluster = bb["review_cluster"]
            person["division"] = get_division_for_workspace(cluster)

        if not person.get("geography"):
            tz = jira.get("timeZone", "")
            if tz:
                if "Asia/Colombo" in tz or "Asia/Kolkata" in tz:
                    person["geography"] = "SL"
                elif "America/" in tz or "US/" in tz:
                    person["geography"] = "US"

            if not person.get("geography") and bb.get("review_cluster"):
                cluster = bb["review_cluster"]
                if cluster == "syscolabs":
                    person["geography"] = "SL"
                elif cluster == "madpayments":
                    person["geography"] = "SL"

        systems_active = 0
        total_activity = 0
        if jira:
            created = jira.get("issues_created_90d", 0) or 0
            resolved = jira.get("issues_resolved_90d", 0) or 0
            if created > 0 or resolved > 0:
                systems_active += 1
                total_activity += created + resolved
        if bb:
            prs_a = bb.get("prs_authored", 0) or 0
            prs_r = bb.get("prs_reviewed", 0) or 0
            if prs_a > 0 or prs_r > 0:
                systems_active += 1
                total_activity += prs_a + prs_r
        conf = person["sources"].get("confluence", {})
        if conf:
            pages = conf.get("pages_90d", 0) or 0
            if pages > 0:
                systems_active += 1
                total_activity += pages

        person["activity"] = {
            "systems_active_90d": systems_active,
            "total_activity_90d": total_activity,
            "level": (
                "high" if total_activity > 50
                else "medium" if total_activity > 10
                else "low" if total_activity > 0
                else "inactive"
            ),
        }

        if person["status"] not in ("departed", "consulting", "bot"):
            if person.get("sources", {}).get("org_chart"):
                if total_activity == 0:
                    person["status"] = "quiet"
                else:
                    person["status"] = "active"
            else:
                if total_activity == 0:
                    person["status"] = "inactive"
                else:
                    person["status"] = "active"

    return people


# ─── Profile Generation ─────────────────────────────────────────────────

def generate_profiles(people: dict):
    """Write per-person JSON profiles to profiles/ directory."""
    for key, person in people.items():
        slug = person.get("id", key.replace(" ", "-"))
        profile = {
            "name": person["canonical_name"],
            "id": slug,
            "title": person.get("title"),
            "team": person.get("team"),
            "manager": person.get("manager"),
            "division": person.get("division"),
            "executive": person.get("executive"),
            "geography": person.get("geography"),
            "status": person.get("status"),
            "email": person.get("email"),
            "aliases": person.get("aliases", []),
            "activity": person.get("activity", {}),
            "systems": list(person.get("sources", {}).keys()),
            "sources": person.get("sources", {}),
        }
        filepath = os.path.join(PROFILES_DIR, f"{slug}.json")
        with open(filepath, "w") as f:
            json.dump(profile, f, indent=2, default=str)

    print(f"  {len(people)} profiles written to {PROFILES_DIR}/")


# ─── CSV Export ──────────────────────────────────────────────────────────

def export_csv(people: dict):
    """Export flat CSV for the minisite and analysis."""
    import csv
    filepath = "analysis/people_directory.csv"
    os.makedirs("analysis", exist_ok=True)

    rows = []
    for key, person in sorted(people.items()):
        jira = person.get("sources", {}).get("jira", {})
        bb = person.get("sources", {}).get("bitbucket", {})
        conf = person.get("sources", {}).get("confluence", {})
        activity = person.get("activity", {})

        rows.append({
            "id": person.get("id", key.replace(" ", "-")),
            "display_name": person["canonical_name"],
            "title": person.get("title", ""),
            "team": person.get("team", ""),
            "manager": person.get("manager", ""),
            "division": person.get("division", ""),
            "geography": person.get("geography", ""),
            "status": person.get("status", ""),
            "email": person.get("email", ""),
            "activity_level": activity.get("level", ""),
            "systems_active_90d": activity.get("systems_active_90d", 0),
            "total_activity_90d": activity.get("total_activity_90d", 0),
            "systems": ",".join(person.get("sources", {}).keys()),
            "bb_workspaces": ",".join(bb.get("workspaces", [])),
            "prs_authored": bb.get("prs_authored", 0),
            "prs_reviewed": bb.get("prs_reviewed", 0),
            "jira_created_90d": jira.get("issues_created_90d", 0),
            "jira_resolved_90d": jira.get("issues_resolved_90d", 0),
            "jira_open_assigned": jira.get("open_assigned", 0),
            "jira_bugs_90d": jira.get("bugs_created_90d", 0),
            "jira_projects": ",".join(jira.get("projects", [])),
            "jira_role": jira.get("role_classification", ""),
            "confluence_pages_total": conf.get("pages_total", 0),
            "confluence_pages_90d": conf.get("pages_90d", 0),
            "aliases": "; ".join(person.get("aliases", [])),
        })

    if rows:
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        print(f"  CSV exported: {filepath} ({len(rows)} rows)")


# ─── Main ────────────────────────────────────────────────────────────────

def main():
    skip_api = "--skip-api" in sys.argv

    print("=" * 60)
    print("PEOPLE REGISTRY — Cross-System Identity Resolution")
    print("=" * 60)
    print()

    resolver = IdentityResolver()

    # Phase 1: Org chart first (highest authority for names/titles/teams)
    print("Phase 1: Collecting from all sources...")
    from collectors.org_chart import collect as org_collect
    org_records = run_collector("org_chart", org_collect)
    for r in org_records:
        resolver.add_person(r)
    print(f"  -> Registry: {len(resolver.people)} people after org chart")

    # Phase 2: System collectors
    if not skip_api:
        from collectors.jira_collector import collect as jira_collect
        jira_records = run_collector("jira", jira_collect)
        for r in jira_records:
            resolver.add_person(r)
        print(f"  -> Registry: {len(resolver.people)} people after Jira")

        from collectors.bitbucket_collector import collect as bb_collect
        bb_records = run_collector("bitbucket", bb_collect)
        for r in bb_records:
            resolver.add_person(r)
        print(f"  -> Registry: {len(resolver.people)} people after Bitbucket")

        from collectors.confluence_collector import collect as conf_collect
        conf_records = run_collector("confluence", conf_collect)
        for r in conf_records:
            resolver.add_person(r)
        print(f"  -> Registry: {len(resolver.people)} people after Confluence")

        from collectors.aws_collector import collect as aws_collect
        aws_records = run_collector("aws", aws_collect)
        for r in aws_records:
            resolver.add_person(r)
        print(f"  -> Registry: {len(resolver.people)} people after AWS")
    else:
        for name in ["jira", "bitbucket", "confluence", "aws"]:
            cache = os.path.join(SOURCES_DIR, f"{name}_cache.json")
            if os.path.exists(cache):
                with open(cache) as f:
                    records = [PersonRecord(**r) for r in json.load(f)]
                for r in records:
                    resolver.add_person(r)
                print(f"  -> {name} (cache): {len(records)} records")

    all_people = resolver.get_all()
    print(f"\n  TOTAL UNIQUE PEOPLE: {len(all_people)}")

    # Phase 3: Enrichment
    print("\nPhase 2: Enrichment...")
    all_people = enrich(all_people)

    status_counts = defaultdict(int)
    for p in all_people.values():
        status_counts[p.get("status", "unknown")] += 1
    print(f"  Status: {dict(status_counts)}")

    geo_counts = defaultdict(int)
    for p in all_people.values():
        geo_counts[p.get("geography") or "unknown"] += 1
    print(f"  Geography: {dict(geo_counts)}")

    team_counts = defaultdict(int)
    for p in all_people.values():
        team_counts[p.get("team") or "No team"] += 1
    top_teams = sorted(team_counts.items(), key=lambda x: -x[1])[:10]
    print(f"  Top teams: {dict(top_teams)}")

    activity = defaultdict(int)
    for p in all_people.values():
        activity[p.get("activity", {}).get("level", "unknown")] += 1
    print(f"  Activity: {dict(activity)}")

    # Phase 4: Output
    print("\nPhase 3: Output...")
    with open(os.path.join(OUTPUT_DIR, "people_master.json"), "w") as f:
        json.dump(all_people, f, indent=2, default=str)
    print(f"  Master registry: {OUTPUT_DIR}/people_master.json")

    match_report = resolver.get_match_report()
    with open(os.path.join(OUTPUT_DIR, "match_report.json"), "w") as f:
        json.dump(match_report, f, indent=2, default=str)
    print(f"  Match report: {OUTPUT_DIR}/match_report.json")
    print(f"    Matches: {match_report['match_types']}")
    print(f"    Ambiguous: {len(match_report['ambiguous'])}")
    print(f"    Unmatched: {len(match_report['unmatched'])}")

    generate_profiles(all_people)
    export_csv(all_people)

    print(f"\n{'='*60}")
    print(f"DONE. {len(all_people)} people in registry.")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
