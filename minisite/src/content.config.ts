import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { csvLoader } from './loaders/csv';
import { jsonExtractLoader } from './loaders/json-extract';

const str = z.string().default('');

const awsCosts = defineCollection({
  loader: csvLoader({ path: '../analysis/aws_cost_summary.csv' }),
  schema: z.object({
    profile: str,
    account_id: str,
    month: str,
    service: str,
    cost: str,
  }),
});

const awsResources = defineCollection({
  loader: csvLoader({ path: '../analysis/aws_resource_inventory.csv' }),
  schema: z.object({
    profile: str,
    account_id: str,
    region: str,
    type: str,
    id: str,
    name: str,
    state: str,
    instance_type: str,
    is_graviton: str,
    is_pre_graviton: str,
    runtime: str,
    is_eol: str,
    memory_mb: str,
    last_modified: str,
    engine: str,
    instance_class: str,
    multi_az: str,
    status: str,
    created: str,
  }),
});

const bitbucketRepos = defineCollection({
  loader: csvLoader({ path: '../analysis/bitbucket_repos.csv' }),
  schema: z.object({
    workspace: str,
    slug: str,
    name: str,
    language: str,
    project: str,
    is_active: str,
    updated_on: str,
    created_on: str,
    has_pipeline: str,
    open_prs: str,
    merged_30d: str,
  }),
});

const bitbucketPRs = defineCollection({
  loader: csvLoader({ path: '../analysis/bitbucket_pr_metrics.csv', idColumn: 'id' }),
  schema: z.object({
    id: str,
    title: str,
    author: str,
    created: str,
    merged: str,
    cycle_hours: str,
    workspace: str,
    repo: str,
  }),
});

const bitbucketCommits = defineCollection({
  loader: csvLoader({ path: '../analysis/bitbucket_commit_frequency.csv' }),
  schema: z.object({
    workspace: str,
    repo: str,
    week: str,
    commits: str,
  }),
});

const jiraProjects = defineCollection({
  loader: csvLoader({ path: '../analysis/jira_project_classification.csv', idColumn: 'key' }),
  schema: z.object({
    key: str,
    name: str,
    style: str,
    type_key: str,
    lead: str,
    category: str,
    issue_count: str,
    classification: str,
  }),
});

const jiraVelocity = defineCollection({
  loader: csvLoader({ path: '../analysis/jira_velocity.csv' }),
  schema: z.object({
    board: str,
    sprint: str,
    start_date: str,
    end_date: str,
    complete_date: str,
    done_issues: str,
    total_issues: str,
    completion_rate: str,
  }),
});

const jiraCycleTime = defineCollection({
  loader: csvLoader({ path: '../analysis/jira_cycle_time.csv', idColumn: 'key' }),
  schema: z.object({
    key: str,
    project: str,
    type: str,
    created: str,
    resolved: str,
    total_lead_time_days: str,
    cycle_time_days: str,
  }),
});

const confluenceSpaces = defineCollection({
  loader: csvLoader({ path: '../analysis/confluence_spaces.csv', idColumn: 'key' }),
  schema: z.object({
    key: str,
    name: str,
    type: str,
    status: str,
    page_count: str,
    recent_pages_count: str,
  }),
});

const confluencePages = defineCollection({
  loader: csvLoader({ path: '../analysis/confluence_page_index.csv', idColumn: 'id' }),
  schema: z.object({
    id: str,
    title: str,
    space_key: str,
    status: str,
    created_at: str,
    version_number: str,
    version_created_at: str,
    author: str,
  }),
});

const userAudit = defineCollection({
  loader: csvLoader({ path: '../analysis/user_audit.csv', idColumn: 'display_name' }),
  schema: z.object({
    display_name: str,
    activity_level: str,
    systems_active_90d: str,
    total_activity_90d: str,
    bb_workspaces: str,
    bb_workspace_count: str,
    bb_prs_authored: str,
    bb_prs_reviewed: str,
    jira_issues_created_90d: str,
    jira_issues_resolved_90d: str,
    jira_open_assigned: str,
    jira_bugs_created_90d: str,
    jira_role: str,
    jira_projects: str,
    confluence_pages_total: str,
    confluence_pages_90d: str,
  }),
});

const toolingCatalog = defineCollection({
  loader: jsonExtractLoader({
    path: '../inventory/tooling_catalog.json',
    key: 'tools',
    idField: 'name',
  }),
  schema: z.object({
    name: z.string(),
    vendor: z.string(),
    category: z.string(),
    status: z.string(),
    source: z.string(),
    cost_status: z.string(),
    notes: z.string().optional(),
    cost_detail: z.string().optional(),
  }),
});

export const collections = {
  awsCosts,
  awsResources,
  bitbucketRepos,
  bitbucketPRs,
  bitbucketCommits,
  jiraProjects,
  jiraVelocity,
  jiraCycleTime,
  confluenceSpaces,
  confluencePages,
  userAudit,
  toolingCatalog,
};
