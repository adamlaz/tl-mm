#!/usr/bin/env python3
"""Generate CSVs, interactive charts, and summary from all inventory data."""

import json
import os
import glob
import numpy as np
import pandas as pd
import tl_echarts_style as zcs

CHARTS_DIR = 'analysis/charts'
CSV_DIR = 'analysis'
os.makedirs(CHARTS_DIR, exist_ok=True)
os.makedirs(CSV_DIR, exist_ok=True)

def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

# ─── AWS ────────────────────────────────────────────────────────────────

def generate_aws_analysis():
    print("=== AWS Analysis ===", flush=True)
    costs = load_json('inventory/aws/cost_normalized.json') or []
    cost_summary = load_json('inventory/aws/cost_summary.json') or {}
    resources = load_json('inventory/aws/resources_flat.json') or []
    lambda_audit = load_json('inventory/aws/lambda_audit.json') or {}
    instance_audit = load_json('inventory/aws/instance_audit.json') or {}

    if costs:
        df_cost = pd.DataFrame(costs)
        df_cost.to_csv(f'{CSV_DIR}/aws_cost_summary.csv', index=False)
        print(f"  -> {CSV_DIR}/aws_cost_summary.csv ({len(df_cost)} rows)")

        march = df_cost[df_cost['month'].str.contains('2026-03', na=False)]
        if not march.empty:
            acct_totals = march.groupby('profile')['cost'].sum().sort_values(ascending=True)
            config = zcs.bar_config(
                acct_totals.index.tolist(),
                [{"text": "Cost", "values": acct_totals.values.tolist()}],
                horizontal=True,
                title='AWS Monthly Cost by Account (March 2026)',
                source="AWS Cost Explorer",
                x_title='Cost (USD)', y_title='Account')
            zcs.write_echarts_json(config, f'{CHARTS_DIR}/aws_cost_by_account.json')

            top_services = march.groupby('service')['cost'].sum().nlargest(15).sort_values(ascending=True)
            config = zcs.bar_config(
                top_services.index.tolist(),
                [{"text": "Cost", "values": top_services.values.tolist()}],
                horizontal=True,
                title='AWS Top 15 Services by Cost (March 2026)',
                source="AWS Cost Explorer",
                x_title='Cost (USD)', y_title='Service')
            zcs.write_echarts_json(config, f'{CHARTS_DIR}/aws_cost_by_service.json')

            svc_costs = march.groupby('service')['cost'].sum().sort_values(ascending=False)
            config = zcs.waterfall_config(
                svc_costs.index.tolist(), svc_costs.values.tolist(),
                title="AWS Monthly Cost Composition \u2014 March 2026",
                source="AWS Cost Explorer")
            zcs.write_echarts_json(config, f'{CHARTS_DIR}/aws_cost_waterfall.json')

            config = zcs.pareto_config(
                svc_costs.index.tolist(), svc_costs.values.tolist(),
                title="AWS Cost Concentration by Service",
                source="AWS Cost Explorer")
            zcs.write_echarts_json(config, f'{CHARTS_DIR}/aws_cost_pareto.json')

        monthly_trend = df_cost.groupby(['month', 'profile'])['cost'].sum().reset_index()
        if not monthly_trend.empty:
            months = sorted(monthly_trend['month'].unique())
            series = []
            for profile_name, group in monthly_trend.groupby('profile'):
                vals = group.set_index('month').reindex(months)['cost'].fillna(0).tolist()
                series.append({"text": profile_name, "values": vals})
            config = zcs.line_config(
                months, series,
                title='AWS Cost Trend by Account -- Jan to Mar 2026',
                source="AWS Cost Explorer",
                x_title='Month', y_title='Cost (USD)')
            zcs.add_zoom_preview(config)
            zcs.write_echarts_json(config, f'{CHARTS_DIR}/aws_cost_trend.json')

    if resources:
        df_res = pd.DataFrame(resources)
        df_res.to_csv(f'{CSV_DIR}/aws_resource_inventory.csv', index=False)
        print(f"  -> {CSV_DIR}/aws_resource_inventory.csv ({len(df_res)} rows)")

        type_counts = df_res.groupby(['profile', 'type']).size().reset_index(name='count')
        profiles = sorted(type_counts['profile'].unique())
        series = []
        for type_name, group in type_counts.groupby('type'):
            counts = group.set_index('profile').reindex(profiles)['count'].fillna(0).astype(int).tolist()
            series.append({"text": type_name, "values": counts})
        config = zcs.bar_config(
            profiles, series, stacked=True,
            title='AWS Resource Inventory by Account and Type',
            source="AWS APIs",
            x_title='Account', y_title='Resources')
        zcs.write_echarts_json(config, f'{CHARTS_DIR}/aws_resource_inventory.json')

    if lambda_audit.get('by_runtime'):
        rt_data = lambda_audit['by_runtime']
        eol_runtimes = {'python2.7', 'python3.6', 'python3.7', 'nodejs6.10', 'nodejs8.10',
                        'nodejs10.x', 'nodejs12.x', 'java8', 'dotnetcore2.1', 'dotnetcore3.1'}
        runtime_names = list(rt_data.keys())
        rt_counts = list(rt_data.values())
        colors = [zcs.TL_STATUS['red'] if r.lower() in eol_runtimes
                  else zcs.TL_CATEGORICAL[0] for r in runtime_names]
        colored_data = [{"value": v, "itemStyle": {"color": c}} for v, c in zip(rt_counts, colors)]
        config = zcs.bar_config(
            runtime_names,
            [{"text": "Functions", "values": colored_data}],
            title='Lambda Runtime Distribution -- EOL Runtimes Highlighted',
            source="AWS Lambda",
            x_title='Runtime', y_title='Function Count')
        zcs.write_echarts_json(config, f'{CHARTS_DIR}/aws_lambda_runtimes.json')

    print(f"  -> {CHARTS_DIR}/aws_*.json charts generated")

# ─── BITBUCKET ──────────────────────────────────────────────────────────

def generate_bitbucket_analysis():
    print("\n=== Bitbucket Analysis ===", flush=True)

    all_repos = []
    for ws_file in glob.glob('inventory/bitbucket/*.json'):
        if 'metrics' in ws_file:
            continue
        data = load_json(ws_file)
        if data and 'repos' in data:
            ws = data.get('workspace', '')
            for r in data['repos']:
                all_repos.append({
                    'workspace': ws, 'slug': r.get('slug', ''), 'name': r.get('name', ''),
                    'language': r.get('language', '') or 'unknown',
                    'project': r.get('project', ''), 'is_active': r.get('is_active', False),
                    'updated_on': r.get('updated_on', ''), 'created_on': r.get('created_on', ''),
                    'has_pipeline': r.get('has_pipeline_config', None),
                    'open_prs': r.get('pr_summary', {}).get('open_count', None) if isinstance(r.get('pr_summary'), dict) else None,
                    'merged_30d': r.get('pr_summary', {}).get('merged_last_30d', None) if isinstance(r.get('pr_summary'), dict) else None,
                })

    if all_repos:
        df_repos = pd.DataFrame(all_repos)
        df_repos.to_csv(f'{CSV_DIR}/bitbucket_repos.csv', index=False)
        print(f"  -> {CSV_DIR}/bitbucket_repos.csv ({len(df_repos)} rows)")

        summary = df_repos.groupby('workspace').agg(
            total=('slug', 'count'),
            active=('is_active', 'sum'),
        ).reset_index()
        summary['stale'] = summary['total'] - summary['active']
        config = zcs.bar_config(
            summary['workspace'].tolist(),
            [
                {"text": "Active", "values": summary['active'].astype(int).tolist()},
                {"text": "Stale", "values": summary['stale'].astype(int).tolist()},
            ],
            stacked=True,
            title='Bitbucket Repos: Active vs Stale by Workspace',
            source="Bitbucket",
            x_title='Workspace', y_title='Repositories')
        zcs.write_echarts_json(config, f'{CHARTS_DIR}/bitbucket_repo_health.json')

        lang_counts = df_repos[df_repos['language'] != 'unknown'].groupby(
            ['workspace', 'language']).size().reset_index(name='count')
        if not lang_counts.empty:
            children_list = []
            for ws, group in lang_counts.groupby('workspace'):
                ws_children = [{"text": row['language'], "value": int(row['count'])}
                               for _, row in group.iterrows()]
                children_list.append({"text": ws, "children": ws_children})
            config = zcs.treemap_config(
                children_list,
                title='Bitbucket Language Distribution by Workspace',
                source="Bitbucket")
            zcs.write_echarts_json(config, f'{CHARTS_DIR}/bitbucket_languages.json')

        pipeline_data = df_repos[df_repos['has_pipeline'].notna()]
        if not pipeline_data.empty:
            pipe_summary = pipeline_data.groupby('workspace').agg(
                with_ci=('has_pipeline', 'sum'),
                total_checked=('has_pipeline', 'count'),
            ).reset_index()
            pipe_summary['without_ci'] = pipe_summary['total_checked'] - pipe_summary['with_ci']
            config = zcs.bar_config(
                pipe_summary['workspace'].tolist(),
                [
                    {"text": "Has CI/CD", "values": pipe_summary['with_ci'].astype(int).tolist()},
                    {"text": "No CI/CD", "values": pipe_summary['without_ci'].astype(int).tolist()},
                ],
                stacked=True,
                title='Bitbucket Pipeline Coverage by Workspace',
                source="Bitbucket",
                x_title='Workspace', y_title='Active Repos')
            zcs.write_echarts_json(config, f'{CHARTS_DIR}/bitbucket_pipeline_coverage.json')

    metrics = load_json('inventory/bitbucket/metrics.json')
    if metrics:
        pr_rows = []
        for m in metrics:
            for pr in m.get('pr_cycle_times', []):
                pr['workspace'] = m['workspace']
                pr['repo'] = m['repo']
                pr_rows.append(pr)
        if pr_rows:
            df_pr = pd.DataFrame(pr_rows)
            df_pr.to_csv(f'{CSV_DIR}/bitbucket_pr_metrics.csv', index=False)
            print(f"  -> {CSV_DIR}/bitbucket_pr_metrics.csv ({len(df_pr)} rows)")

            valid_hours = df_pr['cycle_hours'].dropna()
            if not valid_hours.empty:
                bin_counts, bin_edges = np.histogram(valid_hours, bins=30)
                config = zcs.histogram_config(
                    bin_edges.tolist(), bin_counts.tolist(),
                    title='PR Cycle Time Distribution -- Hours from Created to Merged',
                    source="Bitbucket",
                    x_title='Hours', y_title='Pull Requests')
                zcs.add_reference_line(config, "x", "24", "DORA Elite: < 24h", color=zcs.TL_STATUS["green"])
                zcs.add_reference_line(config, "x", "168", "DORA High: < 1 week", color=zcs.TL_STATUS["amber"])
                zcs.write_echarts_json(config, f'{CHARTS_DIR}/bitbucket_pr_cycle_time.json')

        commit_rows = []
        for m in metrics:
            for week, count in m.get('commits', {}).get('weekly_commits', {}).items():
                commit_rows.append({
                    'workspace': m['workspace'], 'repo': m['repo'],
                    'week': week, 'commits': count,
                })
        if commit_rows:
            df_commits = pd.DataFrame(commit_rows)
            df_commits.to_csv(f'{CSV_DIR}/bitbucket_commit_frequency.csv', index=False)
            print(f"  -> {CSV_DIR}/bitbucket_commit_frequency.csv ({len(df_commits)} rows)")

            weekly_total = df_commits.groupby('week')['commits'].sum().reset_index().sort_values('week')
            config = zcs.bar_config(
                weekly_total['week'].tolist(),
                [{"text": "Commits", "values": weekly_total['commits'].tolist()}],
                title='Weekly Commit Frequency (Top 30 Active Repos)',
                source="Bitbucket",
                x_title='Week', y_title='Commits')
            zcs.add_zoom_preview(config)
            zcs.write_echarts_json(config, f'{CHARTS_DIR}/bitbucket_commit_frequency.json')

    print(f"  -> {CHARTS_DIR}/bitbucket_*.json charts generated")

# ─── JIRA ───────────────────────────────────────────────────────────────

def generate_jira_analysis():
    print("\n=== Jira Analysis (Segmented) ===", flush=True)

    projects = load_json('inventory/jira/projects.json') or []
    issue_dist = load_json('inventory/jira/issue_distribution.json') or {}
    project_counts = load_json('inventory/jira/project_issue_counts.json') or {}
    velocity_full = load_json('inventory/jira/velocity_full.json')
    velocity_v1 = load_json('inventory/jira/velocity.json') or {}
    velocity = velocity_full or velocity_v1
    backlog_age = load_json('inventory/jira/backlog_age.json') or {}
    created_resolved = load_json('inventory/jira/created_vs_resolved.json') or {}
    cycle_time = load_json('inventory/jira/cycle_time.json')

    if projects:
        for p in projects:
            pc_entry = project_counts.get(p['key'], {})
            if isinstance(pc_entry, dict):
                p['issue_count'] = pc_entry.get('count', 'unknown')
                p['classification'] = pc_entry.get('classification', 'unclassified')
            else:
                p['issue_count'] = pc_entry
                p['classification'] = 'unclassified'
        df_proj = pd.DataFrame(projects)
        df_proj.to_csv(f'{CSV_DIR}/jira_projects.csv', index=False)
        df_proj.to_csv(f'{CSV_DIR}/jira_project_classification.csv', index=False)
        print(f"  -> {CSV_DIR}/jira_project_classification.csv ({len(df_proj)} rows)")

    seg_totals = {}
    for seg in ['engineering', 'customer_success', 'operations']:
        seg_data = issue_dist.get(seg, {})
        total = sum(v for k, v in seg_data.items()
                    if isinstance(v, (int, float)) and k in ('bugs', 'stories', 'tasks', 'epics', 'subtasks'))
        seg_totals[seg] = total
    if seg_totals:
        sorted_segs = sorted(seg_totals.items(), key=lambda x: x[1])
        config = zcs.bar_config(
            [k.replace('_', ' ').title() for k, _ in sorted_segs],
            [{"text": "Issues", "values": [v for _, v in sorted_segs]}],
            horizontal=True,
            title='Issue Volume by Organizational Segment',
            source="Jira",
            x_title='Issues', y_title='Segment')
        zcs.write_echarts_json(config, f'{CHARTS_DIR}/jira_org_overview.json')

    for seg_name in ['overall', 'engineering']:
        seg_data = issue_dist.get(seg_name, {})
        type_counts = {k: v for k, v in seg_data.items()
                       if isinstance(v, (int, float)) and k in ('bugs', 'stories', 'tasks', 'epics', 'subtasks')}
        if type_counts:
            sorted_types = sorted(type_counts.items(), key=lambda x: x[1])
            label = seg_name.replace('_', ' ').title()
            config = zcs.bar_config(
                [k.title() for k, _ in sorted_types],
                [{"text": "Issues", "values": [v for _, v in sorted_types]}],
                horizontal=True,
                title=f'Issue Distribution by Type ({label})',
                source="Jira",
                x_title='Issues', y_title='Type')
            zcs.write_echarts_json(config, f'{CHARTS_DIR}/jira_issue_distribution_{seg_name}.json')

    if velocity:
        sprint_rows = []
        for board_name, board_data in velocity.items():
            sprints = board_data if isinstance(board_data, list) else board_data.get('sprints', [])
            for s in sprints:
                if isinstance(s, dict) and s.get('done_issues') is not None:
                    sprint_rows.append({
                        'board': board_name,
                        'sprint': s.get('name', ''),
                        'start_date': s.get('start_date', ''),
                        'end_date': s.get('end_date', ''),
                        'complete_date': s.get('complete_date', ''),
                        'done_issues': s.get('done_issues', 0),
                        'total_issues': s.get('total_issues'),
                        'completion_rate': s.get('completion_rate'),
                    })
        if sprint_rows:
            df_vel = pd.DataFrame(sprint_rows)
            df_vel.to_csv(f'{CSV_DIR}/jira_velocity.csv', index=False)
            print(f"  -> {CSV_DIR}/jira_velocity.csv ({len(df_vel)} rows)")

            boards_with_data = df_vel.groupby('board').size()
            top_boards = boards_with_data.nlargest(10).index.tolist()
            df_top = df_vel[df_vel['board'].isin(top_boards)].copy()
            df_top['complete_date'] = pd.to_datetime(df_top['complete_date'], errors='coerce')
            df_top = df_top.sort_values('complete_date')

            all_dates = sorted(df_top['complete_date'].dropna().unique())
            date_labels = [pd.Timestamp(d).strftime('%Y-%m-%d') for d in all_dates]
            series = []
            for board, group in df_top.groupby('board'):
                date_map = {}
                for _, row in group.iterrows():
                    if pd.notna(row['complete_date']):
                        key = pd.Timestamp(row['complete_date']).strftime('%Y-%m-%d')
                        date_map[key] = int(row['done_issues']) if pd.notna(row['done_issues']) else None
                vals = [date_map.get(d) for d in date_labels]
                series.append({"text": board, "values": vals})
            config = zcs.line_config(
                date_labels, series,
                title='Sprint Velocity Trend (Top 10 Active Boards, Engineering)',
                source="Jira",
                x_title='Sprint End', y_title='Issues Completed')
            zcs.add_zoom_preview(config)
            zcs.write_echarts_json(config, f'{CHARTS_DIR}/jira_velocity_trend.json')

    if backlog_age:
        age_rows = []
        for seg_name in ['overall', 'engineering', 'operations']:
            seg_data = backlog_age.get(seg_name, {})
            if isinstance(seg_data, dict):
                for bucket, count in seg_data.items():
                    if isinstance(count, (int, float)):
                        age_rows.append({'segment': seg_name, 'age_bucket': bucket, 'count': count})
        if age_rows:
            df_age = pd.DataFrame(age_rows)
            buckets = df_age['age_bucket'].unique().tolist()
            series = []
            for seg, group in df_age.groupby('segment'):
                seg_map = dict(zip(group['age_bucket'], group['count']))
                vals = [seg_map.get(b, 0) for b in buckets]
                series.append({"text": seg, "values": vals})
            config = zcs.bar_config(
                buckets, series,
                title='Open Backlog Age Distribution (by Segment)',
                source="Jira",
                x_title='Age Bucket', y_title='Open Issues')
            zcs.write_echarts_json(config, f'{CHARTS_DIR}/jira_backlog_age.json')

    if created_resolved and isinstance(created_resolved, dict):
        all_weeks = []
        seg_dfs = {}
        for seg_name in ['overall', 'engineering']:
            seg_data = created_resolved.get(seg_name, [])
            valid = [w for w in seg_data if isinstance(w, dict) and 'error' not in w]
            if valid:
                df_cr = pd.DataFrame(valid)
                seg_dfs[seg_name] = df_cr
                all_weeks.extend(df_cr['week_start'].tolist())

        weeks = sorted(set(all_weeks))
        if weeks and seg_dfs:
            series_list = []
            for seg_name in ['overall', 'engineering']:
                if seg_name in seg_dfs:
                    df_cr = seg_dfs[seg_name].set_index('week_start').reindex(weeks)
                    suffix = '' if seg_name == 'overall' else ' (Eng)'
                    series_list.append({
                        "type": "line", "text": f"Created{suffix}",
                        "values": df_cr['created'].fillna(0).tolist(),
                    })
                    series_list.append({
                        "type": "line", "text": f"Resolved{suffix}",
                        "values": df_cr['resolved'].fillna(0).tolist(),
                    })
            config = zcs.mixed_config(
                series_list, categories=weeks,
                title='Created vs Resolved: Overall and Engineering (Weekly, 6 Months)',
                source="Jira",
                x_title='Week', y_title='Issues')
            zcs.add_zoom_preview(config)
            zcs.write_echarts_json(config, f'{CHARTS_DIR}/jira_created_vs_resolved.json')

    if cycle_time:
        df_ct = pd.DataFrame(cycle_time)
        df_ct.to_csv(f'{CSV_DIR}/jira_cycle_time.csv', index=False)
        print(f"  -> {CSV_DIR}/jira_cycle_time.csv ({len(df_ct)} rows)")

        ct_valid = df_ct[df_ct['cycle_time_days'].notna() & (df_ct['cycle_time_days'] > 0)]
        if not ct_valid.empty:
            p50 = ct_valid['cycle_time_days'].quantile(0.5)
            p75 = ct_valid['cycle_time_days'].quantile(0.75)
            p95 = ct_valid['cycle_time_days'].quantile(0.95)
            bin_counts, bin_edges = np.histogram(ct_valid['cycle_time_days'], bins=30)
            config = zcs.histogram_config(
                bin_edges.tolist(), bin_counts.tolist(),
                title=f'Jira Cycle Time Distribution (P50={p50:.1f}d, P75={p75:.1f}d, P95={p95:.1f}d)',
                source="Jira",
                x_title='Days (In Progress to Done)', y_title='Issues')
            zcs.add_reference_line(config, "x", "1", "DORA Elite: < 1 day", color=zcs.TL_STATUS["green"])
            zcs.write_echarts_json(config, f'{CHARTS_DIR}/jira_cycle_time.json')

    if project_counts:
        pc_items = []
        for key, entry in project_counts.items():
            if isinstance(entry, dict):
                count = entry.get('count', 0)
            else:
                count = entry if isinstance(entry, (int, float)) else 0
            if isinstance(count, (int, float)) and count > 0:
                pc_items.append((key, int(count)))
        if pc_items:
            pc_items.sort(key=lambda x: x[1], reverse=True)
            config = zcs.pareto_config(
                [p[0] for p in pc_items],
                [p[1] for p in pc_items],
                title="Issue Concentration by Project",
                source="Jira")
            zcs.write_echarts_json(config, f'{CHARTS_DIR}/jira_issue_pareto.json')

    print(f"  -> {CHARTS_DIR}/jira_*.json charts generated")

# ─── CONFLUENCE ─────────────────────────────────────────────────────────

def generate_confluence_analysis():
    print("\n=== Confluence Analysis ===", flush=True)
    spaces = load_json('inventory/confluence/spaces.json') or []
    if spaces:
        rows = []
        for s in spaces:
            pc = s.get('page_count', 0)
            rows.append({
                'key': s.get('key', ''), 'name': s.get('name', ''),
                'type': s.get('type', ''), 'status': s.get('status', ''),
                'page_count': pc if isinstance(pc, (int, float)) else 0,
                'recent_pages_count': len(s.get('recent_pages', [])),
            })
        df_spaces = pd.DataFrame(rows)
        df_spaces.to_csv(f'{CSV_DIR}/confluence_spaces.csv', index=False)
        print(f"  -> {CSV_DIR}/confluence_spaces.csv ({len(df_spaces)} rows)")

        top = df_spaces.nlargest(30, 'page_count')
        if not top.empty and top['page_count'].sum() > 0:
            sorted_top = top.sort_values('page_count')
            labels = sorted_top.apply(
                lambda r: f"{r['key']} ({r['name'][:25]})", axis=1).tolist()
            config = zcs.bar_config(
                labels,
                [{"text": "Pages", "values": sorted_top['page_count'].tolist()}],
                horizontal=True,
                title='Confluence: Top 30 Spaces by Page Count',
                source="Confluence",
                x_title='Pages', y_title='Space')
            zcs.write_echarts_json(config, f'{CHARTS_DIR}/confluence_page_density.json')

    print(f"  -> {CHARTS_DIR}/confluence_*.json charts generated")


# ─── V3 DATA ────────────────────────────────────────────────────────────

def generate_v3_analysis():
    print("\n=== V3 Analysis ===", flush=True)

    reviewer = load_json('inventory/bitbucket/reviewer_concentration.json')
    if reviewer and reviewer.get('global_top_20_reviewers'):
        top20 = reviewer['global_top_20_reviewers']
        df_rev = pd.DataFrame(top20)
        df_rev.to_csv(f'{CSV_DIR}/bb_reviewer_concentration.csv', index=False)
        print(f"  -> {CSV_DIR}/bb_reviewer_concentration.csv ({len(df_rev)} rows)")
        sorted_rev = df_rev.sort_values('total_reviews')
        config = zcs.bar_config(
            sorted_rev['name'].tolist(),
            [{"text": "Reviews", "values": sorted_rev['total_reviews'].tolist()}],
            horizontal=True,
            title='Top 20 PR Reviewers (Cross-Repo)',
            source="Bitbucket")
        zcs.write_echarts_json(config, f'{CHARTS_DIR}/bb_reviewer_concentration.json')

    scope = load_json('inventory/jira/scope_change.json')
    if scope:
        df_scope = pd.DataFrame(scope)
        df_scope.to_csv(f'{CSV_DIR}/jira_scope_change.csv', index=False)
        print(f"  -> {CSV_DIR}/jira_scope_change.csv ({len(df_scope)} rows)")
        if not df_scope.empty and 'scope_change_pct' in df_scope.columns:
            config = zcs.bar_config(
                df_scope['sprint'].tolist(),
                [
                    {"text": "Original Scope", "values": df_scope['original_scope'].tolist()},
                    {"text": "Added Mid-Sprint", "values": df_scope['added_mid_sprint'].tolist()},
                ],
                stacked=True,
                title='Sprint Scope Change: Original vs Added Mid-Sprint',
                source="Jira",
                x_title='Sprint', y_title='Issues')
            zcs.write_echarts_json(config, f'{CHARTS_DIR}/jira_scope_change.json')

    flow = load_json('inventory/jira/flow_distribution.json')
    if flow:
        for seg_name in ['overall', 'engineering']:
            seg_data = flow.get(seg_name, {})
            resolved = seg_data.get('resolved_90d', {})
            numeric = {k: v for k, v in resolved.items() if isinstance(v, (int, float)) and v > 0}
            if numeric:
                label = seg_name.replace('_', ' ').title()
                sorted_items = sorted(numeric.items(), key=lambda x: x[1])
                config = zcs.bar_config(
                    [k.title() for k, _ in sorted_items],
                    [{"text": "Issues Resolved", "values": [v for _, v in sorted_items]}],
                    horizontal=True,
                    title=f'Flow Distribution: Resolved Work, {label} (Last 90 Days)',
                    source="Jira",
                    x_title='Issues Resolved', y_title='Work Type')
                suffix = f'_{seg_name}' if seg_name != 'overall' else ''
                zcs.write_echarts_json(config, f'{CHARTS_DIR}/jira_flow_distribution{suffix}.json')

    assignee = load_json('inventory/jira/assignee_concentration.json')
    if assignee and assignee.get('top_30_assignees'):
        df_assign = pd.DataFrame(assignee['top_30_assignees'])
        df_assign.to_csv(f'{CSV_DIR}/jira_assignee_load.csv', index=False)
        print(f"  -> {CSV_DIR}/jira_assignee_load.csv ({len(df_assign)} rows)")
        role_col = 'role_classification' if 'role_classification' in df_assign.columns else 'is_overloaded'
        top20 = df_assign.sort_values('open_issues').tail(20)
        names = top20['name'].tolist()
        roles = sorted(top20[role_col].unique())
        series = []
        for role in roles:
            vals = [int(row['open_issues']) if row[role_col] == role else 0
                    for _, row in top20.iterrows()]
            series.append({"text": str(role), "values": vals})
        config = zcs.bar_config(
            names, series,
            horizontal=True, stacked=True,
            title='Top 20 Assignees by Open Issue Count (by Role)',
            source="Jira")
        zcs.write_echarts_json(config, f'{CHARTS_DIR}/jira_assignee_load.json')

    tags = load_json('inventory/bitbucket/deploy_tags.json')
    if tags and tags.get('repos'):
        repos_with = [r for r in tags['repos'] if r.get('has_releases')]
        if repos_with:
            tag_rows = []
            for r in repos_with:
                for month, count in r.get('monthly_tags', {}).items():
                    tag_rows.append({'repo': f"{r['workspace']}/{r['repo']}", 'month': month, 'tags': count})
            if tag_rows:
                df_tags = pd.DataFrame(tag_rows)
                months_list = sorted(df_tags['month'].unique())
                series = []
                for repo_name, group in df_tags.groupby('repo'):
                    month_vals = dict(zip(group['month'], group['tags']))
                    vals = [int(month_vals.get(m, 0)) for m in months_list]
                    series.append({"text": repo_name, "values": vals})
                config = zcs.bar_config(
                    months_list, series,
                    title='Deployment Tag Frequency by Repo (6 Months)',
                    source="Bitbucket",
                    x_title='Month', y_title='Tags')
                zcs.write_echarts_json(config, f'{CHARTS_DIR}/bb_deploy_tags.json')

    creation = load_json('inventory/confluence/creation_trend.json')
    if creation:
        valid = [c for c in creation if 'error' not in c]
        if valid:
            df_create = pd.DataFrame(valid)
            config = zcs.bar_config(
                df_create['week_start'].tolist(),
                [{"text": "Pages Created", "values": df_create['pages_created'].tolist()}],
                title='Confluence Page Creation Trend (26 Weeks)',
                source="Confluence",
                x_title='Week', y_title='Pages Created')
            zcs.add_zoom_preview(config)
            zcs.write_echarts_json(config, f'{CHARTS_DIR}/confluence_creation_trend.json')

    print(f"  -> {CHARTS_DIR}/v3 charts generated")


# ─── MAIN ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    generate_aws_analysis()
    generate_bitbucket_analysis()
    generate_jira_analysis()
    generate_confluence_analysis()
    generate_v3_analysis()

    charts = glob.glob(f'{CHARTS_DIR}/*.json')
    csvs = glob.glob(f'{CSV_DIR}/*.csv')
    print(f"\n=== Complete ===")
    print(f"  Charts: {len(charts)} HTML files in {CHARTS_DIR}/")
    print(f"  CSVs: {len(csvs)} files in {CSV_DIR}/")
    for c in sorted(csvs):
        print(f"    {c}")
    for c in sorted(charts):
        print(f"    {c}")
    print("\nDone.", flush=True)
