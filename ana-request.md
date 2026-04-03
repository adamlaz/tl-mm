**Subject:** Pre-work follow-up: Access requests, questions, and early findings

Hi Ana,

Thank you for all the access provisioning — everything moved quickly and I'm grateful. Bitbucket (all four workspaces), Jira, Confluence, AWS SSO (18 accounts), Microsoft Teams, and email are all working. I've completed two rounds of automated inventory scans across all of these and have solid quantitative data to work with ahead of the onsite.

A quick summary of what I've been able to see so far (for context on the requests below), and then the asks:

**What the scans covered:**
- All 18 AWS accounts: service inventory, cost data, resource counts, IAM posture, IaC coverage
- All 4 Bitbucket workspaces: 3,191 repos inventoried, pipeline coverage, PR metrics, commit frequency
- Jira: 141 projects, 313 boards, sprint velocity across 19 active scrum boards, issue distribution, cycle time
- Confluence: 165 spaces with page counts, content search across 14 key terms

This is all read-only analysis — nothing was written or modified in any system.

---

### 1. Monitoring / Observability Access

I found that Mad Mobile runs a self-hosted **Grafana** stack (Mimir for metrics, Loki for logs, Tempo for traces) in the Shared Services AWS account, and there appears to be a separate Grafana instance for Payments. I'd love **viewer access to these Grafana dashboards** — they'll be important for understanding system health, alerting maturity, and on-call patterns ahead of the onsite.

Could you check with Matias or the cloud team on the best way to get me read-only access? A Grafana viewer account would be ideal.

### 2. Other Internal Platforms

A couple of tools mentioned in the pre-read materials that I haven't seen access for:
- **Guru** — mentioned as an AI-produced documentation platform. Is this still in use? If so, I'd appreciate viewer access.
- **Survey tool** — I know you were checking with HR on what's available internally. Any update? I have Google Forms ready as a fallback, but using the internal tool would be better for adoption. The target date for survey deployment is **Monday, April 7**.

### 3. AWS CloudWatch Permissions

The read-only audit role (Global-Audit-RO) I have works well for most services, but it lacks permissions for `cloudwatch:DescribeAlarms`. This means I can see dashboards but not the alerting rules behind them. If Matias or the cloud team can add `cloudwatch:DescribeAlarms` and `cloudwatch:DescribeAlarmHistory` to the audit role, that would let me assess alerting coverage without any broader access changes. Not urgent — this can wait until after the onsite if easier.

### 4. Questions for Internal Routing

The inventory surfaced several things I couldn't identify from the systems alone. Could you help route these to whoever would know?

- **Monvia** (AWS account 219788358213): This is spending **~$25,900/month**, which is significantly more than I'd expect for what appears to be a legacy Leapset/Sysco Labs acquisition artifact. One instance is still running on m1-generation hardware (circa 2012). Another stopped instance is named "leapset-svn." Does anyone know what Monvia is, whether those workloads are still needed, and who owns that account's budget?

- **MenuPad-Prod-Metro** (AWS account 622065827965): Running ~$2,000/month with a live EC2 instance (`venom_new`, r4.xlarge). The instance names don't match current product vocabulary. Is this a legacy deployment for a specific customer?

- **Relate** (in the MM-Archive AWS account): EC2 instances named "Relate1" and "Relate2" (one running), plus a running FTP server (`Mad-Ftp2`). What is Relate, and is the FTP server still needed?

- **Neo/AI platform infrastructure**: I didn't find a dedicated AWS account for Neo. There are active Jira projects (NEO, AAK, LAA) and Confluence spaces, and I found SageMaker artifacts in the CAKE R&D account, but where does the AI platform actually run in production? This would be helpful context for the architecture discussions with Jack and Chathura.

### 5. Cost Observation Worth Flagging

The Madmobile Mgmt account shows **~$309,000/month** in March 2026. This is likely org-level consolidated billing or reserved instance charges rolled up to the management account — not actual compute. But it's worth confirming with the cloud team whether that's the billing structure, because if those are actual workloads running in the management account, that would be unusual. Matias or Matthew Griffin would know.

---

None of this is blocking — the inventory data I have is plenty to prepare for the onsite. These are just things that would sharpen the picture before April 13.

Thanks again for keeping everything moving so smoothly.

Best,
Adam
