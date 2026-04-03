# CEO Ramp Accelerator & Execution Diagnostic

## TECHNOLOGY OPERATIONS REVIEW — Mad Mobile, Inc.

**WORKING DRAFT — v11**

*For discussion between Adam & Don — not yet for broader distribution*

**Adam Lazarus**
Systems & Software Engineering | Ecommerce | Enterprise Platforms | AI Strategy

**Don Salama**
Co-CEO & Acting CFO, Mad Mobile, Inc.

CONFIDENTIAL — March 2026

---

## Contents

1. [Engagement Charter](#1-engagement-charter)
2. [The Actual Objective](#2-the-actual-objective)
3. [Why This Works: The Translation Layer](#3-why-this-works-the-translation-layer)
4. [Engagement Philosophy & Tone](#4-engagement-philosophy--tone)
5. [Company Context & Pre-Engagement Intelligence](#5-company-context--pre-engagement-intelligence)
6. [Diagnostic Framework: The Six Systems](#6-diagnostic-framework-the-six-systems)
7. [Hypothesis Library: Patterns to Prove or Disprove](#7-hypothesis-library-patterns-to-prove-or-disprove)
8. [Three-Week Execution Plan](#8-three-week-execution-plan)
9. [Pre-Work — Now through April 11](#9-pre-work--now-through-april-11-15-hrs-async--5-hrs-meetings)
10. [Week 2: Onsite Diagnostic Sprint — April 13–15](#10-week-2-onsite-diagnostic-sprint--april-1315-20-hrs-onsite--5-hrs-async)
11. [Interview Framework](#11-interview-framework)
12. [Artifacts to Build During Onsite](#12-artifacts-to-build-during-onsite)
13. [Analysis, Synthesis & Deliverables — April 16–25](#13-week-3-analysis-synthesis--deliverables--april-1625-15-hrs)
14. [AI-Augmented Execution Model](#14-ai-augmented-execution-model)
15. [Compensation & Engagement Structure](#15-compensation--engagement-structure)
16. [Handling the Bruce / Investor Context](#16-handling-the-bruce--investor-context)
17. [Defining Success](#17-defining-success)

---

## EXECUTIVE SUMMARY

### The Situation

Mad Mobile ($75M revenue, ~370 people, $70M funded) has strong assets — Sysco, Visa, Best Buy, and Apple partnerships across 21,000+ deployed locations — but is struggling to execute. Engineering is split between legacy POS maintenance (CAKE, acquired from Sysco in 2020) and an AI platform (Neo) that's been heavily marketed but may not be production-ready. Don has been operating as Co-CEO and Acting CFO for approximately two years via Turn 3 Ventures, giving him deep financial and operational visibility — but the technology and engineering execution layer needs translation into actionable business strategy. That's the gap this engagement fills.

### The Engagement

An ~60-hour compressed diagnostic sprint to give Don an executable map of how Mad Mobile actually works, where execution breaks down, and what to fix first — without triggering a fear spiral inside the org.

| Phase | Timeline | What Happens |
|---|---|---|
| Pre-Work | Now → Onsite | AI-augmented system scanning (GitHub, AWS, Jira), engineering health surveys (DORA, Westrum, DevEx), pre-read analysis, alignment sessions with Don |
| Onsite | April 13–15 (Mon–Wed) | 3-day sprint in Tampa: 15+ interviews, architecture walkthroughs, value stream mapping, decision-rights mapping, real case tracing |
| Deliverables | Week after Onsite | CEO operating brief, execution map, friction register, hypothesis scorecard, 30/60/90-day plan, board-ready investor presentation, baseline survey package |

### The Approach

Every part of this assessment is grounded in established, named frameworks — from DORA and McKinsey 7S to Bain's RAPID and Watkins' First 90 Days. But the value isn't in applying any single methodology rigidly. It's in selecting the right tool for each specific question: using Value Stream Mapping to trace where delivery stalls, using the Theory of Constraints to find the single biggest bottleneck, using RAPID to expose where nobody actually owns a decision. The full framework reference is mapped in Section 6.2.

AI makes this practical in three weeks. Automated system analysis produces quantitative baselines from GitHub, AWS, and Jira before the first interview. AI-assisted note-taking and synthesis process each day's findings same-night, so the next morning's conversations are already informed by emerging patterns. First-draft deliverables are AI-generated from accumulated data; Adam's hours focus on the irreplaceable work — interviews, judgment, translation, and narrative. The result is a methodologically rigorous assessment compressed into ~60 hours.

### Five Questions This Answers

1. How is Mad Mobile actually organized to build and ship?
2. Where does execution break down, specifically — with evidence?
3. Which problems are structural vs. process vs. technical debt?
4. What should Don engage in during his first 30/60/90 days?
5. What should be left alone for now?

### Nine Hypotheses to Validate

The engagement tests nine named execution-failure patterns:

Portfolio Sprawl, Sales-Led Chaos, Fake Platforming, Unclear Ownership, Dependency Drag, Legacy Gravity, Missing Cadence, Business-Tech Mistranslation, and Architectural Polarity.

Each is scored with evidence onsite.

### The Deliverable

A CEO Operating Brief structured as the technology chapter of Don's transition playbook: executive summary, execution system map, prioritized friction register, hypothesis scorecard, STARS transition diagnostic, 30/60/90-day plan with an explicit "leave alone" list, and a **board-ready presentation for investor audiences**. A key outcome of this engagement is producing an independent, empirically grounded technology assessment that Don can present directly to Morgan Stanley and the board — establishing credibility through third-party analysis backed by named industry frameworks, not internal narratives.

### Tone, Compensation & Effort

Collaborative and systems-focused — not a blame exercise. All individual interview content is anonymous; only systemic patterns are reported. Compensation is a fixed fee of $10,000 with deferred payment terms; an ongoing advisory role via FAST agreement is a separate conversation if warranted. Total estimated effort: ~60 hours across 3 weeks.

---

## 1. Engagement Charter

> *Note: This is a working document for Adam and Don to align on the engagement before broadening to other stakeholders. Once we're aligned on scope, approach, and logistics, we'll produce a cleaner version for internal distribution at Mad Mobile.*

**Purpose**: Accelerate CEO understanding of Mad Mobile's business/technology operating system and identify the highest-leverage opportunities to improve execution velocity. Don already has deep financial and operational visibility from two years as Acting CFO — this engagement adds the technology translation layer. Equally important: produce an independent, empirically grounded technology assessment that Don can present to the board and investors (Morgan Stanley, Western Alliance) — establishing credibility through third-party analysis backed by named industry frameworks rather than internal narratives.

**Scope**: Product decision-making, engineering organization and delivery, architecture and platform strategy, cross-functional workflows, operating cadence, business-technology alignment, AI strategy (aspiration vs. reality), vendor and tooling utilization, and major systemic blockers.

**Non-goals**: Individual performance review, staffing or termination recommendations, exhaustive code-level audit, forensic blame analysis, or retrospective on outgoing leadership decisions.

**Methods**: Leadership interviews, team-level interviews, workflow walk-throughs, AI-augmented artifact review (automated system audits of GitHub, AWS, Jira, infrastructure), architecture/system mapping, value-stream mapping, and pattern validation against named hypotheses.

**Outputs**: CEO operating brief, execution system map, friction register with prioritized findings, 30/60/90-day action plan (including an explicit "leave alone" list), board-ready presentation for investor audiences, baseline survey package (repeatable at 30/60 days), vendor/tool utilization assessment, and optional stakeholder communication draft.

**Timeline**: 3 weeks. Pre-Work: async + alignment sessions (now through April 11). Onsite: April 13–15 (Mon–Wed). Deliverables: April 16–25.

**Estimated effort**: ~60 hours total. Pre-work: 15 hrs async + 5 hrs meetings. Onsite: 20 hrs onsite + 5 hrs async. Deliverables: 15 hrs async + meetings.

---

## 2. The Actual Objective

This engagement answers five specific questions for Don:

1. **How is Mad Mobile organized to build and ship?** The real operating model, not the org chart version.
2. **Where does execution break down, specifically?** Named bottlenecks with evidence, not anecdotes.
3. **Which problems are structural vs. leadership/decisioning vs. process vs. technical debt?** This distinction determines the intervention type.
4. **What should Don personally engage in during his first 30/60/90 days?** Sequenced, prioritized, with ownership.
5. **What should be left alone for now?** The noisy, political, or lower-leverage areas that will consume attention without producing results.

---

## 3. Why This Works: The Translation Layer

The reason this engagement can deliver outsized value in three weeks is the specific combination of Don's operational depth and Adam's technical translation skills. This section captures the positioning for when we broaden the audience beyond the two of us.

### 3.1 Don's Operating Context

Don has been operating as Co-CEO and Acting CFO for approximately two years, giving him direct visibility into Mad Mobile's financial performance, capital structure, lender relationships (WAB, Morgan Stanley), M&A activity, and board dynamics. He's not arriving cold — he already understands the business from the investor and financial operations side. His prior executive career at New York Life — CSO at NYL Investments, Head of Retirement Plan Services, SVP of NYL Direct — means he understands massive institutional systems with zero-downtime requirements, complex compliance environments, and high-volume transaction processing. That's directly transferable to what Mad Mobile does. The gap isn't operational instinct or business knowledge; it's the translation from financial services infrastructure language into modern software engineering language. That's Adam's job.

### 3.2 Adam's Profile: Domains and Track Record

Adam's career has been built around the exact intersection that Mad Mobile needs to diagnose: the point where business strategy, technology architecture, and execution workflows either align or break. His relevant experience spans:

- **Enterprise software & compliance**: Smarsh (enterprise archiving and signals compliance for financial services), IBM, Microsoft — deep familiarity with regulated, high-stakes software environments where reliability and audit trails are non-negotiable.
- **Ecommerce & platform engineering**: Director of Product & Software Development at CPAP.com and Sleeping.com, where he led a full platform migration from Magento and custom-built systems to the Shopify ecosystem, including architecting a first-of-its-kind AI-driven prescription validation system on AWS. Currently Director of Engineering at Legacybox, operating multiple ecommerce brands (Legacybox, Southtree, Kodak Digitizing) with subscription billing, native mobile apps, and wholesale partner integrations.
- **SaaS, growth engineering & DTC**: Growth Engineer and DTC Product Lead at Four Sigmatic. Co-founder/technical lead at multiple early-stage ventures (Ventract, Buoy Ventures, Trellis, Brandtale). Understands the full spectrum from scrappy startup to enterprise scale.
- **Systems translation**: Career-long pattern of bridging business and engineering — described by colleagues as "a highly technical communicator capable of presenting to both technical and business stakeholders" who "combines strong technical knowledge with uncanny understanding of enterprise business." This is the core skill this engagement requires.
- **AI strategy (practical, not theoretical)**: Hands-on experience deploying AI in production — the CPAP.com prescription processing system, AI-augmented development workflows at Legacybox, and active use of AI tools for engineering productivity. Understands what AI actually delivers today vs. what's marketing.
- **Payments & subscription infrastructure**: Deep experience with payments architecture at Legacybox (Shopify Payments, Recharge, Stripe) including comprehensive payments infrastructure migrations across Braintree, Shopify, Chargebee + Stripe. Directly relevant to Mad Mobile's Visa/Cybersource payments play.

### 3.3 The Translation Gap This Fills

Without a technical translation layer, a CEO in a complex software environment is vulnerable to defensive engineering leaders obscuring operational failures behind dense jargon. Adam's role is to convert opaque engineering realities into actionable business strategies — and to convert business frustrations into specific, addressable technical interventions. The combination of Don's institutional operations instincts, two years of financial/operational context at Mad Mobile, and Adam's software engineering depth is what makes a three-week compressed timeline credible.

---

## 4. Engagement Philosophy & Tone

We both know the framing matters. If engineering and product teams perceive you and your advisor as hostile auditors, they will obfuscate data, hide technical debt, and present a sanitized view. We want candor, not theater.

### 4.1 Core Principles

1. **Collaborative, not adversarial.** Adam is positioned as a peer and resource: "Don's colleague who has deep experience translating between business and technology."
2. **Systems-focused, not blame-focused.** Every finding is framed as: "where does the system make it easy or hard for talented people to succeed?"
3. **Translating between worlds.** Findings will be accessible to investor/board audiences and engineering teams alike.
4. **AI-augmented and practical.** The review itself will leverage AI tools for automated system analysis, note-taking, documentation synthesis, and pattern identification — demonstrating the practical AI integration Adam will also be evaluating within Mad Mobile.
5. **Preserving what works.** Mad Mobile has strong partnerships (Sysco, Visa, Best Buy, Apple, Oracle, Salesforce), real revenue, 21,000+ deployed locations, and talented rank-and-file employees. These are assets to build on.

### 4.2 Internal Messaging

When you're ready to announce this internally, here's the suggested language. We can refine this together:

> *"Adam is helping me accelerate my understanding of how our business, product, engineering, and delivery systems work in practice. He has deep experience translating between business and technology and identifying ways to improve execution. This is not a personnel review. It's an effort to help us remove friction, clarify priorities, and support the team. The more open and candid you are with him, the more useful this will be for all of us."*

### 4.3 Confidentiality Framework

- **Attributable**: Systemic patterns and structural findings will be reported with evidence.
- **Anonymous**: Individual comments will be synthesized into themes, never attributed by name.
- **The promise to employees:** "I won't play telephone with personal comments, but patterns and blockers will be synthesized."
- **Don's choice:** Synthesized findings with the option to request more context on specific areas.

---

## 5. Company Context & Pre-Engagement Intelligence

### 5.1 Business Overview

Mad Mobile is a Tampa, FL-based technology company founded in 2010 by Bruce Bennett, Greg Schmitzer, and Colin Maxey. Connected commerce solutions for restaurant and retail, ~370 employees, Tampa HQ with Sri Lanka engineering, ~$75M estimated revenue. $70M total funding, most recently $50M (secured note, not equity) in June 2024 from Morgan Stanley Expansion Capital and Bridge Bank (Western Alliance). Bruce Bennett was recognized by Goldman Sachs as one of the 100 Most Intriguing Entrepreneurs (2021). The CEO transition reflects the shift from founder-led growth to metrics-driven execution demanded by institutional capital.

### 5.2 Product Portfolio & Platform Architecture

Three distinct platform tiers with different architectures, customers, and operational demands — creating fundamental operational polarity:

| Platform | Architecture | Features | Market |
|---|---|---|---|
| CAKE POS | Legacy monolithic, tightly coupled in-house payment gateway | Transactions, inventory, Sysco ordering, waitlists, core restaurant ops | QSR, full-service, bars, cafes |
| Concierge AI (formerly Mad.x) | Cloud-based APIs, iOS/Android native + cross-platform | Associate mobility, endless aisle, fulfillment, clienteling, appointments | Enterprise retail (Ralph Lauren, MAC, Urban Outfitters) |
| Neo AI Platform | Composable LLM architecture (OpenAI, Anthropic, AWS Titan), visual orchestration | Predictive ordering, auto-segmentation, conversational analytics, agentic workflows | Advanced enterprise retail/dining |

Engineering teams are simultaneously building AI-native platforms AND firefighting legacy POS outages. This split is a primary candidate for the execution breakdown.

### 5.3 The CAKE Acquisition: Legacy and Technical Debt

Acquired from Sysco in 2020, bringing ~4,500+ restaurant locations but also severe technical debt:

- **Bundled payment processing**: Long-term contracts, mandatory in-house payment processing. Lucrative but creates single points of failure.
- **System-wide outages:** When the payment processor goes down, the entire system fails. Restaurants report resorting to writing orders on whiteboards during peak service.
- **Support degradation**: Response times reportedly deteriorated from a promised 12-second answer to unreturned voicemails during critical outages.
- **Hardware dependency**: Hardware-dependent POS integrated into a mobile-first software org — inherent architectural mismatch.

### 5.4 Technology Stack (Known)

- **Mobile**: Swift, Objective-C (iOS), Kotlin, Java (Android), React Native, Flutter (cross-platform) — multiple parallel frameworks.
- **Backend**: Node.js and Java on AWS.
- **Enterprise integrations**: Salesforce, Oracle, SAP, Shopify, Magento.
- **AI layer**: Pluggable LLM integrations (OpenAI, Anthropic, AWS Titan), visual orchestration, prompt templates, "Agentic Identities" with MFA.
- **POS hardware**: CAKE-specific restaurant-grade terminals.

### 5.4.1 CAKE Ecosystem Detail

*Source: Restaurant Update, March 2026 (internal deck).*

The CAKE product line is significantly more complex than the top-level "legacy monolithic POS" description suggests. The live system footprint includes: POS V3 (Pondus), POS V4 (Elio), Kiosk v1, OLO v1, KDS v1, Gift Cards v1, Guest Manager, Kiosk v2, Loyalty v1, OrderPad, CAKEpop, Email Marketing, Restaurant Admin 1.0, and Customer Display. That's **15+ live systems** maintained by ~10 engineers and ~7 QE staff under Randy Brown.

Simultaneously in active development: CAKE Online Ordering UI Refresh, EMS 2.0 Multi Location, Gift Cards (Factor 4), CAKEpop (roadmap features), KDS v2, and VP 3350 (new payment device for MenuPad POS + Kiosk). Planned but not yet started: OLO v2, Loyalty v2, Restaurant Admin 2.0.

Third-party integrations currently in production: Checkmate, 7Shifts, OLO.com, LRS, Paytronix, Bloop, DoorDash, NOLO, Orca, Davo, Parafin, Dolce, QSR KDS.

This surface area vs. team size ratio is a primary investigation target for Hypotheses A (Portfolio Sprawl), F (Legacy Gravity), and I (Architectural Polarity).

### 5.4.2 AI Usage (Current State)

*Source: Restaurant Update "How we use AI" slide, March 2026.*

Mad Mobile is already using AI tools operationally across the restaurant team — this is not theoretical:

- **Design**: Uses AI tooling to tweak application design code directly in app projects. Figma for design assets.
- **Product**: Uses design assets and AI tooling to produce planning assets: user stories, acceptance criteria, Jira tickets.
- **Engineering**: Heavy usage of **Cursor** (AI-assisted IDE) for daily development activities. Uses design assets to generate application shell and reusable components.
- **QE**: Uses planning assets (acceptance criteria) and AI tools to produce automated test cases.
- **Support**: Uses AI to produce documentation and support materials (**Guru**). Uses AI tools to perform proactive and reactive **RCA on production POS logs** (noted as in-progress).

This means the AI strategy assessment should distinguish between Neo (the customer-facing AI platform — aspiration vs. reality) and internal AI adoption for engineering productivity (already happening). The internal AI usage is a positive signal worth understanding and potentially amplifying.

### 5.4.3 Requirements & Prioritization Process (Documented)

The restaurant team has a documented two-stage requirements process:

1. **Ideation & Research Stage** (Product Manager + Product Designer): Customer validation → product research/prototype → product designs → high-level requirements and designs.
2. **Tech Refinement Stage** (adds Architect + Engineering/QE Lead): Engineering and test designs → feature discussions → architecture → final ACs, final designs, approved architecture, reviewed tech design, reviewed QE design → handed to engineering teams.

Architecture must be **ARB (Architecture Review Board) approved** before engineering begins — this is a governance mechanism worth validating onsite.

Prioritization uses a **multi-department scoring model**: each feature is assigned a priority from Product, Sales, CSM, Onboarding, and Support, then ranked by overall score. Executive alignment narrows to the top 5 initiatives. A **GTM tracker** (run by PMO — Mark Guilarte) coordinates release preparation on a 4-week cadence.

The onsite should validate whether this process is actually followed or whether it gets overridden by sales promises or executive directives (Hypothesis B: Sales-Led Chaos).

### 5.5 Organizational Structure

*Source: Official org chart provided by Don, March 2026. Supersedes all earlier versions based on public research.*

#### L1 — Executive Leadership (Report to Bruce Bennett, CEO & Co-Founder)

| Name | Title | Assessment Focus |
|---|---|---|
| Don Salama | Co-CEO & Acting CFO | Strategic oversight, M&A, lender relationships, financial reporting. 1099 via Turn 3 Ventures (not W-2). |
| Greg Schmitzer | President & Co-Founder | Has one direct report (Karen Licker, Sr. Director Marketing). What is his day-to-day operational role? |
| Bill Lodes | Chief Revenue Officer | Owns sales, partner enablement, customer success, customer onboarding, program management, and tech support. Large org (~50+ people). |
| Steven Seigel | Chief Operating Officer | Owns payments strategy, data strategy & analytics, revenue ops. Small org (~5 people). |
| David Strainick | Chief People Officer | Owns HR/People & Culture, Sri Lanka country operations, IT, technical training. |
| Jack Kennedy | Chief Technology Officer | Owns software engineering, product management, enterprise technology, product design. Per Don: CTO in title — Chathura runs most of tech operationally. |

#### L2 — Key Reports Under CTO (Jack Kennedy)

| Name | Title | Notes |
|---|---|---|
| **Chathura Ratnayake** | SVP Global Software Engineering | **Primary engineering leader.** Per Don, basically runs most of tech even though much of it doesn't formally report to him. Key engagement contact. Direct reports: Akshay Bhasin (QE lead), Randy Brown (VP Engineering, Restaurant), Matthew Crumley. |
| **Randy Brown** | VP Engineering, Restaurant | Runs the entire restaurant/CAKE engineering team: front end (CAKEpop/Kiosk v2, Fixed POS, KDS v2/Cloud/Loyalty) and backend (Cloud/EMS). ~10 engineers. Reports to Chathura. **Key interview target — owns the product line where CAKE outages originate.** |
| Akshay Bhasin | QE Lead | Owns Restaurant Quality Engineering team (~7 QE engineers). Reports to Chathura. |
| Zubair Syed | VP Software Engineering | Direct reports: Daniel Lomsak, Matias Riglos, James Oliver, Anthony Goad, Ana Chambers, Nagaswaroopa Kaukuri. |
| Dulanjan Wengappuliarachchi | Sr. Director, Product & GTM | Scope is broader than title suggests: owns Product Management, Product Design, Product Marketing (TBD — role open), and L&D/Training. Reports: Mirunaaliny Somasunthara Iyer, Thaddeus Fox, Richard Farber, Jake L. (Restaurant PM), Shavin P. (Ops Eng PM). **Key open headcount: Payments PM (TBD), Product Marketing Manager (TBD).** |
| Jeremy Diggins | Director Enterprise Technology | |
| Chris Gomersall | Director Product Design | |

#### L2 — Key Reports Under Other Executives

| Name | Title | Reports To | Notes |
|---|---|---|---|
| Karen Licker | Sr. Director Marketing | Greg Schmitzer | Only direct report to the President. |
| Peter Vu | Sr. Sales Manager - Tampa | Bill Lodes | |
| Robert Jaklitsch | VP Partner Enablement | Bill Lodes | |
| Dasunmi Nayakakorala | Director Customer Onboarding | Bill Lodes | |
| Taylor Butto | Director Customer Success | Bill Lodes | |
| Thomas O'Connell III | CE Onboarding Manager | Bill Lodes | |
| Fiddniel Guilarte | Sr. Director Program Management | Bill Lodes | |
| Mark Guilarte | PMO | Bill Lodes | Program management office — runs GTM tracker and release coordination. |
| Joel Maldonado | Tech Support Supervisor | Bill Lodes | Tech support reports to Revenue, not Engineering. |
| Michael Lee | Tech Support Supervisor | Bill Lodes | |
| Andrew Honnold | Sr. Dir. Payments Strategy | Steven Seigel | Payments — relevant to CAKE/Visa assessment. |
| Eric Breland | VP Data Strategy & Analytics | Steven Seigel | |
| Zachary Honnold | Sr. Revenue Ops Analyst | Steven Seigel | |
| **Rajik Gunatilaka** | VP & LK Country Head | David Strainick | **Sri Lanka operations report to People, not CTO.** |
| Bailey Shatney | Director People & Culture | David Strainick | |
| Jorge Maltes | Director Information Technology | David Strainick | **IT reports to People, not CTO.** |
| Adriana Zuniga-Aragon | Technical Training Specialist | David Strainick | |

#### Organizational Structure Observations

The org chart reveals several structural choices worth probing during the onsite:

1. **No dedicated product executive.** Product management (Dulanjan Wengappuliarachchi) and product design (Chris Gomersall) both report to the CTO. There is no separate product leader at the executive level. Does the CTO make product decisions, or does product management operate with autonomy?
2. **Formal vs. informal authority in engineering.** The CTO (Jack Kennedy) holds the title, but per Don, Chathura Ratnayake (SVP Global Software Engineering) "basically runs most of tech." This divergence between formal authority and operational authority is a primary investigation target — it directly impacts decision-making speed, accountability, and team clarity.
3. **Sri Lanka country head reports to Chief People Officer, not CTO.** Rajik Gunatilaka is under David Strainick. The engineering resources in Sri Lanka may have dotted-line relationships to Chathura/Zubair, but the formal reporting runs through People/HR. This is an unusual structure worth understanding.
4. **IT reports to Chief People Officer.** Jorge Maltes (Director IT) reports to Strainick, not Kennedy. Internal IT infrastructure is organizationally separated from product engineering.
5. **Tech support reports to CRO, not engineering.** Two tech support supervisors with 15+ people report up through the revenue org (Bill Lodes). Customer-facing technical support and engineering are organizationally separated.
6. **President has minimal direct org.** Greg Schmitzer (President & Co-Founder) has exactly one direct report — Karen Licker (Sr. Director Marketing). This is a very small org for a President title.
7. **COO org is very lean.** Steven Seigel's COO org is ~5 people covering payments strategy, data/analytics, and revenue ops — significantly smaller than the CRO org.
8. **Restaurant engineering team is small relative to system surface area.** Randy Brown's team (~10 engineers + ~7 QE under Akshay) maintains 15+ live CAKE systems while simultaneously developing 6+ new products/versions. This ratio of system surface area to team size is a primary candidate for execution friction.
9. **Product org is broader than it appears.** Dulanjan Wengappuliarachchi's title is "Sr. Director, Product & GTM" and he owns Product Management, Product Design, Product Marketing, AND L&D/Training — four functions. Two key roles are open (Payments PM, Product Marketing Manager). This is a lot of scope for one Sr. Director under the CTO.
10. **A documented prioritization and GTM process exists.** Multi-department feature scoring, executive alignment on top 5 initiatives, PMO-run release cadence. Whether this process is actually followed or routinely overridden is a key onsite question.

### 5.6 Known Challenges (Pre-Engagement Signal)

Glassdoor: 2.4/5, 31% recommend, 32% positive outlook. Combined with customer reviews and initial conversations:

- **Execution velocity:** Multiple stakeholders describe "trouble executing."
- **AI gap**: Heavy marketing around Neo/agentic commerce, but flagship AI products reportedly not production-ready.
- **Architectural polarity:** AI-native building AND legacy POS firefighting simultaneously.
- **Formal vs. informal authority**: CTO holds the title; SVP Global Software Engineering drives operational execution. Implications for decision-making speed and accountability.
- **Offshore coordination:** Sri Lanka engineering with timezone challenges, reporting through People rather than Engineering.
- **Priority whiplash:** Constantly shifting priorities mid-sprint.
- **CAKE reliability:** System-wide payment outages, degraded support, customer churn.
- **Culture erosion:** Layoffs, shifting bonuses, forced RTO, Houston shutdown. "Toxic culture," "broken promises."
- **Sales-driven distortion:** Sales promises overriding product logic. Unreachable quotas.
- **Investor & leadership dynamics:** Communication gaps with the board, Morgan Stanley — the catalyst for this transition.

---

## 6. Diagnostic Framework: The Six Systems

Evaluate six interconnected systems. Problems in any one cascade into the others.

| System | Core Question | Key Indicators |
|---|---|---|
| **1. Business Direction** | What matters most? What gets funded? What tradeoffs are acceptable? | Portfolio clarity, resource allocation, strategic coherence |
| **2. Product Decision** | Who owns prioritization? How often do sales/board override product? | Roadmap governance, power dynamics, requirement stability |
| **3. Delivery** | How does work move from idea to shipped value? Where are queues and rework? | Cycle time, deploy frequency, WIP, sprint completion |
| **4. Technical** | Where is coupling high? Where is legacy strangling velocity? | Architecture, tech debt ratio, incidents, deploy complexity |
| **5. Operating Cadence** | What meetings/metrics govern execution? Do leaders inspect inputs or narratives? | Meeting structure, dashboards, escalation paths |
| **6. Accountability** | Are teams rewarded for shipping, rescuing, pleasing execs, or avoiding blame? | Comp structures, recognition, promotion criteria |

### 6.1 Stabilize, Optimize, Monetize

**Stabilize**: Ensure core systems are reliable, secure, governed. Map CI/CD, identify single points of failure (especially CAKE payments), stabilize support triage.

**Optimize**: Streamline architecture and ops. Evaluate vendor contracts, rationalize mobile frameworks, clarify reporting relationships and decision rights, establish clear authority boundaries.

**Monetize**: Leverage optimized AI capabilities as growth drivers. Validate Neo is generating revenue, not just compute costs.

### 6.2 Methodological Foundation

Every domain of this assessment is anchored to named, proven frameworks — not ad-hoc judgment. This ensures rigor, repeatability, and credibility with board-level audiences.

| Assessment Domain | Named Frameworks | What They Provide |
|---|---|---|
| **Engineering Performance** | DORA Metrics (Forsgren/Humble/Kim), SPACE Framework (Microsoft Research), DevEx/DX Core 4 (Noda et al.) | Quantitative delivery benchmarks, developer productivity across 5 dimensions, experience survey data |
| **Engineering Culture** | Pragmatic Engineer Test (Orosz), Joel Test (Spolsky), Westrum Culture Model (DORA/BMJ) | Quick yes/no culture health checks, organizational culture typology (pathological → generative) |
| **Organizational Diagnostic** | McKinsey 7S (Peters/Waterman), Galbraith Star Model, Nadler-Tushman Congruence Model | Holistic org effectiveness assessment, operating model design, informal vs. formal org diagnosis |
| **Decision Rights** | Bain RAPID (Rogers/Blenko, HBR 2006), DACI (Intuit/Atlassian), RACI | Map who recommends, decides, approves for critical recurring decisions |
| **Delivery & Flow** | Value Stream Mapping (Rother/Shook), Theory of Constraints (Goldratt), Flow Framework (Kersten) | Visual flow analysis, bottleneck identification, work type distribution (features vs. debt vs. defects) |
| **Team Design** | Team Topologies (Skelton/Pais) | Four team types, three interaction modes, cognitive load assessment |
| **Technology Strategy** | Wardley Mapping (Wardley), Three Horizons (McKinsey/Baghai), ThoughtWorks Technology Radar | Component evolution mapping, innovation portfolio balance, technology governance |
| **Technical Debt** | Fowler's Technical Debt Quadrant, SQALE Method (Letouzey), Kruchten-Nord-Ozkaya Taxonomy (CMU SEI) | Debt classification, automated quantification, systematic prioritization |
| **Architecture** | C4 Model (Brown), ATAM (CMU SEI) | Hierarchical architecture documentation, quality-attribute tradeoff analysis |
| **CEO Transition** | Watkins First 90 Days / STARS (HBR), Spencer Stuart New CEO Launch Pad | Business situation diagnosis, five essential conversations, early win identification |
| **Due Diligence Structure** | PE Tech DD 9-Pillar Framework (Crosslake/West Monroe/EY-Parthenon standard) | Organize all findings into board-ready pillar structure with maturity scores |

These frameworks are layered, not stacked. The pre-work deploys lightweight assessments (DORA Quick Check, DevEx survey, Westrum culture survey, Pragmatic Engineer Test). The onsite sprint uses workshop-driven frameworks (Value Stream Mapping, RAPID decision mapping, Wardley Mapping, Team Topologies classification). Deliverables are organized using the PE DD pillar structure and Watkins' STARS model.

The Nadler-Tushman Congruence Model is particularly relevant here — it explicitly includes the **informal organization** (politics, unwritten rules, shadow power structures) as a diagnostic element. The divergence between Kennedy's formal CTO authority and Chathura's operational leadership is a textbook congruence question.

---

## 7. Hypothesis Library: Patterns to Prove or Disprove

Named hypotheses to validate or rule out onsite. Converts time from exploration into targeted investigation.

| # | Pattern | Description | How to Test |
|---|---|---|---|
| A | **Portfolio Sprawl** | Too many products, insufficient shared platform discipline | How many active codebases? Teams on >1 product? Shared services vs. duplication? |
| B | **Sales-Led Chaos** | Revenue promises create roadmap churn and tech debt | Ask sales what they promise; ask eng what surprises them mid-sprint; ask product who overrides |
| C | **Fake Platforming** | Leadership talks "platform"; teams maintain customer-specific patchwork | Show me the shared platform layer. What does Neo actually consist of in production today? |
| D | **Unclear Ownership** | Formal authority and operational authority are misaligned; decision rights are ambiguous | Map who actually decides on architecture, staffing, priorities vs. who the org chart says should. Trace the Kennedy/Chathura dynamic. Where does product management authority sit without a dedicated product executive? |
| E | **Dependency Drag** | A few people/teams are routing bottlenecks | Whose approval do you need? Who do you wait on? Map the dependency graph |
| F | **Legacy Gravity** | CAKE architecture prevents speed; no triage of must-modernize vs. can-encapsulate | What constraint costs the most velocity? Ratio of legacy maintenance vs. new feature hours? |
| G | **Missing Cadence** | No consistent execution inspection; leadership discovers reality through fire drills | What is the weekly rhythm? What metrics are reviewed? How does bad news travel? |
| H | **Biz-Tech Mistranslation** | Business says "eng is slow"; eng says "business is chaotic"; real issue is undefined tradeoffs | Ask both sides why delivery is slow. Compare answers. Look for structural decision gaps |
| I | **Architectural Polarity** | Simultaneous AI-native building + legacy POS maintenance = irreconcilable eng split | How are teams allocated? Do engineers rotate or get stuck? Is there a migration path? |

---

## 8. Three-Week Execution Plan

The full scope of the engagement is compressed into three weeks by leveraging AI-augmented tooling for automated system analysis, note-taking, documentation synthesis, and pattern identification. Pre-work begins immediately and runs through April 11. The onsite sprint is April 13–15 (Monday–Wednesday). The more pre-work lead time, the more value the onsite delivers.

### 8.1 Timeline Overview

| Phase | Timeline | Focus | Effort |
|---|---|---|---|
| Pre-Work | Now → April 11 | CEO alignment, hypothesis building, pre-read analysis, automated system reconnaissance, interview scheduling, internal messaging | 15 hrs async + 5 hrs meetings (20 hrs) |
| Onsite | April 13–15 (Mon–Wed) | Diagnostic sprint: leadership interviews, team interviews, artifact review, system walkthroughs, value-stream tracing, real case tracing | 20 hrs onsite + 5 hrs async (25 hrs) |
| Deliverables | April 16–25 | Pattern validation, synthesis, friction register, CEO operating brief, 30/60/90 plan, optional board deck | 15 hrs async + meetings |

**Total estimated effort: ~60 hours.** AI augmentation handles the bulk of system scanning, documentation ingestion, interview transcription, and pattern analysis, freeing Adam's hours for the high-judgment work: interviews, interpretation, and synthesis.

---

## 9. Pre-Work — Now through April 11 (15 hrs async + 5 hrs meetings)

The pre-work phase converts the onsite from exploration into validation. Every hour invested here multiplies the value of onsite face time.

### 9.1 AI-Augmented System Reconnaissance (~6 hrs async)

With appropriate access credentials arranged through Don, run automated analysis across Mad Mobile's development and infrastructure tooling before arriving onsite:

- **GitHub / Source Control:** Repository inventory (count, languages, activity recency, contributor concentration). Commit frequency and patterns. PR review cycle times. Branch strategy and merge patterns. Automated testing coverage metrics. CI/CD pipeline configuration review. Identify repos with no recent activity (dead code) vs. high-churn repos.
- **AWS / Infrastructure:** Service inventory and resource utilization. Cost allocation by service/team/product. Deployment architecture mapping. Monitoring and alerting configuration review. Disaster recovery posture. Identify single points of failure and redundancy gaps.
- **Jira / Project Management:** Sprint velocity trends over last 6–12 months. Ticket lifecycle analysis (time in each status). Bug vs. feature ratio. Escalation patterns. Epic completion rates. Backlog health (age, grooming recency). Cross-team dependency tickets. Mid-sprint scope change frequency.
- **Documentation / Wiki:** Coverage audit — what's documented vs. tribal knowledge? Architecture diagram currency. Runbook and playbook inventory. Post-mortem/incident review history.
- **Vendor & Tool Utilization:** Inventory of all engineering and operational tools (monitoring, observability, CI/CD, testing, project management, communication). Identify tools that are paid for but unused, underutilized, or redundant. Flag overlapping capabilities. This is not a contract or pricing review — it's a utilization and effectiveness assessment.

This automated reconnaissance produces a baseline technical health snapshot before a single interview occurs. It converts questions from "tell me about your deployment process" to "I can see your average PR review time is X and deployment frequency is Y — walk me through why."

### 9.2 Deployable Assessments (~3 hrs async)

Deploy four lightweight, established assessments to engineering leads and ICs before the onsite. Total time commitment per person: under 15 minutes. A critical positioning note: many people at Mad Mobile have felt their voices were unheard or ignored under previous leadership. These surveys are not just data collection — they're a concrete signal that new leadership is listening. When introduced with the right framing from Don, the act of asking becomes as valuable as the answers.

These surveys are also designed to be **repeatable** — Mad Mobile's team can re-run them at 30 and 60 days post-engagement without Adam's involvement to measure whether changes are producing results.

Ideally, run these through Mad Mobile's existing internal survey infrastructure so it feels like part of the organization rather than an external exercise. Fallback: Adam spins up Google Forms. Surveys should be introduced with a brief note from Don framing them as part of his onboarding process.

- **DORA Quick Check** (dora.dev/quickcheck): Each engineering lead self-assesses their team's deployment frequency, lead time, change failure rate, and recovery time. Results classify teams as Elite/High/Medium/Low against Google's research benchmarks from 33,000+ professionals. Compare self-reported vs. actual metrics from the automated system scan.
- **Westrum Culture Survey** (6 questions, Likert scale): Measures organizational culture type — pathological, bureaucratic, or generative — based on how information flows. Covers messenger treatment, shared responsibilities, cross-functional collaboration, failure response, and new idea reception. Takes 2 minutes per respondent.
- **DevEx Survey** (DX Core 4, ~14 items): Measures developer experience across feedback loops, cognitive load, and flow state. Results map to four executive-ready dimensions: Speed, Effectiveness, Quality, and Impact.
- **Pragmatic Engineer Test** (12 yes/no questions): Gergely Orosz's modern successor to the Joel Test. Assesses engineering culture maturity. Administer to 3–5 engineering leads.

### 9.3 Pre-Read Package Ingestion (~4 hrs async)

AI-assisted analysis will ingest, index, and identify patterns across these documents:

- Org chart including dotted lines (all eng, product, QA, DevOps, support, Sri Lanka)
- Product portfolio and revenue mix by offering (CAKE vs. Concierge vs. Neo vs. Payments)
- Current roadmap(s) for each product line *(Restaurant roadmap received March 2026 — need Concierge/Retail and Neo/AI roadmaps)*
- Company goals, board goals, CEO goals
- Engineering org structure and team assignments by product
- Deployment environments, release cadence, CI/CD documentation
- Architecture diagrams (even if outdated)
- Top customer escalations from the last 6–12 months (especially CAKE outages)
- KPI / scorecard / dashboard screenshots
- Sprint velocity metrics
- Product requirement / epic / ticketing examples (2–3 representative)
- Incident reviews, post-mortems, retrospectives
- Core systems list: codebases, repos, cloud accounts, observability, CI/CD, CRM, ticketing, support tools, docs
- Open strategic initiatives and known "problem projects"
- Third-party vendor contracts and API dependency inventory (OpenAI, Anthropic, AWS costs)
- Engineering and operations tool inventory — monitoring, observability, CI/CD, testing, project management, communication platforms (what's in use, what's licensed)
- CAKE acquisition integration documentation and current state
- Investor/board concerns Don is willing to share

### 9.4 CEO Alignment Sessions (~5 hrs meetings)

Two to three structured sessions with Don across the pre-work period. Don's two years of operational context means these sessions can go deeper faster than a typical CEO onboarding exercise — he's not speculating, he already knows the landscape.

#### Session 1: Success Criteria & Scope (~90 min)

- Define success: what would make this a win in Don's eyes?
- Confirm scope boundaries and depth per domain
- Establish confidentiality framework and internal messaging approach
- Align on the pre-read package and system access requests
- Draft the introduction message Don will send to leadership

| Domain | Depth | Rationale |
|---|---|---|
| Product management & roadmap governance | Deep | Product sits under CTO with no dedicated product executive — primary investigation target |
| Engineering org & delivery pipeline | Deep | Core of the execution story; Kennedy/Chathura dynamic |
| Architecture / platform / tech debt | Deep | Constrains delivery velocity; CAKE legacy burden |
| QA / release / DevOps / SRE | Medium | Part of delivery system |
| AI strategy (Neo, agentic commerce) | Medium | High investor visibility, high risk of positioning gap |
| Sales-to-delivery handoff | Medium | Common source of churn and broken promises |
| Leadership decision-rights mapping | Medium | Formal vs. informal authority; org design choices |
| Customer support / escalation loop | Light | Signal source; CAKE outage response quality; tech support under CRO |
| Vendor & tool utilization | Medium | Are tools being used? Anything redundant or unused? Not a contract review. |
| Implementation / professional services | Light | Platform vs. services question |
| Finance / investor reporting inputs | Light | Don already has deep visibility here |

#### Session 2: Political Landscape & Hypotheses (~90 min)

- Map the political landscape: who Don trusts, who the org trusts, Bruce-era commitments, investor distortions
- Kennedy/Chathura dynamic — how does it actually work? Where does it break?
- Greg Schmitzer's role going forward — what does the President actually do day-to-day?
- Any "untouchable" narratives
- Don's hypotheses: suspected bottlenecks, sensitive zones, what he fears discovering
- Review initial findings from automated system reconnaissance

#### Session 3: Pre-Onsite Briefing (~60 min)

- Review synthesized pre-read findings and automated system analysis results
- Finalize the hypothesis scorecard with initial evidence
- Confirm interview schedule and priority targets
- Identify the 5 real cases to trace onsite
- Confirm logistics: NDA signed, system access active, conference room reserved for April 13–15

### 9.5 Interview Schedule Design (~2 hrs async)

Pre-schedule every interview so the onsite week is fully utilized. Priority targets:

| Person / Role | Day | Duration | Focus |
|---|---|---|---|
| Don Salama (Co-CEO/Acting CFO) | Daily | 30 min/day | Morning sync + EOD debrief |
| **Jack Kennedy (CTO)** | Mon | 90 min | Architecture, Neo, AI strategy, tech debt, decision-making authority |
| **Chathura Ratnayake (SVP Global Software Eng)** | Mon | 90 min | Day-to-day execution, team health, sprint reality, Sri Lanka coordination, operational authority |
| Dulanjan Wengappuliarachchi (Sr. Dir, Product & GTM) | Mon | 60 min | Roadmap, client promises, how product decisions get made under CTO, open headcount impact |
| Steven Seigel (COO) | Mon | 45 min | Payments strategy, data/analytics, revenue ops |
| **Randy Brown (VP Engineering, Restaurant)** | Tue | 60 min | CAKE engineering reality: team capacity vs. system surface area, outage patterns, legacy vs. new work split, POS V3/V4 coexistence |
| Zubair Syed (VP Software Engineering) | Tue | 45 min | Engineering execution, team allocation, CAKE vs. Neo split |
| Bill Lodes (CRO) | Tue | 45 min | Sales pipeline, feature promises, deal blockers, tech support escalation |
| Engineering Managers / Tech Leads (2–3) | Tue | 45 min each | Sprint reality, blockers, PACE evaluation |
| Senior ICs (2–3) | Tue | 30 min each | Unfiltered ground-level perspective |
| Jeremy Diggins (Dir Enterprise Technology) | Tue | 45 min | Enterprise tech landscape, integrations |
| Rajik Gunatilaka (VP & LK Country Head) | Wed | 45 min (video) | Sri Lanka workflow, communication, quality — reports to Strainick not Kennedy |
| Joel Maldonado or Michael Lee (Tech Support) | Wed | 30 min | CAKE outage response, escalation loop, ticket patterns |
| David Strainick (Chief People Officer) | Wed | 30 min | HR perspective, Sri Lanka management, IT, culture |
| Greg Schmitzer (President) | Wed | 30 min | Partnerships, GTM, his operating role |
| Chris Gomersall (Dir Product Design) | Wed or async | 30 min | Design process, collaboration with product/eng |

### 9.6 Pre-Select Real Cases to Trace

1. One CAKE payment processing outage — trace from detection through support, engineering, and resolution.
2. One recent customer escalation — trace from complaint through organizational response.
3. One delayed strategic initiative — understand structural factors behind the slip.
4. One mid-sprint priority change — trace who requested it and downstream impact.
5. One cross-functional success story — understand what conditions made it work.

### 9.7 Logistics

- **NDA**: Sign before receiving proprietary documents or system access.
- **System access:** Guest/read-only access to GitHub, Jira, AWS console (read-only), monitoring dashboards, internal wiki. Arrange during pre-work period — this has the longest lead time and may require coordination across multiple teams.
- **Location**: Tampa HQ — [Mad Mobile](https://www.google.com/maps/place/Mad+Mobile/).
- **Travel**: Adam travels via Uber from St. Pete to Tampa; Mad Mobile covers travel and meals during the onsite.
- **Workspace**: Reserve a conference room for private interviews and synthesis.
- **Tools**: Adam will use AI-assisted note-taking, transcription, and analysis throughout. All data remains within the NDA scope.
- **Slack / Teams access**: Temporary guest account on whichever platform Mad Mobile uses for the duration of the engagement. Adam will set up a dedicated project channel for interview coordination and logistics, and use DMs for async follow-ups.

---

## 10. Week 2: Onsite Diagnostic Sprint — April 13–15 (20 hrs onsite + 5 hrs async)

The onsite is a structured three-day diagnostic sprint. The majority of time is spent in interviews, artifact walkthroughs, and observation — not receiving slide decks. AI-augmented note-taking captures everything; Adam focuses on listening, probing, and reading the room.

### 10.1 Daily Rhythm

| Time Block | Activity |
|---|---|
| 8:00–8:30 | Morning sync with Don — review findings, adjust plan, update hypothesis scorecard |
| 8:30–12:00 | Scheduled interviews (2–3 sessions) |
| 12:00–1:00 | Lunch with different team members each day (informal) |
| 1:00–3:30 | Interviews or system/artifact walkthroughs (2–3 sessions) |
| 3:30–4:30 | Observe: standup, sprint planning, support queue; or trace a real workflow |
| 4:30–5:30 | Synthesis — update friction register, pattern ID, hypothesis scoring |
| 5:30–6:00 | End-of-day debrief with Don |

Async evening work (~1.5 hrs/night, Mon & Tue): AI-assisted synthesis of interview notes, cross-referencing against automated system data, updating live artifacts. By processing each day's findings same-night, the next morning's interviews are informed by the previous day's patterns.

### 10.2 Day-by-Day Focus

- **Monday — Leadership, Architecture & System Framing.**
  - Executive briefing with Don (board dynamics, investor expectations).
  - Architecture review with CTO (Jack Kennedy) and SVP Global Software Engineering (Chathura Ratnayake) — whiteboard the infrastructure using C4 Model notation (Context and Container levels), map CAKE-to-Neo communication, where AI API calls occur in transaction flow.
  - Begin Wardley Mapping workshop with tech leadership — plot key components on the evolution axis to identify build-vs-buy misalignment.
  - Product direction session with Dulanjan Wengappuliarachchi (Sr. Director, Product & GTM) — how product decisions get made when product reports to the CTO. Explore scope breadth: he owns PM, design, product marketing (open headcount), and L&D. How does the prioritization scoring process actually work? Does executive alignment override the multi-department scoring?
  - Meet COO (Steven Seigel) — payments strategy, data, revenue ops.
  - Apply McKinsey 7S lens across all leadership interviews.
  - ***Goal: build the first-pass map, understand the "official story," and establish the architecture baseline.***

- **Tuesday — Engineering Deep Dive, Cross-Functional Tracing & Decision Rights.**
  - Bypass the C-suite. Interview engineering managers using PACE model (Planning, Alignment, Communication, Execution).
  - Review pre-work DORA metrics and DevEx survey results with each lead.
  - Classify teams against Team Topologies types (stream-aligned, platform, enabling, complicated-subsystem).
  - Apply Theory of Constraints thinking: where does work pile up? Who is the "Brent" (single-point-of-failure person)?
  - Meet VP Software Engineering (Zubair Syed), VP Engineering Restaurant (**Randy Brown** — key session: CAKE team capacity vs. 15+ live systems, outage root causes, POS V3/V4 coexistence), enterprise technology (Jeremy Diggins), senior ICs.
  - Trace 1–2 real customer promises from sale to production using Value Stream Mapping — capture lead time, process time, wait time, and %Complete-and-Accurate at each step.
  - Map decision rights for the 10–15 most critical recurring decisions using Bain's RAPID framework. Special focus: who decides architecture, roadmap, staffing, and incident response — Kennedy? Chathura? Both? Neither?
  - Meet CRO (Bill Lodes) — sales pipeline, feature promises, tech support escalation path.
  - Apply Flow Framework work-type analysis. Facilitate Three Horizons classification of current engineering projects.
  - ***Goal: find where reality deviates from the official story and move from anecdote to pattern.***

- **Wednesday — Validation, Gaps, Sri Lanka & Wrap.**
  - Follow up on surprises from Monday and Tuesday.
  - Sri Lanka team video call with Rajik Gunatilaka (VP & LK Country Head) — explore the reporting-through-People structure.
  - Tech support synthesis — how do issues flow from tech support (under CRO) to engineering (under CTO)? Interview Joel Maldonado or Michael Lee.
  - Meet Greg Schmitzer (President) — understand his operating role. Meet David Strainick (Chief People Officer) — HR, Sri Lanka, IT, culture.
  - Classify technical debt using Fowler's Technical Debt Quadrant.
  - Review Westrum culture survey results by team.
  - Apply Watkins' STARS framework to diagnose which business situation Don is stepping into.
  - Vendor/tool utilization review — walk through the engineering toolchain with Chathura or a senior engineer. Known tools in use: Cursor (AI IDE), Guru (support docs), Figma (design), Jira (project management). Flag unused, redundant, or underutilized tools. Assess whether AI tooling adoption (Cursor, AI for test cases, AI for RCA) is producing measurable productivity gains.
  - Afternoon: final debrief with Don. Review hypothesis scorecard, friction register draft, and STARS diagnosis. Score each of the PE Tech DD 9 Pillars on a preliminary maturity scale. Identify remaining gaps to address async in deliverables week.
  - ***Goal: validate patterns, fill gaps, and transition to deliverable production.***

**Note:** Some lower-priority interviews (product design, enterprise technology details) may happen via video in the days following the onsite if time runs short during the three-day sprint.

---

## 11. Interview Framework

Structured but conversational. AI-assisted note-taking captures everything; Adam focuses on listening and probing.

### 11.1 Universal Opening

> *"Thanks for making time. I'm Adam — I'm helping Don get a grounded understanding of how the organization builds, decides, and delivers. I'm not here to judge individuals. I'm trying to understand where the system makes it easy or hard for talented people to succeed. Nothing you tell me will be attributed to you by name."*

### 11.2 Leadership Track (CTO, COO, CRO, CPO)

- What are your team's top 3 outcomes this quarter?
- How does work enter your system?
- What most often delays execution?
- Where do priorities change late?
- What do other teams misunderstand about yours?
- What creates rework?
- Where do customer commitments and technical reality diverge?
- What decisions are easy here? What decisions are weirdly hard?
- Where are responsibilities ambiguous?
- Which commitments are strategic vs. inherited from the previous era?
- What board/investor pressures distort normal operations?
- What metrics do you trust? Which are missing?
- If you could fix one structural issue in 90 days, what would it be?
- How do you and [other leaders] divide ownership on [specific decisions]?

### 11.3 Engineering & Technical Track

- Walk me through a recent project you're proud of.
- Show me how a real piece of work moves from idea to production.
- Where does work sit waiting? Where does quality break down?
- What kind of work is hardest to estimate? What creates fire drills?
- How does the Sri Lanka relationship actually work day-to-day?
- If I looked at your Jira board right now, what would surprise me?
- What architectural constraint costs you the most velocity?
- Are you maintaining both React Native and Flutter? Why?
- What percentage of your time goes to CAKE legacy vs. Neo/new work?
- The CAKE ecosystem has 15+ live systems and 6+ in development — how does the team of ~10 engineers manage that surface area? What gets sacrificed?
- You're running POS V3 (Pondus) and POS V4 (Elio) simultaneously — what's the migration path? Are both actively maintained?
- How is AI work staffed vs. core platform work?
- How effective is Cursor for your daily engineering work? What other AI tools are you using? What's missing?
- Does the Architecture Review Board (ARB) process work or does it create bottleneck?
- What is one recurring problem leadership underestimates?
- [With pre-work data] I can see your PR review times average X — does that match your experience? What drives it?
- When you need a decision on architecture or priorities, who do you go to? How quickly does it happen?
- What tools do you use daily? Are there any you're paying for but nobody actually uses? Any gaps — tools you wish you had?

### 11.4 Product Track

- How do you decide what goes on the roadmap? Who has veto power?
- The documented prioritization process uses multi-department scoring and executive alignment on top 5 — does that actually work in practice? How often does it get overridden?
- What percentage is proactive vs. reactive?
- How often do sales promises override product logic?
- How does reporting to the CTO work — do you have product autonomy or are engineering priorities dominant?
- You own PM, design, product marketing, and L&D — is that scope manageable? What suffers?
- Two key PM roles are open (Payments, Product Marketing) — how is that impacting delivery?
- Is there a real product org or are you functioning as a request router?

### 11.5 Support, Sales & Cross-Functional Track

- What are the top 3 customer complaints right now?
- Are there features being sold that don't exist or work reliably?
- Walk me through a CAKE payment outage from the support perspective.
- How does bad news travel in this organization?
- When you escalate a technical issue, what's the path from tech support to engineering? How fast does it move?

### 11.6 Universal Closing

> *"Is there anything I haven't asked that you think is important for a new CEO to understand? What's the one thing you'd want Don to know about what it's like to work here?"*

---

## 12. Artifacts to Build During Onsite

Build these live during the week. AI assists with drafting and data integration; Adam provides judgment and structure.

### 12.1 Capability / Product Map + Three Horizons

Products, customer segments, revenue contribution, platform vs. bespoke, team ownership. Apply McKinsey's Three Horizons classification to each product line: H1 (core revenue), H2 (emerging opportunities), H3 (future seeds). Compare actual engineering spend allocation to the 70/20/10 benchmark.

### 12.2 Decision-Rights Map (Bain RAPID)

Map the 10–15 most critical recurring decisions: who Recommends, provides Input, Agrees (narrow veto), Decides, and Performs. Cover roadmap, architecture, delivery commitments, resourcing, incidents, escalations, and pricing exceptions. RAPID insists on a single Decider per decision — where that's missing, you've found a structural bottleneck. Special focus: the Kennedy/Chathura decision-making dynamic and how product decisions flow without a dedicated product executive.

### 12.3 Value-Stream Map (Rother/Shook Method)

Map the primary delivery flows: new feature, bug fix/incident, and infrastructure change. Capture lead time, process time, wait time, and %Complete-and-Accurate at each step. Calculate the activity ratio (process time ÷ lead time) — typical software orgs run 15–25%; below 10% signals severe queue/handoff waste. Pay special attention to handoffs between tech support (CRO org) and engineering (CTO org).

### 12.4 Technology Topology Map (C4 Model)

Using Simon Brown's C4 Model, produce Level 1 (Context) and Level 2 (Container) diagrams. Major systems, integrations, dependencies, fragile components, deployment ownership, data flow, observability gaps, and legacy-but-critical zones. Map the CAKE-to-Neo boundary explicitly.

### 12.5 Flow Distribution Analysis (Flow Framework)

Classify recent Jira work into four types: Features (new value), Defects (quality fixes), Risks (security/compliance), and Debts (architecture). A company spending 70% on defects and debt with 30% on features signals a constrained pipeline.

### 12.6 Friction Register

| Field | Description |
|---|---|
| Symptom | What people describe experiencing |
| Root Cause | Probable structural cause (may span multiple systems) |
| Impact | Business outcome affected and severity |
| Category | Org / Process / Technology / Business Model / Leadership |
| Confidence | High / Medium / Low based on evidence quality |
| Pattern Match | Which hypothesis (A–I) it maps to |
| Severity | Critical / High / Medium / Low |
| Next Action | Recommended intervention and owner candidate |

---

## 13. Week 3: Analysis, Synthesis & Deliverables — April 16–25 (15 hrs)

AI-augmented synthesis generates first drafts from accumulated notes, data, and artifacts. Adam's hours focus on editorial judgment, narrative framing, and quality.

### 13.1 Analysis Methodology

1. **Pattern validation:** Score each hypothesis (A–I) as Confirmed / Partially Confirmed / Not Present, with supporting evidence.
2. **Root cause analysis:** For each major finding, trace the causal chain. Distinguish symptoms from structural causes.
3. **Impact-effort mapping:** Every recommendation mapped on impact (H/M/L) and effort (quick win / medium-term / major initiative).
4. **Tech debt quantification:** Using automated system data, calculate the ratio of legacy maintenance vs. new development.
5. **Narrative framing:** A coherent story connecting business outcomes to organizational and technology changes. Not a generic consultant report.

### 13.2 Deliverables

#### Executive Summary (2–4 pages)

What's working, what's breaking, why, biggest risks, top priorities. No padding.

#### Execution System Map

One visual set: org + RAPID decision rights map, value stream with bottlenecks marked, C4 technology topology, Wardley Map of key components, Team Topologies classification, and six-system health assessment.

#### Findings Matrix (Friction Register)

10–15 prioritized findings organized using the PE Tech DD 9-Pillar structure. Each finding includes: issue, evidence, impact, severity, confidence, pattern match (A–I), recommended action, and owner candidate.

#### Hypothesis Scorecard

Each pattern (A–I) scored as Confirmed / Partially Confirmed / Not Present with evidence summary.

#### STARS Diagnostic

Using Watkins' STARS framework, classify the business situation Don is stepping into: Start-up, Turnaround, Accelerated Growth, Realignment, or Sustaining Success. Positions the entire deliverable as the technology and operations chapter of Don's transition playbook.

#### The 30/60/90-Day Plan

- **First 30 Days — Stabilize & Establish Truth:** Formally acknowledge CAKE technical debt to the eng team (builds credibility). Clarify the CTO role — resolve the gap between Kennedy's formal authority and Chathura's operational authority. Establish one company operating cadence for delivery visibility. Clarify decision rights for roadmap, customer commitments, and architecture. Halt non-revenue-essential feature churn to reallocate capacity to core POS stability and CI/CD. Assess whether forced RTO is driving attrition in critical roles.
- **Next 60 Days — Optimize Interfaces:** Restructure sales/product/engineering interface with mandatory weekly alignment. Move from output metrics to outcome metrics ("CAKE downtime reduction," "support ticket resolution time"). Evaluate whether product management needs its own executive leader vs. reporting to CTO. Address the tech support → engineering escalation path (currently crosses CRO → CTO org boundary). Launch architecture debt triage. Evaluate AI strategy ROI. Rationalize mobile framework duplication if confirmed.
- **Next 90 Days — Strategic Alignment:** Align portfolio and resourcing to priorities. Make org/accountability adjustments based on evidence. Evaluate whether Sri Lanka reporting structure (through People vs. Engineering) is optimal. Publish modernization thesis. Present realistic roadmap to board with empirical data.
- **Leave Alone (for now):** Explicitly list areas to avoid: cosmetic rebranding, reorganizing functioning teams, relitigating historical comp changes, wading into Bruce-era grievances. The CEO's attention is the scarcest resource.

#### Board-Ready Presentation

20–30 slides for non-technical investor audience. Organized around the PE Tech DD pillar structure with maturity scores per pillar. Designed for Don to present directly to Morgan Stanley and the board. This is a core deliverable, not an add-on — a key purpose of this engagement is producing an independent, third-party technology assessment grounded in named industry frameworks and empirical data that gives the board a credible, clear picture of what's working, what needs attention, and what the path forward looks like. The credibility comes from the methodology: DORA benchmarks, Watkins STARS classification, PE DD pillar scoring — not opinion.

#### Stakeholder Communication Draft (Optional)

Script for Don to use internally: appreciative, candid, no blame, focused on enabling teams, clear that change will be sequenced.

#### Baseline Survey Package (Repeatable)

The DORA, Westrum, DevEx, and Pragmatic Engineer surveys deployed during pre-work are designed to be re-run by Mad Mobile's team at 30 and 60 days post-engagement — without Adam's involvement. The deliverable includes the survey instruments, instructions for deployment, and the pre-engagement baseline scores so leadership can measure whether changes are producing results. This makes the engagement self-sustaining: Don's team owns the measurement cadence going forward.

#### Vendor & Tool Utilization Assessment

A summary of the engineering and operational toolchain with utilization findings. Flags tools that are paid for but unused, underutilized, redundant, or misaligned with current workflows. This is not a contract or pricing review — it's a practical assessment of whether the tooling supports or hinders execution.

---

## 14. AI-Augmented Execution Model

The compressed timeline is possible because AI handles the high-volume, repetitive analysis work, freeing Adam's time for the irreplaceable human work.

### 14.1 What AI Handles

- **System reconnaissance:** Automated scanning and analysis of GitHub repos, AWS infrastructure, Jira project data, CI/CD pipelines.
- **Document ingestion:** Processing and indexing the pre-read package.
- **Interview support:** Real-time note-taking and transcription. Immediate post-interview synthesis.
- **Cross-reference analysis:** Comparing what leadership says against what the automated system data shows.
- **Deliverable drafting:** First-draft generation of the friction register, hypothesis scorecard, and report sections.
- **Pattern identification:** Across 15+ interviews and thousands of data points, AI identifies recurring themes, contradictions, and clusters.

### 14.2 What Adam Handles (Irreplaceable)

- **Interviews**: Building trust, reading body language, probing follow-up questions, navigating political sensitivities.
- **Judgment**: Distinguishing genuine problems from noise, weighting findings by organizational context.
- **Translation**: Converting technical findings into business language for Don, the board, and investors.
- **Narrative**: Crafting the story that connects findings to action.
- **Relationship**: Maintaining the collaborative, non-threatening tone throughout.

---

## 15. Compensation & Engagement Structure

### 15.1 The Diagnostic (This Plan)

A fixed fee of **$10,000** for the complete engagement. Payment is fully deferred — Mad Mobile can pay when cash flow allows, potentially into next year. The intent is to remove financial friction entirely during the transition so we can focus on delivering value first. Mad Mobile covers travel (Uber from St. Pete to Tampa) and meals during the onsite.

What we do need in writing before onsite: a simple SOW or engagement letter covering scope, deliverables, timeline, confidentiality/NDA (especially around Neo AI architecture, prompt templates, and POS internals), IP ownership (Adam retains methodology; Mad Mobile owns deliverables), and basic liability limitations.

### 15.2 If an Ongoing Advisory Role Makes Sense

If the diagnostic reveals that sustained advisory support would be valuable — and we both agree it makes sense — we can formalize it using something like the Founder/Advisor Standard Template (FAST agreement). This is a separate conversation from the diagnostic, but worth having the framework ready. Standard parameters for a company at Mad Mobile's stage:

| Element | FAST Standard | Mad Mobile Application |
|---|---|---|
| Equity Range | 0.25%–1.00% of fully diluted cap | 0.50%–1.00% given scope of systemic restructuring and C-suite translation |
| Vesting | 2 years, monthly | Ensures continuous alignment through critical first 24 months |
| Cliff | No cliff (advisory exception) | Reflects immediate delivery of strategic value |
| Asset Type | Non-qualified options or RSAs | Based on 409A valuation and board preferences |

An ongoing advisory role would include: weekly CEO sync, review of priority fixes, help with internal communications, support establishing execution cadence/metrics/decision rights, and attendance at designated strategy or board meetings. But let's see what the diagnostic surfaces first.

---

## 16. Handling the Bruce / Investor Context

We both know this is important context, but it shouldn't be the center of the review. If Adam centers personalities and investor conflict, the engagement gets politicized fast.

- Evaluate the current operating system as it exists today
- Note where external pressure or leadership misalignment shaped incentives
- Do not conduct a retrospective blame study
- Frame everything as "what is the system doing" not "who did this"

This keeps the work useful to Don and safe with all stakeholders — including Bruce and Greg if they retain equity or operational roles.

---

## 17. Defining Success

This engagement succeeds if Don can:

- Explain the company's true operating model in a page
- Identify 3–5 root causes instead of 30 symptoms
- Stop at least one recurring source of churn quickly
- Align business and engineering around explicit tradeoffs
- Distinguish platform investment from custom-service drag
- Install a repeatable execution cadence with real metrics
- Communicate change without triggering panic or defensiveness
- Know where to personally spend time vs. delegate
- Present a credible, independent technology narrative to Morgan Stanley and the board — backed by empirical data and named frameworks, not internal spin
- Know what NOT to touch in the first 90 days
- Resolve the gap between formal and informal authority in the technology organization

That is CEO leverage.

*— End of Plan —*
