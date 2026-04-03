# Mad Mobile Technology Inventory Summary

**Generated:** April 3, 2026
**Scope:** AWS (18 accounts), Bitbucket (4 workspaces), Jira, Confluence
**Access level:** Read-only audit (Global-Audit-RO role in AWS; viewer in Jira/Confluence/Bitbucket)

---

## AWS Summary (18 Accounts)

### Cost Overview (March 2026 estimated monthly)

| Account | ~Monthly Cost | Status |
|---|---|---|
| Retail Prod US | $12,800 | **Primary production** — heaviest account |
| Shared Services | $1,820 | Active — observability stack |
| Payments Prod US | $2,070 | Active — payments infrastructure |
| CAKE R&D | $1,290 | Active — dev/R&D workloads |
| CAKE Development | High (file truncated) | Active — dev/QA/CI |
| Madmobile Mgmt | Moderate | Org management account |
| Retail Prod EU | Low-Moderate | Active — EU Concierge deployment |
| Retail Prod APAC | Low-Moderate | Active — APAC Concierge deployment |
| Retail Prod US DR | Low-Moderate | DR — mirrors US prod |
| MM-Archive | Low | Legacy — running Relate FTP servers |
| MenuPad-Prod-Metro | Low | **Unknown product** — legacy instances |
| Monvia | Low | **Unknown product** — ancient instances (m1.small) |
| DNS Management | $262 | Active — Route53, domain registrations |
| Shared Artifact Registry | $45 | Active — ECR + CodeArtifact |
| Marketplace Seller | Low | AWS Marketplace seller functions |
| Customer Analytics | $3 | Near-dormant — one analytics bucket |
| Forensics | $36 | New (Jan 2026) — VPC provisioned, no workloads |
| Security | Low | ControlTower audit/config logging |

### Account-by-Account Detail

#### Retail Prod US (125062011444) — HEAVIEST ACCOUNT
- **45 EC2 instances** running (mostly m5a.xlarge, m7g.xlarge) — Concierge core-services fleet
- **1 EKS cluster**: `marvel-cloud-prod-us` (Concierge "Marvel" platform)
- **2 ECS clusters**: `redirector-us`, `shop-cpq`
- **41 Lambda functions**: per-customer analytics (Talbots, Guess, Brooks Brothers, Estee Lauder, Signet, Tractor Supply, Urban, Ralph Lauren, etc.), webhooks, SSO handlers
- **~97 S3 buckets**: per-customer analytics, MongoDB dumps, CDN, Helm charts, architecture docs
- **~100 ECR repositories**: management services (menu, store, register, user, organization, pricing, etc.)
- **5 CloudWatch dashboards**: CPU-Credit, CPU-Usage-ASGs, MM-Node, mongodb_backups, rabbitmq-mem
- **Amazon MQ**: $3,289/month — **largest single line item** (RabbitMQ cluster)
- **ElastiCache**: $547/month
- **CloudFormation**: 57 stacks including legacy stacks from 2016 (some in ROLLBACK_COMPLETE)
- **39 IAM users, 100 roles** — highest IAM complexity
- **Key finding**: This is where Concierge/Retail runs. The EC2 fleet + Amazon MQ + ElastiCache pattern suggests a traditional microservices architecture, not fully containerized.

#### Payments Prod US (491085393358)
- **No EC2 instances** — fully containerized on EKS
- **EKS-based**: S3 buckets for `pay-eks-*` Mimir/Loki suggest Grafana observability
- **RDS**: ~$102/month
- **EKS**: $165/month
- **ACM**: $724/month — unusually high, suggests many private CA certificates
- **Terraform state**: `tf-payments-prod-us-state` — infrastructure as code
- **61 IAM roles, 0 IAM users** — clean IAM posture
- **Key finding**: Payments is on a modern EKS stack with its own Grafana observability (Mimir + Loki). This is architecturally cleaner than the Retail account.

#### Shared Services (654654350563)
- **Observability hub**: S3 buckets for Loki (logs), Mimir (metrics), Tempo (traces)
- **EKS cluster**: running the centralized Grafana stack
- **S3**: $474/month — observability data storage
- **ELB**: $246/month — ingress for observability
- **No EC2/RDS** — lean infrastructure
- **Key finding**: This is the centralized observability stack. Grafana + Mimir + Loki + Tempo is a modern, self-hosted monitoring solution (not Datadog/New Relic). Need to verify who has access and which accounts feed into it.

#### CAKE Development (230930891673)
- **Many EC2 instances** including: Jenkins servers, payment-web QA, neo4j, Keycloak, data platform (Kafka, Elasticsearch), QE automation
- **Jenkins present** — confirms Jenkins as CI/CD tool (at least for CAKE/payments)
- **Multiple ECS clusters** for dev workloads
- **Key finding**: CAKE dev environment is EC2-heavy with traditional CI (Jenkins). Neo4j presence suggests graph database usage. Data platform has Kafka + Elasticsearch.

#### CAKE R&D (464176945335)
- **2 EC2 instances**: `DockerPos` (c6i.12xlarge — 48 vCPUs, $1.6K/month!), `rnd-cake-use1-ops-tools`
- **4 ECS clusters**: rnd-cde-secure-ecs, foo, default, cloudservices-rnd-fargate
- **42 Lambda functions**: many legacy (Python 2.7, Node 6/8/10/12) including security automation, Snyk integration, instance scheduling
- **8 VPCs** — sprawling network
- **19 DynamoDB tables**: Terraform state locks, deployment details
- **51 S3 buckets**: Terraform state, pipeline artifacts, SageMaker (ML!)
- **AWS Directory Service**: $67/month — Active Directory
- **Security Hub**: $11/month — enabled here
- **Key finding**: R&D has ML/SageMaker history, a massive DockerPos build server, and heavy Terraform usage. Many legacy Lambda runtimes need upgrading (Python 2.7, Node 6/8/10 are EOL).

#### MenuPad-Prod-Metro (622065827965) — UNKNOWN
- **EC2 instances**: `agony` (m3.large, stopped), `swarm` (m3.medium, stopped), `venom_new` (r4.xlarge, **running**)
- **Key finding**: Instance names don't match MM product vocabulary. m3 instance types are very old. `venom_new` is running — this may be a legacy MenuPad deployment for a specific customer (Metro?). Ask internally.

#### Monvia (219788358213) — UNKNOWN
- **3 EC2 instances**: `voip-new` (m1.small, stopped), `leapset-svn-Ubuntu12.04` (m1.medium, stopped), `monvia-vpc-new-setup` (m1.medium, **running**)
- **m1 instance types** — these are Gen 1 AWS instances from ~2012
- **Key finding**: "leapset-svn" confirms this is a Sysco Labs/Leapset acquisition artifact. Monvia appears to be a pre-CAKE Leapset product. One instance still running. SVN repo suggests pre-Git era code may exist here.

#### MM-Archive (673260261206)
- **EC2 instances**: `Relate1` (stopped), `Mad-Ftp2` (running), `Relate2` (running)
- **Key finding**: "Relate" may be a legacy product. Active FTP server suggests ongoing file transfer operations. Ask what Relate is and why FTP is still running.

#### Other Accounts
- **DNS Management**: Route53 zones for all MM domains. $258 in domain registrations in March.
- **Shared Artifact Registry**: ECR + CodeArtifact for centralized build artifacts. mm-techdocs-storage bucket suggests Backstage/TechDocs.
- **Marketplace Seller**: Lambda functions for AWS Marketplace entitlements — MM sells via AWS Marketplace.
- **Customer Analytics**: Near-dormant. Single "chefs-grille-analytics" bucket.
- **Forensics**: Brand new (Jan 2026). VPC provisioned, no workloads yet.
- **Security**: ControlTower audit account. Config/CloudTrail log centralization. Wiz.io integration (CloudFormation stacks).
- **Retail Prod EU/APAC/DR**: Regional Concierge deployments mirroring US structure.

### AWS Monitoring Posture
- **CloudWatch dashboards found in**: Retail Prod US (5 dashboards), CAKE R&D (1 — "Phoenix")
- **CloudWatch alarms**: Access denied across all accounts (audit role lacks `cloudwatch:DescribeAlarms`)
- **Grafana stack**: Shared Services runs Mimir (metrics) + Loki (logs) + Tempo (traces)
- **Payments has its own**: Mimir + Loki stack
- **Wiz.io**: Security scanning agent deployed across accounts (CloudFormation stacks)
- **GuardDuty**: Active across all accounts
- **No Datadog or New Relic detected** — monitoring is self-hosted Grafana

### Key AWS Findings
1. **CAKE runs in**: CAKE Development (dev/QA), CAKE R&D (R&D/build), and likely in the Retail Prod accounts (production CAKE POS backend services via the Concierge infrastructure)
2. **Retail/Concierge runs in**: Retail Prod US (primary), EU, APAC, US-DR
3. **No dedicated Neo/AI account**: AI work likely happens in CAKE R&D (SageMaker bucket exists) or within existing accounts
4. **Payments is architecturally cleanest**: EKS-native, IaC via Terraform, own observability stack
5. **Retail Prod US is architecturally oldest**: EC2 fleet, Amazon MQ, legacy CloudFormation from 2016
6. **Legacy debt**: MenuPad-Prod-Metro, Monvia, and MM-Archive have running instances on ancient instance types
7. **Jenkins is the CI server** (found in CAKE Development)
8. **Terraform is the IaC tool** (state buckets across many accounts)
9. **Cost optimization opportunities**: DockerPos c6i.12xlarge ($1.6K/month), Amazon MQ ($3.3K/month), stopped instances still incurring EBS costs

---

## Bitbucket Summary (4 Workspaces)

### Overview

| Workspace | Total Repos | Active | Stale | Pipeline Coverage (active) |
|---|---|---|---|---|
| madmobile | 1,422 | 370 (26%) | 1,052 (74%) | Not enumerated |
| syscolabs | 1,527 | 361 (24%) | 1,166 (76%) | Not enumerated |
| madpayments | 80 | 52 (65%) | 28 (35%) | 45 of 52 (87%) |
| syscolabsconf | 162 | 6 (4%) | 156 (96%) | 0 |
| **Total** | **3,191** | **789 (25%)** | **2,402 (75%)** | — |

### madmobile (Core Concierge/Retail)
- **1,422 repos** — largest workspace
- **Top languages**: NodeJS (158), JavaScript (134), C# (90), Java (80), TypeScript (23), Python (9), Swift (5)
- **Key projects**: core-services (213 repos), Archive (190), Menu Pad (94), Concierge (93), core-services-archive (75), madcloud-core (63), Concierge Implementations (58), DevOps (40), Clients (28)
- **Observation**: 74% stale. "Archive" and "core-services-archive" projects suggest deliberate archival. C# presence likely indicates legacy Concierge components or Windows-based services.

### syscolabs (CAKE/Restaurant Legacy)
- **1,527 repos** — largest by count but most are orphaned
- **Top projects**: QA (222 repos!), Platform (152), Payment Gateway (101), Data & Analytics (66), Ops Engineering (55), ReportsNG (26), Platform Utils (24), Catalysts (24), Payment Gateway V2 (21)
- **Languages**: Heavily "unknown" (1,410 of 1,527). Java (37), JavaScript (35), Python (10)
- **Observation**: 76% stale. This is the Sysco Labs (pre-acquisition CAKE) codebase. The massive QA project (222 repos) suggests extensive test infrastructure. Two Payment Gateway projects (v1: 101 repos, v2: 21) confirm payments rewrite history.

### madpayments (Modern Payments)
- **80 repos, 52 active (65%)** — healthiest workspace by activity ratio
- **Languages**: TypeScript dominant (22 repos) — modern stack
- **Projects**: Domain Services (29), Supporting Resources (15), Integrations (12), Libraries (9), Infrastructure (8), Applications (4), Front-End (3)
- **Pipeline coverage**: 45/52 active repos have CI/CD (87%)
- **Recent PR activity**: merchant-service has 23 open PRs, active merges
- **Observation**: This is the most modern, well-organized codebase. TypeScript + domain-driven project structure + high pipeline coverage. The payments team appears to have the best engineering practices.

### syscolabsconf (Legacy CAKE Config)
- **162 repos, 6 active (4%)** — nearly dead
- **Single project**: ECSP (all 162 repos)
- **No pipeline configs** in any active repo
- **All languages "unknown"**
- **Observation**: This appears to be a legacy CAKE-era configuration repository workspace. 96% stale with no CI/CD. Likely contains deployment configs, environment definitions, or per-merchant configs from the Sysco era.

### Key Bitbucket Findings
1. **3,191 total repos, only 789 active (25%)** — massive repo sprawl with 75% stale
2. **Four code lineages confirm incomplete CAKE integration**: Sysco Labs code remains separate from MadMobile code
3. **madpayments is the engineering quality benchmark**: TypeScript, domain-driven, 87% CI/CD coverage
4. **CI/CD appears to be Bitbucket Pipelines** (pipeline configs found in repos) + Jenkins (found in AWS)
5. **Language diversity**: NodeJS/JavaScript dominate Retail; TypeScript dominates Payments; Java + mixed in CAKE legacy
6. **QA investment is enormous**: 222 repos in syscolabs QA project alone
7. **No monorepo pattern** — microservices proliferation across all workspaces

---

## Jira Summary

### Projects
- **113 total projects** across 11 categories
- **Key categories**:
  - **Team** (19 projects): Ahsoka, Kenobi, Thor, Hulk, Wolverine, Spider-Man, Polaris, Sirius, Draco, Vega, Phoenix, Orion, Leo, Castor, Altair, Mira, Libra, Taurus, Apollo, Maui, Ellis Island, Tesla/Nova, Ops Prime — star/constellation/Marvel naming convention
  - **Restaurant** (8): Restaurant (REST), POS Restaurant (PR), MenuPad (MP), Digital Ordering (DO), Customer Engagement (CE), Back Office (BO), Partner Integrations (PI), Platform Restaurant (PLTFRM)
  - **Retail** (7): POS Retail (POS), Core (CORE), Fulfillment (FUL), Clienteling (CLN), Kiosk (KR), Platform Retail (PLTRTL), Template Retail Delivery (TRD)
  - **Customer Success Retail** (20+): Brooks Brothers, Estee, KnitWell/Talbots/FAS, Signet, Ralph Lauren, West Marine, Urban, Guess, Tractor Supply, Rack Room Shoes, Snipes, Wineries, Winmark — each major customer gets their own Jira project
  - **DevOps** (6): DevOps Restaurant (DR), DevOps Payments (DP), DevOps Retail (DEV), Cloud Engineering (CLOUD), DevSecOps (DSO), Change Management (CM)
  - **AI/Neo** (4): AI Evangelism (AI), AI Agent Kanban (AAK), L1 AI Agent (LAA), Neo (NEO)
  - **Programs** (6): Restaurant Program, Retail Program, Platform Program, Payments Strategy, Business Transformation, Cloud Program
  - **Commercialization** (5): CAKE Hardware Refresh, KDS, Loyalty, Label Printer, M60, Marketing
  - **Other**: Governance Risk & Compliance (GRC), IT Projects (ITP), Audits (AUD), Release Management (RM), Product Design (PD)

### Boards
- **177 total boards**: mix of Scrum (~65) and Kanban (~112)
- **Most teams run both**: a Scrum board for sprint execution + a Kanban board for epic/program tracking
- **Notable boards**: Architecture Review Board (ARB), CAKE NEO, EMS2.0 MultiLocation, React/Cinco, Cake OLO, Change Management, GRC Audit Readiness

### Sprint Velocity
- **Tesla/Nova board (Ops Prime sprints)**: 127 → 114 → 78 → 56 completed issues (Q1 2026, bi-weekly) — **declining trend, 56% drop over 3 sprints**
- **Wolverine board**: 13 → 19 → 21 → 40 → 25 → 37 → 36 → 33 → 41 → 53 → 28 → 26 completed issues (Q4 2025 – Q1 2026) — **variable but stable, averaging ~30/sprint**
- Most other scrum boards returned empty sprint arrays — either inactive or no recent sprints

### Issue Distribution & Counts
- **API errors** (410 Gone) on all issue distribution queries — the JQL search endpoint appears restricted or deprecated for this Jira instance
- **Project-level issue counts**: All returned "error" — same API restriction
- **Implication**: Cannot programmatically assess backlog health, bug ratios, or ticket volumes. Will need manual inspection or different API approach.

### Key Jira Findings
1. **Project sprawl**: 113 projects is excessive for a ~370-person company. Many appear to be templates or test projects.
2. **Per-customer Jira projects**: Every major retail customer (Brooks Brothers, Ralph Lauren, etc.) has its own project — this creates cross-project dependency tracking challenges.
3. **Declining velocity signal**: Ops Prime sprint completion dropped 56% over Q1 2026 (127 → 56). Needs investigation — is this scope reduction, team shrinkage, or execution problems?
4. **AI presence is real**: 4 dedicated AI/Neo projects + boards suggest active AI development work (not just marketing).
5. **Team naming convention** (Star Wars + Marvel + astronomy) suggests organized team structure, but 19+ team projects raises questions about team topology and cognitive load.
6. **Service desk exists**: CLD (Developer and Cloud Support) and TSR (Test SRE Restaurant) are service_desk type projects.

---

## Confluence Summary

### Spaces
- **100+ spaces** total (global + personal)
- **~80 global spaces**, ~30 personal spaces
- **Most spaces report page_count of 1** — this appears to be an API limitation (only returns root page count, not total pages)

### Active Spaces (content modified in last 30 days)
| Space | Recent Activity | Last Modified |
|---|---|---|
| Team Tesla (TT) | Release docs, Kiosk releases, Root Cause Analysis, POS VP3350 | Apr 2, 2026 |
| CAKE Payments (POAI) | Accelerated Funding Fix releases | Apr 2, 2026 |
| Payments (P) | Test cases, EMAF transaction resolution | Apr 3, 2026 |
| Mad Mobile Architecture (MMA) | Versions and Deployment Automation | Apr 2, 2026 |
| Product (PROD) | EzCater integration, Error Messages VP3350 | Apr 2, 2026 |
| Operations Solutions (OSME) | New Business fields, Matrix Order Commit | Apr 1, 2026 |
| Leapset Platform (LP) | ALB log analysis, ESB CPU spikes, Release docs | Mar 31, 2026 |
| Cloud Engineering (CCE) | Q1 Vulnerability Assessments, Keycloak VA | Mar 31, 2026 |
| Cake Reports (CR) | KPI & Chart Contract, MLR Project, Test Strategy | Mar 30, 2026 |
| Data & Analytics (DB) | Multi-Location Reporting Auth & Architecture | Mar 31, 2026 |
| Cake Payment Gateway (CPG) | Merchant Cut-Offs, M60 device setup | Mar 31, 2026 |
| CAKE Engineering Excellence (ES) | SMS Token Onboarding Architecture | Mar 27, 2026 |
| Cake Apps (CA) | Agentic Lovable Dev Flow, Restaurant Admin 2.0 | Mar 24, 2026 |
| Concierge Team (PT) | NPM CodeArtifact, Maven CodeArtifact, HTML AppShell | Mar 26, 2026 |
| SWAT (SWAT) | Bissa Server list, REV31/32 Image | Mar 18, 2026 |

### Key Documents Found by Search

**Architecture:**
- "Payment Architecture (ECS and EC2 Components) - Legacy" — CAKE Payments
- "05 - SMS Token Onboarding - Software Architecture" — Engineering Excellence
- "Multi-Location Reporting Architecture and Design" — Data & Analytics
- "Unified KPI & Chart Functional Contract" — Cake Reports
- "Versions and Deployment Automation" — Mad Mobile Architecture
- "HTML AppShell" — Concierge Team

**Operations & Releases:**
- "Root Cause Analysis: Account 11607728 SQS Retry Storm" — Team Tesla
- "Known-Exploited Scan Traffic - ALB log analysis - ESB CPU spikes" — Leapset Platform
- "26-Q1 Internal Vulnerability Assessments" — Cloud Engineering
- "Production Release Calendar" — Program Management
- "Minuteman Build Flow" — Cloud Services Home

**Process:**
- "Agentic Lovable Dev Flow" — Cake Apps (Cursor + Chrome DevTools MCP workflow)
- "3rd Party Integration Onboarding Process" — Partnerships
- "Brainstorming Architecture Developer Prototypes to Improve Processes (BAD-PIP)" — Personal space

**Post-Mortems / RCA:**
- "Root Cause Analysis: Account 11607728 SQS Retry Storm" — confirms RCA process exists
- "Known-Exploited Scan Traffic" — security incident documentation

### Documentation Health Assessment
- **Active documentation culture**: Multiple spaces updated daily, release docs for every deployment
- **Release documentation is strong**: Consistent format with STAG date, PROD date, release owner, test cases
- **Architecture docs exist but fragmented**: Spread across many spaces (MMA, ES, LP, CCE, PT)
- **Security documentation present**: Quarterly vulnerability assessments, security operations space
- **Personal spaces for Sri Lanka team**: Many engineers have personal Confluence spaces (Thiwanka, Mirunaaliny, etc.) suggesting a knowledge-sharing culture
- **Legacy space accumulation**: Many inactive spaces from old teams/projects (Ministry of Fun, Titans, Phoenix, Ultrons, Giants)
- **No centralized runbook space**: Operational knowledge spread across SWAT, SEAOA, LP, CCE

---

## Cross-Platform Observations

### Positive Signals
1. **Multi-account AWS organization** with proper segmentation — not a single-account mess
2. **Grafana/Mimir/Loki/Tempo** observability stack is modern and self-hosted
3. **Terraform** is the IaC standard across accounts
4. **Payments team (madpayments)** demonstrates engineering best practices: TypeScript, domain-driven, 87% CI/CD, EKS-native
5. **GuardDuty + Wiz.io + Security Hub** suggest infosec program exists
6. **Release documentation** is consistent and detailed
7. **ControlTower** governance is deployed across all accounts

### Concerning Patterns
1. **75% repo stale rate** (2,402 of 3,191 repos) — massive code sprawl with unclear ownership
2. **Declining sprint velocity** on key boards — Ops Prime completion dropped 56% in Q1
3. **113 Jira projects** for a ~370-person company — project proliferation suggests organizational complexity
4. **Legacy AWS debt**: m1/m3 instance types still running, Python 2.7/Node 6 Lambdas, CloudFormation stacks from 2016
5. **No dedicated Neo/AI AWS account** despite heavy AI marketing — unclear where AI workloads run in production
6. **Amazon MQ at $3.3K/month** in Retail Prod US — potential modernization opportunity
7. **CloudWatch alarms inaccessible** across all accounts — audit role too restrictive for alarm visibility
8. **Jira API restrictions** (410 errors) prevent programmatic backlog analysis
9. **Four separate Bitbucket workspaces** confirm CAKE acquisition code integration was never completed
10. **Jenkins + Bitbucket Pipelines** — dual CI/CD systems suggest fragmented DevOps practices

### Unknowns Requiring Clarification
1. **MenuPad-Prod-Metro**: What product/customer is this? Running instance on legacy hardware.
2. **Monvia**: Pre-CAKE Leapset product? SVN-era code? One instance still running.
3. **Neo/AI platform location**: No AWS account, but Jira projects (NEO, AAK, LAA) and Confluence spaces exist.
4. **Monitoring tool**: Confirmed Grafana stack exists — but who has dashboards? Are there alerts? Is there an on-call rotation?
5. **CAKE production**: Where does CAKE POS cloud backend actually run? Retail Prod US alongside Concierge? Separate infra?
6. **Relate (in MM-Archive)**: What is this product? Why is an FTP server still running?

### Gaps in Coverage
- **Cost Explorer access blocked** in some accounts (Secrets Manager, CloudWatch alarms)
- **No ECS service detail** for CAKE Development (file too large to fully read)
- **Confluence page counts unreliable** (API returns 1 for most spaces)
- **No Jira issue counts or distribution** (API 410 errors)
- **No monitoring/alerting detail** (CloudWatch alarms access denied)
- **No CI/CD pipeline run history** from Bitbucket (only config presence)
