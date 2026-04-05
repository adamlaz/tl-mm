# Mad Mobile Engagement — Current State & Context

**Date:** April 5, 2026 (updated April 5 evening with Don April 5 call findings, Bloom Intelligence/Winmark research, file consolidation, hypothesis investigation leads, Ana email updates)
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
| Chathura Ratnayake | **CDO** *(was SVP Global Software Engineering)* | ALL engineering (restaurant, enterprise, payments), product, design, platform, PMO, ALL customer support | Mark Guilarte (PMO, 4), Akshay Bhasin (Payments & Financial Services, 20+), Zubair Syed (Enterprise Solutions, 58), Randy Brown (Restaurant Tech, 10), Dulanjan W. (Product & GTM, 10+) |
| Jack Kennedy | CTO | **AI capabilities and platform innovation only** *(operational engineering scope removed)*. **April 5 update:** Currently full-time on single-client AI delivery — building an AI-developed POS application for **Winmark Corporation** ($5M new client, ~1,265 franchise stores including Play It Again Sports). Agentic programming, year-long delivery. Not currently building Neo or internal platform AI. | Jeremy Diggins — very small team |
| Bailey Shatney | **VP of Human Resources** *(new to org chart — was David Strainick's domain)* | HR, recruiting | Renee Pauley (Recruiting). **Note:** L&D (Ayodele Lawal, Adriana Zuniga) may report here per Don's chart OR under Dulanjan's Product team per Chathura's chart — discrepancy flagged. |
| Ana Chambers | Chief of Staff, Strategic Programs | Cross-company execution, initiative alignment | — |

**Key changes from March org chart:**

1. **Steven Siegel (COO) — EXITED.** Payments strategy, data/analytics, revenue ops responsibilities redistributed.
2. **Bill Lodes (CRO) — EXITED.** Staying in consulting capacity on payments strategy transition. Sales absorbed by Greg Schmitzer.
3. **Chathura Ratnayake — PROMOTED to CDO.** Now owns: all engineering across all verticals, product, design, platform, PMO, and ALL customer support. This is the single largest org in the company (~94+ people based on reported counts).
4. **Jack Kennedy — SCOPE NARROWED.** Retains CTO title but operational engineering authority transferred to Chathura. Officially focused on "AI capabilities and innovation across the platform." Direct team is just Jeremy Diggins. (**Correction:** Holly Bobal is under Randy Brown's Restaurant Backend team per Chathura's CDO org chart, not under Kennedy.) **April 5 update from Don:** Kennedy is currently full-time building an AI-developed POS application for Winmark Corporation (a $5M new client — franchisor of Play It Again Sports and other resale retail brands, ~1,265 stores across US/Canada). This is single-client delivery work, not internal platform or Neo development. Needs further investigation: what is being built, what tech stack, is any of it reusable for MM's platform?
5. **David Strainick — MOVED from CPO to COO.** Now owns Account Management, Onboarding, Delivery, and IT. IT (Jorge Maltes → Rosen Georgiev) now reports through COO, not CTO.
6. **Bailey Shatney — NEW to executive team.** VP of HR. Takes over People functions from Strainick.
7. **Manuel Garcia — NEW to executive team.** Interim CFO. Also absorbed Revenue Operations (previously Siegel).
8. **Greg Schmitzer — EXPANDED.** President + now Head of Sales & Marketing. Absorbed Lodes' sales org.
9. **Customer support unified under Chathura (CDO)** — previously under Lodes (CRO). This puts the full build-to-support chain under one executive.

**Kennedy/Chathura dynamic: RESOLVED.** The hypothesis that formal and operational authority were misaligned (Hypothesis D) has been resolved by org structure change. Chathura now has both formal AND operational authority. Kennedy's role is explicitly narrowed to AI/innovation. This is no longer a "live variable" — it's a confirmed finding. Can now be referenced openly in all materials.

### Chathura's Direct Reports (from CDO org chart, April 3)

**Leadership Structure** (per Chathura's org chart PDF):

- **Dulanjan W.** — VP, Product & GTM (10+ people)
- **Randy Brown** — VP Engineering, Restaurant Technology (10 people)
- **Zubair Syed** — VP Engineering, Enterprise Solutions (58 people)
- **Akshay Bhasin** — VP Payments Engineering (20+ people)
- **Mark Guilarte** — VP Program Management (4 people)
- **Customer Support** — all levels, headcount TBD. New under Chathura.

**Note:** Chathura flagged "we are working through some title changes." Titles below are from his April 3 org chart PDF and may differ from earlier sources.

#### Randy Brown — Restaurant Technology (10 people)

| Sub-Team | Name | Title |
|---|---|---|
| **Frontend** | Alexander Baine | Manager, Software Engineering |
| | Cory Renard | Staff Software Engineer |
| | Rob Quin | Software Engineer |
| **Backend** | Kyle Budd | Manager, Software Engineering |
| | Beau Bruderer | Senior Software Engineer |
| | Holly Bobal | Senior Software Engineer |
| | Siva Ganesh | Software Engineer |
| | Harrison Minchew | Lead Software Engineer |
| | Anderson Lavor | Lead Software Engineer |

Team assignments: CAKEpop/Kiosk v2, Fixed POS, KDS v2/Cloud/Loyalty, Cloud/EMS.

#### Akshay Bhasin — Payments & Financial Services (20+ people)

| Sub-Team | Name | Title |
|---|---|---|
| **Payments R&D** | Kevin Reyes | Director, Software Engineering |
| | Trenton Kress | Staff Software Engineer |
| | Pratikchha Kahdka | Software Engineer |
| | Peter Wu | Staff Software Engineer |
| | Paul Robert | Senior Software Engineer |
| | Richard Meitzler | Staff Software Engineer |
| | Gayan K (SL) | Staff Software Engineer |
| | Susampath M (SL) | Senior Software Engineer |
| | Matthew Griffin | Senior Cloud Engineer |
| **Restaurant QE** | Sowjanya Akula | Senior Quality Engineer |
| | Danika M (SL) | Senior Quality Engineer |
| | Darren Blackwell | Quality Automation Engineer |
| | Rekha Mohanan | Senior Quality Engineer |
| | Bill Fenley | Senior Software Engineer, Quality |
| | Kaelon Lucas | Quality Automation Engineer |
| | Patrycja Stevenson | Senior Software Engineer, Quality |
| **Biz Operations** | Andy Honnold | Sr. Director Payments Strategy |
| | Altaaf A (SL) | Payment Operations Manager |
| | Kanchana A (SL) | Senior Payments Operations Analyst |
| | Angie Mroczka | Payment Risk Fraud Analyst |
| **PCI DSS Counterparts** | Mark Freid | Senior Security Engineer |
| | Debbie Keye | PMO |
| | Jorge Maltes | Dir. Information Technology |
| | Matias Riglos | Solution Operations |
| **PMO Counterpart** | Vanessa Sotomayor | Program Manager |
| **Product (TBD)** | TBD | Product Manager |

**Andy Honnold dual-reporting note:** Don's executive org chart places Andy Honnold under Garcia (CFO). Chathura's functional org chart places him under Akshay as Sr. Director Payments Strategy. Likely functional reporting through Payments, administrative through Finance. Clarify onsite.

**Enterprise Solutions Operations note:** Operations team transitioned Nov 2025. 57% reduction on L2 team size (Oct 2025), 72% reduction on L3 team size (Oct 2025). Altaaf and Kanchana support payments ecosystem.

#### Dulanjan W. — Product & GTM (10+ people)

| Sub-Team | Name | Title |
|---|---|---|
| **PM (Restaurant)** | Miru S. | Senior Product Manager |
| | Jake L. | Product Manager |
| | TBD | Product Manager |
| **PM (Payments/Ops/Eng)** | Shavin P. | Senior Product Manager |
| | Richard F. | Product Manager |
| | Thaddeus F. | Product Manager |
| **Product Design** | Chris Gomersall | Director, Product Design |
| **Product Marketing** | TBD | Product Marketing Manager |
| **L&D** | Adriana Z. | Technical Training Specialist |
| | Ayodele L. | Technical Training Specialist |

**L&D reporting discrepancy:** Chathura's CDO org chart places Adriana Z. and Ayodele L. under Dulanjan's Product L&D team. Don's executive org chart placed them under Bailey Shatney (VP HR). Could be a matrix situation or a reorg-day discrepancy. Clarify onsite.

#### Mark Guilarte — PMO (4 people)

| Domain | Name | Title |
|---|---|---|
| Restaurant | Qaiser P. | Senior Program Manager |
| Payments | Vanessa S. | Program Manager |
| AI | Ian B. | Project Lead |
| Ops Engineering | Debbie K. | Senior Project Manager |

### New Names on the Org Chart (Executive Level — from Don's April 3 chart)
- **Manuel Garcia** — Interim CFO
- **Bailey Shatney** — VP Human Resources
- **Mark Do** — Assistant Controller (reports to Garcia)
- **Zachary Honnold** — RevOps (1), reports to Garcia
- **Bobby Jaklitsch** — Field Sales (4), reports to Schmitzer
- **Peter Vu** — Inbound Sales (3), reports to Schmitzer
- **Das DeSilva** — Onboarding (10), reports to Strainick
- **Chip O'Connell** — Onboarding Delivery (3), reports to Strainick
- **Mark Guilarte** — PMO (4), reports to Chathura
- **Renee Pauley** — Recruiting, reports to Shatney

### New Names from CDO Org Chart (from Chathura's April 3 PDF)
- **Alexander Baine** — Manager, Software Engineering (Restaurant Frontend, reports to Randy Brown)
- **Cory Renard** — Staff Software Engineer (Restaurant Frontend)
- **Rob Quin** — Software Engineer (Restaurant Frontend)
- **Kyle Budd** — Manager, Software Engineering (Restaurant Backend)
- **Beau Bruderer** — Senior Software Engineer (Restaurant Backend)
- **Siva Ganesh** — Software Engineer (Restaurant Backend)
- **Harrison Minchew** — Lead Software Engineer (Restaurant Backend)
- **Anderson Lavor** — Lead Software Engineer (Restaurant Backend)
- **Kevin Reyes** — Director, Software Engineering (Payments R&D, reports to Akshay)
- **Trenton Kress** — Staff Software Engineer (Payments R&D)
- **Pratikchha Kahdka** — Software Engineer (Payments R&D)
- **Peter Wu** — Staff Software Engineer (Payments R&D)
- **Paul Robert** — Senior Software Engineer (Payments R&D)
- **Richard Meitzler** — Staff Software Engineer (Payments R&D)
- **Gayan K (SL)** — Staff Software Engineer (Payments R&D)
- **Susampath M (SL)** — Senior Software Engineer (Payments R&D)
- **Sowjanya Akula** — Senior Quality Engineer (Restaurant QE under Akshay)
- **Danika M (SL)** — Senior Quality Engineer (Restaurant QE)
- **Darren Blackwell** — Quality Automation Engineer (Restaurant QE)
- **Rekha Mohanan** — Senior Quality Engineer (Restaurant QE)
- **Bill Fenley** — Senior Software Engineer, Quality (Restaurant QE)
- **Kaelon Lucas** — Quality Automation Engineer (Restaurant QE)
- **Patrycja Stevenson** — Senior Software Engineer, Quality (Restaurant QE)
- **Angie Mroczka** — Payment Risk Fraud Analyst (Payments Biz Ops)
- **Altaaf A (SL)** — Payment Operations Manager (Payments Biz Ops)
- **Kanchana A (SL)** — Senior Payments Operations Analyst (Payments Biz Ops)
- **Mark Freid** — Senior Security Engineer (PCI DSS Compliance)
- **Miru S.** — Senior Product Manager (Product, Restaurant)
- **Jake L.** — Product Manager (Product, Restaurant)
- **Shavin P.** — Senior Product Manager (Product, Payments/Ops/Eng)
- **Richard F.** — Product Manager (Product)
- **Thaddeus F.** — Product Manager (Product)
- **Qaiser P.** — Senior Program Manager (PMO, Restaurant)
- **Ian B.** — Project Lead (PMO, AI)
- **Debbie K.** — Senior Project Manager (PMO, Ops Engineering)

### Departed
- **Steven Siegel** — Former COO. Exited April 3, 2026.
- **Bill Lodes** — Former CRO. Exited April 3, 2026. Consulting on payments strategy transition.

### IT / Infrastructure Contacts (Access Provisioning)
- **Rosen Georgiev** — IT (reports to Strainick/COO). Day-to-day IT operations. Previously identified as Jira/Confluence admin.
- **Jorge Maltes** — Dir. Information Technology. **RESOLVED:** Not departed — confirmed present in Chathura's CDO org chart as PCI DSS Compliance counterpart under Payments. Maltes handles IT governance/compliance; Georgiev handles day-to-day IT under COO.
- **Matias Lopez Riglos** — DevOps/infra ("Solution Operations" per CDO org chart, listed as PCI DSS counterpart under Payments). Filed AWS provisioning ticket. Handles Bitbucket invites.
- **Matthew Griffin** — Senior Cloud Engineer (Payments R&D under Kevin Reyes). Assigned AWS account provisioning (Jira ticket CLD-2431).

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
- Grafana dashboard access — **confirmed for Monday April 6** (Ana: "I can get you access on Monday. Matias is off today for the holiday weekend.")
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
1. **Org chart (executive)** — MadMobile_OrgChart_v2_pptx.pdf (March 2026, from Don). Superseded by April 3 reorg.
2. **Org chart (executive, April 3 reorg)** — From Don, April 3. Executive-level post-reorg structure.
3. **CDO Org Chart & Product Roadmap** — "CDO Organization and Product Roadmap - 2026" PDF from Chathura (April 3). 10-page document containing: leadership structure, product team detail, restaurant engineering team detail, payments & financial services org detail, enterprise solutions operations notes, PMO org, and **product roadmap for CAKE, CAKE+Payments, Payments Ops, and Engineering**.
4. **Restaurant Update deck** — Restaurant_Update_March_2026.pdf. Contains: product team org, restaurant engineering team, prioritization process, requirements process, restaurant roadmap, CAKE ecosystem map, AI usage overview, GTM process.

### Product Roadmap (from CDO Org Chart PDF, April 2026)

| Column | Category | Key Ongoing Projects |
|---|---|---|
| CAKE | Restaurant product | Custom Quick PIN (Mar 15), CAKE OLO V2 UI Revamp (Mar 31), EMS 2.0 Variant Indicator at Location Level (Mar 31), QSR KDS Multi-POS Deployment (Mar 31), KDS V2 PAC Enhancements (TBD), KDS Application (Early May), Restaurant Admin 2.0 (Early May), Reporting (Early May) |
| CAKE + Payments | Payment integrations | New Payment Device VP3350 (Mar 15), MadPay App Hardening for Kiosk (Apr 15), CAKE POP Certification with CyberSource (End Apr), South State Bank Integration (End May) |
| Payments Ops | Operations tooling | Sardine Integration (End Apr), RS2 Integration (End May), CYBS Integration (End May), Customer Health Score Enhancements (TBD), Reporting (TBD), Suspicious Tip Holds (TBD), Worldpay Mastercard MATCH (TBD), Proxy for Portals (TBD) |
| Engineering | Platform/infra | Multi-Location Reporting/Sales Reports (Mar 15), Convert Existing Customers to PAYG (Apr), Onboarding Backend Services to NestJS (TBD), Existing Workflow to Flow Conversion (TBD) |

**Next Up / Planned:** EzCater Integration (Design), Tip Auth Flows (Plan), Updates to TIP Reporting for BBBA (Plan), Tax Exempt Delivery Orders (Plan), Kiosk V2 Reporting (Plan), Support Salaried Employees (Plan), Channel Pricing (Backlog), Handling Menu Variations (Backlog), Hardening (Plan), Gateway Enhancement for Provider ID (TBD), Pre-Auth (Backlog), Dual Pricing/Cash Discount (Backlog), Digital Gift Cards (Backlog), Support Extra Fees (Backlog), PCI Compliance Audit Support (TBD), Migration Tools for MPP (TBD), Reporting for MPP (TBD), Re-Do OLO Flows for MPP (TBD), MadPay App Consolidation (TBD), various onboarding/CPQ fixes (Backlog), Post Support Case Sentiment (Backlog), Automate CC Rates from SF to Payments (Backlog).

### Pending (Ana's team gathering into a shared folder — target: early Monday April 7)

| # | Document | Priority | Status | Notes |
|---|---|---|---|---|
| 1 | Product roadmap: Concierge/Retail | High | Needed | Don confirmed Retail in scope. Completes the product picture alongside restaurant roadmap. |
| 2 | Product roadmap: Neo/AI | High | Needed | Don confirmed Neo/AI in scope. Critical for AI strategy assessment — but per April 5 call, may not exist in any meaningful form. |
| 3 | Revenue breakdown by product line (CAKE vs Concierge vs Neo vs Payments) | High | Needed — Ana working on | Even approximate revenue breakdown is useful. Revenue data owner unclear post-Siegel exit — likely Garcia (CFO) or Strainick (Account Mgmt). |
| 4 | Investor/lender presentation deck | High | Expected from Don directly | Don offered to share on April 5 call. Contains "the problems, the analysis, and the proposed solution" that Morgan Stanley / Western Alliance saw. If routed through Ana, capture it. |
| 5 | Top 3–5 customer escalations (last 12 months) | High | Needed | Especially CAKE payment outages. Gives specific cases to trace onsite. |
| 6 | Architecture diagrams beyond CAKE ecosystem | Medium | Partially received | Have CAKE ecosystem diagram. Need Concierge and Neo system-level architecture. |
| 7 | Engineering team assignments by product line (beyond restaurant) | Medium | Partially received | Have restaurant eng team (Randy) and payments (Akshay). Need Enterprise Solutions (Zubair — 58 people, zero names). |
| 8 | Deployment environments, release cadence, CI/CD documentation | Medium | Partially self-served | Jenkins (CAKE) + Bitbucket Pipelines (Retail, Payments) identified from systems scan. Still need formal environment documentation. |
| 9 | KPI / scorecard / dashboard screenshots | Medium | Needed | Whatever metrics leadership reviews. |
| 10 | Sprint velocity metrics (last 6–12 months) | Medium | Self-served from Jira | Have 19 active scrum boards with velocity data. Multiple declining trends. |
| 11 | Incident reviews / post-mortems / retrospectives | Medium | Partially self-served | 50 structured RCAs from Confluence (2020–2023). Gap in 2024–2025. Asked Ana about where current process lives. |
| 12 | Engineering and operations tool inventory | Medium | Self-served | 48 tools identified across all platforms. Cost data still needed (see ana-request.md items 10–13). |
| 13 | Open strategic initiatives and known problem projects | Medium | Needed | |
| 14 | Third-party vendor contracts and API dependency inventory | Low | Needed | OpenAI, Anthropic, AWS costs. Visa/Cybersource terms. Major SaaS subscriptions. |
| 15 | CAKE acquisition integration docs and current state | Low | Needed | Original integration plan from 2020. What's done? What's left? |
| 16 | Company goals, board goals, CEO goals | Low | Pending Don's deck | Stated priorities for 2026. May be covered by the investor deck Don is sharing. |

---

## 6. What I Know About the Technology Landscape

### CAKE Ecosystem (from Restaurant Update deck)
- **15+ live systems**: POS V3 (Pondus), POS V4 (Elio), Kiosk v1, OLO v1, KDS v1, Gift Cards v1, Guest Manager, Kiosk v2, Loyalty v1, OrderPad, CAKEpop, Email Marketing, Restaurant Admin 1.0, Customer Display
- **POS V3 and V4 running simultaneously** — migration not complete
- **In active development**: CAKE OLO UI Refresh, EMS 2.0 Multi Location, Gift Cards (Factor 4), CAKEpop features, KDS v2, VP 3350 (new payment device)
- **Planned**: OLO v2, Loyalty v2, Restaurant Admin 2.0
- **Third-party integrations**: Checkmate, 7Shifts, OLO.com, LRS, Paytronix, Bloop, DoorDash, NOLO, Orca, Davo, Parafin, Dolce, QSR KDS
- **Team size**: 9 engineers (2 managers, 2 leads, 2 staff, 3 ICs) under Randy Brown. Restaurant QE (7 people) reports under Akshay Bhasin (Payments), not Randy — unusual structure. Combined: ~16 people for 15+ live systems. This ratio vs. system surface area is a primary investigation target.

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
- Neo/AI gap: heavy marketing, **no dedicated production infrastructure found in systems scan** — SageMaker artifacts in R&D only. Don's April 5 comments align with this assessment. **OPEN INVESTIGATION ITEM:** Need to search Jira (NEO, AAK, LAA projects), Bitbucket, and Confluence for Neo artifacts in pre-work, and validate onsite with Kennedy and Chathura. Kennedy currently full-time on Winmark client delivery, not Neo.
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
| B | Sales-Led Chaos | Revenue promises create roadmap churn and tech debt. **Investigation leads (April 5):** Don described a pattern of priority shifting under previous leadership that aligns. Need independent evidence: Jira epic churn/cancellation data, sprint scope change metrics, roadmap revision history, interview corroboration from multiple sources. Don's description shapes where to look — the data must speak for itself. |
| C | Fake Platforming | Leadership talks "platform"; teams maintain customer-specific patchwork. **Investigation leads (April 5):** Don pushed back — CAKE/restaurant may be genuinely platformized. Enterprise/Retail may be where the sprawl lives. Legacy systems "can't evolve" and must be replaced. Need to validate with Bitbucket repo analysis (shared codebases vs. per-customer forks), onsite architecture walkthroughs, interviews with Randy (Restaurant) vs. Zubair (Enterprise). More nuanced than initially assumed. |
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

Five instruments ready. Target deployment: **Monday, April 6** (via Microsoft Forms on MM account, intro from Chathura as CDO).

| Survey | Audience | Time | Questions | Measures |
|---|---|---|---|---|
| DORA Quick Check | Engineering leads/managers (1 per team) | ~3 min | 9 | Deploy frequency, lead time, change failure rate, recovery time |
| Westrum Culture | All eng leads, managers, senior ICs, PMs | ~2 min | 7 | Organizational culture type |
| DevEx (DX Core 4) | Individual contributors only | ~5 min | 18 | Developer experience: feedback loops, cognitive load, flow state |
| Pragmatic Engineer Test | 3–5 engineering leads/senior engineers | ~2 min | 15 | Engineering culture maturity |
| **AI Adoption & Tooling** | **All engineering, product, design, QE** | **~5 min** | **20** | **AI tool adoption, effectiveness, tooling landscape, AI strategy clarity** |

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

**Deployment:** All 5 surveys built in Microsoft Forms on MM account. Ready for Chathura to send. Links below.
**ISSUE: Chathura's email only references 4 surveys, not 5.** His email mentions: Delivery Performance (leads/managers), Team Culture (everyone), Developer Experience (ICs), Engineering Practices (leads/seniors). He dropped the AI Adoption & Tooling survey. **Action needed:** Follow up with Chathura to either add Survey 5 or understand why he excluded it. The AI survey feeds directly into the board deliverable and vendor rationalization — it's important.
**Chathura's survey email key changes from Adam's draft:** Added "As mentioned in technology all hands" framing, deadline April 10, message will come directly from Chathura. His version is polished and ready to send.

**Microsoft Forms Links (all live):**
- **DORA Quick Check** (9 questions): https://forms.cloud.microsoft/Pages/DesignPageV2.aspx?origin=RevampFRE&subpage=design&id=ib_aDhNew0Kr1vaH6f4POuzhwTnhYKxDp5P7TQtHDhRUQU9JNFJJMzg2R1dGUlhWRTYwODc1UURaVi4u
- **Westrum Culture** (7 questions): https://forms.cloud.microsoft/Pages/DesignPageV2.aspx?origin=RevampFRE&subpage=design&id=ib_aDhNew0Kr1vaH6f4POuzhwTnhYKxDp5P7TQtHDhRURjJXR01JU0Q5Tk8xSFNKUVFWMEIxQ1FSMC4u
- **Pragmatic Engineer Test** (15 questions): https://forms.cloud.microsoft/Pages/DesignPageV2.aspx?origin=RevampFRE&subpage=design&id=ib_aDhNew0Kr1vaH6f4POuzhwTnhYKxDp5P7TQtHDhRUNUtQWVRMWlZQRExUME1LMjNJM1lER0xaTC4u
- **AI Adoption & Tooling** (20 questions): https://forms.cloud.microsoft/Pages/DesignPageV2.aspx?origin=RevampFRE&subpage=design&id=ib_aDhNew0Kr1vaH6f4POuzhwTnhYKxDp5P7TQtHDhRUMDNHRTNRU05KRTdRWDJWTE41UFZEMkUxNi4u
- **DevEx (DX Core 4)** (23 questions): https://forms.cloud.microsoft/r/021mP98Sf9

**Designed for re-use:** Mad Mobile can re-run at 30/60 days without Adam.

### Survey Analysis Plan

**Pre-Onsite (by April 12):**
- Score each survey per the scoring guides in the individual survey files
- Segment by team/product area wherever possible (CAKE/Restaurant vs. Concierge/Retail vs. Neo/AI)
- Identify top 3 patterns from each survey
- Flag extreme outliers (very high or very low scores)
- Build 2–3 data-informed interview questions (e.g., "Your team's DORA lead time self-reports as X — does that match your experience?")

**Onsite (April 13–15):**
- Reference survey data during interviews: "The survey data suggests X — does that resonate?"
- Use Westrum culture scores to gauge which teams may be more or less candid
- Cross-reference DORA self-reported metrics against actual system data (see table below)

**Post-Engagement:**
- Package all five surveys with Mad Mobile-specific instructions, baseline scores, and comparison guidance
- Deliver as the "Baseline Survey Package (Repeatable)" — a core deliverable so MM can re-run at 30/60 days
- Include a simple scoring template so Don's team can interpret results without Adam

### DORA Cross-Reference Plan: Self-Reports vs. Actual System Data

| DORA Self-Report | Actual System Metric | Source |
|---|---|---|
| Deploy frequency | Bitbucket merge frequency to default branch; deployment tag frequency per repo | `inventory/bitbucket/metrics.json`, `inventory/bitbucket/deploy_tags.json` |
| Lead time for changes | PR cycle time: ranges from 0.6h (cloud-shared-development) to 235h (concierge-associate) | `inventory/bitbucket/metrics.json` |
| Change failure rate | Jira bug creation rate: 11,985 total bugs, ~916 issues created/month, bug-to-story ratio | `inventory/jira/issue_distribution.json` |
| Recovery time | Grafana MTTR dashboards (pending access) | Awaiting Grafana viewer access |
| Reliability | CloudWatch alarms (pending permission), SLA data from interviews | Awaiting cloudwatch:DescribeAlarms |

If a lead self-reports "weekly deploys" but their repos show biweekly merge cadence, that gap becomes a specific follow-up question in the interview.

---

## 9. Onsite Interview Plan (April 13–15)

**Updated to reflect April 3 reorg. Major changes: Siegel removed, Lodes deprioritized, Strainick refocused, Kennedy handled with care, Chathura expanded.**

### Monday, April 13 — Leadership + Strategy

| Who | Title | Duration | Focus | Notes |
|-----|-------|----------|-------|-------|
| Chathura Ratnayake | CDO | 90–120 min | Full org ownership, execution model, team health, support unification, PMO integration, sprint reality, AI strategy from build side | **Most important interview of the engagement.** Owns the entire build-to-support chain. May need two sessions. |
| Jack Kennedy | CTO | 60 min *(reduced from 90)* | AI/innovation roadmap, Neo platform vision, infrastructure plans, his view of the path forward | **Handle with care.** Operational scope just removed. Focus on what he's building, not what he lost. Don't probe the reorg dynamics directly — let him volunteer. |
| Dulanjan W. | VP, Product & GTM | 60 min | Roadmap governance, product decisions, design process, PM/engineering handoff, product roadmap (from PDF) | Now reports to Chathura. Has 6 named PMs, 1 design director, open marketing role, L&D. Ask about the transition. |
| David Strainick | COO *(was CPO)* | 45 min | Account management, onboarding, delivery execution, IT operations, customer experience | **Completely different interview than planned.** Was going to be 30 min on HR/culture. Now 45 min on operational execution. Ask about IT governance and how onboarding/delivery handoff works with engineering. |

### Tuesday, April 14 — Engineering Deep Dive

| Who | Title | Duration | Focus | Notes |
|-----|-------|----------|-------|-------|
| Randy Brown | VP Eng, Restaurant Technology (10) | 60 min | CAKE engineering, outage patterns, V3→V4 migration, team capacity vs. system surface area | 9 engineers (2 managers, 2 leads, 2 staff, 3 ICs) for 15+ live systems. Frontend (3) and Backend (6) split. This ratio is the story. |
| Zubair Syed | VP Eng, Enterprise Solutions (58) | 60 min | Concierge/Retail execution, enterprise customer projects, team structure, offshore coordination | Largest eng org by headcount. |
| Akshay Bhasin | VP Payments Engineering (20+) | 45 min | Payments engineering, architecture (the cleanest codebase), scaling, how this team operates differently, QE org, PCI compliance | Scope confirmed: Payments R&D (Kevin Reyes, 9), Restaurant QE (7), Biz Operations (4), PCI counterparts. Much larger than originally reported. |
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
- **Survey 5 (AI Adoption & Tooling) instrument designed** (see `05-ai-tooling-survey.md`, 20 questions)
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
- **CDO Org Chart & Product Roadmap received** from Chathura (April 3). 10-page PDF with detailed org chart for all CDO direct reports (except Enterprise Solutions/Zubair which was mostly blank), product roadmap for CAKE/Payments/Engineering. Key corrections: Holly Bobal under Randy Brown (not Kennedy), Akshay Bhasin org is 20+ people (not 18), Randy Brown team is 10 (not 8), Dulanjan title is VP Product & GTM, Jorge Maltes confirmed still at company (PCI counterpart).
- **Ana logistics partially confirmed** (April 3 email): Grafana Monday, pre-reads Monday, interview scheduling next week, conference room needs TV/screen response.
- **Don scope confirmed** (April 3 email): "Retail and Neo/AI in scope please with main focus obviously restaurant."

- **Engagement minisite expanded** — engagement section rebuilt with 6 subpages (timeline, hypotheses, leadership, interviews, deliverables), 3 new components (FindingCard, MilestoneStep, enhanced SectionHeader), 5 new ECharts charts (hypothesis evidence radar, org size treemap, reorg sankey, effort waterfall, methodology heatmap). TL deliverable standards applied throughout (April 5).
- **Don touchbase** (April 5) — casual ~15 min call. Key findings: Kennedy full-time on Winmark client delivery (AI POS app, $5M), Neo has no production infrastructure (Adam's assessment, Don's comments align — still open investigation), Bloom Intelligence partnership evaluation added to scope, Touch Bistro merger context noted (confidential). Don will share investor/lender deck. Onsite timing confirmed: Mon–Wed before Don's LA trip, ~2 hours of Don's time.
- **All 5 surveys built in Microsoft Forms** (April 5) — DORA Quick Check (9 questions), Westrum Culture (7 questions), Pragmatic Engineer Test (15 questions), AI Adoption & Tooling (20 questions), DevEx/DX Core 4 (23 questions). All live with links. Ready for Chathura to distribute.
- **Bloom Intelligence research** (April 5) — AI-powered restaurant CDP based in St. Petersburg, FL. Founded 2006, Will Wilson CEO. Platform: WiFi analytics, customer profiles, marketing automation, reputation management. Captures data *outside* the POS (foot traffic, WiFi, reviews, web). Integrates with POS systems. Small company — Don says "a few million dollar revenue, couple people." The MM fit: Bloom's external customer data + MM's internal POS transaction data = complete customer view. Don asked Adam to evaluate at a basic level, not build.
- **Winmark Corporation research** (April 5) — franchisor of value-oriented retail brands: Play It Again Sports (~280 stores), plus 4 other brands (~1,265 total stores across US/Canada). Has proprietary POS called "Data Recycling System" (DRS) with 20+ years of transaction data. Recently did a digital transformation with Rightpoint (BigCommerce). Kennedy is building an AI-developed POS application for them — this is retail/franchise, not restaurant, so a different vertical from CAKE.
- **File consolidation** (April 5) — archived 7 standalone files into `archive/`, absorbed content into state doc. State doc is now the single source of truth.

### In Progress 🔄
- **Ana + Chathura coordination update** — sending tonight (April 5 evening) with all pending requests, next steps, and pre-onsite logistics. Updated `ana-request.md` with Winmark project visibility, Bloom Intelligence context, and investor deck note.
- **ISSUE:** Chathura's survey intro email only references 4 surveys — dropped AI & Tooling (Survey 5). Following up tonight with link.
- Waiting on Ana: pre-read items not in Confluence — **target: early Monday April 7**
- Waiting on Ana: Grafana viewer access — **confirmed Monday April 7** (Matias off holiday weekend)
- Waiting on Ana: routing questions on Monvia, MenuPad, Relate, Neo/AI
- Waiting on Ana: interview calendar blocks + conference room (April 13–15)
- Waiting on Don: investor/lender deck (offered on April 5 call)
- Mercury banking setup for Translation Layer LLC
- EIN pending from Northwest

### Next Steps (This Week)

**Tonight (April 5):**
1. **Send Ana/Chathura coordination update** — `ana-request.md` covers all open items including new Winmark and Bloom Intelligence items. Include all 5 survey links.

**Monday–Wednesday (April 7–9):**
2. **Grafana capture** — Monday April 7 when access arrives. Dashboard inventory, alert rules, data sources.
3. **Collect pre-read docs** as Ana's folder becomes available Monday.
4. **Finalize interview schedule grid** — send to Ana for calendar booking.
5. **Don Sessions 2 and 3** — target April 7–9. Session 2: political landscape. Session 3: pre-onsite briefing.
6. **Search for Winmark in Jira/Bitbucket/Confluence** — look for project, repo, or space related to Kennedy's client delivery. Evidence of what "AI-developed POS" means.
7. **Dig deeper on Neo** — search Jira NEO/AAK/LAA projects for actual development artifacts, not just project shells. Search Bitbucket for repos. Search Confluence for technical docs vs. marketing material. This is an open investigation item.
8. **Update Kennedy interview prep** — reframe from "AI/innovation roadmap" to: what are you building for Winmark, what's the tech stack, is any of it reusable, what does "Neo" actually mean vs. what Winmark is.
9. **Add Bloom Intelligence to onsite questions for Dulanjan** — he's reportedly already talking to them. What's been discussed? Product fit? Technical integration points?
10. **Gather independent evidence for Hypothesis B** — Jira epic churn/cancellation data, sprint scope change metrics across boards, roadmap revision history in Confluence.

**Thursday–Friday (April 10–11):**
11. **Survey analysis** — surveys close April 10. Analyze results same day. Cross-reference DORA self-reports vs. actual system data. Feed into interview questions.
12. **Pre-onsite briefing with Don** (April 10–11) — final alignment session. Review survey results, confirm interview schedule, identify 5 real cases to trace.
13. **Final hypothesis scorecard update** — score each hypothesis A–I based on all pre-work evidence.
14. **Prep interview questions** — `interview-prep-with-data.md` has data-backed questions per interviewee, review and refine.

**Pre-Onsite (April 11–12):**
15. **Print/prep onsite materials** — C4 diagrams, org chart, key metrics one-pager, interview question sheets.
16. **Travel logistics** — Uber from St. Pete to Tampa HQ, confirm room booking with Ana.

### Data Gaps to Close (Before April 11)
- [ ] **Jira incident query**: Search for issue types "Incident", "Code Red", "Service Interruption" in 2024–2026 to fill the RCA timeline gap.
- [ ] **Root Cause Category field #2**: Query `customfield_10590` ("Root Cause Category", type: array) — may be the active one vs. the 0%-populated `customfield_10382`.
- [ ] **CloudTrail access escalation**: Ask Ana/Matias if audit role can get `cloudtrail:LookupEvents` added, or if there's a CloudTrail S3 bucket to read directly.
- [ ] **Branch protection validation**: Check whether Bitbucket uses project-level branch permissions instead of repo-level.
- [ ] **Pipeline coverage expansion**: Currently only top 30 repos. Consider running for top 100.
- [ ] **Theme-analyze the 30 sprint retrospectives** — extract recurring "what didn't go well" themes across teams.
- [ ] **Deep-read the 2 recent Team Tesla RCAs** — SQS Retry Storm (Dec 2025) and Menu Core API Retry Loop (Sept 2025).
- [ ] **Map top 5 reviewer bottleneck repos to teams** — who owns the repos where John Harre, Holly Culver, etc. are bottlenecks?
- [ ] **Review the auto-generated C4 diagrams** — validate accuracy. Print for onsite.
- [ ] **Scan extracted Confluence architecture pages** — the 94 pages from V5 + the 321KB diagram catalog from V7.
- [ ] **Map CDO product roadmap to team capacity** — 12+ ongoing CAKE projects vs. Randy's 9 engineers + Akshay's 9 R&D engineers.

### SOW / Business
- [ ] Mercury banking setup for Translation Layer LLC
- [ ] EIN pending from Northwest
- [ ] SOW draft — scope, deliverables, timeline, confidentiality, IP ownership, liability
- [ ] Invoice structure — $10K deferred, payment terms TBD

### System Exploration — Completed (Key Answers)
- **Where does Neo/AI live?** No dedicated account. SageMaker in CAKE R&D. Jira projects exist (NEO, AAK, LAA). Confluence docs exist. But no production AI infrastructure found in systems scan. Don's April 5 comments align with this assessment. **OPEN INVESTIGATION:** Need to dig into Jira NEO/AAK/LAA for actual development artifacts (not just project shells), search Bitbucket for repos, and differentiate technical docs from marketing material in Confluence. Kennedy is currently full-time on Winmark client delivery, not Neo. Validate onsite with Kennedy and Chathura.
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
- `analysis/charts/*.json` — 31 interactive Plotly charts (including review network graph)
- `interview-prep-with-data.md` — Per-interviewee data-backed questions organized by interview day
- `ana-request.md` — Ready-to-send coordination email for Ana
- `05-ai-tooling-survey.md` — AI Adoption & Tooling survey instrument (20 questions)
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

### Open Clarifications (Pending Don Call / Onsite)

- **Akshay Bhasin scope: PARTIALLY RESOLVED.** CDO org chart confirms VP Payments Engineering with 20+ people: Payments R&D (Kevin Reyes as Director, 9 people), Restaurant QE (7 people), Biz Operations (Andy Honnold + 3), plus PCI DSS counterparts. This is a much larger org than "18 people" — the March chart was incomplete. **Remaining question:** Was Restaurant QE always under Payments, or is this a reorg consolidation? Having QE for Restaurant under the Payments VP (not the Restaurant VP) is an unusual structure worth probing.
- **IT Director: RESOLVED.** Jorge Maltes confirmed still at company — appears as Dir. Information Technology under PCI DSS Compliance counterparts in Chathura's Payments org chart. Rosen Georgiev handles day-to-day IT under COO (Strainick). Two people, two roles: Maltes = IT governance/compliance, Georgiev = IT operations.
- **Andy Honnold dual-reporting:** Don's executive chart places Andy Honnold (Payments Strategy) under Garcia (CFO). Chathura's functional chart places him under Akshay (Payments VP) as Sr. Director Payments Strategy. Likely functional through Payments, administrative through Finance. Clarify onsite — affects how Payments strategy decisions flow.
- **L&D reporting discrepancy:** Chathura's CDO org chart places Adriana Zuniga and Ayodele Lawal as Technical Training Specialists under Dulanjan's Product L&D team. Don's executive org chart placed them under Bailey Shatney (VP HR). Could be matrix (product-owned content, HR-owned development programs), or a reorg-day discrepancy. Clarify onsite.
- **Enterprise Solutions (Zubair) detail gap:** Chathura's PDF had the Enterprise Solutions org chart page mostly blank (just "Enterprise Solution Org."). The Operations sub-page noted team transitions and reductions (57% L2, 72% L3) but no personnel detail. **Still don't have names/structure for the largest org (58 people).** Need to request from Zubair or Chathura before onsite.
- **Strainick interview recalibration:** Interview shifted from 30 min on HR/culture to 45 min on COO operations. Secondary purpose: validate whether Strainick is in the seat to stay. If Don's answer reveals this was a "promote to move," focus the interview on documenting the customer operations chain (Account Mgmt → Onboarding → Delivery → IT) as a process map rather than relying on Strainick's strategic perspective.
- **Bailey Shatney framing:** Position Adam's deliverables as a potential resource for Bailey. If she's new and ramping, the Westrum Culture survey baseline, Glassdoor data, and interview themes on culture/retention are exactly what she needs to build her own 90-day plan. This creates a natural ally.

---

## 12. Important Engagement Rules

1. **Pre-engagement hypotheses are not findings.** Diagnostic conclusions cannot be synthesized until after the onsite.
2. **Evidence independence.** Don's private comments inform direction and help Adam ask the right questions, but they cannot be attributed as evidence or proof in any deliverable. The entire value of this engagement is that Adam provides independent, outsider findings grounded in quantitative data, surveys, and interviews. Don's quotes are internal context for Adam only — they shape where to look, not what to conclude.
3. **Kennedy/Chathura dynamic is RESOLVED.** The April 3 reorg gave Chathura formal CDO authority over all engineering, product, design, PMO, and customer support. Kennedy narrowed to AI/innovation (currently full-time on Winmark client delivery). Can now be referenced openly in all materials. Onsite validates whether operational reality has caught up to the structural change.
4. **Board/investor deliverable is a core purpose**, not an afterthought. It shapes framing across the charter, executive summary, deliverables, and success criteria.
5. **Surveys designed for Mad Mobile's independent re-use** at 30/60 days. Don't create dependency on Adam.
6. **Friend-to-colleague tone with Don; professional with everyone else.** Careful audience sensitivity in any materials shared with MM leadership.
7. **Anonymous interviews.** Report themes, not who said what.
8. **All public-source research on leadership was mostly wrong.** The official org chart from Don is the authoritative source. Validate everything internally before using externally.
9. **Raw over polished.** For pre-read materials, whatever exists in whatever format is more useful than a curated package.
10. **Deliverables must be sharp and concise.** Don explicitly rejected a 687-page AI-generated document from someone else. He will immediately discard anything that feels AI-padded. Evidence-based, no filler.

---

## 13. Don Call Summaries

### April 5 Touchbase (~15 min, casual — both heading to Easter activities)

**Context:** Quick check-in, didn't cover every item from the prepared call guide. Adam's assessment: "didn't miss anything that's actually important/not already known."

**Key facts learned:**
- **Kennedy/Winmark:** Jack Kennedy is currently full-time building an AI-developed POS application for Winmark Corporation, a $5M new client (franchisor of Play It Again Sports and other resale retail brands, ~1,265 stores). He is "basically agentic programming for this customer delivery this year." His "AI capabilities and platform innovation" role from the reorg is currently single-client delivery, not internal platform or Neo work. He was historically "the guy over retail business tech-wise" — Bruce gave him the CTO title for external credibility. He's been at MM 7–8 years, described as "very strategic thinking and smart" but not an expert on the restaurant business, which is why Chathura was brought in.
- **Neo/AI:** Adam told Don he has "not found anything that's actually more than marketing slides" behind Neo. Don's comments aligned. Neo is "a branded name for our AI customer-facing AI solution." This remains an open investigation item — Adam's systems scan is the primary evidence; Don's comments are directional context, not proof.
- **Bloom Intelligence (NEW SCOPE):** Don asked Adam to evaluate Bloom Intelligence (Will Wilson, CEO) as a potential partnership. Bloom is an AI-powered restaurant CDP based in St. Petersburg. The idea: link MM's POS data with Bloom's external customer data (WiFi, web, reviews). Product/Dulanjan already talking to them. Don is skeptical about credibility ("I don't know whether he's real or not") and worried MM is too unprepared. Kickoff meeting being planned for April. Lightweight scope addition: "just evaluate, not build."
- **Touch Bistro (CONFIDENTIAL):** MM in merger negotiations with Touch Bistro (restaurant-space company, similar size, US/Canada). See Section 14 for details.
- **Board deck:** Don will share the investor/lender presentation deck. Previous CEO "would never step up to making a plan" — investors saw the problems.
- **Strategy whiplash direction:** Don described a pattern of priority shifting under previous leadership. This gives Adam a direction to investigate for Hypothesis B, but is NOT evidence for the deliverable. Need independent quantitative proof.
- **Platform vs. custom direction:** Don pushed back on Adam's probe about per-customer custom code — "not true for restaurant, not true on CAKE." Acknowledged legacy systems that can't evolve. Hypothesis C may be more nuanced than assumed.
- **Lights-on vs. features:** Don described team spending effort keeping things running rather than building. Existing Jira data shows 67% features / 21% defects (aggregate) — need to segment by team onsite.
- **Onsite timing:** Don in Tampa this week, leaves for LA Thursday of the following week, back Monday. Onsite dates (Mon–Wed) confirmed. Don estimates ~2 hours of his time over the 3 days.
- **Flutter:** Confirmed as part of the tech stack — "probably for all our mobile devices."
- **Deliverable tone:** Don rejected a 687-page AI-generated document from someone else. Deliverables must be sharp and concise. Don spends 8–9 hours refining his own decks because AI output "is always a little bit off."

**Questions NOT covered (better for onsite or already resolved):**
- Strainick promote-to-fit/move, Bailey Shatney background, Chathura capacity/priorities, Bhasin scope, revenue data owner, Survey 5 approval, interview schedule adds/removes, off-limits topics.

---

## 14. Confidential — Don Only

*This section contains information shared by Don in private that should NOT be included in any materials shared with Ana, Chathura, or anyone at Mad Mobile.*

### Touch Bistro Potential Merger
- MM is in negotiations to merge with **Touch Bistro**, a restaurant-space company "about our size, all over the US and Canada."
- Estimated synergies: $30–40M, "probably the first operating area."
- Merger dynamic: Touch Bistro would take controlling interest because MM's real equity value post-debt is "probably 35% of theirs." Touch Bistro has "a big PE behind them and capital."
- Touch Bistro is **iOS-based**. MM is Linux/Android/Flutter. "Very different platform design."
- Don frames Adam's work as potentially extending: do the assessment on MM, then do the same on Touch Bistro, then figure out how to merge into one platform.
- **Implication for engagement:** The assessment should be framed for maximum reusability. If a second engagement on Touch Bistro follows, the methodology, frameworks, and tooling should transfer directly.

### Cash Situation
- Cost of capital has increased significantly "because of all our fuckups" plus market conditions.
- Don says any benefit from Adam's work is "in addition to everything I've already committed to" the lenders — not promising engagement outcomes to the board.

---

## 15. Bloom Intelligence Evaluation (In Scope per Don, April 5)

**Company:** Bloom Intelligence (bloomintelligence.com)
**CEO:** Will Wilson (Founder)
**Location:** St. Petersburg, FL (same metro as Mad Mobile in Tampa)
**Founded:** ~2006
**Size:** Small — Don says "a few million dollar revenue, couple people"

**What they do:** AI-powered restaurant customer data platform (CDP). Captures guest data through WiFi analytics, online ordering, and website interactions. Features include:
- Presence analytics (foot traffic, dwell times, conversion rates)
- Customer profile CRM with dynamic profiles across visits/transactions/sentiment
- Automated marketing campaigns (welcome, re-engagement, at-risk)
- AI-powered reputation management (review responses across Google, Yelp, TripAdvisor, OpenTable, Facebook — 5-minute average response time)
- At-risk guest alerts and churn prediction using ML

**Integration points:** WiFi hardware (Cisco Meraki, Ubiquiti, Aruba, Ruckus), marketing platforms (Mailchimp, Constant Contact), POS systems, social platforms.

**The MM partnership thesis:** Bloom captures data *outside* the POS (foot traffic, WiFi, reviews, web behavior). MM captures data *inside* the POS (transactions, orders, menu, payments). Together = complete customer view. The idea: "use their AI solution connected to ours, charge a fee to reimburse them."

**Connection:** Will Wilson is co-owner of Copper Shaker, a MM client. Partnership idea surfaced when that deal closed.

**Don's concerns:** Skeptical about Bloom's credibility and scale. Worried MM is "so unprepared" that a partnership kickoff would waste everyone's time. Wants Adam to do a basic evaluation before committing to a kickoff.

**Internal contacts already engaged:** Dulanjan (Product) is talking to them. Kickoff meeting being planned for April.

**Adam's assessment scope:** Lightweight — "basic specs, not build." Evaluate what Bloom does vs. what MM has. Assess whether there's a real technical integration path or just a marketing idea. Include in onsite questions for Dulanjan.

---

## 16. Vendor Assessment Questions (For Ana/Finance)

Key questions for the vendor/tooling rationalization section of the board deliverable:

**Spend data needed (top priority vendors):**
- Atlassian (Jira, Confluence, Bitbucket) — seats, tier, annual total
- Wiz.io — annual contract ($100K–$300K range typical)
- Datadog — scope and annual cost (confirmed active for Concierge/Retail)
- Five9 — cloud contact center, agent seats, annual cost
- Salesforce — licenses, annual total
- Tyk API Gateway — last renewal 2023 at ~$35K/year, is it current?
- Snyk — contract still active? Annual cost?
- Trend Micro Cloud One — $1,438/month in CAKE Dev AWS, intentional alongside Wiz?
- Slack — paid plan alongside Microsoft Teams?
- Figma — editor seats
- TeamViewer — annual cost for POS remote access
- GitHub — still active alongside Bitbucket? (internal docs flag "Can we get rid of this?")

**Procurement process questions:**
- Is there a centralized procurement process, or do teams buy tools independently?
- Any recent tool consolidation or rationalization efforts?
- Is there a single view of total tooling spend?

**Observability consolidation:**
- 6 monitoring/observability tools identified: Grafana (Mimir/Loki/Tempo), Datadog, Nagios, Munin, Graylog, DB Cacti
- Has anyone proposed consolidating? Is there a roadmap?

**Estimated annual SaaS spend (excluding AWS): $350K–$800K range** based on public pricing. Need actuals to narrow.

---

## 17. Reference Links

- **Engagement Plan (Google Doc):** https://docs.google.com/document/d/1bQeR8VA6-uOQEqNw1FMCoJhX-yBP16UPNtLUal46B9s/edit
- **Jira / Confluence:** https://madmobile-eng.atlassian.net/
- **AWS Provisioning Ticket:** https://madmobile-eng.atlassian.net/browse/CLD-2431
- **Mad Mobile Website:** https://madmobile.com/
- **Bloom Intelligence:** https://bloomintelligence.com/
- **Winmark Corporation:** https://www.winmarkfranchises.com/
