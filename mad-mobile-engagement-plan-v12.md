# CEO Ramp Accelerator & Execution Diagnostic

## TECHNOLOGY OPERATIONS REVIEW — Mad Mobile, Inc.

**WORKING DRAFT — v12**

*For discussion between Adam & Don — not yet for broader distribution*

**Adam Lazarus**
Systems & Software Engineering | Ecommerce | Enterprise Platforms | AI Strategy

**Don Salama**
Co-CEO & Acting CFO, Mad Mobile, Inc.

CONFIDENTIAL — March 2026

---

## What's Changed in v12

- **Scope discipline added.** New triage protocol for the onsite — interview priority tiers, hypothesis convergence rule, daily scope checks. Scope creep is the biggest risk to this engagement; this section addresses it head-on.
- **Concrete pre-work timeline.** Dates from March 24 through April 25 replacing the generic "now through onsite."
- **MM coordination section added.** What Chathura and Kennedy need to action, with deadlines.
- **Companion documents created.** MM Coordination Brief (shareable with Chathura/Kennedy) and NotebookLM source doc (for generating podcast/video/slides to brief them).
- **FAST/advisory section removed.** That's a separate conversation if and when it makes sense.
- **Compensation updated.** $10K penciled in, deferred, final terms pending.
- **Sensitive observations tagged.** Items marked `[PRIVATE]` stay between Adam and Don — they don't go into any materials shared with MM leadership.
- **Deliverables tiered.** Core vs. expected vs. stretch, so we're honest about what's guaranteed.
- **Voice tightened throughout.** Less consulting-speak, more engineer-who-gives-a-damn.

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
9. [Pre-Work — Now through April 11](#9-pre-work--now-through-april-11)
10. [Onsite Diagnostic Sprint — April 13–15](#10-onsite-diagnostic-sprint--april-1315)
11. [Interview Framework](#11-interview-framework)
12. [Artifacts to Build During Onsite](#12-artifacts-to-build-during-onsite)
13. [Analysis, Synthesis & Deliverables — April 16–25](#13-analysis-synthesis--deliverables--april-1625)
14. [AI-Augmented Execution Model](#14-ai-augmented-execution-model)
15. [Compensation & Engagement Structure](#15-compensation--engagement-structure)
16. [Handling the Bruce / Investor Context](#16-handling-the-bruce--investor-context)
17. [Defining Success](#17-defining-success)

---

## EXECUTIVE SUMMARY

Mad Mobile ($75M revenue, ~370 people, $70M funded) has real assets — Sysco, Visa, Best Buy, and Apple partnerships across 21,000+ deployed locations — but it's struggling to execute. Engineering is split between firefighting a legacy POS (CAKE, acquired from Sysco in 2020) and building an AI platform (Neo) that's been marketed hard but may not be production-ready. Don has two years of financial and operational visibility as Co-CEO and Acting CFO. What's missing is the technology translation layer — turning opaque engineering realities into decisions Don can act on. That's what I do.

**The engagement:** A ~60-hour compressed diagnostic sprint across three weeks.

| Phase | Timeline | What Happens |
|---|---|---|
| Pre-Work | Now → April 11 | AI-driven system scanning, engineering health surveys (DORA, Westrum, DevEx), pre-read analysis, alignment sessions with Don |
| Onsite | April 13–15 (Mon–Wed) | 3-day sprint in Tampa: 15+ interviews, architecture walkthroughs, value stream mapping, decision-rights mapping, real case tracing |
| Deliverables | April 16–25 | CEO operating brief, friction register, hypothesis scorecard, 30/60/90-day plan, board-ready presentation, baseline survey package |

**Five questions this answers:** (1) How does Mad Mobile actually build and ship? (2) Where does execution break down — with evidence? (3) Which problems are structural vs. process vs. technical debt? (4) What should Don engage in during his first 30/60/90 days? (5) What should be left alone?

**Nine hypotheses to test** — named execution-failure patterns scored with evidence onsite. Details in [Section 7](#7-hypothesis-library-patterns-to-prove-or-disprove).

**The deliverable:** A CEO Operating Brief that serves as the technology chapter of Don's transition playbook — plus a board-ready presentation Don can take directly to Morgan Stanley. Credibility comes from the methodology (DORA benchmarks, Watkins STARS, PE DD pillar scoring), not opinion.

**Tone:** Not a witch hunt. Systems-focused, anonymous interviews, collaborative. **Compensation:** $10K fixed fee, fully deferred. **Effort:** ~60 hours across 3 weeks.

---

## 1. Engagement Charter

> *This is a working document for Adam and Don. Once we're aligned on scope and approach, we'll produce a cleaner version for internal distribution.*

**Purpose:** Give Don an executable map of Mad Mobile's technology operating system — where execution breaks down, why, and what to fix first. Equally important: produce an independent, empirically grounded technology assessment Don can present to the board and investors. Credibility through third-party analysis backed by named frameworks, not internal narratives.

**Scope:** Product decision-making, engineering org and delivery, architecture and platform strategy, cross-functional workflows, operating cadence, business-technology alignment, AI strategy (aspiration vs. reality), vendor and tooling effectiveness, and major systemic blockers.

**Non-goals:** Individual performance reviews, staffing recommendations, exhaustive code-level audits, forensic blame analysis, or retrospectives on outgoing leadership decisions.

**Outputs:** CEO operating brief, execution system map, friction register, 30/60/90-day plan (with an explicit "leave alone" list), board-ready presentation, baseline survey package (repeatable at 30/60 days), vendor/tool utilization assessment.

**Timeline:** 3 weeks. Pre-work: now through April 11. Onsite: April 13–15. Deliverables: April 16–25.

**Effort:** ~60 hours total. Pre-work: ~20 hrs. Onsite: ~25 hrs + ~3 hrs evening synthesis. Deliverables: ~15 hrs.

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

The reason this delivers outsized value in three weeks is the specific combination of Don's operational depth and my technical translation skills.

### 3.1 Don's Operating Context

Don has two years of direct visibility into Mad Mobile's financial performance, capital structure, lender relationships, M&A activity, and board dynamics. He's not arriving cold. His career at New York Life — CSO at NYL Investments, Head of Retirement Plan Services, SVP of NYL Direct — means he understands massive institutional systems with zero-downtime requirements and high-volume transaction processing. Directly transferable to what Mad Mobile does. The gap isn't operational instinct; it's the translation from financial services infrastructure language into modern software engineering language. That's my job.

### 3.2 What I Bring

My career sits at the exact intersection Mad Mobile needs diagnosed: where business strategy, technology architecture, and execution workflows either align or break.

- **Enterprise software & compliance:** Smarsh, IBM, Microsoft — regulated, high-stakes environments where reliability and audit trails are non-negotiable.
- **Ecommerce & platform engineering:** Led full platform migration at CPAP.com (Magento → Shopify, including an AI-driven prescription validation system on AWS). Currently Director of Engineering at Legacybox running multi-brand ops with subscription billing and native mobile.
- **Systems translation:** Career-long pattern of bridging business and engineering. Described by colleagues as someone who "combines strong technical knowledge with uncanny understanding of enterprise business."
- **AI strategy (practical, not theoretical):** Hands-on production AI — prescription processing at CPAP.com, AI-augmented dev workflows at Legacybox. I know what AI actually delivers today vs. what's marketing.
- **Payments infrastructure:** Comprehensive payments migrations across Braintree, Shopify Payments, Recharge, Chargebee, Stripe. Directly relevant to Mad Mobile's Visa/Cybersource play.

### 3.3 The Translation Gap

Without a technical translation layer, a CEO in a complex software environment is vulnerable to defensive engineering leaders obscuring failures behind jargon. My role: convert opaque engineering realities into decisions Don can act on — and convert business frustrations into specific technical interventions. The combination of Don's institutional operations instincts and my software engineering depth is what makes three weeks credible.

---

## 4. Engagement Philosophy & Tone

### 4.1 Core Principles

1. **Collaborative, not adversarial.** I'm positioned as Don's colleague with deep experience translating between business and technology — not an outside auditor.
2. **Systems-focused, not blame-focused.** Every finding is framed as: "where does the system make it easy or hard for talented people to succeed?"
3. **Translating between worlds.** Findings will make sense to investor/board audiences and engineering teams alike.
4. **AI-augmented and practical.** The review itself uses AI tools for system analysis, note-taking, documentation synthesis, and pattern identification — demonstrating the practical AI integration I'll also be evaluating within Mad Mobile.
5. **Preserving what works.** Mad Mobile has strong partnerships, real revenue, 21,000+ deployed locations, and talented people. These are assets to build on, not tear down.

### 4.2 Internal Messaging

When Don is ready to announce this internally:

> *"Adam is helping me accelerate my understanding of how our business, product, engineering, and delivery systems work in practice. He has deep experience translating between business and technology and identifying ways to improve execution. This is not a personnel review. It's an effort to help us remove friction, clarify priorities, and support the team. The more open and candid you are with him, the more useful this will be for all of us."*

### 4.3 Confidentiality Framework

- **Attributable:** Systemic patterns and structural findings are reported with evidence.
- **Anonymous:** Individual comments get synthesized into themes — never attributed by name.
- **The promise I make to every interviewee:** "I won't play telephone with personal comments. Only patterns and blockers get reported."
- **Don's choice:** Synthesized findings with the option to request more context on specific areas.

### 4.4 What Interviewees Should Expect

This can be forwarded to people before their sessions:

> *"Your session will be 30–60 minutes, one-on-one with Adam. It's conversational — not a quiz and not a performance review. He'll ask about how work flows through your team, where things get stuck, and what you'd change if you could. Everything you say stays anonymous — only patterns get reported, never individual comments. The more honest you are, the more useful this is for everyone."*

---

## 5. Company Context & Pre-Engagement Intelligence

### 5.1 Business Overview

Mad Mobile is a Tampa, FL-based technology company founded in 2010 by Bruce Bennett, Greg Schmitzer, and Colin Maxey. Connected commerce solutions for restaurant and retail. ~370 employees, Tampa HQ with Sri Lanka engineering, ~$75M estimated revenue. $70M total funding, most recently $50M (secured note, not equity) in June 2024 from Morgan Stanley Expansion Capital and Bridge Bank (Western Alliance). Bruce Bennett was recognized by Goldman Sachs as one of the 100 Most Intriguing Entrepreneurs (2021). The CEO transition reflects the shift from founder-led growth to the metrics-driven execution institutional capital demands.

### 5.2 Product Portfolio & Platform Architecture

Three platform tiers with fundamentally different architectures, customers, and operational demands:

| Platform | Architecture | Features | Market |
|---|---|---|---|
| CAKE POS | Legacy monolithic, tightly coupled in-house payment gateway | Transactions, inventory, Sysco ordering, waitlists, core restaurant ops | QSR, full-service, bars, cafes |
| Concierge AI (formerly Mad.x) | Cloud-based APIs, iOS/Android native + cross-platform | Associate mobility, endless aisle, fulfillment, clienteling, appointments | Enterprise retail (Ralph Lauren, MAC, Urban Outfitters) |
| Neo AI Platform | Composable LLM architecture (OpenAI, Anthropic, AWS Titan), visual orchestration | Predictive ordering, auto-segmentation, conversational analytics, agentic workflows | Advanced enterprise retail/dining |

Engineering is simultaneously building AI-native platforms AND firefighting legacy POS outages. That split is a primary candidate for the execution breakdown.

### 5.3 The CAKE Acquisition: Legacy and Technical Debt

Acquired from Sysco in 2020. Brought ~4,500+ restaurant locations (pending confirmation) but also severe technical debt:

- **Bundled payment processing:** Long-term contracts, mandatory in-house payment processing. Lucrative but creates single points of failure.
- **System-wide outages:** When the payment processor goes down, everything fails. Restaurants resorting to writing orders on whiteboards during peak service.
- **Support degradation:** Response times reportedly went from a promised 12-second answer to unreturned voicemails during critical outages.
- **Hardware dependency:** Hardware-dependent POS integrated into a mobile-first software org — architectural mismatch at the core.

### 5.4 Technology Stack (Known)

- **Mobile:** Swift, Objective-C (iOS), Kotlin, Java (Android), React Native, Flutter (cross-platform) — multiple parallel frameworks.
- **Backend:** Node.js and Java on AWS.
- **Enterprise integrations:** Salesforce, Oracle, SAP, Shopify, Magento.
- **AI layer:** Pluggable LLM integrations (OpenAI, Anthropic, AWS Titan), visual orchestration, prompt templates, "Agentic Identities" with MFA.
- **POS hardware:** CAKE-specific restaurant-grade terminals.

#### 5.4.1 CAKE Ecosystem Detail

*Source: Restaurant Update, March 2026 (internal deck).*

The CAKE product line is far more complex than "legacy monolithic POS" suggests. The live system footprint includes: POS V3 (Pondus), POS V4 (Elio), Kiosk v1, OLO v1, KDS v1, Gift Cards v1, Guest Manager, Kiosk v2, Loyalty v1, OrderPad, CAKEpop, Email Marketing, Restaurant Admin 1.0, and Customer Display. **15+ live systems** maintained by ~10 engineers and ~7 QE staff under Randy Brown.

Simultaneously in active development: CAKE Online Ordering UI Refresh, EMS 2.0 Multi Location, Gift Cards (Factor 4), CAKEpop (roadmap features), KDS v2, and VP 3350 (new payment device). Planned: OLO v2, Loyalty v2, Restaurant Admin 2.0.

Third-party integrations in production: Checkmate, 7Shifts, OLO.com, LRS, Paytronix, Bloop, DoorDash, NOLO, Orca, Davo, Parafin, Dolce, QSR KDS.

That surface area vs. team size ratio is a primary investigation target for Hypotheses A (Portfolio Sprawl), F (Legacy Gravity), and I (Architectural Polarity).

#### 5.4.2 AI Usage (Current State)

*Source: Restaurant Update "How we use AI" slide, March 2026.*

Mad Mobile is already using AI tools operationally — this isn't theoretical:

- **Design:** AI tooling to tweak application design code directly in app projects. Figma for design assets.
- **Product:** AI tooling to produce planning assets — user stories, acceptance criteria, Jira tickets.
- **Engineering:** Heavy use of **Cursor** for daily development. AI-generated application shells and reusable components from design assets.
- **QE:** AI-generated automated test cases from acceptance criteria.
- **Support:** AI-produced documentation via **Guru**. AI-driven proactive and reactive **RCA on production POS logs** (in progress).

The AI strategy assessment should distinguish between Neo (customer-facing AI platform — aspiration vs. reality) and internal AI adoption for engineering productivity (already happening and worth understanding/amplifying).

#### 5.4.3 Requirements & Prioritization Process (Documented)

The restaurant team has a documented two-stage process:

1. **Ideation & Research** (PM + Designer): Customer validation → prototype → designs → high-level requirements.
2. **Tech Refinement** (adds Architect + Eng/QE Lead): Engineering and test designs → feature discussions → architecture → final ACs, approved architecture, reviewed designs → handed to engineering.

Architecture must be **ARB (Architecture Review Board) approved** before engineering begins — a governance mechanism worth validating onsite.

Prioritization uses a **multi-department scoring model**: each feature scored by Product, Sales, CSM, Onboarding, and Support, then ranked by overall score. Executive alignment narrows to the top 5 initiatives. A **GTM tracker** (run by PMO — Mark Guilarte) coordinates releases on a 4-week cadence.

The onsite should validate whether this process is actually followed or gets overridden by sales promises and executive directives (Hypothesis B: Sales-Led Chaos).

### 5.5 Organizational Structure

*Source: Official org chart provided by Don, March 2026.*

#### L1 — Executive Leadership (Report to Bruce Bennett, CEO & Co-Founder)

| Name | Title | Assessment Focus |
|---|---|---|
| Don Salama | Co-CEO & Acting CFO | Strategic oversight, M&A, lender relationships, financial reporting. 1099 via Turn 3 Ventures (not W-2). |
| Greg Schmitzer | President & Co-Founder | Has one direct report (Karen Licker, Sr. Director Marketing). What is his day-to-day operational role? |
| Bill Lodes | Chief Revenue Officer | Owns sales, partner enablement, customer success, customer onboarding, program management, and tech support. Large org (~50+ people). |
| Steven Seigel | Chief Operating Officer | Owns payments strategy, data strategy & analytics, revenue ops. Small org (~5 people). |
| David Strainick | Chief People Officer | Owns HR/People & Culture, Sri Lanka country operations, IT, technical training. |
| Jack Kennedy | Chief Technology Officer | Owns software engineering, product management, enterprise technology, product design. **`[PRIVATE]`** Per Don: CTO in title — Chathura runs most of tech operationally. |

#### L2 — Key Reports Under CTO (Jack Kennedy)

| Name | Title | Notes |
|---|---|---|
| **Chathura Ratnayake** | SVP Global Software Engineering | **Primary engineering leader.** **`[PRIVATE]`** Per Don, basically runs most of tech even though much of it doesn't formally report to him. Key engagement contact. Direct reports: Akshay Bhasin (QE lead), Randy Brown (VP Engineering, Restaurant), Matthew Crumley. |
| **Randy Brown** | VP Engineering, Restaurant | Runs the entire restaurant/CAKE engineering team: front end (CAKEpop/Kiosk v2, Fixed POS, KDS v2/Cloud/Loyalty) and backend (Cloud/EMS). ~10 engineers. Reports to Chathura. **Key interview target — owns the product line where CAKE outages originate.** |
| Akshay Bhasin | QE Lead | Owns Restaurant QE team (~7 engineers). Reports to Chathura. |
| Zubair Syed | VP Software Engineering | Direct reports: Daniel Lomsak, Matias Riglos, James Oliver, Anthony Goad, Ana Chambers, Nagaswaroopa Kaukuri. |
| Dulanjan Wengappuliarachchi | Sr. Director, Product & GTM | Scope broader than title suggests: owns Product Management, Product Design, Product Marketing (open headcount), and L&D/Training. Reports: Mirunaaliny Somasunthara Iyer, Thaddeus Fox, Richard Farber, Jake L. (Restaurant PM), Shavin P. (Ops Eng PM). **Open roles: Payments PM (TBD), Product Marketing Manager (TBD).** |
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
| Mark Guilarte | PMO | Bill Lodes | Runs GTM tracker and release coordination. |
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

1. **No dedicated product executive.** Product management and product design both report to the CTO. No separate product leader at the exec level. Does the CTO make product decisions, or does PM operate with autonomy?
2. **`[PRIVATE]`** **Formal vs. informal authority in engineering.** The CTO holds the title, but Chathura Ratnayake drives operational execution. This divergence directly impacts decision-making speed, accountability, and team clarity — primary investigation target.
3. **Sri Lanka country head reports to CPO, not CTO.** Engineering resources in Sri Lanka may have dotted-line relationships to Chathura/Zubair, but the formal reporting runs through People/HR. Unusual structure worth understanding.
4. **IT reports to CPO.** Internal IT infrastructure is organizationally separated from product engineering.
5. **Tech support reports to CRO, not engineering.** 15+ people in tech support report through the revenue org. Customer-facing technical support and engineering are organizationally separated.
6. **President has minimal direct org.** Greg Schmitzer has exactly one direct report. Small org for a President title.
7. **COO org is very lean.** Steven Seigel's ~5 people cover payments strategy, data/analytics, and revenue ops — significantly smaller than the CRO org.
8. **Restaurant engineering team is small relative to system surface area.** Randy Brown's ~10 engineers + ~7 QE maintain 15+ live systems while simultaneously developing 6+ new products. This ratio is a primary candidate for execution friction.
9. **Product org is broader than it appears.** Dulanjan owns PM, Product Design, Product Marketing, AND L&D/Training — four functions. Two roles are open (Payments PM, Product Marketing Manager). A lot of scope for one Sr. Director.
10. **A documented prioritization process exists.** Multi-department scoring, executive alignment on top 5, PMO-run release cadence. Whether this actually gets followed or routinely overridden is a critical onsite question.

### 5.6 Known Challenges (Pre-Engagement Signal)

Glassdoor: 2.4/5, 31% recommend, 32% positive outlook. Combined with customer reviews and conversations:

- **Execution velocity:** Multiple people describe "trouble executing."
- **AI gap:** Heavy marketing around Neo/agentic commerce; flagship AI products reportedly not production-ready.
- **Architectural polarity:** AI-native building AND legacy POS firefighting simultaneously.
- **`[PRIVATE]`** **Formal vs. informal authority:** CTO holds the title; SVP Global Software Engineering drives operational execution.
- **Offshore coordination:** Sri Lanka engineering with timezone challenges, reporting through People rather than Engineering.
- **Priority whiplash:** Constantly shifting priorities mid-sprint.
- **CAKE reliability:** System-wide payment outages, degraded support, customer churn.
- **Culture erosion:** Layoffs, shifting bonuses, forced RTO, Houston shutdown. "Toxic culture," "broken promises."
- **Sales-driven distortion:** Sales promises overriding product logic. Unreachable quotas.
- **Investor & leadership dynamics:** Communication gaps with the board — the catalyst for this transition.

---

## 6. Diagnostic Framework: The Six Systems

Six interconnected systems. Problems in any one cascade into the others.

| System | Core Question | What I'm Looking For |
|---|---|---|
| **1. Business Direction** | What matters most? What gets funded? | Portfolio clarity, resource allocation, strategic coherence |
| **2. Product Decision** | Who owns prioritization? How often do sales/board override product? | Roadmap governance, power dynamics, requirement stability |
| **3. Delivery** | How does work move from idea to shipped value? | Cycle time, deploy frequency, WIP, sprint completion |
| **4. Technical** | Where is coupling high? Where is legacy strangling velocity? | Architecture, tech debt ratio, incidents, deploy complexity |
| **5. Operating Cadence** | What meetings/metrics govern execution? | Meeting structure, dashboards, escalation paths |
| **6. Accountability** | Are teams rewarded for shipping, rescuing, pleasing execs, or avoiding blame? | Comp structures, recognition, promotion criteria |

### 6.1 Stabilize, Optimize, Monetize

**Stabilize:** Make sure core systems are reliable, secure, and governed. Map CI/CD, find single points of failure (especially CAKE payments), fix the support triage.

**Optimize:** Clean up architecture and ops. Rationalize mobile frameworks, clarify reporting relationships and decision rights, establish clear authority boundaries. Assess vendor/tool effectiveness — are the tools being used? Are any redundant or wasting money?

**Monetize:** Validate that AI capabilities are generating revenue, not just compute costs. Is Neo a product or a demo?

### 6.2 Methodological Foundation

Every part of this assessment uses named, proven frameworks. This isn't ad-hoc judgment — it's structured, repeatable, and credible with board-level audiences. Organized by when they get applied:

**Pre-Work (Surveys & Automated Analysis)**

| Framework | What It Does |
|---|---|
| DORA Metrics (Forsgren/Humble/Kim) | Quantitative delivery benchmarks — deploy frequency, lead time, change failure rate, recovery time |
| Westrum Culture Model (DORA/BMJ) | Organizational culture type — pathological, bureaucratic, or generative |
| DevEx/DX Core 4 (Noda et al.) | Developer experience across feedback loops, cognitive load, and flow state |
| Pragmatic Engineer Test (Orosz) | 12 yes/no engineering culture maturity checks |

**Onsite (Interviews & Workshops)**

| Framework | What It Does |
|---|---|
| McKinsey 7S / Nadler-Tushman Congruence | Holistic org diagnostic — especially informal vs. formal org misalignment |
| Bain RAPID (Rogers/Blenko, HBR 2006) | Map who recommends, decides, approves for critical recurring decisions |
| Value Stream Mapping (Rother/Shook) | Visual flow analysis — where work stalls, where handoffs break |
| Theory of Constraints (Goldratt) | Find the single biggest bottleneck |
| Team Topologies (Skelton/Pais) | Classify team types and interaction modes; assess cognitive load |
| Wardley Mapping (Wardley) / Three Horizons (McKinsey) | Component evolution, innovation portfolio balance, build-vs-buy alignment |

**Deliverables (Organizing Structure)**

| Framework | What It Does |
|---|---|
| PE Tech DD 9-Pillar (Crosslake/West Monroe/EY-Parthenon) | Board-ready pillar structure with maturity scores |
| Watkins STARS (HBR First 90 Days) | CEO transition situation diagnosis — Start-up, Turnaround, Accelerated Growth, Realignment, or Sustaining Success |
| C4 Model (Brown) | Hierarchical architecture documentation (Context and Container levels) |
| Fowler's Technical Debt Quadrant | Debt classification — deliberate vs. inadvertent, prudent vs. reckless |
| Flow Framework (Kersten) | Work type distribution — features vs. defects vs. risks vs. debt |

---

## 7. Hypothesis Library: Patterns to Prove or Disprove

Nine named hypotheses to validate or rule out onsite. These convert time from open-ended exploration into targeted investigation.

| # | Pattern | What I'm Testing | How |
|---|---|---|---|
| A | **Portfolio Sprawl** | Too many products, no shared platform discipline | Count active codebases. Teams on >1 product? Shared services vs. duplication? |
| B | **Sales-Led Chaos** | Revenue promises create roadmap churn and tech debt | Ask sales what they promise. Ask eng what surprises them mid-sprint. Ask product who overrides. |
| C | **Fake Platforming** | Leadership talks "platform"; teams maintain customer-specific patchwork | Show me the shared platform layer. What does Neo actually consist of in production? |
| D | **Unclear Ownership** | Formal authority and operational authority are misaligned | Map who actually decides on architecture, staffing, priorities. **`[PRIVATE]`** Trace the Kennedy/Chathura dynamic. |
| E | **Dependency Drag** | A few people/teams are routing bottlenecks | Whose approval do you need? Who do you wait on? Map the dependency graph. |
| F | **Legacy Gravity** | CAKE architecture prevents speed; no triage of must-modernize vs. can-encapsulate | What constraint costs the most velocity? Ratio of maintenance vs. new feature hours? |
| G | **Missing Cadence** | No consistent execution inspection; leadership discovers reality through fire drills | What's the weekly rhythm? What metrics are reviewed? How does bad news travel? |
| H | **Biz-Tech Mistranslation** | Business says "eng is slow"; eng says "business is chaotic"; real issue is undefined tradeoffs | Ask both sides why delivery is slow. Compare answers. Look for structural decision gaps. |
| I | **Architectural Polarity** | Simultaneous AI-native building + legacy POS maintenance = irreconcilable eng split | How are teams allocated? Do engineers rotate or get stuck? Is there a migration path? |

---

## 8. Three-Week Execution Plan

### 8.1 Timeline Overview

| Phase | Timeline | Focus | Effort |
|---|---|---|---|
| Pre-Work | Now → April 11 | CEO alignment, hypothesis building, pre-read analysis, system reconnaissance, interview scheduling, internal messaging | ~20 hrs (15 async + 5 meetings) |
| Onsite | April 13–15 (Mon–Wed) | Diagnostic sprint: 15+ interviews, artifact review, system walkthroughs, value-stream tracing, real case tracing | ~28 hrs (25 onsite + 3 evening synthesis) |
| Deliverables | April 16–25 | Pattern validation, synthesis, friction register, CEO operating brief, 30/60/90 plan, board deck | ~15 hrs |

**Total: ~63 hours.** AI handles the volume work — scanning repos, ingesting docs, transcribing interviews, spotting patterns. That frees my time for the stuff machines can't do: reading the room, asking the follow-up question nobody expected, and connecting what engineering says to what the business needs.

### 8.2 Concrete Pre-Work Timeline

| Date | Milestone |
|---|---|
| March 24–28 | Don briefs Chathura and Kennedy; shares coordination brief + NotebookLM materials |
| March 28–April 1 | System access requests initiated; pre-read collection begins |
| April 1–3 | Don sends survey introduction message to engineering |
| April 3–4 | Surveys go live |
| April 4–7 | I begin system reconnaissance as access comes online |
| April 7 | Pre-read package target from MM side |
| April 7–9 | Adam-Don Session 2 (Political Landscape) and Session 3 (Pre-Onsite Briefing) |
| April 10 | Survey reminder; surveys close April 11 |
| April 11–12 | Final prep: survey analysis, hypothesis scorecard update, interview schedule confirmed |
| April 13–15 | **Onsite diagnostic sprint** |
| April 16–25 | Deliverables |

### 8.3 Scope Discipline & Triage Protocol

Scope creep is the biggest risk to this engagement. Nine hypotheses, six systems, 15+ interviews, vendor/tool assessment, value stream mapping, and RAPID decision mapping — in three days. Here's how I keep it honest:

**Time-boxing rule.** Every onsite interview has a hard stop. Buffer time between sessions is for synthesis, not overflow. If a conversation is productive, I note what to follow up on async — I don't let it eat the next slot.

**Interview priority tiers.** If the schedule slips or someone is unavailable:

| Tier | People | Rationale |
|---|---|---|
| **Tier 1 — Must happen onsite** | Chathura, Kennedy, Randy Brown, Dulanjan, Zubair, Bill Lodes, Steven Seigel, 2–3 senior ICs | Core hypothesis owners. Face-to-face is irreplaceable for reading dynamics. |
| **Tier 2 — Can go async/video** | Greg Schmitzer, Chris Gomersall, David Strainick, Rajik Gunatilaka (already video), Joel Maldonado/Michael Lee | Important but information can be gathered remotely. |

**Hypothesis convergence.** By end of Day 1, I narrow from 9 hypotheses to 4–5 with the strongest signal. Days 2 and 3 focus investigation on those. The rest get scored as "Insufficient Evidence" or "Not Present" — I don't force-validate everything.

**Daily scope check.** Every morning sync with Don includes two questions: "What are we trying to prove today?" and "What are we explicitly NOT chasing?"

**What I will NOT try to do onsite:**
- Exhaustive code review
- Contract-level vendor/pricing analysis
- Detailed architecture documentation (C4 Level 3+)
- Historical blame analysis
- Individual performance assessment

---

## 9. Pre-Work — Now through April 11

Every hour invested here multiplies the value of onsite face time. By the time I walk into the first interview, I already have the numbers.

### 9.1 AI-Augmented System Reconnaissance (~6 hrs async)

With access credentials arranged through Don and Chathura, I'll run automated analysis across Mad Mobile's development and infrastructure systems — including but not limited to source control, project management, cloud infrastructure, monitoring, and documentation platforms. Specific tooling inventory to be confirmed during coordination with Chathura.

- **Source Control (GitHub or equivalent):** Repo inventory, commit frequency, PR review cycle times, branch strategy, testing coverage, CI/CD pipeline config. Identify dead repos vs. high-churn repos.
- **Cloud Infrastructure (AWS or equivalent):** Service inventory, resource utilization, cost allocation by product, deployment architecture, monitoring/alerting config, disaster recovery posture, single points of failure.
- **Project Management (Jira or equivalent):** Sprint velocity over 6–12 months, ticket lifecycle analysis, bug vs. feature ratio, epic completion rates, backlog health, cross-team dependencies, mid-sprint scope changes.
- **Documentation / Wiki:** Coverage audit — what's documented vs. tribal knowledge. Architecture diagram currency. Runbook inventory. Post-mortem history.
- **Vendor & Tool Utilization:** Inventory all engineering and ops tools. Identify what's paid for but unused, underutilized, or redundant. This is about effectiveness, not contract pricing — I'm looking at whether the tooling supports or hinders execution.

This turns every interview from "tell me about your process" into "I can see your average PR review time is X and deployment frequency is Y — walk me through why."

### 9.2 Deployable Assessments (~3 hrs async)

Four lightweight assessments deployed to engineering leads and ICs before the onsite. Under 15 minutes per person. Nobody wants to do surveys, so these are short by design.

A positioning note: many people at Mad Mobile have felt their voices were unheard. These surveys aren't just data collection — they're a concrete signal that new leadership is listening. When introduced with the right framing from Don, the act of asking is as valuable as the answers.

These are also designed to be **repeatable** — Mad Mobile can re-run them at 30 and 60 days without my involvement to track whether changes are working.

- **DORA Quick Check** (dora.dev/quickcheck): Self-assessed delivery performance per team. Classified as Elite/High/Medium/Low against Google's research benchmarks.
- **Westrum Culture Survey** (7 questions, Likert scale): Organizational culture type — pathological, bureaucratic, or generative. 2 minutes per person.
- **DevEx Survey** (DX Core 4, ~18 items): Developer experience across feedback loops, cognitive load, and flow state.
- **Pragmatic Engineer Test** (15 yes/no questions): Modern engineering culture maturity check. Administered to 3–5 engineering leads.

### 9.3 Pre-Read Package Ingestion (~4 hrs async)

AI-assisted analysis ingests, indexes, and identifies patterns across:

- Org chart including dotted lines (updated version pending from Don's HR)
- Product portfolio and revenue mix by offering
- Roadmaps for each product line *(Restaurant roadmap received — need Concierge/Retail and Neo/AI)*
- Company goals, board goals, CEO goals
- Engineering org structure and team assignments
- Deployment environments, release cadence, CI/CD docs
- Architecture diagrams (even if outdated)
- Top customer escalations from the last 6–12 months (especially CAKE outages)
- Sprint velocity metrics
- Incident reviews, post-mortems, retrospectives
- Core systems list: repos, cloud accounts, observability, CI/CD, CRM, ticketing, support tools, docs
- Engineering and ops tool inventory
- Third-party vendor/API dependencies (OpenAI, Anthropic, AWS costs)
- CAKE acquisition integration docs and current state

### 9.4 CEO Alignment Sessions (~5 hrs meetings)

Two to three sessions with Don across pre-work. Don's two years of operational context means these go deeper faster — he's not speculating, he already knows the landscape.

#### Session 1: Success Criteria & Scope (~90 min)

- What does success look like for Don?
- Confirm scope boundaries and depth per domain
- Establish confidentiality framework and internal messaging
- Align on pre-read package and system access requests
- Draft the introduction message Don sends to leadership

| Domain | Depth | Why |
|---|---|---|
| Product management & roadmap governance | Deep | Product under CTO with no dedicated product exec — primary target |
| Engineering org & delivery pipeline | Deep | Core execution story |
| Architecture / platform / tech debt | Deep | Constrains delivery velocity; CAKE legacy burden |
| QA / release / DevOps / SRE | Medium | Part of delivery system |
| AI strategy (Neo, agentic commerce) | Medium | High investor visibility, high positioning-gap risk |
| Sales-to-delivery handoff | Medium | Common source of churn and broken promises |
| Leadership decision-rights mapping | Medium | Formal vs. informal authority; org design choices |
| Vendor & tool utilization | Medium | Effectiveness and friction, not contract reviews |
| Customer support / escalation loop | Light | Signal source; tech support under CRO not Engineering |
| Finance / investor reporting inputs | Light | Don already has deep visibility here |

#### Session 2: Political Landscape & Hypotheses (~90 min)

- Map the political landscape: who Don trusts, who the org trusts, Bruce-era commitments, investor distortions
- **`[PRIVATE]`** Kennedy/Chathura dynamic — how does it actually work? Where does it break?
- Greg Schmitzer's role going forward
- Don's hypotheses: suspected bottlenecks, sensitive zones, what he fears discovering
- Review initial system reconnaissance findings

#### Session 3: Pre-Onsite Briefing (~60 min)

- Review synthesized pre-read findings and system analysis results
- Finalize hypothesis scorecard with initial evidence
- Confirm interview schedule and priority targets
- Identify the 5 real cases to trace onsite
- Confirm logistics: NDA signed, system access active, conference room reserved

### 9.5 Interview Schedule Design (~2 hrs async)

| Person / Role | Day | Duration | Focus | Tier |
|---|---|---|---|---|
| Don Salama (Co-CEO/Acting CFO) | Daily | 30 min/day | Morning sync + EOD debrief | — |
| **Jack Kennedy (CTO)** | Mon | 90 min | Architecture, Neo, AI strategy, tech debt, decision-making authority | 1 |
| **Chathura Ratnayake (SVP Global Software Eng)** | Mon | 90 min | Day-to-day execution, team health, sprint reality, Sri Lanka coordination | 1 |
| Dulanjan Wengappuliarachchi (Sr. Dir, Product & GTM) | Mon | 60 min | Roadmap, client promises, how product decisions get made, open headcount impact | 1 |
| Steven Seigel (COO) | Mon | 45 min | Payments strategy, data/analytics, revenue ops | 1 |
| **Randy Brown (VP Engineering, Restaurant)** | Tue | 60 min | CAKE team capacity vs. system surface area, outage patterns, POS V3/V4 coexistence | 1 |
| Zubair Syed (VP Software Engineering) | Tue | 45 min | Engineering execution, team allocation, CAKE vs. Neo split | 1 |
| Bill Lodes (CRO) | Tue | 45 min | Sales pipeline, feature promises, deal blockers, tech support escalation | 1 |
| Engineering Managers / Tech Leads (2–3) | Tue | 45 min each | Sprint reality, blockers, ground-level perspective | 1 |
| Senior ICs (2–3) | Tue | 30 min each | Unfiltered ground-level perspective | 1 |
| Jeremy Diggins (Dir Enterprise Technology) | Tue | 45 min | Enterprise tech landscape, integrations | 2 |
| Rajik Gunatilaka (VP & LK Country Head) | Wed | 45 min (video) | Sri Lanka workflow, communication, quality | 2 |
| Joel Maldonado or Michael Lee (Tech Support) | Wed | 30 min | CAKE outage response, escalation loop, ticket patterns | 2 |
| David Strainick (Chief People Officer) | Wed | 30 min | HR perspective, Sri Lanka management, IT, culture | 2 |
| Greg Schmitzer (President) | Wed | 30 min | Partnerships, GTM, his operating role | 2 |
| Chris Gomersall (Dir Product Design) | Wed or async | 30 min | Design process, collaboration with product/eng | 2 |

### 9.6 Pre-Select Real Cases to Trace

1. One CAKE payment processing outage — trace from detection through support, engineering, and resolution.
2. One recent customer escalation — trace from complaint through organizational response.
3. One delayed strategic initiative — understand the structural factors behind the slip.
4. One mid-sprint priority change — trace who requested it and downstream impact.
5. One cross-functional success story — understand what conditions made it work.

### 9.7 Logistics

- **NDA:** Signed before receiving proprietary documents or system access.
- **System access:** Read-only to development and infrastructure systems. See `system-access-request.md` for specifics.
- **Location:** Tampa HQ. Travel via Uber from St. Pete; Mad Mobile covers travel and meals during onsite.
- **Workspace:** Conference room reserved for private interviews and synthesis.
- **Tools:** AI-assisted note-taking, transcription, and analysis throughout. All data stays within NDA scope.
- **Slack / Teams access:** Temporary guest account for the engagement duration. Dedicated project channel for coordination; DMs for async follow-ups.

### 9.8 MM-Side Coordination Requirements

What Chathura and Kennedy need to action. See the companion **MM Coordination Brief** for the shareable version.

| Action | Owner | Deadline | Notes |
|---|---|---|---|
| Read-only system access (source control, PM tool, cloud, monitoring, docs) | Chathura / IT (Jorge Maltes) | April 1 | Longest lead time. See `system-access-request.md`. |
| Pre-read document collection (roadmaps, arch diagrams, incident reports) | Chathura / Dulanjan | April 7 | See `pre-read-package-request.md`. Raw/outdated is fine. |
| Interview calendar blocks (15+ sessions, April 13–15) | Chathura / Kennedy | April 7 | I'll send the schedule; they book the people. |
| Survey deployment or distribution assistance | Chathura | April 3 | 4 surveys, under 15 min per person. Don introduces, team distributes. |
| Conference room + workspace reserved (April 13–15) | Kennedy or admin | April 7 | Needs to support private 1:1 conversations. |
| Slack/Teams guest account for Adam | IT (Jorge Maltes) | April 1 | Dedicated channel for coordination. |
| Communicate engagement to their teams | Chathura / Kennedy | After Don's intro | Use Don's messaging from Section 4.2. |

---

## 10. Onsite Diagnostic Sprint — April 13–15

Three days. The majority of time is interviews, artifact walkthroughs, and observation — not slide decks. AI note-taking captures everything; I focus on listening, probing, and reading the room.

### 10.1 Daily Rhythm

| Time | Activity |
|---|---|
| 8:00–8:30 | Morning sync with Don — review findings, adjust plan, update hypothesis scorecard |
| 8:30–12:00 | Scheduled interviews (2–3 sessions) |
| 12:00–1:00 | Lunch with different team members each day (informal) |
| 1:00–4:00 | Interviews or system/artifact walkthroughs (2–3 sessions) |
| 4:00–5:00 | Synthesis — update friction register, hypothesis scoring |
| 5:00–5:30 | End-of-day debrief with Don |

Evening work (Mon & Tue, ~1.5 hrs): AI-assisted synthesis of interview notes, cross-referencing against system data, updating live artifacts. Processing each day's findings same-night means the next morning's conversations are informed by emerging patterns.

### 10.2 Day-by-Day Focus

**Monday — Leadership, Architecture & System Framing.**
- Architecture review with Kennedy and Chathura — whiteboard the infrastructure using C4 notation, map CAKE-to-Neo communication, where AI API calls occur in transaction flow.
- Begin Wardley Mapping workshop with tech leadership — plot components on the evolution axis to spot build-vs-buy misalignment.
- Product direction session with Dulanjan — how product decisions get made under the CTO. Explore his scope (PM, design, product marketing, L&D). Does the multi-department scoring process actually work? Does exec alignment override it?
- COO session (Steven Seigel) — payments strategy, data, revenue ops.
- McKinsey 7S lens across all leadership interviews.
- **Goal: build the first-pass map and understand the "official story."**

**Tuesday — Engineering Deep Dive, Cross-Functional Tracing & Decision Rights.**
- Bypass the C-suite. Interview engineering managers using PACE model (Planning, Alignment, Communication, Execution).
- Review DORA metrics and DevEx survey results with each lead.
- Classify teams against Team Topologies types.
- Theory of Constraints: where does work pile up? Who is the "Brent" — the single-point-of-failure person everyone depends on?
- **Randy Brown** — critical session: CAKE team capacity vs. 15+ live systems, outage root causes, POS V3/V4 coexistence.
- Zubair Syed, senior ICs, enterprise technology.
- Trace 1–2 real customer promises from sale to production using Value Stream Mapping — capture lead time, process time, wait time, %Complete-and-Accurate at each step.
- Map decision rights for the 10–15 most critical recurring decisions using RAPID.
- CRO session (Bill Lodes) — sales pipeline, feature promises, tech support escalation path.
- **Goal: find where reality deviates from the official story. Move from anecdote to pattern.**

**Wednesday — Validation, Gaps, Sri Lanka & Wrap.**
- Follow up on surprises from Monday and Tuesday.
- Sri Lanka team video call with Rajik Gunatilaka — explore the reporting-through-People structure.
- Tech support synthesis — how do issues flow from tech support (under CRO) to engineering (under CTO)?
- Greg Schmitzer — understand his operating role. David Strainick — HR, Sri Lanka, IT, culture.
- Classify technical debt using Fowler's Quadrant.
- Review Westrum culture survey results by team.
- Watkins STARS framework — diagnose which situation Don is stepping into.
- Vendor/tool utilization review — walk the engineering toolchain with Chathura or a senior engineer. Flag unused, redundant, or underused tools. Assess whether AI tooling (Cursor, AI for tests, AI for RCA) is producing measurable gains.
- Afternoon: final debrief with Don. Review hypothesis scorecard, friction register draft, STARS diagnosis. Score PE DD 9 Pillars on a preliminary maturity scale. Identify gaps to fill async.
- **Goal: validate patterns, fill gaps, transition to deliverable production.**

Lower-priority interviews (product design, enterprise tech details) can go to video in the days following the onsite if time runs short.

---

## 11. Interview Framework

Structured but conversational. AI note-taking captures everything; I focus on listening and probing.

### 11.1 Universal Opening

> *"Thanks for making time. I'm Adam — I'm helping Don get a grounded understanding of how the organization builds, decides, and delivers. I'm not here to judge individuals. I'm trying to understand where the system makes it easy or hard for talented people to succeed. Nothing you tell me will be attributed to you by name."*

### 11.2 Leadership Track

*Must-ask:*
- What are your team's top 3 outcomes this quarter?
- How does work enter your system? Where do customer commitments and technical reality diverge?
- What decisions are easy here? What decisions are weirdly hard?
- Which commitments are strategic vs. inherited from the previous era?
- If you could fix one structural issue in 90 days, what would it be?
- How do you and [other leaders] divide ownership on [specific decisions]?

*If time:*
- What board/investor pressures distort normal operations?
- What metrics do you trust? Which are missing?

### 11.3 Engineering & Technical Track

*Must-ask:*
- Walk me through a recent project you're proud of. Show me how a real piece of work moves from idea to production.
- What architectural constraint costs you the most velocity?
- What percentage of your time goes to CAKE legacy vs. Neo/new work?
- The CAKE ecosystem has 15+ live systems and 6+ in development — how does ~10 engineers manage that? What gets sacrificed?
- POS V3 (Pondus) and POS V4 (Elio) are running simultaneously — what's the migration path? Are both actively maintained?
- Does the ARB process work or does it create a bottleneck?
- When you need a decision on architecture or priorities, who do you go to? How fast does it happen?
- What tools do you use daily? Anything you're paying for that nobody uses? Any gaps?
- [With pre-work data] I can see your PR review times average X — does that match your experience?

*If time:*
- How does the Sri Lanka relationship actually work day-to-day?
- Are you maintaining both React Native and Flutter? Why?
- How effective is Cursor for your daily engineering work?

### 11.4 Product Track

- How do you decide what goes on the roadmap? Who has veto power?
- The documented prioritization process uses multi-department scoring and exec alignment on top 5 — does that actually work? How often does it get overridden?
- What percentage is proactive vs. reactive?
- How often do sales promises override product logic?
- How does reporting to the CTO work — do you have product autonomy or are engineering priorities dominant?
- You own PM, design, product marketing, and L&D — is that scope manageable? What suffers?
- Two PM roles are open (Payments, Product Marketing) — how is that impacting delivery?
- Is there a real product org or are you functioning as a request router?

### 11.5 Support, Sales & Cross-Functional Track

- What are the top 3 customer complaints right now?
- Are there features being sold that don't exist or work reliably?
- Walk me through a CAKE payment outage from the support perspective.
- When you escalate a technical issue, what's the path from tech support to engineering? How fast does it move?

### 11.6 Universal Closing

> *"Is there anything I haven't asked that you think is important for a new CEO to understand? What's the one thing you'd want Don to know about what it's like to work here?"*

---

## 12. Artifacts to Build During Onsite

Built live during the sprint. AI drafts and integrates data; I provide judgment and structure.

**Capability / Product Map + Three Horizons.** Products, customer segments, revenue contribution, platform vs. bespoke, team ownership. H1 (core revenue), H2 (emerging), H3 (seeds). Compare actual engineering spend to 70/20/10 benchmark.

**Decision-Rights Map (RAPID).** 10–15 critical recurring decisions: who Recommends, provides Input, Agrees, Decides, Performs. RAPID insists on a single Decider per decision — where that's missing, I've found a structural bottleneck.

**Value-Stream Map.** Primary delivery flows: new feature, bug fix, infrastructure change. Lead time, process time, wait time, %Complete-and-Accurate at each step. Activity ratio below 10% signals severe queue/handoff waste.

**Technology Topology Map (C4).** Level 1 (Context) and Level 2 (Container) diagrams. Major systems, integrations, dependencies, fragile components, deployment ownership. Map the CAKE-to-Neo boundary explicitly.

**Flow Distribution Analysis.** Classify recent Jira work into Features, Defects, Risks, and Debts. A company spending 70% on defects and debt with 30% on features is in a constrained pipeline.

**Friction Register.**

| Field | Description |
|---|---|
| Symptom | What people describe experiencing |
| Root Cause | Structural cause (may span multiple systems) |
| Impact | Business outcome affected and severity |
| Category | Org / Process / Technology / Business Model / Leadership |
| Confidence | High / Medium / Low based on evidence quality |
| Pattern Match | Which hypothesis (A–I) it maps to |
| Severity | Critical / High / Medium / Low |
| Next Action | Recommended intervention and owner candidate |

---

## 13. Analysis, Synthesis & Deliverables — April 16–25

AI-generated first drafts from accumulated notes, data, and artifacts. My hours go to editorial judgment, narrative framing, and quality.

### 13.1 Analysis Methodology

1. **Pattern validation:** Score each hypothesis (A–I) as Confirmed / Partially Confirmed / Not Present with evidence.
2. **Root cause analysis:** For each major finding, trace the causal chain. Distinguish symptoms from structural causes.
3. **Impact-effort mapping:** Every recommendation mapped on impact (H/M/L) and effort (quick win / medium-term / major initiative).
4. **Tech debt quantification:** Using system data, calculate legacy maintenance vs. new development ratio.
5. **Narrative framing:** A coherent story connecting business outcomes to organizational and technology changes. Not a generic consultant report.

### 13.2 Deliverables

**Core — Non-negotiable:**

| Deliverable | What It Is |
|---|---|
| **CEO Operating Brief** (2–4 pages) | What's working, what's breaking, why, biggest risks, top priorities. The main document Don uses. |
| **Friction Register** | 10–15 prioritized findings organized by PE DD 9-Pillar structure. Issue, evidence, impact, severity, pattern match, recommended action, owner candidate. |
| **Hypothesis Scorecard** | Each pattern (A–I) scored Confirmed / Partially Confirmed / Not Present with evidence summary. |
| **30/60/90-Day Plan** | Sequenced actions with an explicit "Leave Alone" list. |
| **Baseline Survey Package** | DORA, Westrum, DevEx, and Pragmatic Engineer surveys with instructions so MM can re-run at 30/60 days without me. Includes pre-engagement baseline scores. |

**Expected — Plan to deliver:**

| Deliverable | What It Is |
|---|---|
| **Board-Ready Presentation** | 20–30 slides for non-technical investor audience. PE DD pillar structure with maturity scores. Designed for Don to present directly to Morgan Stanley and the board. |
| **Execution System Map** | Visual set: org + RAPID decision rights, value stream with bottlenecks, C4 topology, Team Topologies classification, six-system health. |
| **Vendor/Tool Utilization Assessment** | Engineering toolchain summary with findings on what's used, what's wasted, what's missing. |

**Stretch — If time allows:**

| Deliverable | What It Is |
|---|---|
| Stakeholder Communication Draft | Script for Don's internal messaging. Appreciative, candid, no blame, change will be sequenced. |
| STARS Diagnostic | Watkins framework classification — may fold into the CEO Operating Brief instead of standalone. |

### 13.3 The 30/60/90-Day Plan

- **First 30 Days — Stabilize & Establish Truth:** Formally acknowledge CAKE technical debt to engineering (builds credibility). Clarify the CTO role — resolve the gap between formal authority and operational authority. Establish one company operating cadence for delivery visibility. Clarify decision rights for roadmap, customer commitments, and architecture. Halt non-revenue-essential feature churn to reallocate capacity to core POS stability. Assess whether forced RTO is driving attrition.
- **Next 60 Days — Optimize Interfaces:** Restructure sales/product/engineering interface with mandatory weekly alignment. Move from output metrics to outcome metrics ("CAKE downtime reduction," "support ticket resolution time"). Evaluate whether product management needs its own executive leader. Address the tech support → engineering escalation path (crosses CRO → CTO boundary). Launch architecture debt triage. Evaluate AI strategy ROI.
- **Next 90 Days — Strategic Alignment:** Align portfolio and resourcing to priorities. Make org/accountability adjustments based on evidence. Evaluate Sri Lanka reporting structure. Publish modernization thesis. Present realistic roadmap to board with empirical data.
- **Leave Alone (for now):** Cosmetic rebranding, reorganizing functioning teams, relitigating historical comp changes, wading into Bruce-era grievances. The CEO's attention is the scarcest resource.

---

## 14. AI-Augmented Execution Model

The compressed timeline works because AI handles the volume and I handle the judgment.

**What AI does:**
- Scans repos, infrastructure, project data, CI/CD pipelines before the first interview
- Ingests and indexes the pre-read package
- Real-time note-taking and transcription during interviews
- Cross-references what leadership says against what the system data shows
- First-draft generation of friction register, scorecard, and report sections
- Spots recurring themes, contradictions, and clusters across 15+ interviews

**What I do (irreplaceable):**
- Build trust in interviews, read body language, probe follow-ups, navigate political sensitivities
- Distinguish real problems from noise, weight findings by organizational context
- Convert technical findings into business language for Don, the board, and investors
- Craft the narrative that connects findings to action
- Maintain the collaborative, non-threatening tone throughout

---

## 15. Compensation & Engagement Structure

A fixed fee of **$10,000** for the complete engagement. Final terms pending — Adam and Don to confirm. Payment is fully deferred — Mad Mobile can pay when cash flow allows, potentially into next year. The intent is to remove financial friction entirely so we can focus on delivering value first. Mad Mobile covers travel (Uber from St. Pete) and meals during onsite.

What we need in writing before onsite: a simple SOW or engagement letter covering scope, deliverables, timeline, confidentiality/NDA (especially around Neo AI architecture, prompt templates, and POS internals), IP ownership (I retain methodology; Mad Mobile owns deliverables), and basic liability limitations.

---

## 16. Handling the Bruce / Investor Context

Important context, but it shouldn't be the center of the review. If I center personalities and investor conflict, the engagement gets politicized fast.

- Evaluate the current operating system as it exists today
- Note where external pressure or leadership misalignment shaped incentives
- Do not conduct a retrospective blame study
- Frame everything as "what is the system doing" not "who did this"

This keeps the work useful to Don and safe with all stakeholders — including Bruce and Greg if they retain equity or operational roles.

---

## 17. Defining Success

This engagement succeeds if Don can:

1. **Explain the operating model in a page** — the real one, not the org chart version
2. **Name 3–5 root causes** instead of chasing 30 symptoms
3. **Stop at least one recurring source of churn** within 30 days
4. **Present a credible technology narrative to Morgan Stanley** — backed by data and frameworks, not internal spin
5. **Know where to spend his time vs. delegate** — and what NOT to touch in the first 90 days
6. **Install a repeatable execution cadence** with real metrics that replace fire-drill management
7. **Communicate change without triggering panic** — sequenced, collaborative, evidence-based

That is CEO leverage.

*— End of Plan —*
