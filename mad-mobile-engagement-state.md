# Mad Mobile Engagement — Current State & Context

**Date:** April 4, 2026 (updated April 4 with V7 "sponge mode" deep collection — 25 enrichment items across all platforms)
**Author:** Adam Lazarus (Director of Engineering, Legacybox | Translation Layer LLC)
**Purpose:** Complete context transfer for system exploration and pre-work analysis

---

## 1. What This Is

A ~60-hour compressed technology and operations diagnostic sprint for **Mad Mobile, Inc.** — a Tampa-based vertical SaaS company (~370 employees, ~$75M revenue, $70M funded). Products: CAKE POS (restaurant), Concierge (retail), Neo AI Platform, and payments infrastructure. 21,000+ deployed locations. Key partnerships: Sysco, Visa/Cybersource, Best Buy, Apple, Oracle, Salesforce.

**Primary sponsor:** Don Salama — Co-CEO & Acting CFO, Adam's close colleague of ~10 years.

**Dual purpose:**
1. Give Don an executable technology translation layer to complement his existing financial and operational visibility
2. Produce an independent, empirically grounded technology assessment for the board and investors (Morgan Stanley, Western Alliance)

**Consulting entity:** Translation Layer LLC (Florida, formed April 1, 2026). NDA executed under Adam's personal name; SOW will be under the LLC.

**Compensation:** $10,000 fixed fee, fully deferred. Mad Mobile covers Uber travel (St. Pete → Tampa) and meals during the onsite.

---

## 2. Engagement Structure

| Phase | Timeline | What Happens |
|---|---|---|
| Pre-Work | Now → April 11 | System scanning, surveys, document review, alignment with Don |
| Onsite Sprint | April 13–15 (Mon–Wed), Tampa HQ | 15+ interviews, architecture walkthroughs, case tracing |
| Deliverables | April 16–25 | CEO operating brief, friction register, 30/60/90 plan, board deck, survey baseline |

**Five questions this answers:**
1. How does Mad Mobile actually build and ship?
2. Where does execution break down — with evidence?
3. Which problems are structural vs. process vs. technical debt?
4. What should Don engage in during his first 30/60/90 days?
5. What should be left alone?

---

## 3. Key People

### Engagement Team
- **Don Salama** — Co-CEO. Primary sponsor and strategic collaborator. Announced the reorg April 3. Directly oversees all C-suite.
- **Ana Chambers** — Chief of Staff, Strategic Programs. Formally announced in the reorg (was previously absent from org chart). Don's operational right hand. Primary logistics coordinator.

### Mad Mobile Leadership — Post-Reorg (April 3, 2026)

**Don's Direct Reports (7):**

| Name | Title | Scope | Headcount (approx) |
|---|---|---|---|
| Manuel Garcia | Interim CFO | Finance, Revenue Operations | Small — Mark Do (Controller), Zach Honnold (RevOps, 1), Andy Honnold (Payments Strategy, 1) |
| Greg Schmitzer | President & Head of Sales & Marketing | Field sales, inbound sales, marketing strategy | Bobby Jaklitsch (Field, 4), Peter Vu (Inbound, 3), Karen Licker (Marketing, 1) |
| David Strainick | **COO** *(was Chief People Officer)* | Account Management, Customer Onboarding, Customer Delivery, IT | Das DeSilva (Onboarding, 10), Dir. Account Mgmt (9), Rosen Georgiev (IT), Chip O'Connell (Onboarding Delivery, 3) |
| Chathura Ratnayake | **CDO** *(was SVP Global Software Engineering)* | ALL engineering (restaurant, enterprise, payments), product, design, platform, PMO, ALL customer support | Mark Guilarte (PMO, 4), Akshay Bhasin (Payments, 18), Zubair Syed (Enterprise Solutions, 58), Randy Brown (CAKE Tech, 8), Dulanjan W. (Product & Design, 6) |
| Jack Kennedy | CTO | **AI capabilities and platform innovation only** *(operational engineering scope removed)* | Jeremy Diggins, Holly Bobal — small team |
| Bailey Shatney | **VP of Human Resources** *(new to org chart — was David Strainick's domain)* | HR, recruiting, L&D | Renee Pauley (Recruiting), Ayodele Lawal (L&D), Adriana Zuniga (L&D) |
| Ana Chambers | Chief of Staff, Strategic Programs | Cross-company execution, initiative alignment | — |

**Key changes from March org chart:**

1. **Steven Siegel (COO) — EXITED.** Payments strategy, data/analytics, revenue ops responsibilities redistributed.
2. **Bill Lodes (CRO) — EXITED.** Staying in consulting capacity on payments strategy transition. Sales absorbed by Greg Schmitzer.
3. **Chathura Ratnayake — PROMOTED to CDO.** Now owns: all engineering across all verticals, product, design, platform, PMO, and ALL customer support. This is the single largest org in the company (~94+ people based on reported counts).
4. **Jack Kennedy — SCOPE NARROWED.** Retains CTO title but operational engineering authority transferred to Chathura. Now focused on "AI capabilities and innovation across the platform." Very small direct team (Jeremy Diggins + Holly Bobal).
5. **David Strainick — MOVED from CPO to COO.** Now owns Account Management, Onboarding, Delivery, and IT. IT (Jorge Maltes → Rosen Georgiev) now reports through COO, not CTO.
6. **Bailey Shatney — NEW to executive team.** VP of HR. Takes over People functions from Strainick.
7. **Manuel Garcia — NEW to executive team.** Interim CFO. Also absorbed Revenue Operations (previously Siegel).
8. **Greg Schmitzer — EXPANDED.** President + now Head of Sales & Marketing. Absorbed Lodes' sales org.
9. **Customer support unified under Chathura (CDO)** — previously under Lodes (CRO). This puts the full build-to-support chain under one executive.

**Kennedy/Chathura dynamic: RESOLVED.** The hypothesis that formal and operational authority were misaligned (Hypothesis D) has been resolved by org structure change. Chathura now has both formal AND operational authority. Kennedy's role is explicitly narrowed to AI/innovation. This is no longer a "live variable" — it's a confirmed finding. Can now be referenced openly in all materials.

### Chathura's Direct Reports (from org chart)
- **Mark Guilarte** — PMO (4 people). New under Chathura.
- **Akshay Bhasin** — Payments (18 people). Previously QE Lead — scope expanded or relabeled to Payments.
- **Zubair Syed** — Enterprise Solutions (58 people). Largest eng org.
- **Randy Brown** — CAKE Tech (8 people). Restaurant engineering.
- **Dulanjan Wengappuliarachchi** — Product & Design (6 people).
- **Customer Support** — all levels, headcount TBD. New under Chathura.

### New Names on the Org Chart
- **Manuel Garcia** — Interim CFO
- **Bailey Shatney** — VP Human Resources
- **Mark Do** — Assistant Controller (reports to Garcia)
- **Zachary Honnold** — RevOps (1), reports to Garcia
- **Andrew Honnold** — Payments Strategy (1), reports to Garcia
- **Bobby Jaklitsch** — Field Sales (4), reports to Schmitzer
- **Peter Vu** — Inbound Sales (3), reports to Schmitzer
- **Das DeSilva** — Onboarding (10), reports to Strainick
- **Chip O'Connell** — Onboarding Delivery (3), reports to Strainick
- **Mark Guilarte** — PMO (4), reports to Chathura
- **Holly Bobal** — reports to Kennedy (role TBD)
- **Renee Pauley** — Recruiting, reports to Shatney
- **Ayodele Lawal** — L&D, reports to Shatney
- **Adriana Zuniga** — L&D, reports to Shatney

### Departed
- **Steven Siegel** — Former COO. Exited April 3, 2026.
- **Bill Lodes** — Former CRO. Exited April 3, 2026. Consulting on payments strategy transition.

### IT / Infrastructure Contacts (Access Provisioning)
- **Rosen Georgiev** — IT (reports to Strainick/COO). Previously identified as Jira/Confluence admin. April org chart shows him under IT. **Clarification needed:** March chart listed Jorge Maltes as Director Information Technology — confirm whether Maltes departed or chart shows different level.
- **Matias Lopez Riglos** — DevOps/infra. Filed AWS provisioning ticket. Handles Bitbucket invites. Reports to Zubair Syed.
- **Matthew Griffin** — Cloud team. Assigned AWS account provisioning (Jira ticket CLD-2431).

### Sri Lanka
- **Rajik Gunatilaka** — VP & LK Country Head. Reports to Strainick (COO), not CDO. Engineering resources in Sri Lanka have dotted-line relationships to Chathura/Zubair.

---

## 4. Current Access (Confirmed April 2, 2026)

### Active
- **Mad Mobile Email:** adam.lazarus@madmobile.com (Microsoft/Outlook)
- **Microsoft Teams:** Active. Connected to Global Hub & system monitoring alert channels.
- **Bitbucket:** Four organizations:
  - MadMobile (core)
  - Sysco Labs (CAKE legacy from acquisition)
  - Mad Payments (separate payments codebase)
  - Sysco Labs Conf (likely CAKE-era config/code)
- **Jira / Confluence:** https://madmobile-eng.atlassian.net/wiki/welcome
- **AWS SSO:** 18 accounts (see detail below)

### AWS Account Inventory (18 accounts)

| Account Name | Account ID | Email | Notes |
|---|---|---|---|
| CAKE Development | 230930891673 | aws+cake-dev@madmobile.com | CAKE dev environment |
| CAKE R and D | 464176945335 | aws+cake-rnd@madmobile.com | CAKE R&D — experimental? |
| Customer Analytics | 024848459322 | aws+customer-analytics@madmobile.com | Data/analytics |
| DNS Management | 381491928564 | aws+dns-mgmt@madmobile.com | DNS infrastructure |
| Forensics | 040591922250 | aws+forensics@madmobile.com | Security forensics — suggests some infosec maturity |
| Madmobile Mgmt | 302042158767 | aws+madmobile-mgmt@madmobile.com | Management/org account |
| Marketplace Seller | 026090514637 | aws+marketplace-seller@madmobile.com | Unknown — investigate |
| MenuPad-Prod-Metro | 622065827965 | aws+menupad-prod-metro@madmobile.com | Unknown — not in pre-read materials. Acquired product? Legacy brand? |
| MM-Archive | 673260261206 | aws+archive@madmobile.com | Archive/cold storage |
| Monvia | 219788358213 | aws+monvia@madmobile.com | Unknown — not in pre-read materials. Acquired product? |
| Payments Prod US | 491085393358 | aws+payments-prod-us@madmobile.com | Production payments — critical |
| Retail Prod APAC | 357856625432 | aws+retail-prod-apac@madmobile.com | Concierge/Retail — Asia Pacific |
| Retail Prod EU | 266315811211 | aws+retail-prod-eu@madmobile.com | Concierge/Retail — Europe |
| Retail Prod US | 125062011444 | aws+retail-prod-us@madmobile.com | Concierge/Retail — US primary |
| Retail Prod US DR | 542575560358 | aws+retail-prod-us-dr@madmobile.com | Concierge/Retail — US disaster recovery |
| Security | 155215164482 | aws+audit@madmobile.com | Security/audit account |
| Shared Artifact Registry | 278608866843 | aws+shared-artifacts@madmobile.com | Shared build artifacts (ECR? S3?) |
| Shared Services | 654654350563 | aws+shared-services@madmobile.com | Shared infrastructure services |

**Observations from AWS structure (updated April 3 with automated inventory):**
- Multi-account org with proper segmentation — ControlTower governance deployed across all accounts
- **Total AWS spend: ~$383K/month** (March 2026). ~$309K in Mgmt account (likely consolidated billing/RIs — needs confirmation). Next largest: Monvia ($25.9K), CAKE Dev ($14.7K), Retail Prod US ($13.0K)
- **201 running EC2 instances** across all accounts, **23 stopped**, **167 pre-Graviton (83%)**
- **248 Lambda functions**, **53 on EOL runtimes (21%)** including Python 2.7, Node 6/8/10/12
- **Retail Prod US is the heaviest workload account**: 45 EC2 instances, EKS cluster (`marvel-cloud-prod-us`), Amazon MQ ($3.3K/month), 57 CloudFormation stacks (some from 2016)
- **Payments Prod US is architecturally cleanest**: Fully containerized on EKS, no EC2, Terraform IaC, own Grafana observability, 0 IAM users / 61 roles
- **Monitoring is self-hosted Grafana** (Mimir + Loki + Tempo) in Shared Services — not Datadog/New Relic
- **Jenkins is CI/CD** for CAKE (found in CAKE Development), **Bitbucket Pipelines** for other workloads
- **Terraform is the IaC standard** (state buckets across many accounts)
- **Security posture**: GuardDuty active across all accounts, Wiz.io deployed, Security Hub in R&D, Forensics account provisioned (Jan 2026)
- **MenuPad-Prod-Metro**: Running instance (`venom_new`, r4.xlarge), ~$2K/month. Legacy — asked Ana to route internally.
- **Monvia**: **$25.9K/month** — significantly more than expected for legacy. Contains Leapset-era SVN instance, m1 hardware. Asked Ana to investigate.
- **MM-Archive**: Running "Relate" instances + FTP server. Legacy product — asked Ana.
- **No dedicated Neo/AI account**: SageMaker artifacts found in CAKE R&D, but no production AI infrastructure identified. Asked Ana to route to Jack/Chathura.
- Shared Artifact Registry has ECR + CodeArtifact + a `mm-techdocs-storage` bucket (suggests Backstage/TechDocs)
- Marketplace Seller account has Lambda functions for AWS Marketplace entitlements — MM sells via AWS Marketplace

### Confirmed (Updated April 3)
- **Monitoring**: Grafana/Mimir/Loki/Tempo (self-hosted in Shared Services). Viewer access requested.
- **CI/CD**: Jenkins (CAKE) + Bitbucket Pipelines (Retail, Payments). Dual system.
- **IaC**: Terraform (state buckets in multiple accounts)

### Not Yet Confirmed
- Grafana dashboard access (requested from Ana/Matias)
- Guru access (requested from Ana)
- Internal survey tool (Ana checking with HR)

### Phase 2 Access (Partially Complete)
- ✅ Bitbucket API key (created, working across all 4 workspaces)
- ✅ Atlassian API token (created, working for Jira + Confluence)
- ✅ AWS CLI / SSO (18 profiles configured, `Global-Audit-RO` role)
- ⏳ Grafana viewer access (requested)
- ⏳ CloudWatch alarm permissions (`cloudwatch:DescribeAlarms` not in audit role — requested)

---

## 5. What I Already Have (Pre-Read Materials)

### Received
1. **Org chart** — MadMobile_OrgChart_v2_pptx.pdf (March 2026, from Don). Updated version pending from HR.
2. **Restaurant Update deck** — Restaurant_Update_March_2026.pdf. Contains: product team org, restaurant engineering team, prioritization process, requirements process, restaurant roadmap, CAKE ecosystem map, AI usage overview, GTM process.

### Pending (Ana's team gathering into a shared folder)
- Product roadmaps: Concierge/Retail, Neo/AI
- Revenue breakdown by product line
- Architecture diagrams beyond CAKE ecosystem
- Engineering team assignments by product line (beyond restaurant)
- Deployment environments, release cadence, CI/CD documentation
- Top customer escalations (especially CAKE payment outages)
- KPI / scorecard / dashboard screenshots
- Sprint velocity metrics (last 6–12 months)
- Incident reviews / post-mortems / retrospectives
- Engineering and operations tool inventory
- Open strategic initiatives and known problem projects

---

## 6. What I Know About the Technology Landscape

### CAKE Ecosystem (from Restaurant Update deck)
- **15+ live systems**: POS V3 (Pondus), POS V4 (Elio), Kiosk v1, OLO v1, KDS v1, Gift Cards v1, Guest Manager, Kiosk v2, Loyalty v1, OrderPad, CAKEpop, Email Marketing, Restaurant Admin 1.0, Customer Display
- **POS V3 and V4 running simultaneously** — migration not complete
- **In active development**: CAKE OLO UI Refresh, EMS 2.0 Multi Location, Gift Cards (Factor 4), CAKEpop features, KDS v2, VP 3350 (new payment device)
- **Planned**: OLO v2, Loyalty v2, Restaurant Admin 2.0
- **Third-party integrations**: Checkmate, 7Shifts, OLO.com, LRS, Paytronix, Bloop, DoorDash, NOLO, Orca, Davo, Parafin, Dolce, QSR KDS
- **Team size**: ~10 engineers + ~7 QE under Randy Brown. This ratio vs. system surface area is a primary investigation target.

### Source Control (Bitbucket) — Inventoried April 3

| Workspace | Total Repos | Active (90d) | Stale | CI/CD Coverage |
|---|---|---|---|---|
| madmobile | 1,422 | 370 (26%) | 1,052 (74%) | Checked |
| syscolabs | 1,527 | 361 (24%) | 1,166 (76%) | Checked |
| madpayments | 80 | 52 (65%) | 28 (35%) | 45/52 (87%) |
| syscolabsconf | 162 | 6 (4%) | 156 (96%) | 0 |
| **Total** | **3,191** | **789 (25%)** | **2,402 (75%)** | — |

- **75% of repos are stale** — massive code sprawl with unclear ownership
- **madpayments is the engineering quality benchmark**: TypeScript, domain-driven project structure, 87% CI/CD coverage, fully containerized on EKS
- **madmobile**: NodeJS/JavaScript dominant (158/134 repos), C# (90), Java (80). Key projects: core-services (213), Archive (190), Menu Pad (94), Concierge (93)
- **syscolabs**: CAKE/Leapset legacy. 1,410 of 1,527 repos have "unknown" language. QA project alone has 222 repos. Two Payment Gateway projects (v1: 101 repos, v2: 21)
- **syscolabsconf**: Nearly dead (4% active). Single ECSP project, likely CAKE-era per-merchant configs
- **No monorepo pattern** — microservices proliferation across all workspaces
- **Four code lineages confirm CAKE acquisition integration was never completed**

### Jira — Inventoried April 3 (Segmented)

**Key finding: Jira is the company's universal work system**, not just engineering's tool. Of 141 projects, ~68 are engineering, ~50 are customer success (per-client implementations), and ~23 are operations/governance (GRC, audits, business transformation, programs). This is itself a finding about operating cadence (Hypothesis G).

| Segment | Projects | Open Issues | >1 Year Old | Bugs | Stories |
|---|---|---|---|---|---|
| **Overall** | 141 | 18,583 | 13,377 (72%) | 11,985 | 31,614 |
| **Engineering** | ~68 | 13,725 | 9,115 (66%) | 8,712 | 26,734 |
| **Customer Success** | ~50 | 2,525 | 1,957 (77%) | 3,186 | 2,231 |
| **Operations** | ~23 | 2,102 | 2,080 (99%) | 72 | 2,577 |

- **313 boards** (89 scrum, 224 kanban)
- **Engineering backlog**: 13,725 open issues, 66% older than 1 year — still significant backlog debt
- **CS backlog**: 2,525 open issues, 77% older than 1 year — customer implementations stalling
- **Operations backlog**: 2,102 open, 99% older than 1 year — nearly all dormant
- **Created vs resolved (26 weeks)**: Engineering: 4,701 created / 4,432 resolved (net -269). Overall: 5,790 / 5,212 (net -578). Engineering backlog growing slower than overall.
- **Sprint velocity (19 active scrum boards)**: Multiple declining trends. Ops Prime dropped from 127 → 56 issues/sprint in Q1 2026 (-56%). OS board dropped from 114 → 49 (-57%).
- **Cycle time P50 = 59 days** (engineering-only, In Progress to Done). P75 = 210 days. P95 = 233 days.
- **Flow distribution (engineering, last 90d resolved)**: 67% features, 21% defects, 11% epics, 1% tasks — not in firefighting mode
- **32 per-customer Jira projects**: Every major retail customer (Brooks Brothers, Ralph Lauren, Estee Lauder, etc.) gets their own project — creates cross-project tracking complexity and reveals how CS work flows (or doesn't) into engineering
- **4 active AI/Neo projects**: AI Evangelism, AI Agent Kanban, L1 AI Agent, Neo — confirms active AI development
- **Largest projects by issue count**: REST (17,318), OS (4,794), DSO (4,762), CE (4,441), DR (4,218), BO (4,091)
- **Assignee concentration (role-classified)**: Top 30 assignees include 14 engineering ICs, 5 engineering leads, 6 customer success, 4 operations, 1 cross-functional. 4 people have 50+ open issues assigned.

### Confluence — Inventoried April 3

- **165 spaces** (80 global, ~30 personal, rest inactive)
- **Top spaces by page count**: Leapset Platform (6,445), POS (3,024), CAKE Payments (2,203), Data & Analytics (2,056), Cake Payment Gateway (1,838), Cloud Engineering (1,752)
- **Active documentation culture**: Multiple spaces updated daily, consistent release docs
- **Architecture docs exist but fragmented**: Spread across MMA, ES, LP, CCE, PT spaces
- **No centralized runbook space**: Operational knowledge scattered across SWAT, SEAOA, LP, CCE
- **RCA process confirmed**: "Root Cause Analysis: Account 11607728 SQS Retry Storm" in Team Tesla
- **"Agentic Lovable Dev Flow"** in Cake Apps — Cursor + Chrome DevTools MCP workflow documentation

### Current AI Tooling in Use
- **Cursor** — heavy use for daily development
- **Guru** — AI-produced documentation
- **AI for user stories/test cases** — product and QE workflows
- **AI-driven RCA on production POS logs** — in progress
- **Architecture Review Board (ARB)** exists for requirements/prioritization

### Known Challenges (Pre-Engagement Signal + System Evidence)
- Glassdoor: 2.4/5, 31% recommend, 32% positive outlook
- Execution velocity problems — **now confirmed quantitatively**: declining sprint velocity, 59-day cycle time P50, backlog growing faster than it's being resolved
- Neo/AI gap: heavy marketing, **no dedicated production infrastructure found** — SageMaker artifacts in R&D only
- CAKE reliability: system-wide payment outages
- Priority whiplash: shifting priorities mid-sprint
- Sales-driven distortion: sales promises overriding product logic
- Culture erosion: layoffs, shifted bonuses, forced RTO, Houston office shutdown
- Offshore coordination: Sri Lanka timezone challenges, reporting through People not Engineering
- **Legacy infrastructure debt**: 83% pre-Graviton EC2, 21% EOL Lambda runtimes, running instances on m1-generation hardware from 2012, CloudFormation stacks from 2016
- **Backlog debt**: 72% of 18,583 open issues are older than 1 year
- **Epic completion rate: 27.7%** — 481 engineering epics in last 12 months, only 133 resolved. REST project worst at 18.5% (260 epics, 48 resolved). NEO project: 12.5% (8 epics, 1 resolved).
- **Priority system is broken**: 89.4% of open engineering issues are marked "High", 10.6% are "None". No other priority levels in use. Priority is meaningless as a triage signal.
- **Estimation discipline near zero**: Story Points field populated on only 9% of resolved stories (27 of 300 sampled)
- **Root Cause Category process not followed**: Jira field "Probable/Actual Root Cause Category" exists but is populated on 0% of resolved bugs. Process documented in Confluence but not enforced.
- **90% of ECS containers have no health checks**: 61 of 68 active ECS services have no container health check configured — services can be unhealthy without detection
- **Incident timeline**: 50 structured post-mortems parsed from Confluence. Peak year: 2022 (26 incidents). Top system: Payments (19), Reports (11), Menu (10). Root causes: application bugs (8), infrastructure/cloud (8), payment provider failures (7), database/RDS (7). **DATA GAP NOTE:** The Taurus space structured RCA process (DE-xxxxx POST MORTEM format) ran 2020–2023, then largely stopped. Team Tesla picked up RCA writing in 2025 (SQS Retry Storm, Menu Core Retry Loop). Only 5 incidents from 2024, 2 from 2025. This could mean: (a) the RCA process died, (b) it migrated to Teams/Slack/Guru, (c) incidents genuinely decreased, or (d) the team changed and the new people don't use the same space. This is a key onsite question — "where do incident reviews happen now?"
- **Reviewer bottlenecks**: 57 people handle 100+ code reviews each. Top 5: John Harre (581), Holly Culver (508), Wenushka Dikowita (481), Dan McCune (471), Matias Lopez Riglos (463). 17 repos have a single reviewer handling >50% of all PRs.
- **Branch protection absent**: 0 of 30 checked repos have required approvals or passing build checks. No branch restrictions enforced.
- **201 open PRs, 95% stale**: 191 older than 7 days, 175 older than 30 days. 66 (33%) have zero reviewers assigned. 167 (83%) have zero comments.
- **Pipeline success rate: 60.7%** — 1,563 pipeline runs across 30 repos. Nearly 40% of builds fail.

### Known Data Gaps & Caveats (V7)
- **Incident timeline gap (2024–2026)**: Structured RCA docs in Confluence largely stop after 2023. Either the process lapsed, moved to another tool, or incidents decreased. Only 5 docs from 2024, 2 from 2025 (both in Team Tesla, not Taurus). **Needs onsite clarification: where do incident reviews happen now?** May also need to query Jira for "Incident" or "Code Red" issue types from 2024–2026.
- **CloudTrail access denied**: The `Global-Audit-RO` role does not include `cloudtrail:LookupEvents`. Zero deployment frequency data from AWS. Only deploy signal is Bitbucket pipeline timestamps and git tags.
- **Branch protection data may undercount**: 0 of 30 repos showed restrictions via the Bitbucket API. Could mean genuine absence or the API endpoint handles restrictions differently (e.g., project-level vs. repo-level restrictions). Validate onsite.
- **Pipeline history covers 30 of 789 active repos**: The 60.7% success rate is from the top 30 most active repos — may not represent the full fleet. Could be better or worse for less-active repos.
- **Grafana still inaccessible**: The actual monitoring dashboards, alert rules, and on-call configuration remain invisible. CloudWatch dashboards captured are a proxy, not the primary observability layer.
- **No Jira incident query**: Searched Confluence for RCAs but did not query Jira for issue type "Incident" or "Code Red" in 2024–2026. This could fill the incident timeline gap.
- **Root Cause Category field empty may mean wrong field**: The field "Probable/Actual Root Cause Category" (customfield_10382) showed 0% population. There's also "Root Cause Category" (customfield_10590, type: array) that wasn't queried — may be the active one.

---

## 7. Diagnostic Framework

### Six Systems Being Evaluated
1. **Business Direction** — Portfolio clarity, resource allocation, strategic coherence
2. **Product Decision** — Roadmap governance, power dynamics, requirement stability
3. **Delivery** — Cycle time, deploy frequency, WIP, sprint completion
4. **Technical** — Architecture, tech debt ratio, incidents, deploy complexity
5. **Operating Cadence** — Meeting structure, dashboards, escalation paths
6. **Accountability** — Incentive structures, recognition, promotion criteria

### Nine Hypotheses to Test

| # | Pattern | What I'm Testing |
|---|---|---|
| A | Portfolio Sprawl | Too many products, no shared platform discipline |
| B | Sales-Led Chaos | Revenue promises create roadmap churn and tech debt |
| C | Fake Platforming | Leadership talks "platform"; teams maintain customer-specific patchwork |
| D | Unclear Ownership | Formal authority and operational authority are misaligned — **CONFIRMED and resolved by April 3 reorg.** Chathura now CDO with formal authority; Kennedy narrowed to AI/innovation. Onsite validates whether operational reality matches structural change. |
| E | Dependency Drag | A few people/teams are routing bottlenecks |
| F | Legacy Gravity | CAKE architecture prevents speed; no triage of must-modernize vs. can-encapsulate |
| G | Missing Cadence | No consistent execution inspection; leadership discovers reality through fire drills |
| H | Biz-Tech Mistranslation | Business says "eng is slow"; eng says "business is chaotic"; real issue is undefined tradeoffs |
| I | Architectural Polarity | Simultaneous AI-native building + legacy POS maintenance = irreconcilable eng split |

### Methodology & Frameworks
- **Pre-Work surveys:** DORA, Westrum Culture, DevEx/DX Core 4, Pragmatic Engineer Test, AI Adoption & Tooling
- **Onsite:** McKinsey 7S, RAPID, Value Stream Mapping, Theory of Constraints, Team Topologies, Wardley Mapping
- **Deliverables:** PE Tech DD 9-Pillar, Watkins STARS, C4 Model, Fowler's Tech Debt Quadrant, Flow Framework

---

## 8. Surveys

Five instruments ready. Target deployment: **Monday, April 7** (via Microsoft Forms on MM account, intro from Chathura as CDO).

| Survey | Audience | Time | Questions | Measures |
|---|---|---|---|---|
| DORA Quick Check | Engineering leads/managers (1 per team) | ~3 min | 9 | Deploy frequency, lead time, change failure rate, recovery time |
| Westrum Culture | All eng leads, managers, senior ICs, PMs | ~2 min | 7 | Organizational culture type |
| DevEx (DX Core 4) | Individual contributors only | ~5 min | 18 | Developer experience: feedback loops, cognitive load, flow state |
| Pragmatic Engineer Test | 3–5 engineering leads/senior engineers | ~2 min | 15 | Engineering culture maturity |
| **AI Adoption & Tooling** | **All engineering, product, design, QE** | **~5 min** | **16** | **AI tool adoption, effectiveness, tooling landscape, AI strategy clarity** |

**Total time per person: under 20 minutes.** Most people take 2–3 of the 5 based on their role.

**Who Takes What:**

| Role | DORA | Westrum | DevEx | Pragmatic Eng | AI & Tooling |
|---|---|---|---|---|---|
| Engineering Manager / Lead | ✅ | ✅ | | ✅ | ✅ |
| Senior IC / Staff Engineer | | ✅ | ✅ | ✅ | ✅ |
| Software Engineer | | ✅ | ✅ | | ✅ |
| QE Engineer | | ✅ | ✅ | | ✅ |
| Product Manager | | ✅ | | | ✅ |
| Product Designer | | ✅ | | | ✅ |

**Deployment:** Building in Microsoft Forms on MM account. Intro message from Chathura (as CDO). Draft message sent to Ana for Chathura's review (April 3 email). Chathura message needs update to reference 5 surveys instead of 4.
**DevEx survey draft live:** https://forms.cloud.microsoft/r/021mP98Sf9
**Designed for re-use:** Mad Mobile can re-run at 30/60 days without Adam.

---

## 9. Onsite Interview Plan (April 13–15)

**Updated to reflect April 3 reorg. Major changes: Siegel removed, Lodes deprioritized, Strainick refocused, Kennedy handled with care, Chathura expanded.**

### Monday, April 13 — Leadership + Strategy

| Who | Title | Duration | Focus | Notes |
|-----|-------|----------|-------|-------|
| Chathura Ratnayake | CDO | 90–120 min | Full org ownership, execution model, team health, support unification, PMO integration, sprint reality, AI strategy from build side | **Most important interview of the engagement.** Owns the entire build-to-support chain. May need two sessions. |
| Jack Kennedy | CTO | 60 min *(reduced from 90)* | AI/innovation roadmap, Neo platform vision, infrastructure plans, his view of the path forward | **Handle with care.** Operational scope just removed. Focus on what he's building, not what he lost. Don't probe the reorg dynamics directly — let him volunteer. |
| Dulanjan W. | Sr. Dir. Product & Design | 60 min | Roadmap governance, product decisions, design process, PM/engineering handoff | Now reports to Chathura. Ask about the transition. |
| David Strainick | COO *(was CPO)* | 45 min | Account management, onboarding, delivery execution, IT operations, customer experience | **Completely different interview than planned.** Was going to be 30 min on HR/culture. Now 45 min on operational execution. Ask about IT governance and how onboarding/delivery handoff works with engineering. |

### Tuesday, April 14 — Engineering Deep Dive

| Who | Title | Duration | Focus | Notes |
|-----|-------|----------|-------|-------|
| Randy Brown | VP Eng, CAKE Tech (8) | 60 min | CAKE engineering, outage patterns, V3→V4 migration, team capacity vs. system surface area | 8 engineers for 15+ live systems. This ratio is the story. |
| Zubair Syed | VP Eng, Enterprise Solutions (58) | 60 min | Concierge/Retail execution, enterprise customer projects, team structure, offshore coordination | Largest eng org by headcount. |
| Akshay Bhasin | Payments (18) | 45 min | Payments engineering, architecture (the cleanest codebase), scaling, how this team operates differently | Scope appears expanded from QE Lead to Payments org. Clarify. |
| Mark Guilarte | PMO (4) | 30 min | Project management process, cross-team coordination, execution discipline | New under Chathura. How does PMO integrate with engineering sprints? |
| Engineering Managers (2–3) | Various | 45 min each | Team execution, dependencies, sprint reality, tooling | Target: one from CAKE, one from Enterprise, one from Payments |
| Senior ICs (2–3) | Various | 30 min each | Day-to-day delivery, tooling, AI usage, what slows them down | |

### Wednesday, April 15 — Cross-Functional + Validation

| Who | Title | Duration | Focus | Notes |
|-----|-------|----------|-------|-------|
| Rajik Gunatilaka | VP & LK Country Head | 45 min (video) | Sri Lanka engineering ops, timezone coordination, reporting lines | Reports to Strainick (COO) now, not CPO. Dotted line to Chathura. |
| Greg Schmitzer | President & Head of Sales & Marketing | 30 min | Sales/marketing strategy, revenue story, feature promise pipeline | Expanded role — absorbed CRO scope. |
| Jeremy Diggins | Dir. Enterprise Technology | 30 min | Enterprise tech, infrastructure decisions | Reports to Kennedy. |
| Bailey Shatney | VP Human Resources | 30 min | Culture, hiring, retention, L&D, team health | New to exec team. Took over from Strainick. |
| Customer Support Lead (TBD) | TBD | 30 min | Escalation paths, support→engineering handoff | Now under Chathura. Key to understanding full chain. |
| Chris Gomersall | Dir. Product Design | 30 min or async | Design process, PM/design/eng collaboration | |
| Bill Lodes (optional) | Former CRO, consulting | 30 min | Payments strategy context, transition items | Only if available and Don thinks it's valuable. Low priority. |

**Total interview slots: ~18–21 (was 15+)**
**Room booking:** Ana will coordinate once schedule is locked.

---

## 10. Deliverables (April 16–25)

### Core (Guaranteed)
- **CEO Operating Brief** — the technology chapter of Don's transition playbook
- **Friction Register** — prioritized list of execution friction points with evidence
- **Hypothesis Scorecard** — each of the nine patterns scored (confirmed / partial / not observed)
- **30/60/90-Day Action Plan** — sequenced recommendations
- **Board/Investor Presentation** — board-ready deck Don can take to Morgan Stanley
- **Baseline Survey Package** — all four surveys with Mad Mobile-specific instructions, baseline scores, and comparison guidance for 30/60-day re-runs

### Expected
- Architecture topology maps (C4 Context and Container level)
- Value stream maps for key workflows
- Decision-rights map (RAPID)
- Vendor/tool utilization assessment

---

## 11. What I'm Doing Right Now (This Week)

### Completed ✅
- NDA executed (personal name)
- Translation Layer LLC formed (Florida, Northwest Registered Agent)
- translationlayer.ai domain registered (Cloudflare)
- MM email active (adam.lazarus@madmobile.com)
- Microsoft Teams access
- Bitbucket access (4 orgs) + API key (programmatic access working)
- Jira / Confluence access + API token (programmatic access working)
- AWS SSO (18 accounts) + CLI profiles configured (all 18 accounts, `Global-Audit-RO` role)
- Jira comment confirming AWS access (CLD-2431)
- **V1 system inventory** — automated scans across all 4 platforms (April 2–3)
- **V2 enhanced inventory** — fixed Jira API issues, expanded velocity coverage, corrected Confluence page counts, added DORA-adjacent metrics (April 3)
- **V3 targeted data collection** — PR reviewer concentration, sprint scope change, flow distribution, assignee analysis, deploy tags, Confluence trends, post-mortem catalog, AWS ECS/Route53 deep (April 3)
- **V4 Jira segmentation** — classified all 141 projects into engineering/CS/operations, re-ran all Jira queries with segmented output, role-classified assignees (April 3)
- **V5 Confluence content extraction** — 14,111 pages indexed across 15 key spaces, 94 most relevant pages content-extracted to `inventory/confluence/content/` (April 3)
- **V5 AI tooling analysis** — scanned 30 repos for AI config files (8 have Cursor/Claude/AGENTS.md), cataloged AI docs in Confluence, enumerated SageMaker/Bedrock usage in AWS (April 3)
- **V5 Tooling catalog** — 28 tools identified across all platforms with cost status (see `inventory/tooling_catalog.json`)
- **V6 cross-system user audit** — 168 unique users identified across Bitbucket/Jira/Confluence/AWS, per-user activity profiles, cross-system access mapping (April 3)
- **Vendor spend request drafted** for Don (see `vendor-spend-request.md`)
- **Quantitative analysis pipeline** — 15 CSV exports, 29+ interactive HTML charts in `analysis/charts/`
- **Ana coordination email drafted** — logistics and action items (see `ana-request.md`)
- **April 3 reorg mapped and analyzed** — updated people, interview schedule, hypothesis status
- **Survey 5 (AI Adoption & Tooling) instrument designed** (see `05-ai-tooling-survey.md`, 16 questions)
- **Chathura survey intro message drafted** and sent to Ana (April 3 email) — needs update to reference 5 surveys instead of 4
- **Ana email sent** acknowledging reorg, including text-only org chart for working reference
- **Don call guide prepared** (see `don-call-guide-april3.md`, 13 questions across reorg, board deliverable, onsite prep)
- **Mermaid.js org chart diagram created** (see `mad-mobile-org-chart.mmd`) for graphical use
- **Engagement minisite built** — Astro-based dashboard with 8 pages (Dashboard, AWS, Engineering, Delivery, Documentation, People, Tooling, Charts), 25+ embedded Plotly charts, data tables, metric cards (see `minisite/`)
- **V7 "sponge mode" deep collection** — 25 enrichment items across all tiers (April 4):
  - **Tier 1**: CloudTrail (access denied — audit role limitation), Bitbucket pipeline history (30 repos, 1,563 runs, 60.7% success), AWS EKS/RDS/ElastiCache deep (EKS K8s 1.30, 8 RDS instances, ElastiCache clusters), Jira epic completion (27.7%) + priority distribution (89.4% High) + blocking chains + status transitions, Bitbucket branch protection (0 repos protected) + open PR aging (201 open, 95% stale), incident/RCA timeline (50 incidents parsed, Payments #1), reviewer concentration FIXED (1,464 edges, 217 nodes), sprint retrospective extraction (30 retros from 6 teams)
  - **Tier 2**: AWS cost optimization, security posture scan (GuardDuty, ACM, IAM, S3), Confluence architecture diagram catalog (321KB), cross-system deploy correlation, bus factor analysis (57 heavy reviewers, 17 bottleneck repos), dependency/package analysis (Node 12, Java 4, TypeScript 8, React 5), CloudWatch dashboard content (6 dashboards), ECS task definition analysis (68 services, 90% no health checks, 49 images), AWS tagging compliance audit, Jira custom fields (Root Cause 0% populated, Story Points 9%)
  - **Tier 3**: AWS network topology, Jira workflow audit, Confluence labels/blog posts, AWS backup/DR assessment, PR review network visualization (interactive HTML), auto-generated C4 context + container diagrams
- **Engagement minisite updated** — V7 findings added to all pages (Dashboard, Engineering, Delivery, AWS, Documentation). 31 charts, 17 CSVs, 94 JSON inventory files, 124 content text files, 3 Mermaid diagrams.

### In Progress 🔄
- Building all 5 surveys in Microsoft Forms on MM account (DevEx draft live: https://forms.cloud.microsoft/r/021mP98Sf9)
- Working with Don on reorg-specific questions via call guide (Kennedy's future, Strainick appointment, Shatney background, Bhasin scope, board deck transparency)
- Waiting on Ana: pre-read items not in Confluence (roadmaps as decks, revenue breakdown by product line)
- Waiting on Ana: Grafana viewer access (route to Matias/cloud team)
- Waiting on Ana: routing questions on Monvia, MenuPad, Relate, Neo/AI
- Waiting on Ana: interview calendar blocks + conference room (April 13–15)
- Mercury banking setup for Translation Layer LLC
- EIN pending from Northwest

### Next Steps (This Week)
1. **Send Ana coordination email** — `ana-request.md` is ready to send
2. **Finish building surveys in Microsoft Forms** — all five instruments (DORA, Westrum, DevEx, Pragmatic Engineer, AI Adoption & Tooling)
3. **Finalize interview schedule grid** — send to Ana for calendar booking
4. **Work with Don** on survey intro message and deployment timing (target: April 7)
5. **Collect pre-read docs** as Ana's folder becomes available
6. **Review analysis charts** — open `analysis/charts/*.html` in browser, identify top findings to lead with onsite
7. **Prep interview questions** — `interview-prep-with-data.md` has data-backed questions per interviewee, review and refine

### System Exploration — Completed (Key Answers)
- **Where does Neo/AI live?** No dedicated account. SageMaker in CAKE R&D. Jira projects exist (NEO, AAK, LAA). Confluence docs exist. But no production AI infrastructure found. **This is a key onsite question for Jack/Chathura.**
- **What are MenuPad-Prod-Metro and Monvia?** Legacy accounts with running instances. Monvia is costing $25.9K/month. **Escalated to Ana.**
- **What CI/CD tools are in use?** Jenkins (CAKE, found in CAKE Dev account) + Bitbucket Pipelines (Retail, Payments). Dual CI/CD system.
- **How are the four Bitbucket orgs related?** madmobile = Concierge/Retail core. syscolabs = CAKE/Leapset legacy. madpayments = Modern payments (TypeScript, domain-driven). syscolabsconf = Dead CAKE-era configs.
- **What monitoring/observability exists?** Self-hosted Grafana stack (Mimir + Loki + Tempo) in Shared Services. Payments has its own Grafana instance. **Not Datadog or New Relic.** Viewer access requested.
- **Are there other platforms?** Wiz.io for security scanning. GuardDuty across all accounts. AWS Marketplace seller functions. Backstage/TechDocs likely (mm-techdocs-storage bucket found).

### Pre-Work Quantitative Baseline (Available for Onsite)

| Metric | Overall | Engineering Only | Source |
|---|---|---|---|
| AWS monthly spend | ~$383K (March 2026) | — | Cost Explorer |
| AWS running EC2 instances | 201 | — | EC2 API |
| EC2 pre-Graviton percentage | 83% (167/201) | — | EC2 API |
| Lambda EOL runtime percentage | 21% (53/248) | — | Lambda API |
| ECS clusters / services | 38 clusters, 357 services | — | ECS API |
| Total Bitbucket repos | 3,191 across 4 workspaces | — | Bitbucket API |
| Active repos (commits in 90d) | 789 (25%) | — | Bitbucket API |
| madpayments CI/CD coverage | 87% | — | Bitbucket API |
| PR cycle time (sample) | ~27–31h avg for active repos | — | Bitbucket API |
| Jira projects | 141 | ~68 engineering | Jira API |
| Jira boards | 313 (89 scrum, 224 kanban) | — | Jira API |
| Open Jira issues | **18,583** | **13,725** | Jira approximate-count |
| Open issues > 1 year old | 13,377 (72%) | 9,115 (66%) | Jira approximate-count |
| Created last 90d | 2,912 | — | Jira approximate-count |
| Resolved last 90d | 2,973 | — | Jira approximate-count |
| 26-week net backlog growth | -578 (growing) | -269 (growing slower) | Jira approximate-count |
| Flow distribution (resolved 90d) | — | 67% features, 21% defects | Jira approximate-count |
| Sprint velocity trend | — | Declining on multiple boards | Jira Agile API |
| Cycle time P50 (engineering) | — | 59 days | Jira changelog |
| Overloaded assignees (>50 open) | 4 people | — | Jira search |
| Confluence spaces | 165 | — | Confluence API |
| Confluence pages indexed | 14,111 across 15 spaces | — | Confluence API |
| Confluence content extracted | 94 key pages (architecture, RCAs, deployment) | — | Confluence API |
| Unique users across systems | 168 | — | Cross-system audit |
| High activity users (90d) | 32 | — | Cross-system audit |
| Inactive users with access | 65 (39%) | — | Cross-system audit |
| Bitbucket-only users | 61 | — | Cross-system audit |
| Users in both BB + Jira | 69 | — | Cross-system audit |
| Tools identified | 28 | — | Multi-source catalog |
| AI tooling adoption (repos) | 8/30 (27%) with Cursor/Claude/AGENTS.md | — | Bitbucket source API |
| Epic completion rate (12mo) | — | 27.7% (133 of 481) | Jira search |
| REST project epic completion | — | 18.5% (48 of 260) | Jira search |
| NEO project epic completion | — | 12.5% (1 of 8) | Jira search |
| Priority distribution (eng) | — | 89.4% High, 10.6% None | Jira search |
| Story Points coverage | — | 9% of stories estimated | Jira search |
| Root Cause Category populated | — | 0% of resolved bugs | Jira field analysis |
| Pipeline success rate | — | 60.7% (1,563 runs, 30 repos) | Bitbucket Pipelines API |
| ECS containers without health check | 90% (61/68) | — | ECS task definitions |
| ECS unique container images | 49 | — | ECS task definitions |
| EKS clusters | 2 (K8s 1.30, 1.32) | — | EKS API |
| RDS instances (dev) | 8 (MySQL 5.7×3, 8.0×3, PG 15+17) | — | RDS API |
| Reviewer network nodes/edges | 217 / 1,464 | — | Bitbucket PR API |
| Top reviewer (John Harre) | 581 reviews given | — | Bitbucket PR API |
| Reviewer bottleneck repos | 17 (>50% single reviewer) | — | Bitbucket PR API |
| Branch protection (active repos) | 0 of 30 have restrictions | — | Bitbucket API |
| Open PRs | 201 total, 175 >30 days old | — | Bitbucket API |
| Open PRs with 0 comments | 167 (83%) | — | Bitbucket API |
| Incident/RCA documents parsed | 50 (peak year 2022: 26) | — | Confluence API |
| Top incident system | Payments (19), Reports (11), Menu (10) | — | Confluence RCA analysis |
| Sprint retrospectives extracted | 30 across 6 teams | — | Confluence API |
| Heavy reviewers (>100 reviews) | 57 people | — | Bitbucket PR API |
| Tech stack (top 30 repos) | Node(12), Java(4), TS(8), React(5), NestJS(3) | — | Bitbucket source API |

### Analysis Artifacts (in repo)
- `inventory/` — Raw JSON inventory data (18 AWS, 4 BB, Jira, Confluence, users) with segmented Jira output
- `inventory/users/` — Cross-system user audit (168 users with per-user activity profiles)
- `inventory/confluence/content/` — 94 extracted Confluence pages (architecture, RCAs, deployment docs)
- `inventory/tooling_catalog.json` — 28 identified tools with vendor, category, cost status
- `analysis/*.csv` — 17 spreadsheet-ready CSV exports
- `analysis/charts/*.html` — 31 interactive Plotly charts (including review network graph)
- `interview-prep-with-data.md` — Per-interviewee data-backed questions organized by interview day
- `vendor-spend-request.md` — Ready for Don: SaaS/tooling spend request
- `ana-request.md` — Ready-to-send coordination email for Ana
- `scripts/` — 44 reusable inventory and analysis scripts
- `minisite/` — Astro-based engagement dashboard (10 pages, 31 charts, V7 deep analysis sections, Vercel deploy)
- `inventory/cross_system/` — Cross-system correlation data (deploy lead time, bus factor analysis)
- `inventory/confluence/rca_structured.json` — 50 structured incident records with systems, teams, resolution times
- `inventory/confluence/retrospectives.json` — 30 sprint retrospective extractions
- `inventory/aws/ecs_task_definitions.json` — 68 ECS service microservice architecture map
- `inventory/aws/eks_clusters.json` — EKS cluster deep data (K8s versions, node groups, add-ons)
- `inventory/aws/rds_instances.json` — 8 RDS instances with engine versions, encryption, Multi-AZ
- `inventory/aws/security_posture.json` — GuardDuty, ACM, IAM, S3 security data
- `inventory/aws/network_topology.json` — VPC peering, NAT gateways, security groups
- `inventory/aws/backup_dr.json` — Backup plans, snapshot policies
- `inventory/mad-mobile-c4-context.mmd` — Auto-generated C4 Context diagram
- `inventory/mad-mobile-c4-container.mmd` — Auto-generated C4 Container diagram
- `mad-mobile-org-chart.mmd` — Mermaid.js org chart (post-reorg, April 3)
- `don-call-guide-april3.md` — Structured call guide for Don (13 questions)
- `05-ai-tooling-survey.md` — AI Adoption & Tooling survey instrument (16 questions)
- `state-update-april3-reorg.md` — Reorg change log and update instructions

### Open Clarifications (Pending Don Call / Onsite)

- **Akshay Bhasin scope:** March org chart = QE Lead (7 people). April org chart = Payments (18 people). Either a scope expansion (absorbed Payments engineering) or a relabeling (March chart was incomplete). Clarify onsite — 18 people in Payments is a significant org.
- **IT Director:** March org chart listed Jorge Maltes as Director Information Technology. April org chart shows Rosen Georgiev under IT (Strainick). Either Maltes left/was moved and Rosen absorbed IT, or the chart shows a different level. Clarify — IT now reports through COO, whoever runs IT is Adam's contact for infrastructure access and tooling governance.
- **Strainick interview recalibration:** Interview shifted from 30 min on HR/culture to 45 min on COO operations. Secondary purpose: validate whether Strainick is in the seat to stay. If Don's answer reveals this was a "promote to move," focus the interview on documenting the customer operations chain (Account Mgmt → Onboarding → Delivery → IT) as a process map rather than relying on Strainick's strategic perspective.
- **Bailey Shatney framing:** Position Adam's deliverables as a potential resource for Bailey. If she's new and ramping, the Westrum Culture survey baseline, Glassdoor data, and interview themes on culture/retention are exactly what she needs to build her own 90-day plan. This creates a natural ally.

---

## 12. Important Engagement Rules

1. **Pre-engagement hypotheses are not findings.** Diagnostic conclusions cannot be synthesized until after the onsite.
2. **Kennedy/Chathura dynamic is RESOLVED.** The April 3 reorg gave Chathura formal CDO authority over all engineering, product, design, PMO, and customer support. Kennedy narrowed to AI/innovation. Can now be referenced openly in all materials. Onsite validates whether operational reality has caught up to the structural change.
3. **Board/investor deliverable is a core purpose**, not an afterthought. It shapes framing across the charter, executive summary, deliverables, and success criteria.
4. **Surveys designed for Mad Mobile's independent re-use** at 30/60 days. Don't create dependency on Adam.
5. **Friend-to-colleague tone with Don; professional with everyone else.** Careful audience sensitivity in any materials shared with MM leadership.
6. **Anonymous interviews.** Report themes, not who said what.
7. **All public-source research on leadership was mostly wrong.** The official org chart from Don is the authoritative source. Validate everything internally before using externally.
8. **Raw over polished.** For pre-read materials, whatever exists in whatever format is more useful than a curated package.

---

## 13. Reference Links

- **Engagement Plan (Google Doc):** https://docs.google.com/document/d/1bQeR8VA6-uOQEqNw1FMCoJhX-yBP16UPNtLUal46B9s/edit
- **Jira / Confluence:** https://madmobile-eng.atlassian.net/
- **AWS Provisioning Ticket:** https://madmobile-eng.atlassian.net/browse/CLD-2431
- **Mad Mobile Website:** https://madmobile.com/
