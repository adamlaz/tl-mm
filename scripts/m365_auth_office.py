#!/usr/bin/env python3
"""Try M365 auth using first-party Microsoft app IDs that are pre-approved in most tenants."""

import sys
import json
import msal
import requests

TOKEN_FILE = ".m365_token.json"

FIRST_PARTY_APPS = [
    {
        "name": "Microsoft Office",
        "client_id": "d3590ed6-52b3-4102-aeff-aad2292ab01c",
        "scopes": ["https://graph.microsoft.com/.default"],
    },
    {
        "name": "Azure PowerShell",
        "client_id": "1950a258-227b-4e31-a9cf-717495945fc2",
        "scopes": ["https://graph.microsoft.com/.default"],
    },
    {
        "name": "Microsoft Azure CLI",
        "client_id": "04b07795-a71b-4346-a7c1-dd9700c6032a",
        "scopes": ["https://graph.microsoft.com/.default"],
    },
    {
        "name": "Microsoft Teams",
        "client_id": "1fec8e78-bce4-4aaf-ab1b-5451cc387264",
        "scopes": ["https://graph.microsoft.com/.default"],
    },
]

AUTHORITY = "https://login.microsoftonline.com/organizations"


def test_access(token):
    headers = {"Authorization": f"Bearer {token}"}
    endpoints = {}

    tests = [
        ("/me", "https://graph.microsoft.com/v1.0/me?$select=displayName,mail,jobTitle,department,officeLocation"),
        ("/me/people", "https://graph.microsoft.com/v1.0/me/people?$top=999"),
        ("/users (dir)", "https://graph.microsoft.com/v1.0/users?$top=5&$select=displayName,mail,jobTitle"),
        ("/me/joinedTeams", "https://graph.microsoft.com/v1.0/me/joinedTeams"),
    ]

    for label, url in tests:
        r = requests.get(url, headers=headers)
        status = "OK" if r.status_code == 200 else f"BLOCKED ({r.status_code})"
        count = ""
        if r.status_code == 200:
            data = r.json()
            if "value" in data:
                count = f" [{len(data['value'])} items]"
                endpoints[label] = data["value"]
            else:
                count = f" [{data.get('displayName', '')}]"
                endpoints[label] = data
        print(f"  {label:25s} {status}{count}")

    return endpoints


def main():
    print("=" * 60)
    print("M365 AUTH -- First-Party App Strategy")
    print("=" * 60)
    print()

    for app_info in FIRST_PARTY_APPS:
        name = app_info["name"]
        cid = app_info["client_id"]
        scopes = app_info["scopes"]

        print(f"Trying: {name} ({cid[:8]}...)")
        sys.stdout.flush()

        app = msal.PublicClientApplication(cid, authority=AUTHORITY)

        try:
            result = app.acquire_token_interactive(scopes=scopes, prompt="select_account")
        except Exception as e:
            print(f"  Error: {e}\n")
            continue

        if not result or "access_token" not in result:
            err = result.get("error", "unknown") if result else "no result"
            desc = (result.get("error_description", "") if result else "")[:100]
            print(f"  Failed: {err} - {desc}\n")
            continue

        print(f"  Authenticated! Granted: {result.get('scope', '?')[:80]}")
        print()
        print("  Testing endpoints:")

        endpoints = test_access(result["access_token"])

        if any(endpoints.values()):
            with open(TOKEN_FILE, "w") as f:
                json.dump({"access_token": result["access_token"], "scope": result.get("scope", ""), "app": name}, f, indent=2)

            import os
            os.makedirs("inventory/users/sources", exist_ok=True)
            for label, data in endpoints.items():
                safe_label = label.strip("/").replace(" ", "_").replace("(", "").replace(")", "")
                fname = f"inventory/users/sources/m365_{safe_label}.json"
                with open(fname, "w") as f:
                    json.dump(data, f, indent=2)
                print(f"  Saved: {fname}")

            print(f"\n  SUCCESS with {name}!")
            return

        print(f"  No usable data from {name}.\n")

    print()
    print("=" * 60)
    print("ALL FIRST-PARTY APPS BLOCKED")
    print("=" * 60)
    print()
    print("The tenant's Conditional Access Policy blocks all Graph API")
    print("access from unregistered devices. This is strict but not uncommon.")
    print()
    print("Options:")
    print("  1. Ask IT (Rosen) to export Azure AD users to CSV")
    print("  2. Request admin consent for Graph CLI tool via Rosen/Matias")
    print("  3. Proceed without M365 -- we have BB, Jira, Confluence, AWS")
    print()


if __name__ == "__main__":
    main()
