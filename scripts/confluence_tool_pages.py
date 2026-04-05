#!/usr/bin/env python3
"""Fetch and parse key Confluence pages for tooling/cost/vendor data."""

import requests
import json
import os
import re
from requests.auth import HTTPBasicAuth
from html.parser import HTMLParser

CONFLUENCE_URL = os.environ.get("ATLASSIAN_URL", "https://madmobile-eng.atlassian.net")
CONFLUENCE_EMAIL = os.environ.get("ATLASSIAN_EMAIL", "adam.lazarus@madmobile.com")
CONFLUENCE_TOKEN = os.environ["ATLASSIAN_TOKEN"]
AUTH = HTTPBasicAuth(CONFLUENCE_EMAIL, CONFLUENCE_TOKEN)
HEADERS = {"Accept": "application/json"}

PAGES = {
    "ai_tools": 246251848,
    "engineering_software": 394231819,
    "cake_engineering_tools": 259096688,
    "tooling_evaluation": 360801807,
    "snyk_implementation": 360803312,
    "datadog_reference": 626065488,
    "datadog_concierge": 537198965,
    "vendor_contracts_restaurant": 359432790,
    "vendor_contracts_payments": 268042370,
    "aws_cost_savings_2025": 750977029,
    "quicksight_dashboards": 573636624,
    "cost_center_mapping": 503545918,
    "bedrock_costing": 360776087,
    "software_procurement": 355763969,
}


class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_cell = False
        self.rows = []
        self.current_row = []
        self.current_cell = ""

    def handle_starttag(self, tag, attrs):
        if tag in ("td", "th"):
            self.in_cell = True
            self.current_cell = ""

    def handle_endtag(self, tag):
        if tag in ("td", "th"):
            self.in_cell = False
            self.current_row.append(self.current_cell.strip())
        if tag == "tr":
            if self.current_row:
                self.rows.append(self.current_row)
            self.current_row = []

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell += data


class ListParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_li = False
        self.items = []
        self.current = ""

    def handle_starttag(self, tag, attrs):
        if tag == "li":
            self.in_li = True
            self.current = ""

    def handle_endtag(self, tag):
        if tag == "li":
            self.in_li = False
            if self.current.strip():
                self.items.append(self.current.strip())

    def handle_data(self, data):
        if self.in_li:
            self.current += data


def clean_text(html):
    text = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", text).strip()


if __name__ == "__main__":
    os.makedirs("inventory/confluence/tooling_pages", exist_ok=True)

    results = {}
    for name, cid in PAGES.items():
        try:
            resp = requests.get(
                f"{CONFLUENCE_URL}/wiki/rest/api/content/{cid}",
                auth=AUTH, headers=HEADERS,
                params={"expand": "body.storage,version,space"},
            )
            resp.raise_for_status()
            d = resp.json()
            body = d.get("body", {}).get("storage", {}).get("value", "")

            tp = TableParser()
            tp.feed(body)
            lp = ListParser()
            lp.feed(body)
            text = clean_text(body)

            results[name] = {
                "title": d.get("title", ""),
                "content_id": cid,
                "space_key": d.get("space", {}).get("key", ""),
                "space_name": d.get("space", {}).get("name", ""),
                "version": d.get("version", {}).get("number", 0),
                "last_modified": d.get("version", {}).get("when", ""),
                "tables": tp.rows,
                "lists": lp.items,
                "text": text,
            }
            print(f"OK: {name} ({d.get('title','')}) - {len(tp.rows)} rows, {len(lp.items)} items, {len(text)} chars")
        except Exception as e:
            results[name] = {"error": str(e), "content_id": cid}
            print(f"ERR: {name} - {e}")

    with open("inventory/confluence/tooling_pages/extracted_pages.json", "w") as f:
        json.dump(results, f, indent=2)

    ok = len([r for r in results.values() if "error" not in r])
    print(f"\nDone. {ok}/{len(PAGES)} pages extracted.")
