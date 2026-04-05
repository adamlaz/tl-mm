import json
import os
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

from collectors import PersonRecord

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env.local"
PAGE_INDEX_PATH = BASE_DIR / "inventory" / "confluence" / "page_index.json"

BASE_URL = "https://madmobile-eng.atlassian.net/wiki"
EMAIL = "adam.lazarus@madmobile.com"
RATE_LIMIT_SECONDS = 0.15


def _load_token() -> str:
    with open(ENV_PATH) as f:
        for line in f:
            if line.startswith("ATLASSIAN_TOKEN="):
                return line.split("=", 1)[1].strip().strip('"')
    raise RuntimeError("ATLASSIAN_TOKEN not found in .env.local")


def _resolve_users(account_ids: list[str], session: requests.Session) -> dict:
    resolved = {}
    total = len(account_ids)
    for i, aid in enumerate(account_ids, 1):
        if i % 25 == 0 or i == total:
            print(f"  Resolving users: {i}/{total}")
        try:
            resp = session.get(
                f"{BASE_URL}/rest/api/user",
                params={"accountId": aid},
            )
            if resp.status_code == 200:
                data = resp.json()
                resolved[aid] = {
                    "displayName": data.get("displayName", aid),
                    "email": data.get("email"),
                }
            else:
                print(f"  Skipping {aid}: HTTP {resp.status_code}")
        except requests.RequestException as e:
            print(f"  Skipping {aid}: {e}")
        time.sleep(RATE_LIMIT_SECONDS)
    return resolved


def collect() -> list[PersonRecord]:
    token = _load_token()
    session = requests.Session()
    session.auth = (EMAIL, token)
    session.headers["Accept"] = "application/json"

    print("Loading page index...")
    with open(PAGE_INDEX_PATH) as f:
        pages = json.load(f)
    print(f"  {len(pages)} pages loaded")

    cutoff = datetime.now(timezone.utc) - timedelta(days=90)

    author_pages: dict[str, list[dict]] = {}
    for page in pages:
        aid = page.get("author")
        if aid:
            author_pages.setdefault(aid, []).append(page)

    unique_ids = list(author_pages.keys())
    print(f"Resolving {len(unique_ids)} unique author IDs...")
    user_map = _resolve_users(unique_ids, session)
    print(f"  Resolved {len(user_map)} of {len(unique_ids)} authors")

    records = []
    for aid, info in user_map.items():
        pages_for_author = author_pages.get(aid, [])
        pages_total = len(pages_for_author)

        pages_90d = 0
        spaces = set()
        for p in pages_for_author:
            spaces.add(p.get("space_key", "unknown"))
            ts = p.get("version_created_at")
            if ts:
                try:
                    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    if dt >= cutoff:
                        pages_90d += 1
                except ValueError:
                    pass

        records.append(PersonRecord(
            source="confluence",
            canonical_name=info["displayName"],
            account_id=aid,
            email=info.get("email"),
            metadata={
                "pages_total": pages_total,
                "pages_90d": pages_90d,
                "spaces": sorted(spaces),
            },
        ))

    print(f"Collected {len(records)} Confluence person records")
    return records


if __name__ == "__main__":
    collect()
