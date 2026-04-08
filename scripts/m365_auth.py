#!/usr/bin/env python3
"""Microsoft Graph API authentication helpers.

Supports two flows:
  - Client credentials (application permissions): Calendars.ReadBasic.All, People.Read.All, User.Read.All
  - Delegated (interactive browser): User.Read, Calendars.Read, People.Read, etc.

Credentials loaded from .env file (M365_CLIENT_ID, M365_TENANT_ID, M365_CLIENT_SECRET).
"""

import sys
import json
import os
from pathlib import Path

import msal
import requests

ENV_FILE = Path(__file__).parent.parent / ".env"
TOKEN_FILE = Path(__file__).parent.parent / ".m365_token.json"
GRAPH_BASE = "https://graph.microsoft.com/v1.0"


def _load_env():
    """Load credentials from .env file."""
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    client_id = env.get("M365_CLIENT_ID", os.environ.get("M365_CLIENT_ID", ""))
    tenant_id = env.get("M365_TENANT_ID", os.environ.get("M365_TENANT_ID", ""))
    client_secret = env.get("M365_CLIENT_SECRET", os.environ.get("M365_CLIENT_SECRET", ""))
    if not client_id or not tenant_id:
        print("ERROR: M365_CLIENT_ID and M365_TENANT_ID required in .env")
        sys.exit(1)
    return client_id, tenant_id, client_secret


def get_app_token():
    """Acquire token via client credentials flow (application permissions)."""
    client_id, tenant_id, client_secret = _load_env()
    if not client_secret:
        print("ERROR: M365_CLIENT_SECRET required in .env for app token")
        sys.exit(1)
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    app = msal.ConfidentialClientApplication(client_id, authority=authority, client_credential=client_secret)
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if not result or "access_token" not in result:
        err = result.get("error", "unknown") if result else "no result"
        desc = result.get("error_description", "")[:300] if result else ""
        print(f"App auth failed: {err} -- {desc}")
        sys.exit(1)
    return result["access_token"]


def get_delegated_token(scopes=None):
    """Acquire token via interactive browser flow (delegated permissions)."""
    client_id, tenant_id, _ = _load_env()
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    if scopes is None:
        scopes = ["User.Read", "User.Read.All", "People.Read", "Calendars.Read", "Group.Read.All", "Team.ReadBasic.All"]
    if TOKEN_FILE.exists():
        cached = json.loads(TOKEN_FILE.read_text())
        token = cached.get("access_token")
        if token:
            r = requests.get(f"{GRAPH_BASE}/me", headers={"Authorization": f"Bearer {token}"})
            if r.status_code == 200:
                return token
    app = msal.PublicClientApplication(client_id, authority=authority)
    print("Opening browser for sign-in...")
    result = app.acquire_token_interactive(scopes=scopes)
    if not result or "access_token" not in result:
        err = result.get("error", "unknown") if result else "no result"
        print(f"Delegated auth failed: {err}")
        sys.exit(1)
    token = result["access_token"]
    TOKEN_FILE.write_text(json.dumps({"access_token": token, "scope": result.get("scope", ""), "client_id": client_id, "tenant_id": tenant_id}, indent=2))
    return token


def graph_get(token, path, params=None):
    """GET request to Graph API with automatic pagination."""
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{GRAPH_BASE}{path}" if not path.startswith("http") else path
    all_values = []
    while url:
        r = requests.get(url, headers=headers, params=params)
        if r.status_code != 200:
            return {"error": r.status_code, "message": r.text[:300], "values": all_values}
        data = r.json()
        all_values.extend(data.get("value", []))
        url = data.get("@odata.nextLink")
        params = None
    return {"values": all_values}


def graph_post(token, path, body):
    """POST request to Graph API."""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url = f"{GRAPH_BASE}{path}"
    r = requests.post(url, headers=headers, json=body)
    if r.status_code not in (200, 201):
        return {"error": r.status_code, "message": r.text[:300]}
    return r.json()


if __name__ == "__main__":
    print("=" * 60)
    print("M365 AUTH TEST")
    print("=" * 60)

    print("\n--- App token (client credentials) ---")
    app_token = get_app_token()
    print("  App token acquired")
    h = {"Authorization": f"Bearer {app_token}"}

    r = requests.get(f"{GRAPH_BASE}/users?$top=3&$select=displayName,mail", headers=h)
    print(f"  /users: {r.status_code}", end="")
    if r.status_code == 200:
        print(f" -> {len(r.json().get('value',[]))} sample users")
    else:
        print(f" -> {r.text[:150]}")

    r = requests.get(f"{GRAPH_BASE}/users?$top=1&$select=id,displayName", headers=h)
    if r.status_code == 200 and r.json().get("value"):
        uid = r.json()["value"][0]["id"]
        r2 = requests.get(f"{GRAPH_BASE}/users/{uid}/calendarView?$top=1&startDateTime=2026-04-07T00:00:00Z&endDateTime=2026-04-08T00:00:00Z&$select=start,end,attendees", headers=h)
        print(f"  /users/{{id}}/calendarView: {r2.status_code}")
        r3 = requests.get(f"{GRAPH_BASE}/users/{uid}/people?$top=3", headers=h)
        print(f"  /users/{{id}}/people: {r3.status_code}")

    r = requests.get(f"{GRAPH_BASE}/groups?$top=3&$select=displayName,groupTypes", headers=h)
    print(f"  /groups: {r.status_code}")

    print("\nDone.")
