#!/usr/bin/env python3
"""Bitbucket AI tooling adoption scan -- check repos for Cursor, Copilot, and other AI configs."""

import requests
import json
import os
import time

BB_API = "https://api.bitbucket.org/2.0"
BB_USER = os.environ.get("BB_USER", "adam.lazarus@madmobile.com")
BB_TOKEN = os.environ["BB_TOKEN"]
AUTH = (BB_USER, BB_TOKEN)

AI_FILES = [
    '.cursorrules',
    '.cursorignore',
    '.cursor/rules',
    'cursor.json',
    '.github/copilot-instructions.md',
    '.aider.conf.yml',
    '.ai/',
    'AGENTS.md',
    'CLAUDE.md',
    '.codex/',
]


def check_file_exists(workspace, repo_slug, path):
    try:
        resp = requests.get(f"{BB_API}/repositories/{workspace}/{repo_slug}/src/HEAD/{path}",
                           auth=AUTH)
        return resp.status_code == 200
    except Exception:
        return False


if __name__ == '__main__':
    os.makedirs('inventory/bitbucket', exist_ok=True)

    metrics = json.load(open('inventory/bitbucket/metrics.json'))
    repos = [(m['workspace'], m['repo'], m.get('language', '')) for m in metrics]

    results = []
    for i, (ws, repo, lang) in enumerate(repos):
        print(f"[{i+1}/{len(repos)}] {ws}/{repo}...", flush=True)
        found_files = []
        for ai_file in AI_FILES:
            if check_file_exists(ws, repo, ai_file):
                found_files.append(ai_file)
                print(f"  FOUND: {ai_file}", flush=True)
        results.append({
            'workspace': ws,
            'repo': repo,
            'language': lang,
            'ai_files_found': found_files,
            'has_ai_tooling': len(found_files) > 0,
            'tools_detected': list(set(
                ['cursor' if 'cursor' in f.lower() else
                 'copilot' if 'copilot' in f.lower() or 'github' in f.lower() else
                 'aider' if 'aider' in f.lower() else
                 'claude' if 'claude' in f.lower() or 'AGENTS' in f else
                 'codex' if 'codex' in f.lower() else 'other'
                 for f in found_files]
            )),
        })
        time.sleep(0.3)

    adoption = sum(1 for r in results if r['has_ai_tooling'])
    with open('inventory/bitbucket/ai_tooling.json', 'w') as f:
        json.dump({
            'repos_scanned': len(results),
            'repos_with_ai_tooling': adoption,
            'adoption_rate': round(adoption / len(results) * 100, 1) if results else 0,
            'repos': results,
        }, f, indent=2)
    print(f"\n-> {adoption}/{len(results)} repos have AI tooling configs")
    print("Done.", flush=True)
