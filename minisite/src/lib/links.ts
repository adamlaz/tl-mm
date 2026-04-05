const CONFLUENCE_BASE = 'https://madmobile-eng.atlassian.net/wiki';
const JIRA_BASE = 'https://madmobile-eng.atlassian.net';
const BITBUCKET_BASE = 'https://bitbucket.org';

export function confluenceSpaceUrl(key: string): string {
  return `${CONFLUENCE_BASE}/spaces/${key}`;
}

export function confluencePageUrl(pageId: string): string {
  return `${CONFLUENCE_BASE}/pages/${pageId}`;
}

export function jiraProjectUrl(key: string): string {
  return `${JIRA_BASE}/jira/software/projects/${key}/board`;
}

export function jiraIssueUrl(key: string): string {
  return `${JIRA_BASE}/browse/${key}`;
}

export function bitbucketRepoUrl(workspace: string, slug: string): string {
  return `${BITBUCKET_BASE}/${workspace}/${slug}`;
}

export function personUrl(slug: string): string {
  return `/people/${slug}`;
}

/**
 * Generate a person slug from display_name using the same logic as people_registry.py.
 * Handles the `(Unlicensed)` suffix that Atlassian adds to deactivated users.
 * Only use this as a fallback — prefer the `id` field from the CSV/JSON when available.
 */
export function personSlug(displayName: string): string {
  return displayName
    .toLowerCase()
    .trim()
    .replace(/\s+/g, '-')
    .replace(/\./g, '-');
}
