#!/usr/bin/env python3
"""Authenticate to Microsoft Graph API and test access.

Tries progressively lower permission scopes:
  1. User.Read only (no admin consent needed) + People API + GAL search
  2. Exchange Web Services / Outlook contacts
  3. Manual fallback instructions
"""

import sys
import json
import msal
import requests

CLIENT_ID = "14d82eec-204b-4c2f-b7e8-296a70dab67e"
AUTHORITY = "https://login.microsoftonline.com/organizations"

TOKEN_FILE = ".m365_token.json"

SCOPE_TIERS = [
    {
        "name": "User.Read + People + Contacts",
        "scopes": ["User.Read", "People.Read", "Contacts.Read"],
        "description": "Basic profile + People API (no admin consent required)",
    },
    {
        "name": "User.Read only",
        "scopes": ["User.Read"],
        "description": "Minimal -- just your own profile",
    },
]


def try_auth(app, scopes, tier_name):
    """Try interactive browser auth with given scopes."""
    print(f"  Trying: {tier_name}")
    print(f"  Scopes: {', '.join(scopes)}")
    print(f"  Opening browser...")
    sys.stdout.flush()
    try:
        result = app.acquire_token_interactive(scopes=scopes)
        if result and "access_token" in result:
            print(f"  SUCCESS!")
            return result
        err = result.get("error", "unknown") if result else "no result"
        desc = result.get("error_description", "")[:120] if result else ""
        print(f"  Failed: {err} - {desc}")
        return None
    except Exception as e:
        print(f"  Exception: {e}")
        return None


def test_endpoints(token):
    """Test what we can access with the granted token."""
    headers = {"Authorization": f"Bearer {token}"}
    results = {}

    print("\nTesting accessible endpoints:\n")

    # /me -- own profile
    r = requests.get("https://graph.microsoft.com/v1.0/me?$select=displayName,mail,jobTitle,department,officeLocation,userPrincipalName", headers=headers)
    print(f"  /me                  : {r.status_code}", end="")
    if r.status_code == 200:
        d = r.json()
        print(f"  -> {d.get('displayName')} ({d.get('mail')})")
        results["me"] = d
    else:
        print()

    # /me/people -- People API (up to 1000 relevant people, no admin consent)
    r = requests.get("https://graph.microsoft.com/v1.0/me/people?$top=999", headers=headers)
    print(f"  /me/people           : {r.status_code}", end="")
    if r.status_code == 200:
        ppl = r.json().get("value", [])
        print(f"  -> {len(ppl)} people")
        results["people"] = ppl
    else:
        print(f"  -> {r.text[:100]}")

    # /me/contacts -- Outlook contacts
    r = requests.get("https://graph.microsoft.com/v1.0/me/contacts?$top=999", headers=headers)
    print(f"  /me/contacts         : {r.status_code}", end="")
    if r.status_code == 200:
        contacts = r.json().get("value", [])
        print(f"  -> {len(contacts)} contacts")
        results["contacts"] = contacts
    else:
        print(f"  -> {r.text[:100]}")

    # /users -- directory enumeration (probably needs admin consent)
    r = requests.get("https://graph.microsoft.com/v1.0/users?$top=5&$select=displayName,mail,jobTitle,department", headers=headers)
    print(f"  /users               : {r.status_code}", end="")
    if r.status_code == 200:
        u = r.json().get("value", [])
        print(f"  -> FULL DIRECTORY ACCESS ({len(u)} sample)")
        results["users_accessible"] = True
    else:
        print(f"  -> blocked (expected)")
        results["users_accessible"] = False

    # /me/joinedTeams -- Teams membership
    r = requests.get("https://graph.microsoft.com/v1.0/me/joinedTeams", headers=headers)
    print(f"  /me/joinedTeams      : {r.status_code}", end="")
    if r.status_code == 200:
        teams = r.json().get("value", [])
        print(f"  -> {len(teams)} teams")
        results["teams"] = teams
    else:
        print(f"  -> {r.text[:100]}")

    # /me/transitiveMemberOf -- groups/teams the user belongs to
    r = requests.get("https://graph.microsoft.com/v1.0/me/transitiveMemberOf?$top=999", headers=headers)
    print(f"  /me/transitiveMemberOf: {r.status_code}", end="")
    if r.status_code == 200:
        groups = r.json().get("value", [])
        print(f"  -> {len(groups)} groups/teams")
        results["groups"] = groups
    else:
        print()

    # GAL search via /me/people with search query (finds people in the directory)
    r = requests.get("https://graph.microsoft.com/v1.0/me/people?$search=%22%22&$top=999&$select=displayName,scoredEmailAddresses,jobTitle,department,officeLocation", headers=headers)
    print(f"  /me/people (search)  : {r.status_code}", end="")
    if r.status_code == 200:
        searched = r.json().get("value", [])
        print(f"  -> {len(searched)} people via search")
        results["people_search"] = searched
    else:
        print()

    return results


def main():
    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)

    print("=" * 60)
    print("MICROSOFT 365 AUTHENTICATION")
    print("  (Using user-consent-only scopes)")
    print("=" * 60)
    print()

    result = None
    for tier in SCOPE_TIERS:
        result = try_auth(app, tier["scopes"], tier["name"])
        if result:
            break
        print()

    if not result:
        print()
        print("All auth attempts blocked by Conditional Access Policy.")
        print("The tenant requires registered/compliant devices for all Graph API access.")
        sys.exit(1)

    token = result["access_token"]
    granted = result.get("scope", "")

    with open(TOKEN_FILE, "w") as f:
        json.dump({"access_token": token, "scope": granted}, f, indent=2)

    print(f"\nScopes granted: {granted}\n")

    endpoints = test_endpoints(token)

    # Save whatever we got
    import os
    os.makedirs("inventory/users/sources", exist_ok=True)

    if endpoints.get("people"):
        with open("inventory/users/sources/m365_people.json", "w") as f:
            json.dump(endpoints["people"], f, indent=2)
        print(f"\nSaved {len(endpoints['people'])} people to inventory/users/sources/m365_people.json")

    if endpoints.get("people_search"):
        with open("inventory/users/sources/m365_people_search.json", "w") as f:
            json.dump(endpoints["people_search"], f, indent=2)
        print(f"Saved {len(endpoints['people_search'])} people (search) to inventory/users/sources/m365_people_search.json")

    if endpoints.get("contacts"):
        with open("inventory/users/sources/m365_contacts.json", "w") as f:
            json.dump(endpoints["contacts"], f, indent=2)
        print(f"Saved {len(endpoints['contacts'])} contacts to inventory/users/sources/m365_contacts.json")

    if endpoints.get("teams"):
        with open("inventory/users/sources/m365_teams.json", "w") as f:
            json.dump(endpoints["teams"], f, indent=2)
        print(f"Saved {len(endpoints['teams'])} teams to inventory/users/sources/m365_teams.json")

    if endpoints.get("groups"):
        with open("inventory/users/sources/m365_groups.json", "w") as f:
            json.dump(endpoints["groups"], f, indent=2)
        print(f"Saved {len(endpoints['groups'])} groups to inventory/users/sources/m365_groups.json")

    if endpoints.get("me"):
        with open("inventory/users/sources/m365_me.json", "w") as f:
            json.dump(endpoints["me"], f, indent=2)

    total_people = len(endpoints.get("people", [])) + len(endpoints.get("people_search", []))
    print(f"\n{'='*60}")
    print(f"TOTAL PEOPLE DISCOVERED: {total_people}")
    if endpoints.get("users_accessible"):
        print("Full directory access available!")
    else:
        print("Full directory (/users) blocked -- using People API data.")
        print("This gives us names + emails for people relevant to your account.")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
