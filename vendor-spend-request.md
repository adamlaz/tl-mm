**For:** Don (verbal or async)
**Re:** Tooling and software spend — data needed for vendor utilization assessment

---

Hey Don,

One piece I want to include in the diagnostic is a vendor/tool utilization assessment — what the org pays for, what's actually used, and where there might be overlap or waste.

From the system scan, I've identified **28 tools** in active use across engineering, security, infrastructure, and AI. Some are included in AWS or Microsoft 365 licensing, but many are separate vendor contracts — and I don't have visibility into the cost side.

**What I need:**

1. **Annual or monthly SaaS/tool spend by vendor** — even a rough export from finance or procurement would work. The ones I'm most interested in:
   - Atlassian (Jira, Confluence, Bitbucket — how many seats?)
   - Cursor (how many seats? which teams?)
   - Wiz.io (annual contract?)
   - Snyk (if in use — seats or repo-based?)
   - Guru (still active? how many users?)
   - Figma (seats?)
   - Any monitoring/APM tools not visible in the infrastructure (Datadog, New Relic, PagerDuty, OpsGenie?)
   - Kafka/Confluent (if using Confluent vs open source)
   - Elasticsearch/Elastic (OSS vs subscription)
   - n8n (self-hosted vs cloud)

2. **Is there a centralized procurement process**, or do teams buy tools independently? This matters for understanding whether there's a single view of total tooling spend.

3. **Any recent tool consolidation or rationalization efforts** — have there been decisions to sunset tools or standardize?

**Why this matters for the assessment:**
- The org is running dual CI/CD (Jenkins + Bitbucket Pipelines) — is that intentional or inertia?
- Multiple AI tools are in use (Cursor, Claude/Anthropic, AWS Bedrock, SageMaker) — is there a coordinated AI strategy or are teams experimenting independently?
- Self-hosted observability (Grafana) is a mature choice, but the total cost of ownership vs. a managed service is worth understanding.
- 28 tools across a ~370-person company is a lot of surface area to maintain.

I can compile the full list of identified tools with where I found each one if that's helpful for the conversation with finance.

Adam
