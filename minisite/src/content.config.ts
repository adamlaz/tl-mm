/**
 * Content collection registry for the Mad Mobile engagement minisite.
 *
 * Each collection maps to a CSV or JSON file in the parent repo's `analysis/`
 * or `inventory/` directory. Schemas are intentionally loose (`z.string().default('')`)
 * because upstream data quality varies — validation happens at the page level.
 */
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

const bbAiTooling = defineCollection({
  loader: csvLoader({ path: '../analysis/bb_ai_tooling.csv' }),
  schema: z.object({
    workspace: str,
    repo: str,
    language: str,
    ai_files_found: str,
    has_ai_tooling: str,
    tools_detected: str,
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

const jiraAssigneeLoad = defineCollection({
  loader: csvLoader({ path: '../analysis/jira_assignee_load.csv', idColumn: 'name' }),
  schema: z.object({
    name: str,
    open_issues: str,
    bugs: str,
    stories: str,
    tasks: str,
    epics: str,
    other: str,
    project_count: str,
    projects: str,
    role_classification: str,
    primary_category: str,
    engineering_projects: str,
    customer_success_projects: str,
    operations_projects: str,
    is_overloaded: str,
  }),
});

const jiraScopeChange = defineCollection({
  loader: csvLoader({ path: '../analysis/jira_scope_change.csv' }),
  schema: z.object({
    board: str,
    sprint: str,
    sprint_id: str,
    start_date: str,
    total_issues: str,
    sampled: str,
    original_scope: str,
    added_mid_sprint: str,
    unknown: str,
    scope_change_pct: str,
    done_issues: str,
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

const peopleDirectory = defineCollection({
  loader: csvLoader({ path: '../analysis/people_directory.csv', idColumn: 'id' }),
  schema: z.object({
    id: str,
    display_name: str,
    title: str,
    team: str,
    manager: str,
    division: str,
    geography: str,
    status: str,
    email: str,
    activity_level: str,
    systems_active_90d: str,
    total_activity_90d: str,
    systems: str,
    bb_workspaces: str,
    prs_authored: str,
    prs_reviewed: str,
    jira_created_90d: str,
    jira_resolved_90d: str,
    jira_open_assigned: str,
    jira_bugs_90d: str,
    jira_projects: str,
    jira_role: str,
    confluence_pages_total: str,
    confluence_pages_90d: str,
    aliases: str,
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
    estimated_annual_cost: z.string().optional(),
    pricing_model: z.string().optional(),
    pricing_notes: z.string().optional(),
    teams_using: z.array(z.string()).optional(),
    shared_or_individual: z.string().optional(),
    overlap_with: z.array(z.string()).optional(),
    interview_question: z.string().nullable().optional(),
  }),
});

const awsCostSavings = defineCollection({
  loader: csvLoader({ path: '../analysis/aws_cost_savings.csv' }),
  schema: z.object({
    task: str,
    domain: str,
    category: str,
    start_date: str,
    end_date: str,
    monthly_savings: str,
    yearly_savings: str,
    notes: str,
    jira_ticket: str,
  }),
});

export const collections = {
  awsCosts,
  awsResources,
  awsCostSavings,
  bitbucketRepos,
  bitbucketPRs,
  bitbucketCommits,
  bbAiTooling,
  jiraProjects,
  jiraVelocity,
  jiraCycleTime,
  jiraAssigneeLoad,
  jiraScopeChange,
  confluenceSpaces,
  confluencePages,
  userAudit,
  peopleDirectory,
  toolingCatalog,
};
