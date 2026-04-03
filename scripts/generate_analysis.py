#!/usr/bin/env python3
"""Generate CSVs, interactive charts, and summary from all inventory data."""

import json
import os
import glob
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import defaultdict

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
            fig = px.bar(x=acct_totals.values, y=acct_totals.index, orientation='h',
                         title='AWS Monthly Cost by Account (March 2026)',
                         labels={'x': 'Cost (USD)', 'y': 'Account'})
            fig.update_layout(height=600, margin=dict(l=200))
            fig.write_html(f'{CHARTS_DIR}/aws_cost_by_account.html')

            top_services = march.groupby('service')['cost'].sum().nlargest(15).sort_values(ascending=True)
            fig2 = px.bar(x=top_services.values, y=top_services.index, orientation='h',
                          title='AWS Top 15 Services by Cost (March 2026)',
                          labels={'x': 'Cost (USD)', 'y': 'Service'})
            fig2.update_layout(height=500, margin=dict(l=300))
            fig2.write_html(f'{CHARTS_DIR}/aws_cost_by_service.html')

        monthly_trend = df_cost.groupby(['month', 'profile'])['cost'].sum().reset_index()
        if not monthly_trend.empty:
            fig3 = px.line(monthly_trend, x='month', y='cost', color='profile',
                           title='AWS Cost Trend by Account (3 months)')
            fig3.update_layout(height=500)
            fig3.write_html(f'{CHARTS_DIR}/aws_cost_trend.html')

    if resources:
        df_res = pd.DataFrame(resources)
        df_res.to_csv(f'{CSV_DIR}/aws_resource_inventory.csv', index=False)
        print(f"  -> {CSV_DIR}/aws_resource_inventory.csv ({len(df_res)} rows)")

        type_counts = df_res.groupby(['profile', 'type']).size().reset_index(name='count')
        fig4 = px.bar(type_counts, x='profile', y='count', color='type',
                      title='AWS Resource Inventory by Account and Type')
        fig4.update_layout(height=500, xaxis_tickangle=-45, margin=dict(b=150))
        fig4.write_html(f'{CHARTS_DIR}/aws_resource_inventory.html')

    if lambda_audit.get('by_runtime'):
        rt_data = lambda_audit['by_runtime']
        eol_runtimes = {'python2.7', 'python3.6', 'python3.7', 'nodejs6.10', 'nodejs8.10',
                        'nodejs10.x', 'nodejs12.x', 'java8', 'dotnetcore2.1', 'dotnetcore3.1'}
        colors = ['#e74c3c' if r.lower() in eol_runtimes else '#3498db' for r in rt_data.keys()]
        fig5 = go.Figure(go.Bar(x=list(rt_data.keys()), y=list(rt_data.values()),
                                marker_color=colors))
        fig5.update_layout(title='Lambda Runtime Distribution (Red = EOL)',
                           xaxis_title='Runtime', yaxis_title='Count',
                           height=400, xaxis_tickangle=-45)
        fig5.write_html(f'{CHARTS_DIR}/aws_lambda_runtimes.html')

    print(f"  -> {CHARTS_DIR}/aws_*.html charts generated")

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
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Active', x=summary['workspace'], y=summary['active']))
        fig.add_trace(go.Bar(name='Stale', x=summary['workspace'], y=summary['stale']))
        fig.update_layout(barmode='stack', title='Bitbucket Repos: Active vs Stale by Workspace',
                          yaxis_title='Repositories', height=400)
        fig.write_html(f'{CHARTS_DIR}/bitbucket_repo_health.html')

        lang_counts = df_repos[df_repos['language'] != 'unknown'].groupby(
            ['workspace', 'language']).size().reset_index(name='count')
        if not lang_counts.empty:
            fig2 = px.treemap(lang_counts, path=['workspace', 'language'], values='count',
                              title='Bitbucket Language Distribution by Workspace')
            fig2.update_layout(height=600)
            fig2.write_html(f'{CHARTS_DIR}/bitbucket_languages.html')

        pipeline_data = df_repos[df_repos['has_pipeline'].notna()]
        if not pipeline_data.empty:
            pipe_summary = pipeline_data.groupby('workspace').agg(
                with_ci=('has_pipeline', 'sum'),
                total_checked=('has_pipeline', 'count'),
            ).reset_index()
            pipe_summary['without_ci'] = pipe_summary['total_checked'] - pipe_summary['with_ci']
            fig3 = go.Figure()
            fig3.add_trace(go.Bar(name='Has CI/CD', x=pipe_summary['workspace'], y=pipe_summary['with_ci']))
            fig3.add_trace(go.Bar(name='No CI/CD', x=pipe_summary['workspace'], y=pipe_summary['without_ci']))
            fig3.update_layout(barmode='stack', title='Bitbucket Pipeline Coverage by Workspace',
                              yaxis_title='Active Repos', height=400)
            fig3.write_html(f'{CHARTS_DIR}/bitbucket_pipeline_coverage.html')

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

            fig4 = px.histogram(df_pr, x='cycle_hours', nbins=30,
                                title='PR Cycle Time Distribution (hours)',
                                labels={'cycle_hours': 'Hours from Created to Merged'})
            fig4.update_layout(height=400)
            fig4.write_html(f'{CHARTS_DIR}/bitbucket_pr_cycle_time.html')

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
            fig5 = px.bar(weekly_total, x='week', y='commits',
                          title='Weekly Commit Frequency (Top 30 Active Repos)')
            fig5.update_layout(height=400, xaxis_tickangle=-45)
            fig5.write_html(f'{CHARTS_DIR}/bitbucket_commit_frequency.html')

    print(f"  -> {CHARTS_DIR}/bitbucket_*.html charts generated")

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

    # Org-wide overview: issue volume by segment
    seg_totals = {}
    for seg in ['engineering', 'customer_success', 'operations']:
        seg_data = issue_dist.get(seg, {})
        total = sum(v for k, v in seg_data.items()
                    if isinstance(v, (int, float)) and k in ('bugs', 'stories', 'tasks', 'epics', 'subtasks'))
        seg_totals[seg] = total
    if seg_totals:
        fig_overview = px.pie(names=list(seg_totals.keys()), values=list(seg_totals.values()),
                              title='Jira: Issue Volume by Org Segment')
        fig_overview.update_layout(height=400)
        fig_overview.write_html(f'{CHARTS_DIR}/jira_org_overview.html')

    # Issue distribution: engineering vs overall
    for seg_name in ['overall', 'engineering']:
        seg_data = issue_dist.get(seg_name, {})
        type_counts = {k: v for k, v in seg_data.items()
                       if isinstance(v, (int, float)) and k in ('bugs', 'stories', 'tasks', 'epics', 'subtasks')}
        if type_counts:
            title = f'Issue Distribution by Type ({seg_name.replace("_", " ").title()})'
            fig = px.pie(names=list(type_counts.keys()), values=list(type_counts.values()), title=title)
            fig.update_layout(height=400)
            fig.write_html(f'{CHARTS_DIR}/jira_issue_distribution_{seg_name}.html')

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
            fig2 = px.line(df_top, x='complete_date', y='done_issues', color='board',
                           title='Sprint Velocity Trend (Top 10 Active Boards, Engineering)',
                           labels={'done_issues': 'Issues Completed', 'complete_date': 'Sprint End'})
            fig2.update_layout(height=500)
            fig2.write_html(f'{CHARTS_DIR}/jira_velocity_trend.html')

    # Backlog age: side-by-side segments
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
            fig3 = px.bar(df_age, x='age_bucket', y='count', color='segment', barmode='group',
                          title='Open Backlog Age Distribution (by Segment)',
                          labels={'age_bucket': 'Age Bucket', 'count': 'Open Issues'})
            fig3.update_layout(height=450)
            fig3.write_html(f'{CHARTS_DIR}/jira_backlog_age.html')

    # Created vs resolved: overall + engineering on same chart
    if created_resolved and isinstance(created_resolved, dict):
        fig4 = make_subplots(specs=[[{"secondary_y": True}]])
        for seg_name in ['overall', 'engineering']:
            seg_data = created_resolved.get(seg_name, [])
            valid = [w for w in seg_data if isinstance(w, dict) and 'error' not in w]
            if valid:
                df_cr = pd.DataFrame(valid)
                suffix = '' if seg_name == 'overall' else ' (Eng)'
                dash = None if seg_name == 'overall' else 'dash'
                fig4.add_trace(go.Scatter(x=df_cr['week_start'], y=df_cr['created'],
                                          name=f'Created{suffix}', mode='lines+markers',
                                          line=dict(dash=dash)), secondary_y=False)
                fig4.add_trace(go.Scatter(x=df_cr['week_start'], y=df_cr['resolved'],
                                          name=f'Resolved{suffix}', mode='lines+markers',
                                          line=dict(dash=dash)), secondary_y=False)
        fig4.update_layout(title='Created vs Resolved: Overall and Engineering (Weekly, 6 months)',
                           height=500, xaxis_tickangle=-45)
        fig4.write_html(f'{CHARTS_DIR}/jira_created_vs_resolved.html')

    if cycle_time:
        df_ct = pd.DataFrame(cycle_time)
        df_ct.to_csv(f'{CSV_DIR}/jira_cycle_time.csv', index=False)
        print(f"  -> {CSV_DIR}/jira_cycle_time.csv ({len(df_ct)} rows)")

        ct_valid = df_ct[df_ct['cycle_time_days'].notna() & (df_ct['cycle_time_days'] > 0)]
        if not ct_valid.empty:
            p50 = ct_valid['cycle_time_days'].quantile(0.5)
            p75 = ct_valid['cycle_time_days'].quantile(0.75)
            p95 = ct_valid['cycle_time_days'].quantile(0.95)
            fig5 = px.histogram(ct_valid, x='cycle_time_days', nbins=30,
                                title=f'Jira Cycle Time Distribution (P50={p50:.1f}d, P75={p75:.1f}d, P95={p95:.1f}d)',
                                labels={'cycle_time_days': 'Days (In Progress to Done)'})
            fig5.add_vline(x=p50, line_dash="dash", annotation_text=f"P50: {p50:.1f}d")
            fig5.add_vline(x=p75, line_dash="dash", annotation_text=f"P75: {p75:.1f}d")
            fig5.update_layout(height=400)
            fig5.write_html(f'{CHARTS_DIR}/jira_cycle_time.html')

    print(f"  -> {CHARTS_DIR}/jira_*.html charts generated")

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
            fig = px.bar(top.sort_values('page_count'), x='page_count',
                         y=top.sort_values('page_count').apply(lambda r: f"{r['key']} ({r['name'][:25]})", axis=1),
                         orientation='h',
                         title='Confluence: Top 30 Spaces by Page Count',
                         labels={'x': 'Pages', 'y': 'Space'})
            fig.update_layout(height=700, margin=dict(l=250))
            fig.write_html(f'{CHARTS_DIR}/confluence_page_density.html')

    print(f"  -> {CHARTS_DIR}/confluence_*.html charts generated")


# ─── V3 DATA ────────────────────────────────────────────────────────────

def generate_v3_analysis():
    print("\n=== V3 Analysis ===", flush=True)

    reviewer = load_json('inventory/bitbucket/reviewer_concentration.json')
    if reviewer and reviewer.get('global_top_20_reviewers'):
        top20 = reviewer['global_top_20_reviewers']
        df_rev = pd.DataFrame(top20)
        df_rev.to_csv(f'{CSV_DIR}/bb_reviewer_concentration.csv', index=False)
        print(f"  -> {CSV_DIR}/bb_reviewer_concentration.csv ({len(df_rev)} rows)")
        fig = px.bar(df_rev.sort_values('total_reviews'), x='total_reviews', y='name',
                     orientation='h', title='Top 20 PR Reviewers (Cross-Repo)')
        fig.update_layout(height=500, margin=dict(l=200))
        fig.write_html(f'{CHARTS_DIR}/bb_reviewer_concentration.html')

    scope = load_json('inventory/jira/scope_change.json')
    if scope:
        df_scope = pd.DataFrame(scope)
        df_scope.to_csv(f'{CSV_DIR}/jira_scope_change.csv', index=False)
        print(f"  -> {CSV_DIR}/jira_scope_change.csv ({len(df_scope)} rows)")
        if not df_scope.empty and 'scope_change_pct' in df_scope.columns:
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Original Scope', x=df_scope['sprint'], y=df_scope['original_scope']))
            fig.add_trace(go.Bar(name='Added Mid-Sprint', x=df_scope['sprint'], y=df_scope['added_mid_sprint']))
            fig.update_layout(barmode='stack', title='Sprint Scope Change: Original vs Added Mid-Sprint',
                              height=500, xaxis_tickangle=-45, margin=dict(b=150))
            fig.write_html(f'{CHARTS_DIR}/jira_scope_change.html')

    flow = load_json('inventory/jira/flow_distribution.json')
    if flow:
        for seg_name in ['overall', 'engineering']:
            seg_data = flow.get(seg_name, {})
            resolved = seg_data.get('resolved_90d', {})
            numeric = {k: v for k, v in resolved.items() if isinstance(v, (int, float)) and v > 0}
            if numeric:
                label = seg_name.replace('_', ' ').title()
                fig = px.pie(names=list(numeric.keys()), values=list(numeric.values()),
                             title=f'Flow Distribution: Resolved Work, {label} (Last 90 Days)')
                fig.update_layout(height=400)
                suffix = f'_{seg_name}' if seg_name != 'overall' else ''
                fig.write_html(f'{CHARTS_DIR}/jira_flow_distribution{suffix}.html')

    assignee = load_json('inventory/jira/assignee_concentration.json')
    if assignee and assignee.get('top_30_assignees'):
        df_assign = pd.DataFrame(assignee['top_30_assignees'])
        df_assign.to_csv(f'{CSV_DIR}/jira_assignee_load.csv', index=False)
        print(f"  -> {CSV_DIR}/jira_assignee_load.csv ({len(df_assign)} rows)")
        role_col = 'role_classification' if 'role_classification' in df_assign.columns else 'is_overloaded'
        fig = px.bar(df_assign.sort_values('open_issues').tail(20),
                     x='open_issues', y='name', orientation='h',
                     title='Top 20 Assignees by Open Issue Count (by Role)',
                     color=role_col)
        fig.update_layout(height=500, margin=dict(l=200))
        fig.write_html(f'{CHARTS_DIR}/jira_assignee_load.html')

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
                fig = px.bar(df_tags, x='month', y='tags', color='repo',
                             title='Deployment Tag Frequency by Repo (6 months)')
                fig.update_layout(height=500, xaxis_tickangle=-45)
                fig.write_html(f'{CHARTS_DIR}/bb_deploy_tags.html')

    creation = load_json('inventory/confluence/creation_trend.json')
    if creation:
        valid = [c for c in creation if 'error' not in c]
        if valid:
            df_create = pd.DataFrame(valid)
            fig = px.bar(df_create, x='week_start', y='pages_created',
                         title='Confluence Page Creation Trend (26 Weeks)')
            fig.update_layout(height=400, xaxis_tickangle=-45)
            fig.write_html(f'{CHARTS_DIR}/confluence_creation_trend.html')

    print(f"  -> {CHARTS_DIR}/v3 charts generated")


# ─── MAIN ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    generate_aws_analysis()
    generate_bitbucket_analysis()
    generate_jira_analysis()
    generate_confluence_analysis()
    generate_v3_analysis()

    charts = glob.glob(f'{CHARTS_DIR}/*.html')
    csvs = glob.glob(f'{CSV_DIR}/*.csv')
    print(f"\n=== Complete ===")
    print(f"  Charts: {len(charts)} HTML files in {CHARTS_DIR}/")
    print(f"  CSVs: {len(csvs)} files in {CSV_DIR}/")
    for c in sorted(csvs):
        print(f"    {c}")
    for c in sorted(charts):
        print(f"    {c}")
    print("\nDone.", flush=True)
