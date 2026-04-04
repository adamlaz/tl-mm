#!/usr/bin/env python3
"""Cross-system deployment correlation: merge-to-build lead time and deploy frequency."""

import json
import os
from datetime import datetime, timezone
from collections import defaultdict
import statistics

def parse_ts(s):
    if not s:
        return None
    try:
        s = s.replace('Z', '+00:00')
        return datetime.fromisoformat(s)
    except Exception:
        return None

def main():
    os.makedirs('inventory/cross_system', exist_ok=True)

    pipeline_data = {}
    try:
        ph = json.load(open('inventory/bitbucket/pipeline_history.json'))
        for repo in ph.get('per_repo', []):
            key = f"{repo.get('workspace','')}/{repo.get('repo','')}"
            pipeline_data[key] = repo
    except Exception as e:
        print(f"Pipeline history: {e}")

    metrics_data = {}
    try:
        metrics = json.load(open('inventory/bitbucket/metrics.json'))
        for m in metrics:
            key = f"{m.get('workspace','')}/{m.get('repo','')}"
            metrics_data[key] = m
    except Exception as e:
        print(f"Metrics: {e}")

    deploy_tags = {}
    try:
        dt = json.load(open('inventory/bitbucket/deploy_tags.json'))
        for entry in dt if isinstance(dt, list) else dt.get('repos', []):
            key = f"{entry.get('workspace','')}/{entry.get('repo','')}"
            deploy_tags[key] = entry
    except Exception as e:
        print(f"Deploy tags: {e}")

    results = []
    for key in set(list(pipeline_data.keys()) + list(metrics_data.keys())):
        pipe = pipeline_data.get(key, {})
        met = metrics_data.get(key, {})
        tags = deploy_tags.get(key, {})

        entry = {
            'repo': key,
            'workspace': key.split('/')[0] if '/' in key else '',
        }

        if pipe:
            entry['pipeline_runs'] = pipe.get('total_runs', 0)
            entry['success_rate_pct'] = pipe.get('success_rate_pct', 0)
            entry['median_build_seconds'] = pipe.get('median_build_seconds', 0)
            entry['p95_build_seconds'] = pipe.get('p95_build_seconds', 0)

        if met:
            pr_data = met.get('pr_summary', met.get('prs', {}))
            entry['avg_pr_hours'] = pr_data.get('avg_hours', 0) if isinstance(pr_data, dict) else 0
            entry['total_commits_90d'] = met.get('commit_count', met.get('commits_90d', 0))

        tag_list = tags.get('tags', [])
        if len(tag_list) >= 2:
            tag_dates = []
            for t in tag_list:
                d = parse_ts(t.get('date', t.get('target', {}).get('date', '')))
                if d:
                    tag_dates.append(d)
            tag_dates.sort()
            if len(tag_dates) >= 2:
                intervals = [(tag_dates[i+1] - tag_dates[i]).total_seconds() / 86400
                             for i in range(len(tag_dates)-1)]
                entry['deploy_frequency_days'] = round(statistics.median(intervals), 1)
                entry['total_releases'] = len(tag_dates)

        results.append(entry)

    repos_with_pipelines = [r for r in results if r.get('pipeline_runs', 0) > 0]
    repos_with_deploys = [r for r in results if 'deploy_frequency_days' in r]

    build_times = [r['median_build_seconds'] for r in repos_with_pipelines if r.get('median_build_seconds', 0) > 0]
    deploy_freqs = [r['deploy_frequency_days'] for r in repos_with_deploys]

    output = {
        'total_repos_analyzed': len(results),
        'repos_with_pipeline_data': len(repos_with_pipelines),
        'repos_with_deploy_tags': len(repos_with_deploys),
        'overall_median_build_seconds': round(statistics.median(build_times), 1) if build_times else None,
        'overall_median_deploy_frequency_days': round(statistics.median(deploy_freqs), 1) if deploy_freqs else None,
        'fastest_deployers': sorted(repos_with_deploys, key=lambda r: r.get('deploy_frequency_days', 999))[:10],
        'slowest_deployers': sorted(repos_with_deploys, key=lambda r: r.get('deploy_frequency_days', 0), reverse=True)[:10],
        'worst_build_reliability': sorted(repos_with_pipelines, key=lambda r: r.get('success_rate_pct', 100))[:10],
        'per_repo': results,
    }

    with open('inventory/cross_system/deploy_lead_time.json', 'w') as f:
        json.dump(output, f, indent=2)
    print(f"Repos analyzed: {len(results)}")
    print(f"With pipelines: {len(repos_with_pipelines)}")
    print(f"With deploy tags: {len(repos_with_deploys)}")
    print(f"Median build time: {output['overall_median_build_seconds']}s")
    print(f"Median deploy freq: {output['overall_median_deploy_frequency_days']} days")
    print("Done.")

if __name__ == '__main__':
    main()
