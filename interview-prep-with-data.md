# Interview Prep — Data-Backed Questions

**Purpose:** Per-interviewee cheat sheet with specific data points from the pre-work system inventory. These replace generic probes with questions that are harder to deflect. Each question cites its data source and the hypothesis it tests.

**Usage:** Print or have open on a laptop during each interview. Lead with the universal opening, then use these questions to guide the conversation. Don't read them verbatim — they're prompts to weave in naturally.

**Data Note — Jira Segmentation:** Jira is the system of record for the entire company, not just engineering. Of 141 projects, ~68 are engineering, ~50 are customer success implementations, and ~23 are operations/governance. All Jira numbers below are presented as: **overall (engineering-only)**. Engineering-only numbers are the relevant benchmark for DORA and delivery metrics. Overall numbers show how the whole machine operates. Key segmented stats:
- Open issues: **18,583 overall (13,725 engineering)**
- Older than 1 year: **13,377 overall (9,115 engineering — 66%)**
- Created last 90d: **2,912 overall (engineering net -269, overall net -578)**
- Engineering resolved 90d: 67% features, 21% defects (Flow Framework)

---

## Monday, April 13 — Leadership + Architecture

### Jack Kennedy (CTO, 60 min)

| # | Question | Data Point | Hypothesis |
|---|---|---|---|
| 1 | "I've looked across all 18 AWS accounts and can't find a dedicated Neo/AI production environment. I see SageMaker artifacts in the R&D account and active Jira projects (NEO, AAK, LAA), but where does the AI platform actually run in production?" | No Neo/AI AWS account found; SageMaker bucket in mm-cake-r-and-d | C (Fake Platforming) |
| 2 | "83% of running EC2 instances are on pre-Graviton hardware, and 21% of Lambda functions are on end-of-life runtimes — Python 2.7, Node 6, Node 8. Is there a modernization initiative, or is that a known tradeoff?" | 167/201 pre-Graviton; 53/248 EOL Lambdas | F (Legacy Gravity) |
| 3 | "The Shared Services account runs a full Grafana stack — Mimir, Loki, Tempo. That's a mature observability choice. How broadly adopted is it? Do all teams have dashboards and on-call alerts, or is it concentrated in one group?" | Grafana/Mimir/Loki/Tempo in mm-shared-services; Payments has its own instance | G (Missing Cadence) |
| 4 | "The Payments team is architecturally very different from Retail — fully containerized on EKS, Terraform IaC, zero IAM users, their own observability. Was that a deliberate engineering decision? Why doesn't the rest of the org look like that?" | mm-payments-prod-us: 0 EC2, EKS-native, 61 roles, TF state. mm-retail-prod-us: 45 EC2, Amazon MQ, legacy CFN | I (Architectural Polarity) |
| 5 | "There are 3,191 repos across four Bitbucket workspaces, and 75% haven't been touched in 90 days. Is there a repo lifecycle policy, or does everything live forever?" | 2,402/3,191 repos stale | A (Portfolio Sprawl) |

**If time:**
- "Jenkins is running in the CAKE Dev account alongside Bitbucket Pipelines in many repos. Is the intent to consolidate, or are these serving different needs?"
- "The CAKE R&D account has a c6i.12xlarge instance called DockerPos running at ~$1,600/month. What does it build?"

---

### Chathura Ratnayake (CDO, 90–120 min)

| # | Question | Data Point | Hypothesis |
|---|---|---|---|
| 1 | "Sprint velocity on the Ops Prime board dropped from 127 to 56 completed issues per sprint across Q1 — a 56% decline. The OS board shows a similar pattern, 114 down to 49. What happened in Q1?" | Tesla/Ops Prime: 127→114→78→56; OS: 131→119→127→114→78→56→46→49 | G (Missing Cadence) |
| 2 | "There are 18,583 open Jira issues across the org — 13,725 of those are in engineering projects, and 66% of the engineering backlog is older than a year. The remaining 5,000 are customer success implementations and operations. Is the backlog actively groomed, or has it become a place where tickets go to die?" | Overall: 18,583 open, 13,377 >1yr. Engineering: 13,725 open, 9,115 >1yr (66%) | G (Missing Cadence) |
| 3 | "Over the last 26 weeks, engineering projects created 4,701 issues and resolved 4,432 — a net growth of ~269. When you add CS and operations, the org-wide gap is 578. Is anyone tracking that trend?" | Eng: created 4,701 / resolved 4,432. Overall: 5,790 / 5,212 | H (Biz-Tech Mistranslation) |
| 4 | "The madpayments workspace operates very differently from the rest — TypeScript, domain-driven project structure, 87% CI/CD coverage, EKS-native, zero IAM users. Was that an intentional experiment? Could it be a model for other teams?" | madpayments: 80 repos, 65% active, 87% CI/CD vs madmobile 26% active, syscolabs 24% | I (Architectural Polarity) |
| 5 | "How do you allocate engineering capacity across the four Bitbucket workspaces? The syscolabs workspace has 1,527 repos but 76% are stale. Is there a clear boundary between CAKE-era code and new development?" | Workspace activity breakdown | A (Portfolio Sprawl) |

| 6 | "Jira tracks everything — sprint work, Brooks Brothers implementations, GRC audits, hardware commercialization. 50 of 141 projects are non-engineering. Is that by design? Does the noise affect engineering teams' ability to see their own work clearly?" | 141 projects: ~68 eng, ~50 CS, ~23 ops | G (Missing Cadence) |

**If time:**
- "PR cycle times vary wildly — cloud-shared-development averages 0.6 hours, while concierge-associate averages 236 hours. What drives that spread?"
- "How does the Sri Lanka team plug into this? Which workspaces and repos do they primarily contribute to?"

---

### Dulanjan Wengappuliarachchi (VP, Product & GTM, 60 min)

| # | Question | Data Point | Hypothesis |
|---|---|---|---|
| 1 | "Every major retail customer has their own Jira project — Brooks Brothers, Ralph Lauren, Estee Lauder, Signet, Tractor Supply, and more. How do you roll up a portfolio view across 20+ customer projects?" | 20+ customer-specific Jira projects | A (Portfolio Sprawl) |
| 2 | "In the last 30 days across all of Jira, 916 issues were created but only 658 resolved. For engineering specifically, the gap is smaller but still growing — 269 net over 26 weeks. How do you decide what gets deprioritized?" | Overall: 916 created / 658 resolved (30d). Eng 26-week net: -269 | B (Sales-Led Chaos) |
| 3 | "The documented prioritization process uses multi-department scoring and exec alignment on the top 5. How often does a customer escalation or sales promise override that process mid-sprint?" | From Restaurant Update deck; sprint scope change data (pending from V3 scripts) | B (Sales-Led Chaos) |
| 4 | "You have 6 PMs — 3 on Restaurant (Miru, Jake, TBD) and 3 on Payments/Ops/Engineering (Shavin, Richard, Thaddeus). Plus Chris on design, an open marketing role, and L&D. That's a broad scope. What suffers most from that breadth right now?" | CDO org chart detail, open headcount | E (Dependency Drag) |
| 5 | "The CDO roadmap shows 12+ ongoing CAKE projects, 4+ Payments integrations, and Engineering platform work — plus a 'Next Up' queue of 20+ items. How does the multi-department scoring process actually work with that volume? Does executive alignment on the top 5 hold, or does it get overridden?" | CDO product roadmap | B (Sales-Led Chaos) |
| 6 | "Don confirmed that Retail and Neo/AI are in scope for this review, not just CAKE. What do the Concierge/Retail and Neo/AI product roadmaps look like? Are those managed through your team or through different PMs?" | Don scope email | A (Portfolio Sprawl) |

---

### Akshay Bhasin (VP Payments Engineering, 20+, 45 min)

| # | Question | Data Point | Hypothesis |
|---|---|---|---|
| 1 | "The payments codebase has 87% CI/CD coverage, TypeScript throughout, domain-driven project structure, and the cleanest architecture in the company. Your team runs very differently from CAKE and Enterprise. Was that a deliberate engineering decision, and how did you get there?" | madpayments: 80 repos, 65% active, 87% CI/CD, EKS-native, 0 IAM users, TF state | I (Architectural Polarity) |
| 2 | "Your org has 9 Payments R&D engineers under Kevin Reyes, plus 7 Restaurant QE engineers, plus Biz Ops, plus PCI counterparts. That's 20+ people. Restaurant QE reporting under Payments rather than Restaurant Technology is unusual — how does that work? Do your QE engineers sit in the same sprints as Randy's developers?" | CDO org chart PDF | E (Dependency Drag) |
| 3 | "The CDO roadmap shows 4+ Payments integration projects ongoing — Sardine, RS2, CYBS, South State Bank. Plus 6+ Payments Ops projects. How do 9 R&D engineers cover that while also supporting the CAKE payment gateway?" | CDO org chart product roadmap | A (Portfolio Sprawl) |
| 4 | "Payments had 19 incidents in our RCA data, most in 2021–2022. The peak was 26 incidents in 2022. Has reliability actually improved, or did the documentation practice just stop?" | 50 structured RCAs parsed, Payments top system | F (Legacy Gravity) |
| 5 | "Your SL engineers (Gayan K., Susampath M.) are in R&D. How does the US/SL split work for payments development specifically? PR reviews, timezone handoffs, code ownership?" | CDO org chart showing SL staff in R&D | E (Dependency Drag) |

---

### Mark Guilarte (VP Program Management, 4 people, 30 min)

| # | Question | Data Point | Hypothesis |
|---|---|---|---|
| 1 | "Your team has one PM per domain — Qaiser on Restaurant, Vanessa on Payments, Ian on AI, Debbie on Ops Engineering. That's 4 people coordinating across 100+ engineers. How do you maintain visibility across all those teams?" | CDO org chart PMO assignments | G (Missing Cadence) |
| 2 | "The product roadmap shows 12+ ongoing CAKE projects, 4+ Payments integrations, and Engineering platform work. How does the PMO GTM tracker work in practice? Does it actually drive the 4-week release cadence, or do teams ship independently?" | CDO org chart product roadmap; Restaurant Update deck GTM process | G (Missing Cadence) |
| 3 | "Ian is the Project Lead for AI. What does that portfolio look like day-to-day? Which AI/Neo projects are active, and who is he coordinating with — Kennedy's team, Chathura's, or both?" | PMO AI assignment vs. Kennedy/Chathura split | C (Fake Platforming) |

---

## Tuesday, April 14 — Engineering Deep Dive

### Randy Brown (VP Eng, Restaurant Technology, 10 people, 60 min)

| # | Question | Data Point | Hypothesis |
|---|---|---|---|
| 1 | "The REST Jira project has 17,318 issues — more than the next four projects combined. How much of that is actively worked versus inherited backlog?" | REST: 17,318; next: OS 4,794, DSO 4,762, CE 4,441, DR 4,218 | F (Legacy Gravity) |
| 2 | "The syscolabs workspace has 1,527 repos, but 76% haven't been touched in 90 days. The QA project alone has 222 repos. Is there a plan to archive or consolidate?" | syscolabs: 1,527 repos, 361 active, 1,166 stale | A (Portfolio Sprawl) |
| 3 | "PR cycle time for cake-payment-gateway averages 78 hours. react-cinco averages 31 hours. OLO averages 24 hours. Are these the same team? What drives the difference?" | PR metrics from bitbucket/metrics.json | E (Dependency Drag) |
| 4 | "I found Jenkins servers running in the CAKE Development AWS account. Are you on Jenkins, Bitbucket Pipelines, or both? Is there a consolidation plan?" | Jenkins EC2 in mm-cake-development; bitbucket-pipelines.yml in repos | I (Architectural Polarity) |
| 5 | "The CAKE ecosystem has 15+ live systems maintained by 9 engineers — 3 frontend under Alexander Baine, 6 backend under Kyle Budd. The QE team (7 people) reports to Akshay in Payments, not to you. How does that work day-to-day?" | CDO org chart detail | E (Dependency Drag) |
| 6 | "Your roadmap shows 12+ ongoing projects — OLO V2, EMS 2.0, QSR KDS, KDS v2, Restaurant Admin 2.0, VP3350, and more. With your team assignments (CAKEpop/Kiosk v2, Fixed POS, KDS v2/Cloud/Loyalty, Cloud/EMS), how do you allocate 9 engineers across all of that?" | CDO org chart product roadmap + team assignments | A (Portfolio Sprawl) |
| 7 | "POS V3 (Pondus) and V4 (Elio) are running simultaneously. What's the migration path? Are both actively maintained?" | Restaurant Update deck | F (Legacy Gravity) |

---

### Zubair Syed (VP Eng, Enterprise Solutions, 58 people, 60 min)

| # | Question | Data Point | Hypothesis |
|---|---|---|---|
| 1 | "How do you allocate teams across the four Bitbucket workspaces? Do engineers move between madmobile, syscolabs, and madpayments, or are they siloed?" | 4 workspaces with different cultures | I (Architectural Polarity) |
| 2 | "PR reviewer concentration data [from V3 scripts] — are there individuals who review a disproportionate share of PRs? Who are the bottleneck reviewers?" | Pending: reviewer_concentration.json | E (Dependency Drag) |
| 3 | "Assignee concentration data [from V3 scripts] — are there people with 50+ open issues assigned?" | Pending: assignee_concentration.json | E (Dependency Drag) |

---

### Bill Lodes (Former CRO, consulting — OPTIONAL, 30 min)

*Lodes exited April 3. Only interview if available and Don thinks it's valuable. Low priority.*

| # | Question | Data Point | Hypothesis |
|---|---|---|---|
| 1 | "Customer support is now unified under Chathura (CDO). When you ran it, how did escalations flow from support to engineering? What broke in that handoff?" | Reorg change | G (Missing Cadence) |
| 2 | "The 32 per-customer Jira projects — was that your team's model? How did customer requests become engineering work items?" | 32 customer success Jira projects, 2,525 open CS issues | B (Sales-Led Chaos) |

---

### Engineering Managers (2–3, 45 min each)

Adapt these based on which team they lead. Look up their team's board in `inventory/jira/velocity_full.json` and their repos in `inventory/bitbucket/metrics.json` before each session.

| # | Question Template | Source |
|---|---|---|
| 1 | "Your board [NAME] shows [TREND] over the last N sprints — [VALUES]. Does that match your experience? What drove it?" | velocity_full.json |
| 2 | "Your team's average PR merge time on [REPO] is X hours. Does that feel right, or are there outliers skewing it?" | bitbucket/metrics.json |
| 3 | "The Confluence space for [AREA] has X pages. When you need to understand how something works, where do you actually go — Confluence, a person, or somewhere else?" | confluence/spaces.json |
| 4 | "What percentage of your sprint goes to planned work versus interrupt-driven work (escalations, bugs, support)?" | Flow distribution data (pending) |
| 5 | "When priorities change mid-sprint, how does your team hear about it?" | Hypothesis B, G |

---

### Senior ICs (2–3, 30 min each)

| # | Question | Hypothesis |
|---|---|---|
| 1 | "Walk me through the last piece of work you shipped to production. How long from first commit to production? What slowed it down?" | DORA lead time |
| 2 | "How many different repos, languages, and tools do you touch in a typical week?" | Cognitive load / I (Architectural Polarity) |
| 3 | "When you need a decision on architecture or priorities, who do you go to? How long does it take?" | D (Unclear Ownership) |
| 4 | "Are you using Cursor for daily development? How effective is it? What would make AI tooling more useful for your workflow?" | AI strategy assessment |

---

## Wednesday, April 15 — Cross-Functional Validation

### Rajik Gunatilaka (VP & LK Country Head, 45 min video)

| # | Question | Data Point | Hypothesis |
|---|---|---|---|
| 1 | "Which Bitbucket workspaces and repos do the Sri Lanka engineers primarily contribute to?" | 4 workspaces, unclear LK allocation | D (Unclear Ownership) |
| 2 | "How do PR reviews work across the timezone boundary? Do PRs from LK sit overnight waiting for US review, or is there local review authority?" | PR cycle time variance | E (Dependency Drag) |
| 3 | "You report to the COO (Strainick), not the CDO (Chathura). How does that work day-to-day? Do your engineers take technical direction from Chathura/Zubair while reporting through you administratively?" | Org chart: LK → Strainick (COO), dotted line to Chathura (CDO) | D (Unclear Ownership) |

---

### Customer Support Lead (TBD, 30 min)

*Support now unified under Chathura (CDO) — previously under Lodes (CRO). Key to understanding the full build-to-support chain.*

| # | Question | Data Point | Hypothesis |
|---|---|---|---|
| 1 | "Support is now under Chathura, the same executive who owns engineering. Has that changed how escalations work? Is the path from support ticket to engineering fix shorter now?" | Reorg: support → CDO | G (Missing Cadence) |
| 2 | "Walk me through a CAKE payment outage from the support perspective — from first customer call to resolution. Who gets paged, what tools do you use, and how long does it typically take?" | 19 Payments incidents in RCA data | F (Legacy Gravity) |
| 3 | "When you escalate a technical issue, what's the typical response time from engineering? Hours? Days?" | — | G (Missing Cadence) |

---

### David Strainick (COO, 45 min)

*Moved from CPO to COO in April 3 reorg. Now owns Account Management, Onboarding, Delivery, IT — the entire customer operations chain. Completely different interview than originally planned.*

| # | Question | Data Point | Hypothesis |
|---|---|---|---|
| 1 | "You now own the full customer operations chain — Account Management (9), Onboarding (Das DeSilva, 10), Delivery (Chip O'Connell, 3), and IT (Rosen Georgiev). Walk me through how a new customer goes from signed contract to live deployment. Where does it break?" | Org chart: COO scope | G (Missing Cadence) |
| 2 | "IT reports to you now, not CTO. Jorge Maltes is still Dir. IT working on PCI compliance, Rosen Georgiev handles day-to-day ops. How do you govern IT priorities across both compliance and operations?" | CDO org chart + executive chart | D (Unclear Ownership) |
| 3 | "Sri Lanka's country head (Rajik Gunatilaka) reports to you. Engineering resources there have dotted lines to Chathura/Zubair. How does that work in practice? Who sets priorities for SL engineers?" | Org chart: SL → COO, not CDO | D (Unclear Ownership) |
| 4 | "The 32 per-customer Jira projects for retail clients — Brooks Brothers, Ralph Lauren, Estee Lauder — each with their own project space. How does a customer request flow from your Account Management team into engineering?" | 32 customer success Jira projects, 2,525 open CS issues | B (Sales-Led Chaos) |

---

### Greg Schmitzer (President & Head of Sales & Marketing, 30 min)

*Expanded role — absorbed Lodes' sales org. Now has Bobby Jaklitsch (Field Sales, 4), Peter Vu (Inbound, 3), Karen Licker (Marketing, 1).*

| # | Question | Data Point | Hypothesis |
|---|---|---|---|
| 1 | "You've absorbed the full sales organization — field sales, inbound, and marketing. With Don confirming Retail and Neo/AI are in scope alongside CAKE, how does the sales team position these three product lines?" | Don scope email + reorg | A (Portfolio Sprawl) |
| 2 | "Are there features being sold today that don't exist or don't work reliably? The CDO roadmap shows dozens of items marked TBD or Backlog. How does the sales team know what's actually shippable?" | CDO product roadmap | B (Sales-Led Chaos) |
| 3 | "The Sysco/CAKE partnership and acquisition — from your perspective, is the integration done? The codebase still has two separate Bitbucket workspaces." | 4 Bitbucket workspaces | F (Legacy Gravity) |

---

### Chris Gomersall (Director Product Design, 30 min or async)

| # | Question | Hypothesis |
|---|---|---|
| 1 | "How does design hand off to engineering? Is there a design system, or is each product line building its own components?" | A (Portfolio Sprawl) |
| 2 | "The engagement found an 'Agentic Lovable Dev Flow' document in Confluence — Cursor + Chrome DevTools MCP. Is the design team experimenting with AI tooling too?" | AI strategy |

---

## Reference: Hypothesis Key

| Code | Pattern | One-Liner |
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
