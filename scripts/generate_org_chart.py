#!/usr/bin/env python3
"""Generate a flat JSON array for d3-org-chart from org chart data.

Output: analysis/charts/org_chart_data.json
Format: [{id, parentId, name, role, level, headcount, division}, ...]
"""

import json
import os

ROOT = os.path.join(os.path.dirname(__file__), os.pardir)
CHARTS_DIR = os.path.join(ROOT, "analysis", "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

PEOPLE_MASTER = os.path.join(ROOT, "inventory", "users", "people_master.json")


def _slug(name: str) -> str:
    return name.lower().replace(" ", "-").replace(".", "")


def _load_people_master() -> dict:
    try:
        with open(PEOPLE_MASTER) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def build_org_data() -> list[dict]:
    """Build flat org chart data with parent references."""
    people_master = _load_people_master()

    def _lookup(name: str) -> dict:
        key = name.lower()
        return people_master.get(key, {})

    def _activity(pm: dict) -> str:
        return pm.get("activity", {}).get("level", "unknown")

    def _geo(pm: dict) -> str:
        return pm.get("geography", "")

    nodes: list[dict] = []

    def add(name, role, level, parent_id=None, headcount=None, division=""):
        nid = _slug(name)
        pm = _lookup(name)
        nodes.append({
            "id": nid,
            "parentId": parent_id,
            "name": name,
            "role": role,
            "level": level,
            "headcount": headcount,
            "division": division,
            "geography": _geo(pm),
            "activityLevel": _activity(pm),
        })
        return nid

    ceo = add("Don Salama", "Co-CEO", "ceo", division="Executive")

    # -- Chief of Staff (dotted line, still include in hierarchy) --
    add("Ana Chambers", "Chief of Staff, Strategic Programs", "staff", ceo, division="Executive")

    # -- Finance --
    cfo = add("Manuel Garcia", "Interim CFO", "csuite", ceo, headcount=3, division="Finance")
    add("Mark Do", "Ass't Controller", "staff", cfo, division="Finance")
    add("Zach Honnold", "RevOps", "staff", cfo, division="Finance")

    # -- Sales & Marketing --
    greg = add("Greg Schmitzer", "President, Sales & Marketing", "csuite", ceo, headcount=8, division="Sales & Marketing")
    add("Bobby Jaklitsch", "Field Sales", "staff", greg, headcount=4, division="Sales & Marketing")
    add("Peter Vu", "Inbound", "staff", greg, headcount=3, division="Sales & Marketing")
    add("Karen Licker", "Marketing", "staff", greg, headcount=1, division="Sales & Marketing")

    # -- Operations --
    coo = add("David Strainick", "COO", "csuite", ceo, headcount=22, division="Operations")
    add("Das DeSilva", "Onboarding", "staff", coo, headcount=10, division="Operations")
    add("Dir. Account Mgmt", "Account Management", "staff", coo, headcount=9, division="Operations")
    add("Rosen Georgiev", "IT Ops", "staff", coo, division="Operations")
    add("Chip O'Connell", "Onboarding Delivery", "staff", coo, headcount=3, division="Operations")

    # -- Digital / Engineering (CDO) --
    cdo = add("Chathura Ratnayake", "Chief Digital Officer", "csuite", ceo, headcount=100, division="Digital & Engineering")

    # Product & GTM
    dulanjan = add("Dulanjan W.", "VP Product & GTM", "l2", cdo, headcount=10, division="Product & GTM")
    add("PM Restaurant", "Miru S., Jake L., TBD", "subteam", dulanjan, division="Product & GTM")
    add("PM Payments/Ops/Eng", "Shavin P., Richard F., Thaddeus F.", "subteam", dulanjan, division="Product & GTM")
    add("Chris Gomersall", "Dir. Product Design", "subteam", dulanjan, division="Product & GTM")
    add("L&D", "Adriana Z., Ayodele L.", "subteam", dulanjan, division="Product & GTM")

    # Restaurant Technology
    randy = add("Randy Brown", "VP Eng, Restaurant Tech", "l2", cdo, headcount=10, division="Restaurant Technology")
    fe = add("Frontend", "Alexander Baine, Mgr", "subteam", randy, division="Restaurant Technology")
    be = add("Backend", "Kyle Budd, Mgr", "subteam", randy, division="Restaurant Technology")
    add("Cory Renard", "Staff Software Eng", "staff", fe, division="Restaurant Technology")
    add("Rob Quin", "Software Eng", "staff", fe, division="Restaurant Technology")
    add("Beau Bruderer", "Senior Software Eng", "staff", be, division="Restaurant Technology")
    add("Holly Bobal", "Senior Software Eng", "staff", be, division="Restaurant Technology")
    add("Siva Ganesh", "Software Eng", "staff", be, division="Restaurant Technology")
    add("Harrison Minchew", "Lead Software Eng", "staff", be, division="Restaurant Technology")
    add("Anderson Lavor", "Lead Software Eng", "staff", be, division="Restaurant Technology")

    # Enterprise Solutions
    add("Zubair Syed", "VP Eng, Enterprise Solutions", "l2", cdo, headcount=58, division="Enterprise Solutions")

    # Payments Engineering
    akshay = add("Akshay Bhasin", "VP Payments Engineering", "l2", cdo, headcount=20, division="Payments Engineering")
    add("Payments R&D", "Kevin Reyes, Dir.", "subteam", akshay, headcount=9, division="Payments Engineering")
    add("Restaurant QE", "Quality Engineering", "subteam", akshay, headcount=7, division="Payments Engineering")
    add("Biz Operations", "Andy Honnold, Sr Dir", "subteam", akshay, headcount=4, division="Payments Engineering")
    add("PCI/Compliance", "Freid, Maltes, Riglos, Keye", "subteam", akshay, division="Payments Engineering")

    # Program Management
    guilarte = add("Mark Guilarte", "VP Program Management", "l2", cdo, headcount=4, division="Program Management")
    add("Qaiser P.", "Sr PM — Restaurant", "staff", guilarte, division="Program Management")
    add("Vanessa S.", "PM — Payments", "staff", guilarte, division="Program Management")
    add("Ian B.", "Project Lead — AI", "staff", guilarte, division="Program Management")
    add("Debbie K.", "Sr PM — Ops Eng", "staff", guilarte, division="Program Management")

    # Customer Support
    add("Customer Support", "All levels", "staff", cdo, division="Customer Support")

    # -- Technology / AI --
    cto = add("Jack Kennedy", "CTO", "csuite", ceo, division="Technology & AI")
    add("Jeremy Diggins", "Dir. Enterprise Technology", "staff", cto, division="Technology & AI")

    # -- Human Resources --
    hr = add("Bailey Shatney", "VP of Human Resources", "csuite", ceo, division="Human Resources")
    add("Renee Pauley", "Recruiting", "staff", hr, division="Human Resources")

    return nodes


def main():
    print("=== Org Chart (d3-org-chart flat JSON) ===", flush=True)
    data = build_org_data()
    out_path = os.path.join(CHARTS_DIR, "org_chart_data.json")
    with open(out_path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  -> {out_path}  ({len(data)} nodes)")
    print("Done.", flush=True)


if __name__ == "__main__":
    main()
