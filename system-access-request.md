# System Access Request — Draft Message

**Context:** This message is from Adam to whoever Don identifies as the right person to coordinate system access. Adjust the recipient and tone based on who it goes to (could be an IT admin, could be Chathura or an engineering lead).

---

## Option A: If going through Don (Don forwards or introduces Adam)

**Subject:** System access for technology review — read-only, pre-April 13

Hi [Name],

Don asked me to reach out to coordinate some system access ahead of the technology review I'm doing with the team the week of April 13th.

I'm looking for **read-only / guest access** to the following systems. I don't need admin or write access to anything — just enough visibility to do some baseline analysis before I arrive onsite.

**Priority (need these first):**

1. **GitHub** (or whatever source control is in use) — read-only access to repositories. I'm looking at repo inventory, commit patterns, PR review cycles, CI/CD pipeline configuration, and testing coverage. Guest/viewer access is fine.

2. **Jira** (or project management tool) — read-only access to projects. I'm looking at sprint velocity trends, ticket lifecycle, backlog health, and cross-team dependencies. Viewer access is fine.

3. **AWS Console** — read-only access. I'm looking at service inventory, deployment architecture, monitoring/alerting configuration, and cost allocation patterns. The IAM ReadOnlyAccess managed policy is perfect if that's easiest.

**Nice to have (if easy to arrange):**

4. **Monitoring / Observability dashboards** — whatever the team uses (Datadog, New Relic, CloudWatch, Grafana, etc.). Read-only / viewer.

5. **Internal wiki / documentation** — Confluence, Notion, Guru, or wherever architecture docs, runbooks, and post-mortems live. Viewer access.

6. **Slack or Teams** — temporary guest account for the duration of the engagement (now through ~April 25). I'll use it for interview coordination, async follow-ups, and a dedicated project channel. I can work with DMs if a full guest account is complicated.

**What I need from you:**
- Which of these systems can you set up guest/read-only access for?
- Any that require additional approval (security review, etc.)?
- What information do you need from me? (email, SSH key, etc.)

My email: [adam's email]

Happy to hop on a quick call if it's easier to walk through. No rush on everything at once — if we can get GitHub and Jira first, that's the highest value for the pre-work.

Thanks,
Adam

---

## Option B: Shorter version if Don is handling it directly

**Subject:** System access list for Adam

Hey Don,

Here's what I need for pre-work. All read-only:

1. **GitHub** — repo viewer access (commit patterns, PR cycles, CI/CD config)
2. **Jira** — project viewer (sprint velocity, ticket lifecycle, backlog)
3. **AWS Console** — ReadOnlyAccess IAM policy (service inventory, deployment architecture, monitoring)
4. **Monitoring dashboards** — whatever they use (Datadog, New Relic, etc.)
5. **Wiki/docs** — Confluence, Notion, Guru, wherever arch docs and post-mortems live
6. **Slack or Teams** — temp guest account for the engagement

GitHub and Jira are the highest priority — those give me the most pre-work value. AWS is next. The rest are nice-to-haves.

Who should I coordinate with? Happy to deal directly with IT or whoever manages access.

Adam

---

## Notes for Adam

- Jorge Maltes (Director Information Technology, reports to Strainick) is likely the person who manages system access. But IT reports to the Chief People Officer, not the CTO — so you may need Don to make the introduction or Chathura to champion the request internally.
- The AWS ReadOnlyAccess managed IAM policy is the cleanest way to get console access without any write permissions. Suggest this specifically if they ask how to scope it.
- For GitHub, a "guest" or "outside collaborator" with read-only access to relevant orgs/repos is standard.
- System access was flagged on the phone call as potentially being "a bit of work" — get this moving ASAP. It has the longest lead time of any pre-work item.
