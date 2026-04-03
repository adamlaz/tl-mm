# Mad Mobile Engagement — Current State & Context

**Date:** April 3, 2026 (updated from April 2 with automated inventory findings)
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
- **Don Salama** — Co-CEO/Acting CFO. Primary sponsor and strategic collaborator.
- **Ana** — Chief of Staff, Strategic Programs. Don's operational right hand. Primary logistics coordinator (NDA, system access, onsite scheduling, document gathering). Not on the original org chart.

### Mad Mobile Leadership (CTO Org)
- **Jack Kennedy** — CTO. Formal authority. Audience-sensitive dynamic with Chathura — do not surface in shared materials until validated onsite.
- **Chathura Ratnayake** — SVP Global Software Engineering. Operational authority per Don. Key engagement contact. Direct reports include Akshay Bhasin (QE), Randy Brown (VP Eng Restaurant), Matthew Crumley.
- **Randy Brown** — VP Engineering, Restaurant. Runs CAKE/restaurant engineering (~10 engineers + ~7 QE). Key interview target — owns the product line where CAKE outages originate. Reports to Chathura.
- **Zubair Syed** — VP Software Engineering. Direct reports include: Daniel Lomsak, Matias Lopez Riglos, James Oliver, Anthony Goad, Ana Chambers, Nagaswaroopa Kaukuri.
- **Dulanjan Wengappuliarachchi** — Sr. Director, Product & GTM. Broader scope than title suggests — owns PM, Product Design, Product Marketing, L&D/Training. Two open roles (Payments PM, Product Marketing Manager).
- **Akshay Bhasin** — QE Lead. Restaurant QE team (~7 engineers). Reports to Chathura.
- **Jeremy Diggins** — Director Enterprise Technology.
- **Chris Gomersall** — Director Product Design.

### Other Executives
- **Steven Seigel** — COO. Payments strategy, data/analytics, revenue ops. Small org (~5 people).
- **Bill Lodes** — CRO. Sales, partner enablement, customer success, onboarding, PMO, tech support. Large org (~50+ people). Tech support reports here, not to engineering.
- **David Strainick** — Chief People Officer. Owns HR, Sri Lanka country operations, IT, technical training.
- **Greg Schmitzer** — President & Co-Founder. One direct report (Karen Licker, Sr. Director Marketing).

### IT / Infrastructure Contacts (Access Provisioning)
- **Jorge Maltes** — Director Information Technology. Reports to Strainick (CPO), not CTO. IT access contact.
- **Matias Lopez Riglos** — DevOps/infra. Filed AWS provisioning ticket. Handles Bitbucket invites. Reports to Zubair Syed.
- **Rosen Georgiev** — Jira/Confluence admin.
- **Matthew Griffin** — Cloud team. Assigned AWS account provisioning (Jira ticket CLD-2431).

### Sri Lanka
- **Rajik Gunatilaka** — VP & LK Country Head. Reports to Strainick (CPO), not CTO. Engineering resources in Sri Lanka have dotted-line relationships to Chathura/Zubair.

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

### Jira — Inventoried April 3

- **141 projects**, **313 boards** (89 scrum, 224 kanban)
- **~55K total issues**: 31,614 stories, 11,985 bugs, 6,988 subtasks, 4,099 epics, 242 tasks
- **18,583 open issues**: 85% older than 6 months, **72% older than 1 year** — massive backlog debt
- **Created vs resolved (26 weeks)**: 5,790 created, 5,212 resolved — **net growth of 578 issues** (backlog expanding)
- **Sprint velocity (19 active scrum boards)**: Multiple declining trends. Ops Prime dropped from 127 → 56 issues/sprint in Q1 2026 (-56%). OS board dropped from 114 → 49 (-57%).
- **Cycle time P50 = 59 days** (In Progress to Done). P75 = 210 days. P95 = 233 days.
- **Per-customer Jira projects**: Every major retail customer (Brooks Brothers, Ralph Lauren, Estee Lauder, etc.) gets their own project — creates cross-project tracking complexity
- **4 active AI/Neo projects**: AI Evangelism, AI Agent Kanban, L1 AI Agent, Neo — confirms active AI development
- **Largest projects by issue count**: REST (17,318), OS (4,794), DSO (4,762), CE (4,441), DR (4,218), BO (4,091)

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
| D | Unclear Ownership | Formal authority and operational authority are misaligned |
| E | Dependency Drag | A few people/teams are routing bottlenecks |
| F | Legacy Gravity | CAKE architecture prevents speed; no triage of must-modernize vs. can-encapsulate |
| G | Missing Cadence | No consistent execution inspection; leadership discovers reality through fire drills |
| H | Biz-Tech Mistranslation | Business says "eng is slow"; eng says "business is chaotic"; real issue is undefined tradeoffs |
| I | Architectural Polarity | Simultaneous AI-native building + legacy POS maintenance = irreconcilable eng split |

### Methodology & Frameworks
- **Pre-Work surveys:** DORA, Westrum Culture, DevEx/DX Core 4, Pragmatic Engineer Test
- **Onsite:** McKinsey 7S, RAPID, Value Stream Mapping, Theory of Constraints, Team Topologies, Wardley Mapping
- **Deliverables:** PE Tech DD 9-Pillar, Watkins STARS, C4 Model, Fowler's Tech Debt Quadrant, Flow Framework

---

## 8. Surveys (Not Yet Deployed)

Four instruments ready. Target deployment: **Monday, April 7** (pending survey tool confirmation and Don's intro message).

| Survey | Audience | Time | Questions | Measures |
|---|---|---|---|---|
| DORA Quick Check | Engineering leads/managers (1 per team) | ~3 min | 9 | Deploy frequency, lead time, change failure rate, recovery time |
| Westrum Culture | All eng leads, managers, senior ICs, PMs | ~2 min | 7 | Organizational culture type |
| DevEx (DX Core 4) | Individual contributors only | ~5 min | 18 | Feedback loops, cognitive load, flow state, satisfaction |
| Pragmatic Engineer Test | 3–5 engineering leads/senior engineers | ~2 min | 15 | Engineering culture maturity |

**Deployment options:** Use MM's internal survey tool (preferred — checking with HR), or Google Forms fallback.
**Dependency:** Don needs to send an intro message to engineering before surveys go out. Template is written and ready.
**Designed for re-use:** Mad Mobile can re-run at 30/60 days without Adam.

---

## 9. Onsite Interview Plan (April 13–15)

### Monday, April 13 — Leadership + Architecture
| Who | Duration | Focus |
|-----|----------|--------|
| Jack Kennedy | 90 min | Architecture, AI strategy, tech debt |
| Chathura Ratnayake | 90 min | Execution, team health, sprint reality |
| Dulanjan Wengappuliarachchi | 60 min | Roadmap / product decisions |
| Steven Seigel | 45 min | Payments, data, revenue ops |

### Tuesday, April 14 — Engineering Deep Dive
| Who | Duration | Focus |
|-----|----------|--------|
| Randy Brown | 60 min | CAKE engineering, outage patterns |
| Zubair Syed | 45 min | Engineering execution, team allocation |
| Bill Lodes | 45 min | Sales pipeline, feature promises |
| Engineering Managers (2–3) | 45 min each | Team execution, dependencies |
| Senior ICs (2–3) | 30 min each | Day-to-day delivery, tooling |
| Jeremy Diggins | 45 min | Enterprise technology |

### Wednesday, April 15 — Cross-Functional Validation
| Who | Duration | Focus |
|-----|----------|--------|
| Rajik Gunatilaka | 45 min (video) | Sri Lanka engineering |
| Tech Support | 30 min | Escalation paths |
| David Strainick | 30 min | HR / culture |
| Greg Schmitzer | 30 min | Partnerships / GTM |
| Chris Gomersall | 30 min or async | Design |

**Room booking:** Ana will coordinate once interview schedule is locked.

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
- **Quantitative analysis pipeline** — 9 CSV exports, 16 interactive HTML charts in `analysis/charts/`
- **Ana request email drafted** with findings and follow-up access requests (see `ana-request.md`)

### In Progress 🔄
- Waiting on Ana: internal survey tool info from HR
- Waiting on Ana: document gathering folder
- Waiting on Ana: Grafana viewer access (requested)
- Waiting on Ana: answers to Monvia ($25.9K/month!), MenuPad, Relate, Neo/AI infra questions
- Don's intro message for surveys (not yet discussed internally — template ready)
- Mercury banking setup for Translation Layer LLC
- EIN pending from Northwest

### Next Steps (This Week)
1. **Send Ana request email** — `ana-request.md` is ready to send
2. **Build surveys** — have Google Forms ready as fallback regardless of what MM's tool is
3. **Finalize interview schedule** — send to Ana for calendar booking
4. **Nudge Don** on the survey intro message timing (target: ahead of Monday deployment)
5. **Collect pre-read docs** as Ana's folder becomes available
6. **Review analysis charts** — open `analysis/charts/*.html` in browser, identify top findings to lead with onsite
7. **Prep interview questions** — update with specific data points from inventory (e.g., "Your PR cycle time averages X hours — walk me through why")

### System Exploration — Completed (Key Answers)
- **Where does Neo/AI live?** No dedicated account. SageMaker in CAKE R&D. Jira projects exist (NEO, AAK, LAA). Confluence docs exist. But no production AI infrastructure found. **This is a key onsite question for Jack/Chathura.**
- **What are MenuPad-Prod-Metro and Monvia?** Legacy accounts with running instances. Monvia is costing $25.9K/month. **Escalated to Ana.**
- **What CI/CD tools are in use?** Jenkins (CAKE, found in CAKE Dev account) + Bitbucket Pipelines (Retail, Payments). Dual CI/CD system.
- **How are the four Bitbucket orgs related?** madmobile = Concierge/Retail core. syscolabs = CAKE/Leapset legacy. madpayments = Modern payments (TypeScript, domain-driven). syscolabsconf = Dead CAKE-era configs.
- **What monitoring/observability exists?** Self-hosted Grafana stack (Mimir + Loki + Tempo) in Shared Services. Payments has its own Grafana instance. **Not Datadog or New Relic.** Viewer access requested.
- **Are there other platforms?** Wiz.io for security scanning. GuardDuty across all accounts. AWS Marketplace seller functions. Backstage/TechDocs likely (mm-techdocs-storage bucket found).

### Pre-Work Quantitative Baseline (Available for Onsite)

| Metric | Value | Source |
|---|---|---|
| AWS monthly spend | ~$383K (March 2026) | Cost Explorer |
| AWS running EC2 instances | 201 | EC2 API |
| EC2 pre-Graviton percentage | 83% (167/201) | EC2 API |
| Lambda EOL runtime percentage | 21% (53/248) | Lambda API |
| Total Bitbucket repos | 3,191 across 4 workspaces | Bitbucket API |
| Active repos (commits in 90d) | 789 (25%) | Bitbucket API |
| Stale repos | 2,402 (75%) | Bitbucket API |
| madpayments CI/CD coverage | 87% | Bitbucket API |
| Jira projects | 141 | Jira API |
| Jira boards | 313 (89 scrum, 224 kanban) | Jira API |
| Total Jira issues | ~55,000 | Jira approximate-count |
| Open Jira issues | 18,583 | Jira approximate-count |
| Open issues > 1 year old | 13,376 (72%) | Jira approximate-count |
| Issues created (last 90d) | 2,912 | Jira approximate-count |
| Issues resolved (last 90d) | 2,973 | Jira approximate-count |
| Sprint velocity trend | Declining on multiple boards | Jira Agile API |
| Cycle time P50 | 59 days | Jira changelog |
| Confluence spaces | 165 | Confluence API |
| Largest Confluence space | Leapset Platform (6,445 pages) | Confluence API |
| PR cycle time (sample) | ~27–31h avg for active repos | Bitbucket API |

### Analysis Artifacts (in repo)
- `inventory/` — Raw JSON inventory data (18 AWS, 4 BB, Jira, Confluence)
- `analysis/*.csv` — 9 spreadsheet-ready CSV exports
- `analysis/charts/*.html` — 16 interactive plotly charts (open in browser)
- `inventory/summary.md` — V1 consolidated summary
- `ana-request.md` — Ready-to-send email for Ana
- `scripts/` — Reusable inventory and analysis scripts

---

## 12. Important Engagement Rules

1. **Pre-engagement hypotheses are not findings.** Diagnostic conclusions cannot be synthesized until after the onsite.
2. **Kennedy/Chathura dynamic is a live variable.** Do not surface in any shared materials until validated onsite. Treat with audience sensitivity in all documents.
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
