#!/usr/bin/env python3
"""Scan Bitbucket repos for tool usage signals in config files."""

import requests
import json
import os
import time

BB_API = "https://api.bitbucket.org/2.0"
BB_USER = os.environ.get("BB_USER", "adam.lazarus@madmobile.com")
BB_TOKEN = os.environ["BB_TOKEN"]
AUTH = (BB_USER, BB_TOKEN)

WORKSPACES = ["madmobile", "syscolabs", "madpayments", "syscolabsconf"]
MAX_REPOS = 20

CONFIG_FILES = [
    "package.json", "Dockerfile", "docker-compose.yml",
    "bitbucket-pipelines.yml", "Jenkinsfile", "sonar-project.properties",
    ".snyk", "pom.xml", "build.gradle", "tsconfig.json",
    ".eslintrc.json", ".prettierrc", "jest.config.js", "jest.config.ts",
]

TOOL_SIGNALS = {
    "sonarqube": ["sonar", "sonarqube"],
    "snyk": ["snyk"],
    "docker": ["docker"],
    "jest": ["jest"],
    "eslint": ["eslint"],
    "prettier": ["prettier"],
    "datadog": ["datadog", "dd-trace", "dd-agent"],
    "sentry": ["sentry", "@sentry"],
    "webpack": ["webpack"],
    "vite": ["vite"],
    "typescript": ["typescript"],
    "newrelic": ["newrelic", "new-relic"],
    "redis": ["redis", "ioredis"],
    "mongodb": ["mongodb", "mongoose"],
    "postgres": ["pg ", "postgres", "sequelize"],
    "mysql": ["mysql", "mysql2"],
    "elasticsearch": ["elasticsearch", "@elastic"],
    "kafka": ["kafka", "kafkajs"],
    "rabbitmq": ["amqplib", "rabbitmq"],
    "maven": ["maven"],
    "gradle": ["gradle"],
}


def get_repos(workspace):
    repos = []
    resp = requests.get(f"{BB_API}/repositories/{workspace}",
                        auth=AUTH, params={"pagelen": MAX_REPOS, "sort": "-updated_on"})
    resp.raise_for_status()
    for r in resp.json().get("values", []):
        repos.append({
            "slug": r["slug"], "name": r.get("name", r["slug"]),
            "language": r.get("language", ""),
            "updated_on": r.get("updated_on", ""),
            "project": r.get("project", {}).get("name", "") if r.get("project") else "",
        })
    return repos


def get_file(workspace, slug, path):
    try:
        r = requests.get(f"{BB_API}/repositories/{workspace}/{slug}/src/HEAD/{path}", auth=AUTH)
        return r.text[:10000] if r.status_code == 200 else None
    except Exception:
        return None


def detect_tools(content, filename):
    found = set()
    lower = content.lower()
    for tool, signals in TOOL_SIGNALS.items():
        if any(s in lower for s in signals):
            found.add(tool)
    if filename == "package.json":
        try:
            pkg = json.loads(content)
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            for dep in deps:
                dl = dep.lower()
                for tool, signals in TOOL_SIGNALS.items():
                    if any(s in dl for s in signals):
                        found.add(tool)
        except (json.JSONDecodeError, TypeError):
            pass
    return list(found)


if __name__ == "__main__":
    os.makedirs("inventory/bitbucket", exist_ok=True)
    all_results = []

    for ws in WORKSPACES:
        print(f"\n=== {ws} ===")
        repos = get_repos(ws)
        print(f"  {len(repos)} repos")

        for repo in repos:
            slug = repo["slug"]
            repo_tools = {}
            has_pipe = False
            has_jenkins = False

            for cf in CONFIG_FILES:
                content = get_file(ws, slug, cf)
                if content:
                    if cf == "bitbucket-pipelines.yml":
                        has_pipe = True
                    if cf == "Jenkinsfile":
                        has_jenkins = True
                    tools = detect_tools(content, cf)
                    if tools:
                        repo_tools[cf] = tools
                time.sleep(0.05)

            all_tools = set()
            for t in repo_tools.values():
                all_tools.update(t)

            ci = "both" if has_pipe and has_jenkins else "bitbucket_pipelines" if has_pipe else "jenkins" if has_jenkins else "none"
            result = {
                "workspace": ws, "repo": slug, "language": repo["language"],
                "project": repo["project"], "updated_on": repo["updated_on"],
                "config_files_found": list(repo_tools.keys()),
                "tools_detected": sorted(all_tools),
                "tools_by_file": repo_tools,
                "ci_system": ci,
            }
            all_results.append(result)
            if all_tools:
                print(f"  {slug}: {', '.join(sorted(all_tools))} [CI: {ci}]")
            time.sleep(0.1)

    with open("inventory/bitbucket/tool_dependency_scan.json", "w") as f:
        json.dump({"repos_scanned": len(all_results), "results": all_results}, f, indent=2)

    tool_counts = {}
    ci_counts = {"bitbucket_pipelines": 0, "jenkins": 0, "both": 0, "none": 0}
    for r in all_results:
        ci_counts[r["ci_system"]] += 1
        for t in r["tools_detected"]:
            tool_counts.setdefault(t, {"count": 0, "repos": []})
            tool_counts[t]["count"] += 1
            tool_counts[t]["repos"].append(f"{r['workspace']}/{r['repo']}")

    print(f"\n=== Summary ===\nScanned: {len(all_results)} repos")
    print(f"CI/CD: {json.dumps(ci_counts)}")
    for t, d in sorted(tool_counts.items(), key=lambda x: -x[1]["count"]):
        print(f"  {t}: {d['count']} repos")

    with open("inventory/bitbucket/tool_summary.json", "w") as f:
        json.dump({"tool_counts": tool_counts, "ci_summary": ci_counts}, f, indent=2)
