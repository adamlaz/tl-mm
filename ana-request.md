**Subject:** Pre-work follow-up: Access requests and questions

Hi Ana,

Thank you for all the access provisioning — everything moved quickly and I'm grateful. Bitbucket (all four workspaces), Jira, Confluence, AWS SSO (18 accounts), Microsoft Teams, and email are all working. I've been able to run initial inventory scans across all of these and have some solid data to work with ahead of the onsite.

A few items surfaced during the scan that I'd love your help with:

---

### 1. Monitoring / Observability Access

I found that Mad Mobile runs a self-hosted Grafana stack (Mimir for metrics, Loki for logs, Tempo for traces) in the Shared Services AWS account, and there appears to be a separate Grafana instance for Payments. I'd love viewer access to these Grafana dashboards if possible — they'll be important for understanding system health and alerting maturity ahead of the onsite. Could you check with Matias or the cloud team on the best way to get me read-only access?

### 2. Other Internal Platforms

A couple of tools were mentioned in the pre-read materials that I haven't seen access for yet:
- **Guru** — mentioned as an AI-produced documentation platform. Is this still in use? If so, I'd appreciate viewer access.
- **Survey tool** — I know you were checking with HR on what's available internally. Any update on that? I have Google Forms ready as a fallback, but using the internal tool would be better for adoption. The target date for survey deployment is Monday, April 7.

### 3. Phase 2 Programmatic Access (No Rush)

For the deeper analysis after the initial scan, I may need:
- **Jira API token** — the current JQL search endpoints are returning 410 errors for issue counts and distribution queries. A personal API token would let me use the newer REST API to pull backlog health metrics.
- **AWS Cost Explorer** — I have cost data for most accounts, but a few had access restrictions on Secrets Manager and CloudWatch alarm details. Matias may be able to adjust the audit role permissions if needed.

These aren't urgent — they're for Phase 2 analysis after the onsite.

### 4. Questions for Internal Routing

A few things came up during the AWS inventory that I couldn't identify from the systems alone. Could you help route these to the right person?

- **MenuPad-Prod-Metro** (AWS account 622065827965): This has a running EC2 instance but I can't tell what product or customer it serves. The instance names don't match current product vocabulary. Is this a legacy deployment for a specific customer?

- **Monvia** (AWS account 219788358213): This has a running instance on very old hardware (m1.medium — circa 2012). One of the stopped instances is named "leapset-svn," which suggests it's from the Sysco Labs / Leapset era. Does anyone know what Monvia was, and whether the running instance can be decommissioned?

- **Neo/AI platform infrastructure**: I didn't find a dedicated AWS account for Neo. There are active Jira projects (NEO, AAK, LAA) and Confluence spaces, but where does the AI platform actually run in production? This would be helpful context for the architecture discussions with Jack and Chathura.

- **Relate** (in the MM-Archive AWS account): There are EC2 instances named "Relate1" and "Relate2" (one running), plus a running FTP server. What is Relate, and is the FTP server still needed?

---

None of this is blocking — the inventory data I have is plenty to prepare for the onsite. These are just things that would sharpen the picture before April 13.

Thanks again for keeping everything moving so smoothly.

Best,
Adam
