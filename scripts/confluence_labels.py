#!/usr/bin/env python3
"""Audit Confluence blog posts and label usage across spaces."""

import json
import os
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv(".env.local")

BASE_URL = os.environ.get("ATLASSIAN_URL", "https://madmobile-eng.atlassian.net")
AUTH = HTTPBasicAuth(
    os.environ.get("ATLASSIAN_EMAIL", "adam.lazarus@madmobile.com"),
    os.environ["ATLASSIAN_TOKEN"],
)
HEADERS = {"Accept": "application/json"}
API_DELAY = 0.4

OUT_DIR = "inventory/confluence"
os.makedirs(OUT_DIR, exist_ok=True)

TARGET_LABELS = ["architecture", "rca", "release", "deployment"]


def api_get(path, params=None):
    url = f"{BASE_URL}{path}"
    resp = requests.get(url, auth=AUTH, headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json()


def search_cql(cql, limit=50, expand=None):
    """Run a CQL search with pagination."""
    results = []
    start = 0
    while True:
        params = {"cql": cql, "limit": min(limit - len(results), 50), "start": start}
        if expand:
            params["expand"] = expand
        data = api_get("/wiki/rest/api/content/search", params=params)
        batch = data.get("results", [])
        results.extend(batch)
        if len(results) >= limit or not batch:
            break
        start += len(batch)
        time.sleep(API_DELAY)
    return results[:limit]


def fetch_labels_for_content(content_id):
    try:
        data = api_get(f"/wiki/rest/api/content/{content_id}/label")
        return [l.get("name", "") for l in data.get("results", [])]
    except Exception:
        return []


def fetch_popular_labels():
    """Try to get popular/system labels via the REST API."""
    try:
        data = api_get("/wiki/rest/api/label", params={"type": "popular", "maxResults": 50})
        return data.get("labels", data.get("results", []))
    except requests.HTTPError:
        pass
    try:
        data = api_get("/wiki/rest/api/label", params={"maxResults": 50})
        return data.get("labels", data.get("results", []))
    except Exception as e:
        print(f"  Popular labels API not available: {e}")
        return None


def main():
    print("=" * 60)
    print("Confluence Blog Posts & Label Audit")
    print("=" * 60)

    # --- Blog Posts ---
    print("\n[1/3] Searching for blog posts (2024+)...")
    cql_blog = 'type=blogpost AND created >= "2024-01-01"'
    try:
        blog_posts = search_cql(cql_blog, limit=50, expand="space,metadata.labels,version")
    except Exception as e:
        print(f"  Blog search failed: {e}")
        blog_posts = []
    print(f"  Found {len(blog_posts)} blog posts")

    blog_summaries = []
    space_counts = Counter()
    blog_label_counts = Counter()
    for bp in blog_posts:
        space = bp.get("space", {})
        space_key = space.get("key", "")
        space_counts[space_key] += 1

        labels = []
        meta_labels = bp.get("metadata", {}).get("labels", {}).get("results", [])
        if meta_labels:
            labels = [l.get("name", "") for l in meta_labels]
        else:
            time.sleep(API_DELAY)
            labels = fetch_labels_for_content(bp["id"])

        for l in labels:
            blog_label_counts[l] += 1

        version = bp.get("version", {})
        blog_summaries.append({
            "id": bp.get("id", ""),
            "title": bp.get("title", ""),
            "space_key": space_key,
            "space_name": space.get("name", ""),
            "created": version.get("when", ""),
            "labels": labels,
        })

    # --- Popular Labels ---
    print("\n[2/3] Fetching popular labels...")
    time.sleep(API_DELAY)
    popular_raw = fetch_popular_labels()
    popular_labels = []
    if popular_raw:
        for l in popular_raw:
            if isinstance(l, dict):
                popular_labels.append({
                    "name": l.get("name", l.get("label", "")),
                    "count": l.get("count", 0),
                })
            else:
                popular_labels.append({"name": str(l), "count": 0})
        print(f"  Got {len(popular_labels)} popular labels")
    else:
        print("  Not available — will derive from search results")

    # --- Target Label Counts ---
    print("\n[3/3] Counting content per target label...")
    label_results = {}
    for label in TARGET_LABELS:
        time.sleep(API_DELAY)
        cql = f'label = "{label}"'
        try:
            data = api_get("/wiki/rest/api/content/search", params={
                "cql": cql, "limit": 1,
            })
            total = data.get("totalSize", data.get("size", len(data.get("results", []))))
            label_results[label] = total
            print(f"  label={label:20s}  → {total} pages")
        except Exception as e:
            print(f"  label={label:20s}  → error: {e}")
            label_results[label] = None

    # --- Blog output ---
    blog_output = {
        "extracted_at": datetime.now().isoformat(),
        "cql": cql_blog,
        "total": len(blog_summaries),
        "by_space": dict(space_counts.most_common()),
        "label_frequency": dict(blog_label_counts.most_common(30)),
        "posts": blog_summaries,
    }
    blog_path = os.path.join(OUT_DIR, "blog_posts.json")
    with open(blog_path, "w") as f:
        json.dump(blog_output, f, indent=2, default=str)
    print(f"\nWrote {blog_path}")

    # --- Labels output ---
    labels_output = {
        "extracted_at": datetime.now().isoformat(),
        "target_labels": label_results,
        "popular_labels": popular_labels if popular_labels else "not_available",
        "blog_label_frequency": dict(blog_label_counts.most_common(50)),
    }
    labels_path = os.path.join(OUT_DIR, "labels.json")
    with open(labels_path, "w") as f:
        json.dump(labels_output, f, indent=2, default=str)
    print(f"Wrote {labels_path}")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    print(f"\nBlog posts (2024+): {len(blog_summaries)}")
    if space_counts:
        print(f"  By space (top 10):")
        for space, count in space_counts.most_common(10):
            print(f"    {space:15s}  {count} posts")

    if blog_label_counts:
        print(f"\n  Most-used labels on blog posts:")
        for label, count in blog_label_counts.most_common(10):
            print(f"    {label:25s}  {count}x")

    print(f"\nTarget label page counts:")
    for label, count in label_results.items():
        val = str(count) if count is not None else "error"
        print(f"  {label:20s}  {val} pages")

    if popular_labels:
        print(f"\nPopular labels (top 10):")
        for l in popular_labels[:10]:
            print(f"  {l['name']:25s}  ({l.get('count', '?')} uses)")

    print()


if __name__ == "__main__":
    main()
