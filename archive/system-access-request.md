# System Access Request — Mad Mobile Engagement

**From:** Adam Lazarus

**Context:** This is the detailed access request for pre-work. Don shared a coordination brief with Chathura and Kennedy covering the engagement overview — this document is the specific "what I need and why" for whoever provisions access.

Access comes in two phases. Phase 1 is standard viewer/read-only — enough for me to see the landscape. Phase 2 is programmatic access (API tokens, CLI, service accounts) so I can deploy AI tooling against the systems for automated analysis. Phase 2 requests come as follow-ups once I know what I'm working with.

---

## Phase 1 — Read-Only / Viewer Access (by April 1)

Initial reconnaissance. I need to see how systems are structured, pull baseline metrics, and understand the landscape before arriving onsite April 13.

**Priority (need these first):**

1. **Source control** (GitHub or equivalent) — read-only access to repositories. I'm looking at repo inventory, commit patterns, PR review cycles, CI/CD pipeline config, and testing coverage. Guest/viewer or outside collaborator with read-only is fine.

2. **Project management** (Jira or equivalent) — read-only access to projects. Sprint velocity trends, ticket lifecycle, backlog health, cross-team dependencies. Viewer access is fine.

3. **Cloud infrastructure** (AWS or equivalent) — read-only console access. Service inventory, deployment architecture, monitoring/alerting config, cost allocation. The IAM `ReadOnlyAccess` managed policy is the cleanest way to scope this.

**Also needed (if easy to arrange):**

4. **Monitoring / observability** — whatever the team uses (Datadog, New Relic, CloudWatch, Grafana, etc.). Viewer access.

5. **Internal documentation** — Confluence, Notion, Guru, or wherever architecture docs, runbooks, and post-mortems live. Viewer access.

6. **Slack or Teams** — temporary guest account for the engagement duration (now through ~April 25). I'll set up a dedicated coordination channel and use DMs for async follow-ups.

---

## Phase 2 — Programmatic / CLI / API Access (escalating during pre-work)

Once I can see the systems, I'll know exactly what to point tooling at. Phase 2 is where the real pre-work value comes from — not just viewing dashboards but running automated scans, pulling data via API, and connecting AI analysis tooling to the infrastructure.

**What I'll need for each system (specific requests come as follow-ups):**

- **API tokens / personal access tokens** — GitHub PAT, Jira API token, cloud provider API keys, etc.
- **CLI access** — AWS CLI with appropriate IAM role, GitHub CLI, any other CLI tooling the team uses
- **IAM roles / service accounts** — scoped to read operations (actual API-level read access, not just console viewer)
- **MCP server access** or equivalent programmatic integration points where supported
- **Data export capabilities** — webhook access, bulk export, or query APIs for pulling data into my analysis pipeline

**How this works in practice:** I'll send follow-up requests within a few days of getting Phase 1 access. Each follow-up will be scoped to specific systems with specific read-level permissions. I'm not asking for write or admin access — this is about reading data and running analysis, not touching production systems.

---

## What I'm Doing With This Access

For anyone in IT or security who wants to know why an outside consultant needs programmatic API access:

I use AI-augmented tooling (Cursor, custom analysis scripts, API integrations) to produce quantitative baselines from engineering systems — things like deployment frequency, PR cycle times, incident patterns, architecture topology, and cost allocation. This is the data foundation that turns the onsite from "tell me about your process" into "I can see your numbers — walk me through why."

**What I am NOT doing:**
- Making changes to any production system
- Writing to any repository, ticket, or infrastructure resource
- Running anything that affects system performance or availability
- Accessing customer/user data (PII, payment data, etc.)
- Retaining access beyond the engagement duration (~April 25)

All findings stay within NDA scope. Access gets revoked after the engagement wraps.

---

## Quick Summary for Don

Hey Don,

Here's what I need for pre-work. Two phases:

**Phase 1 — viewer access (by April 1):**
1. Source control (GitHub or equivalent) — repo viewer
2. Project management (Jira or equivalent) — project viewer
3. Cloud infrastructure (AWS or equivalent) — ReadOnlyAccess IAM policy
4. Monitoring dashboards — whatever they use
5. Wiki/docs — wherever architecture docs and post-mortems live
6. Slack or Teams — temp guest account

**Phase 2 — programmatic/API access (follow-ups after Phase 1):**
Once I can see the systems, I'll send specific requests for API tokens, CLI access, and service accounts so I can run automated analysis. All read-only, all scoped.

Source control and project management are the highest priority — those give me the most pre-work value. Cloud infrastructure is next. The rest are nice-to-haves for Phase 1.

Who should I coordinate with? Happy to deal directly with IT or whoever manages access.

Adam

---

## Phase 2 Follow-Up Template

Use this when sending specific programmatic access requests after Phase 1 is provisioned:

**Subject:** Follow-up access request — [System Name] API/CLI

Hi [Name],

Thanks for getting the viewer access set up. Now that I can see [System], I'd like to connect my analysis tooling to pull data programmatically. Here's what I need:

- **System:** [e.g., GitHub]
- **Access type:** [e.g., Personal Access Token with `repo:read` and `org:read` scopes]
- **What I'm doing with it:** [e.g., Automated repo analysis — commit frequency, PR cycle times, contributor patterns, CI/CD pipeline health]
- **Duration:** Through ~April 25 (engagement end)

This is read-only — I won't be writing to any repos, changing any configs, or accessing anything outside the scoped permissions.

Let me know if you need anything else from my side to set this up.

Thanks,
Adam

---

## Notes (for Adam)

- **Jorge Maltes** (Director Information Technology, reports to Strainick) is the likely access contact. But IT reports to the Chief People Officer, not the CTO — Don may need to make the introduction or Chathura may need to champion the request internally.
- For AWS, the `ReadOnlyAccess` managed IAM policy is the cleanest Phase 1 scope. For Phase 2, a custom IAM role or programmatic user with specific read-level API permissions may be needed.
- For GitHub, "outside collaborator" with read-only is standard for Phase 1. A PAT with `repo:read` scope is Phase 2.
- System access was flagged on the March 24 call as potentially being "a bit of work." Get Phase 1 moving ASAP — it has the longest lead time of any pre-work item.
- Chathura is the engineering-side champion for access requests per v12 Section 9.8. The coordination brief already tells him access is his responsibility by April 1.
- Phase 2 requests will vary by system. Some may be trivial (Jira API token = 2 minutes). Others may require security review (AWS programmatic access, monitoring API keys). Plan for variance.
