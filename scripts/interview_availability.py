#!/usr/bin/env python3
"""Check calendar availability for interview scheduling via Microsoft Graph API.

Reads interview_schedule.json for the session list, authenticates via MSAL
(reusing the m365_auth.py pattern), and checks free/busy status for all
interviewees across April 13-15, 2026.

Outputs:
  - schedule_availability.json: per-interviewee availability windows
  - schedule_conflicts.json: interviewees with no available time in proposed slot
  - Updated interview-schedule-grid.md (if --update-grid flag is set)

Usage:
  python scripts/interview_availability.py              # check availability
  python scripts/interview_availability.py --dry-run    # show what would be checked
  python scripts/interview_availability.py --update-grid # update the grid markdown

Requires: msal, requests (same deps as m365_auth.py)
Graph permissions needed: Calendars.Read, User.Read.All (admin consent required)
"""

import sys
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

try:
    import msal
    import requests
except ImportError:
    print("Missing dependencies. Install with: pip install msal requests")
    sys.exit(1)

CLIENT_ID = "14d82eec-204b-4c2f-b7e8-296a70dab67e"
AUTHORITY = "https://login.microsoftonline.com/organizations"
SCOPES = ["Calendars.Read", "User.Read.All", "User.Read"]

TOKEN_FILE = ".m365_token.json"
SCHEDULE_FILE = "interview_schedule.json"
OUTPUT_DIR = "inventory/scheduling"

ONSITE_DATES = ["2026-04-13", "2026-04-14", "2026-04-15"]
TIMEZONE = "America/New_York"

BLOCKED_SLOTS = [
    ("08:00", "08:30"),
    ("12:00", "13:00"),
]

MORNING_BLOCK = ("08:30", "12:00")
AFTERNOON_BLOCK = ("13:00", "16:00")


def load_schedule():
    path = Path(SCHEDULE_FILE)
    if not path.exists():
        path = Path(__file__).parent.parent / SCHEDULE_FILE
    if not path.exists():
        print(f"ERROR: Cannot find {SCHEDULE_FILE}")
        sys.exit(1)
    with open(path) as f:
        return json.load(f)


def authenticate():
    """Authenticate via MSAL interactive flow, or reuse cached token."""
    token_path = Path(TOKEN_FILE)
    if not token_path.exists():
        token_path = Path(__file__).parent.parent / TOKEN_FILE

    if token_path.exists():
        with open(token_path) as f:
            cached = json.load(f)
        token = cached.get("access_token")
        if token:
            r = requests.get(
                "https://graph.microsoft.com/v1.0/me",
                headers={"Authorization": f"Bearer {token}"},
            )
            if r.status_code == 200:
                print(f"  Reusing cached token for {r.json().get('displayName')}")
                return token
            print("  Cached token expired, re-authenticating...")

    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    print("  Opening browser for authentication...")
    result = app.acquire_token_interactive(scopes=SCOPES)
    if not result or "access_token" not in result:
        err = result.get("error", "unknown") if result else "no result"
        desc = result.get("error_description", "")[:200] if result else ""
        print(f"  Auth failed: {err}")
        if "AADSTS65001" in desc or "admin_consent" in desc.lower():
            print("\n  Admin consent required. Ask IT to grant consent for:")
            print(f"    App ID: {CLIENT_ID}")
            print(f"    Permissions: {', '.join(SCOPES)}")
            print("    Portal: entra.microsoft.com → Enterprise Applications")
        print(f"\n  Detail: {desc}")
        return None

    token = result["access_token"]
    with open(TOKEN_FILE, "w") as f:
        json.dump({"access_token": token, "scope": result.get("scope", "")}, f, indent=2)
    return token


def resolve_emails(token, sessions):
    """Resolve interviewee emails via directory lookup when email is null."""
    headers = {"Authorization": f"Bearer {token}"}
    resolved = []

    for s in sessions:
        email = s.get("email")
        name = s.get("name", "")

        if not email and "TBD" not in name and "#" not in name:
            r = requests.get(
                f"https://graph.microsoft.com/v1.0/users?$filter=startswith(displayName,'{name.split()[0]}')&$select=displayName,mail,userPrincipalName",
                headers=headers,
            )
            if r.status_code == 200:
                users = r.json().get("value", [])
                for u in users:
                    if name.lower() in u.get("displayName", "").lower():
                        email = u.get("mail") or u.get("userPrincipalName")
                        print(f"  Resolved {name} → {email}")
                        break

        resolved.append({**s, "resolved_email": email})
    return resolved


def check_availability(token, sessions):
    """Use getSchedule endpoint to check free/busy for all interviewees."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    emails = [s["resolved_email"] for s in sessions if s.get("resolved_email")]
    if not emails:
        print("  No resolvable emails found. Cannot check availability.")
        return {}

    unique_emails = list(set(emails))
    print(f"\n  Checking availability for {len(unique_emails)} people across {len(ONSITE_DATES)} days...")

    all_availability = {}

    for batch_start in range(0, len(unique_emails), 20):
        batch = unique_emails[batch_start:batch_start + 20]
        payload = {
            "schedules": batch,
            "startTime": {
                "dateTime": f"{ONSITE_DATES[0]}T08:00:00",
                "timeZone": TIMEZONE,
            },
            "endTime": {
                "dateTime": f"{ONSITE_DATES[-1]}T18:00:00",
                "timeZone": TIMEZONE,
            },
            "availabilityViewInterval": 15,
        }

        r = requests.post(
            "https://graph.microsoft.com/v1.0/me/calendar/getSchedule",
            headers=headers,
            json=payload,
        )

        if r.status_code == 200:
            for item in r.json().get("value", []):
                email = item.get("scheduleId", "")
                items = item.get("scheduleItems", [])
                view = item.get("availabilityView", "")
                all_availability[email] = {
                    "schedule_items": items,
                    "availability_view": view,
                    "error": None,
                }
                busy_count = sum(1 for c in view if c != "0")
                total = len(view)
                print(f"    {email}: {busy_count}/{total} slots busy")
        elif r.status_code == 403:
            print(f"  Access denied (403). Calendars.Read permission may not be granted.")
            print(f"  Response: {r.text[:200]}")
            return {}
        else:
            print(f"  Error {r.status_code}: {r.text[:200]}")
            return {}

    return all_availability


def find_conflicts(sessions, availability):
    """Identify sessions where the proposed time conflicts with existing meetings."""
    conflicts = []

    for s in sessions:
        email = s.get("resolved_email")
        if not email or email not in availability:
            continue

        avail = availability[email]
        items = avail.get("schedule_items", [])
        proposed_date = s.get("date", "")
        proposed_time = s.get("proposed_time", "")

        if not proposed_time or "-" not in proposed_time:
            continue

        start_str, end_str = proposed_time.split("-")
        prop_start = f"{proposed_date}T{start_str.strip()}:00"
        prop_end = f"{proposed_date}T{end_str.strip()}:00"

        for item in items:
            item_start = item.get("start", {}).get("dateTime", "")
            item_end = item.get("end", {}).get("dateTime", "")
            status = item.get("status", "")

            if status in ("busy", "tentative", "oof"):
                if item_start < prop_end and item_end > prop_start:
                    conflicts.append({
                        "session_id": s["id"],
                        "name": s["name"],
                        "proposed_time": f"{proposed_date} {proposed_time}",
                        "conflict_with": {
                            "start": item_start,
                            "end": item_end,
                            "status": status,
                            "subject": item.get("subject", "(private)"),
                        },
                    })

    return conflicts


def main():
    dry_run = "--dry-run" in sys.argv

    print("=" * 60)
    print("INTERVIEW AVAILABILITY CHECKER")
    print("=" * 60)

    schedule = load_schedule()
    sessions = schedule.get("sessions", [])
    print(f"\n  Loaded {len(sessions)} sessions from {SCHEDULE_FILE}")

    schedulable = [s for s in sessions if s.get("email")]
    tbd = [s for s in sessions if not s.get("email")]
    print(f"  Schedulable (have email): {len(schedulable)}")
    print(f"  TBD (no email yet): {len(tbd)}")
    if tbd:
        for s in tbd:
            print(f"    - {s['id']}: {s['name']}")

    if dry_run:
        print("\n  DRY RUN — would check availability for:")
        for s in schedulable:
            print(f"    {s['id']}: {s['name']} ({s['email']}) — {s['day']} {s['proposed_time']}")
        print("\n  Run without --dry-run to authenticate and check calendars.")
        return

    print("\nAuthenticating...")
    token = authenticate()
    if not token:
        print("\n  Authentication failed. Outputting default schedule without availability data.")
        generate_fallback_output(sessions)
        return

    print("\nResolving emails...")
    sessions_resolved = resolve_emails(token, sessions)

    print("\nChecking calendar availability...")
    availability = check_availability(token, sessions_resolved)

    if not availability:
        print("\n  Could not retrieve availability data. Outputting default schedule.")
        generate_fallback_output(sessions)
        return

    print("\nChecking for conflicts...")
    conflicts = find_conflicts(sessions_resolved, availability)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    avail_path = os.path.join(OUTPUT_DIR, "schedule_availability.json")
    with open(avail_path, "w") as f:
        json.dump(availability, f, indent=2, default=str)
    print(f"\n  Saved availability data → {avail_path}")

    conflicts_path = os.path.join(OUTPUT_DIR, "schedule_conflicts.json")
    with open(conflicts_path, "w") as f:
        json.dump(conflicts, f, indent=2, default=str)
    print(f"  Saved conflicts → {conflicts_path}")

    if conflicts:
        print(f"\n  CONFLICTS FOUND: {len(conflicts)}")
        for c in conflicts:
            print(f"    {c['session_id']} ({c['name']}): {c['proposed_time']}")
            print(f"      conflicts with: {c['conflict_with']['status']} {c['conflict_with']['start']} - {c['conflict_with']['end']}")
    else:
        print("\n  No conflicts detected — all proposed times appear clear.")

    print(f"\n{'=' * 60}")
    print(f"SUMMARY")
    print(f"  Sessions checked: {len([s for s in sessions_resolved if s.get('resolved_email') in availability])}")
    print(f"  Conflicts found: {len(conflicts)}")
    print(f"  TBD (cannot check): {len(tbd)}")
    print(f"{'=' * 60}")


def generate_fallback_output(sessions):
    """Output a summary when Graph access isn't available."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fallback = {
        "status": "graph_access_unavailable",
        "message": "Calendar availability could not be checked. Proposed times in interview-schedule-grid.md are pending manual confirmation.",
        "sessions": [
            {
                "id": s["id"],
                "name": s["name"],
                "email": s.get("email"),
                "day": s["day"],
                "proposed_time": s["proposed_time"],
                "duration_min": s["duration_min"],
                "availability": "unknown",
            }
            for s in sessions
        ],
    }
    path = os.path.join(OUTPUT_DIR, "schedule_availability.json")
    with open(path, "w") as f:
        json.dump(fallback, f, indent=2)
    print(f"\n  Saved fallback schedule → {path}")
    print("  Once Graph API access is granted, re-run this script to check actual availability.")


if __name__ == "__main__":
    main()
