# Mad Mobile Engagement — Comprehensive Context & Decision Log

**Last updated:** March 24, 2026  
**Purpose:** Single reference file capturing all conversations, decisions, corrections, comments, and context across the Mad Mobile engagement planning process. Use this to iterate on the next round of updates to the [Google Doc](https://docs.google.com/document/d/1bQeR8VA6-uOQEqNw1FMCoJhX-yBP16UPNtLUal46B9s/edit).

---

## Table of Contents

1. [Engagement Overview](#1-engagement-overview)
2. [Key People & Relationships](#2-key-people--relationships)
3. [Document Version History](#3-document-version-history)
4. [Decisions Made](#4-decisions-made)
5. [Fact-Check Corrections Applied to Google Doc](#5-fact-check-corrections-applied-to-google-doc)
6. [Google Doc Comments (16 Pre-Written for Don)](#6-google-doc-comments-16-pre-written-for-don)
7. [Email to Don (Final Version)](#7-email-to-don-final-version)
8. [NotebookLM Podcast Prompt](#8-notebooklm-podcast-prompt)
9. [Open Items & Pending Don's Input](#9-open-items--pending-dons-input)
10. [Key Design Principles & Framing Decisions](#10-key-design-principles--framing-decisions)
11. [Adam's Positioning & Profile](#11-adams-positioning--profile)
12. [Frameworks & Methodology Catalog](#12-frameworks--methodology-catalog)
13. [New Information to Incorporate (Post-Don Review)](#13-new-information-to-incorporate-post-don-review)
14. [Current State of the Google Doc](#14-current-state-of-the-google-doc)

---

## 1. Engagement Overview

**What:** A ~80-hour, three-week compressed CEO ramp accelerator and technology operations diagnostic for Mad Mobile, Inc.

**Who:** Adam Lazarus (consultant/advisor) for Don Salama (Incoming/Co-CEO, Mad Mobile)

**Why:** Mad Mobile has strong assets ($75M revenue, ~370 employees, Sysco/Visa/Best Buy/Apple partnerships, 21,000+ deployed locations) but is struggling to execute. Don is stepping into a Co-CEO role from a board member position and needs a clear, honest picture of the operating reality fast. The outgoing CEO (Bruce Bennett) and investors (Morgan Stanley, Goldman Sachs) have had communication breakdowns — that's the catalyst for the transition.

**Structure:**
- **Pre-Work (Now → Onsite):** AI-augmented system reconnaissance (GitHub, AWS, Jira), engineering surveys (DORA, Westrum, DevEx, Pragmatic Engineer Test), pre-read analysis, 3 alignment sessions with Don
- **Onsite (3–5 days in Tampa, dates TBD):** 15+ interviews, architecture walkthroughs, value stream mapping, decision-rights mapping, real case tracing
- **Deliverables (Week after onsite):** CEO operating brief, execution map, friction register, hypothesis scorecard, STARS diagnostic, 30/60/90-day plan, optional board deck

**Google Doc:** https://docs.google.com/document/d/1bQeR8VA6-uOQEqNw1FMCoJhX-yBP16UPNtLUal46B9s/edit

---

## 2. Key People & Relationships

### Engagement Team
- **Adam Lazarus** — Consultant. Director of Engineering at Legacybox (full-time job; needs to coordinate time off for onsite). ~10-year friendship with Don. Systems & Software Engineering | Ecommerce | Enterprise Platforms | AI Strategy.
- **Don Salama** — Incoming/Co-CEO, Mad Mobile. Previously board member/investor. Executive background at New York Life (CSO at NYL Investments, Head of Retirement Plan Services, SVP of NYL Direct). Also chief strategist for Turner Motorsport team at IMSA races.

### Mad Mobile Leadership (as of Google Doc — needs Don's validation)
| Name | Title(s) | Notes |
|---|---|---|
| Bruce Bennett | Founder & CEO (outgoing) | Co-founded company 2010. Goldman Sachs 100 Most Intriguing Entrepreneurs 2021. |
| Greg Schmitzer | Co-Founder & President | GTM, partnerships. Role in transition unclear. |
| Jared Rodriguez | CTO | Long-term AI architecture, Neo ownership. Since July 2017. |
| Asiri Liyanage | Head of Engineering | Day-to-day execution, Sri Lanka coordination. |
| Jack Kennedy | EVP of AI / COO / EVP Platform / VP Eng | Multiple overlapping titles — major red flag. What does he actually own? |
| Heather Jordan | EVP, Product Leader | Product roadmap, client promises. |
| Ron May | Chief Innovation Officer | AI/innovation push — aligned with or competing against CTO? |
| Steven Grant → Chris Thomley → Vacant? | CFO | Steven Grant departed. Chris Thomley succeeded but may also have departed. Needs Don's confirmation. |
| Brandan Rabdau | CRO | Replaced Doug Iverson (who departed). Sales pipeline, feature promises. |
| David Strainick | CPO | Added from fact-check. Needs more context from Don. |
| Thomas Lichtwerch | EVP Global Retail Sales | Added from fact-check. Needs more context from Don. |
| Mike Jackson | COO | Added from fact-check. Overlaps with Jack Kennedy's COO title — needs clarification. |
| Don Salama | Incoming/Co-CEO | Transitioning from oversight to operations. |

### Investors
- **Morgan Stanley Expansion Capital** — $50M secured note (not equity), June 2024
- **Bridge Bank (Western Alliance)** — Part of the June 2024 funding
- **Goldman Sachs** — Bruce was recognized as one of their 100 Most Intriguing Entrepreneurs (2021). Goldman's role as an investor needs clarification from Don — the relationship may be recognition-based rather than a direct investment.

### Background Context (NOT in document)
- Adam had an ex-girlfriend who previously worked at Mad Mobile in HR and then IT project management. She no longer works there. This gave Adam informal insider perspective on challenges. **Decision: Leave entirely out of all documents.** Don already knows.
- Adam and Don are ~10-year friends, met at University of Tampa. **Decision: Keep implicit in the document — Don knows, and the doc doesn't need to explain it.**

---

## 3. Document Version History

The engagement plan went through 8+ versions across conversations:

- **v1:** Initial plan built from web research on Mad Mobile (Glassdoor, press, product info). Basic structure.
- **v2:** Incorporated Gemini deep research output — more leadership names, CAKE acquisition details, tech stack specifics.
- **v3:** Restructured around "CEO Ramp Accelerator" framing. Added Six Systems framework, Hypothesis Library (A–H initially, later A–I), Friction Register format.
- **v4:** Added named frameworks and methodologies throughout (DORA, RAPID, Value Stream Mapping, etc.). Deep research on applicable frameworks.
- **v5:** Tone shift from formal proposal to working document between collaborators. Adam's positioning rewritten as hybrid (domains first, career as evidence). Compensation simplified. "Incoming CEO" → title adjustments.
- **v6:** Added deployable assessments section (DORA Quick Check, Westrum, DevEx, Pragmatic Engineer Test). Added Slack/Teams access request. Survey positioning as "new leadership is listening."
- **v7:** Added methodological foundation table (Section 6.2), framework-specific applications woven into onsite day-by-day, deliverable sections updated with framework references.
- **v8 (current Google Doc):** Incorporated fact-check corrections (departed executives, payment terminology, product names, additional leadership). Title page and Incoming/Co-CEO updates. Pre-work timeline changed from "Week 1" to "Now → Onsite." Scope boundaries table added back into Section 9.4.

---

## 4. Decisions Made

These are explicit decisions made during our planning conversations:

### Positioning & Framing
- **Document audience:** Adam and Don only, until aligned — then broaden to other stakeholders
- **Adam's positioning:** Hybrid approach — lead with domains/capabilities, then career as supporting evidence. NOT just "Director of Engineering at Legacybox."
- **Descriptor line:** "Systems & Software Engineering | Ecommerce | Enterprise Platforms | AI Strategy"
- **Ex-girlfriend context:** Entirely excluded from all documents
- **University of Tampa / friendship duration:** Keep implicit
- **Don's title:** "Incoming/Co-CEO" throughout (Bruce still partially in the picture)
- **Document title:** "CEO Ramp Accelerator & Execution Diagnostic" — NOT a "technology audit"

### Engagement Structure
- **Pre-work is NOT a rigid "Week 1"** — it starts now and runs through whenever onsite lands. The more lead time, the better.
- **Proposed onsite dates:** Week of April 14 or April 21 (Adam unavailable April 6–10)
- **Adam needs lead time** to arrange coverage at Legacybox for the onsite week
- **Onsite duration:** 3–5 days in Tampa (flexible)
- **Total effort:** ~80 hours across 3 weeks

### Compensation
- **Diagnostic:** One-time fixed fee, friendly deferred terms. Specific amount TBD through conversation, not in document.
- **Advisory role:** Separate conversation from diagnostic. FAST agreement framework ready if both parties see value.
- **SOW/engagement letter** needed before onsite for NDA coverage, IP ownership, liability.

### Methodology
- **Use named, proven frameworks** everywhere possible — credibility with stakeholders who don't know Adam yet, and structured checklists to follow rather than improvising
- **Hypotheses are things to TEST onsite, not conclusions** — critical framing for NotebookLM podcast and all communications
- **Pre-engagement intel clearly distinguished from actual findings** — conclusions can't be drawn until after the onsite

### Communication Format
- **NotebookLM podcast** used to communicate the engagement plan to Don (he was listening during a drive to Sebring for IMSA)
- **Google Doc comments** for specific decision points Don needs to weigh in on
- **Email** sent with link to Google Doc

### Surveys & Internal Positioning
- **Surveys should run through Mad Mobile's existing internal survey infrastructure** if possible (SurveyMonkey, Google Forms, Typeform, whatever they use). Fallback: Adam spins up Google Forms.
- **Surveys are NOT just data collection** — they're a signal that new leadership is listening. People at Mad Mobile have felt unheard. The act of asking is as valuable as the answers.
- **Temporary Slack or Teams guest account** requested for engagement duration. Dedicated project channel for coordination. Passive culture observation as a bonus.

---

## 5. Fact-Check Corrections Applied to Google Doc

From a dedicated fact-checking conversation, these corrections were identified and incorporated:

### Critical Corrections (Applied)
1. **Steven Grant (CFO) — departed.** Updated in Google Doc as "Steven Grant → Chris Thomley → Vacant?" with a note that Don needs to confirm current status.
2. **Doug Iverson (CRO) — departed.** Replaced with **Brandan Rabdau** as CRO in the leadership table and interview schedule. The Wednesday CRO reference in Section 10.2 (Day-by-Day Focus) still says "Doug Iverson" — **needs to be updated to Brandan Rabdau.**
3. **CAKE restaurant count:** ~4,500 in the doc; research suggests 5,000+. Left as ~4,500 pending Don's confirmation of current number.

### Important Corrections (Applied)
4. **"Closed-loop payments"** changed to **"Bundled payment processing"** — more accurate term. "Two-year contracts" changed to "Long-term contracts" since the specific contract length is unverified.
5. **"Mad.x"** product name updated to **"Concierge AI (formerly Mad.x)"** — reflecting current branding.
6. **Jack Kennedy's titles** updated to include "EVP of AI" based on research findings.

### Additions (Applied)
7. **Additional executives added** to leadership table: David Strainick (CPO), Thomas Lichtwerch (EVP Global Retail Sales), Mike Jackson (COO).
8. **$50M funding clarified** as "secured note, not equity" — important distinction for understanding Mad Mobile's capital structure.
9. **Colin Maxey** added as third co-founder in Section 5.1.

### Still Needs Updating
- **Section 10.2, Wednesday:** CRO reference still says "Doug Iverson" — should be "Brandan Rabdau"
- **Goldman Sachs relationship:** Listed as investor but may be recognition-only (100 Most Intriguing Entrepreneurs). Don needs to clarify.

---

## 6. Google Doc Comments (16 Pre-Written for Don)

These were written in Adam's voice — short, casual, friend-to-friend. Designed to be copy-pasted as Google Doc comments on specific sections.

### Comment 1 — Target Onsite Week
**Location:** Section 8.1 — Timeline table, "Onsite" row
> Proposing week of April 14 or April 21. I'm out April 6-10. Pre-work starts now and runs through whenever we land this. Which week works better? Any board/investor conflicts to avoid?

### Comment 2 — System Access
**Location:** Section 9.1 — System Reconnaissance, "With appropriate access credentials arranged through Don"
> Most time-sensitive logistics item. I need read-only access to GitHub, AWS, and Jira before the onsite. Who on the MM side do I coordinate with to get this set up?

### Comment 3 — Survey Deployment
**Location:** Section 9.2 — Deployable Assessments, "deploy four lightweight, established assessments"
> These surveys are 2-10 min each. I think they'll land well — people who've felt unheard will notice someone's actually asking. Should we run them through whatever internal survey tool MM already has? Also — Slack or Teams? I'd love a temp guest account for the duration so I can run this through a dedicated channel instead of email.

### Comment 4 — Pre-Read Package
**Location:** Section 9.3 — Pre-Read Package, the document list
> Who's the right person to pull most of this together? Doesn't need to be polished — whatever exists is more useful than a curated package.

### Comment 5 — Internal Messaging
**Location:** Section 4.2 — Internal Messaging, the block quote
> How does this language feel? When should it go out relative to my arrival? Should it come from you alone or jointly with Greg?

### Comment 6 — Leadership Table Validation
**Location:** Section 5.5 — Leadership Structure table
> Can you validate/correct this? Assembled from public sources. Is Jack really holding three titles? Is Ron May still CIO? Anyone missing?

### Comment 7 — Political Landscape
**Location:** Section 9.4 — Session 2: Political Landscape, "Map the political landscape"
> This is the unfiltered session. Can do it entirely verbal. Key things: who will be candid vs. perform, Bruce-era commitments still shaping behavior, CTO/CIO dynamic, Greg's posture.

### Comment 8 — Real Cases to Trace
**Location:** Section 9.6 — Real Cases to Trace, the five numbered cases
> Start thinking about specific cases for me to follow — especially the CAKE outage one. Have these by Session 2 and I'll build them into the interview schedule.

### Comment 9 — Interview Schedule
**Location:** Section 9.5 — Interview Schedule table
> Priority order feel right? Anyone to add? Flag anyone who might be defensive — don't need to avoid them, just want to know going in.

### Comment 10 — Scope Depth
**Location:** Section 9.4 — Session 1, scope boundaries table
> Anything marked "Light" that should go deeper? Anything "Deep" that matters less to you?

### Comment 11 — Confidentiality Framework
**Location:** Section 4.3 — Confidentiality Framework, "Don's choice"
> My rec: synthesized only, never attributed. More context in our private debriefs if needed. Need to be aligned on this before I start interviewing — it's the promise I make to everyone.

### Comment 12 — Compensation
**Location:** Section 15.1 — Compensation, "specifics to be worked out"
> Let's discuss on a call. Main thing I need before onsite is a simple engagement letter for NDA coverage. Who handles that on your side?

### Comment 13 — Hypothesis Gut Check
**Location:** Section 7 — Hypothesis Library table
> Which of these resonate with your gut? Which would surprise you if true?

### Comment 14 — Bruce / Investor Context
**Location:** Section 16 — Bruce / Investor Context
> What does Bruce's involvement look like going forward? Anything about the investor relationship I should know?

### Comment 15 — Known Challenges Validation
**Location:** Section 5.6 — Known Challenges, the list
> Anything here wrong, overstated, or missing?

### Comment 16 — Board Deck Decision
**Location:** Executive Summary — "The Deliverable", "optional board-ready presentation"
> Do you want the board deck? If yes I'll build it into the timeline from the start.

---

## 7. Email to Don (Final Version)

**Subject:** Mad Mobile plan - ready for your eyes

> Hey Don,
>
> I put together a comprehensive plan for the Mad Mobile engagement. It covers the full scope — pre-work, onsite diagnostic, deliverables, methodology, interview targets, the works. It's a working draft for us to refine together before we share anything more broadly.
>
> https://docs.google.com/document/d/1bQeR8VA6-uOQEqNw1FMCoJhX-yBP16UPNtLUal46B9s/edit
>
> I dropped comments throughout on the specific things I need your input on — scope decisions, access logistics, political landscape questions, and a few things only you can answer about the internal dynamics. Might be good flight reading this week — no rush to respond to everything at once, but take a pass through and we can discuss.
>
> For the onsite, I'm proposing either the week of April 14 or April 21. I'm out April 6-10 and need a couple weeks to arrange coverage at Legacybox, so either of those weeks works well. Pre-work starts now and runs through whenever we land onsite — the more lead time the better, especially for getting system access and running the engineering surveys.
>
> Speaking of which — the earlier we can arrange read-only guest credentials for GitHub, AWS, and Jira, the more prepared I'll be when I arrive. That's the one logistics item with the longest lead time.
>
> When you're back from travel, let's get our first working session on the calendar — 90 minutes, just us. We'll nail down success criteria, scope, and the internal messaging before anything else moves.
>
> Looking forward to this.
>
> Adam

---

## 8. NotebookLM Podcast Prompt

The original prompt over-indexed on diagnosing Mad Mobile's problems. This revised version steers toward scope and alignment:

> **This document is a working draft engagement plan written by Adam Lazarus for Don Salama. The podcast should focus on what Adam and Don need to align on before the engagement begins — NOT on diagnosing Mad Mobile's problems. The diagnostic hasn't happened yet; the problems listed in the document are pre-engagement hypotheses to be tested, not conclusions.**
>
> **Structure the conversation around these themes:**
>
> 1. **What this engagement actually is** — an 80-hour compressed sprint to give Don an executable operating map, not a traditional consulting audit. Explain the three-week structure (pre-work, onsite, deliverables) and what each phase produces.
>
> 2. **What Don needs to decide or provide** — system access, internal messaging/positioning to the team, interview scheduling, pre-read documents, which alignment sessions to prioritize, and how much of the political landscape he's comfortable sharing.
>
> 3. **How Adam's background maps to this specific problem** — the translation layer concept, why the combination of Don's institutional ops experience and Adam's software engineering depth makes the compressed timeline credible.
>
> 4. **The methodology in plain language** — explain the named frameworks (DORA, RAPID, Value Stream Mapping, etc.) not as jargon but as specific tools that answer specific questions. Don doesn't need to memorize them; he needs to understand what each one reveals.
>
> 5. **The hypothesis-driven approach** — Adam isn't arriving with an open-ended "tell me everything." There are nine named patterns to prove or disprove. Walk through what those are and why that structure matters.
>
> 6. **Tone and confidentiality** — how this gets positioned internally so people are candid, not defensive. The anonymity framework. Why this matters for data quality.
>
> 7. **Deliverables Don will walk away with** — the CEO operating brief, friction register, 30/60/90 plan, board deck. What makes these useful vs. a typical consultant slide deck.
>
> 8. **Open questions and next steps** — compensation structure, NDA/SOW logistics, onsite dates, advisory role as a separate conversation.
>
> **Audience context:** Don and Adam are the only audience. Don will be listening during a drive from St. Pete to Sebring for an IMSA race where he's chief strategist on the Turner Motorsport team, so he won't be reading the document — this podcast needs to communicate the engagement plan clearly enough that he can come back to Adam with questions, refinements, and decisions. Keep the energy conversational and direct. Avoid speculating about what the diagnostic will find — that's the whole point of doing it.

---

## 9. Open Items & Pending Don's Input

These are the items that require Don's response before the engagement can proceed. Organized by priority:

### Time-Sensitive (Blocks Everything Else)
1. **Target onsite week** — April 14 or April 21? Any conflicts?
2. **System access logistics** — Who at MM coordinates read-only access to GitHub, AWS, Jira?
3. **SOW / engagement letter** — Who handles this on MM's side? Need NDA coverage before onsite.

### Pre-Onsite Planning
4. **Internal messaging** — Tone check on suggested language. Timing relative to onsite. From Don alone or jointly with Greg?
5. **Leadership table validation** — Correct roles, departed people, missing names?
6. **Survey infrastructure** — What internal survey tool does MM use? Slack or Teams?
7. **Pre-read package** — Who compiles documents?
8. **Interview schedule** — Priority order, additions, politically sensitive people?

### Strategic / Contextual
9. **Scope depth levels** — Any "Light" domains that should go deeper? Any "Deep" that matters less?
10. **Hypothesis gut check** — Which patterns resonate? Which would surprise?
11. **Real cases to trace** — Specific CAKE outage, delayed initiative, mid-sprint change, etc.
12. **Bruce's ongoing involvement** — Board seat? Advisory? Equity-only?
13. **Investor relationship details** — Goldman Sachs role? Morgan Stanley dynamics?
14. **Known challenges** — Anything wrong, overstated, or missing from Section 5.6?
15. **Confidentiality framework** — Confirm synthesized-not-attributed approach
16. **Board deck** — Yes or no? If yes, built into Week 3 timeline from the start.
17. **Compensation specifics** — Discuss on a call, not in writing.

---

## 10. Key Design Principles & Framing Decisions

These principles emerged across our conversations and should guide all future iterations:

### Pre-Engagement vs. Findings
- Pre-engagement hypotheses must be clearly distinguished from actual findings
- Conclusions CANNOT be drawn until after the onsite visit
- The nine hypotheses (A–I) are patterns to TEST, not diagnoses
- Communication about the engagement should never speculate about what the diagnostic will find

### Tone & Positioning
- **Collaborative, not adversarial.** Adam is "Don's friend who has deep experience translating between business and technology" — not an outside auditor.
- **Systems-focused, not blame-focused.** "Where does the system make it easy or hard for talented people to succeed?"
- **Anonymous interviews.** Individual comments synthesized into themes, never attributed by name.
- **Preserving what works.** Mad Mobile has real assets — partnerships, revenue, deployed locations, talented employees.

### Communication Format Matching
- Communication format should match the audience's context (e.g., audio podcast for Don during travel, not a document to read)
- Google Doc comments for specific decision points (actionable, answerable questions)
- Working document tone, not formal proposal tone

### Framework Usage
- Named, proven frameworks for credibility and structure
- Applied at specific phases where they add value — not all at once
- Week 1: lightweight assessments (DORA, Westrum, DevEx, Pragmatic Engineer)
- Week 2: workshop-driven frameworks (VSM, RAPID, Wardley, Team Topologies)
- Week 3: organizing frameworks (PE DD 9-Pillar, Watkins STARS)

---

## 11. Adam's Positioning & Profile

### Descriptor Line
"Systems & Software Engineering | Ecommerce | Enterprise Platforms | AI Strategy"

### Domain Experience (Lead with these)
1. **Enterprise software & compliance:** Smarsh, IBM, Microsoft — regulated, high-stakes environments
2. **Ecommerce & platform engineering:** CPAP.com (Shopify migration, AI prescription system), Legacybox (multi-brand ops, native mobile, subscription billing)
3. **SaaS, growth engineering & DTC:** Four Sigmatic, Ventract, Buoy Ventures, Trellis, Brandtale
4. **Systems translation:** "Highly technical communicator" who "combines strong technical knowledge with uncanny understanding of enterprise business"
5. **AI strategy (practical):** CPAP.com prescription processing, AI-augmented workflows at Legacybox
6. **Payments & subscription infrastructure:** Legacybox payments migrations (Braintree, Shopify Payments, Recharge, Chargebee, Stripe) — directly relevant to Mad Mobile's Visa/Cybersource play

### What NOT to include
- Don't lead with "Director of Engineering at Legacybox" — too narrow
- Don't mention the University of Tampa or friendship explicitly
- Don't mention the ex-girlfriend context at all

---

## 12. Frameworks & Methodology Catalog

Full catalog of named frameworks used in the engagement, organized by assessment domain:

| Assessment Domain | Frameworks | When Applied |
|---|---|---|
| Engineering Performance | DORA Metrics, SPACE Framework, DevEx/DX Core 4 | Pre-work surveys + onsite validation |
| Engineering Culture | Pragmatic Engineer Test, Joel Test, Westrum Culture Model | Pre-work surveys |
| Organizational Diagnostic | McKinsey 7S, Galbraith Star Model, Nadler-Tushman Congruence | Onsite leadership interviews |
| Decision Rights | Bain RAPID, DACI, RACI | Onsite Wednesday mapping |
| Delivery & Flow | Value Stream Mapping, Theory of Constraints, Flow Framework | Onsite Wednesday tracing |
| Team Design | Team Topologies | Onsite Tuesday classification |
| Technology Strategy | Wardley Mapping, Three Horizons, ThoughtWorks Tech Radar | Onsite Monday workshop |
| Technical Debt | Fowler's Quadrant, SQALE Method, Kruchten-Nord-Ozkaya | Onsite Thursday classification |
| Architecture | C4 Model, ATAM | Onsite Monday walkthroughs |
| CEO Transition | Watkins First 90 Days / STARS, Spencer Stuart New CEO Launch Pad | Week 3 deliverables |
| Due Diligence Structure | PE Tech DD 9-Pillar (Crosslake/West Monroe/EY-Parthenon) | Week 3 findings organization |

---

## 13. New Information to Incorporate (Post-Don Review)

**This section is where you capture new information from Don's review sessions. Fill this in as you get feedback.**

### From Don's Review Session(s)
- [ ] Onsite week confirmed: _____
- [ ] Leadership table corrections: _____
- [ ] CFO status confirmed: _____
- [ ] CRO confirmed as Brandan Rabdau: _____
- [ ] Mike Jackson COO vs. Jack Kennedy COO — clarified: _____
- [ ] David Strainick CPO — role/scope: _____
- [ ] Thomas Lichtwerch — role/scope: _____
- [ ] Bruce's ongoing role: _____
- [ ] Goldman Sachs relationship clarified: _____
- [ ] Greg Schmitzer's posture on transition: _____
- [ ] Internal messaging — tone adjustments: _____
- [ ] Survey infrastructure identified (Slack/Teams? Survey tool?): _____
- [ ] System access contact identified: _____
- [ ] Pre-read package owner identified: _____
- [ ] Hypothesis gut check — Don's reactions: _____
- [ ] Known challenges — corrections/additions: _____
- [ ] Real cases identified for tracing: _____
- [ ] Board deck — yes or no: _____
- [ ] Compensation discussed: _____
- [ ] Scope depth adjustments: _____
- [ ] Additional context from Don: _____

### Known Doc Issues Still to Fix
- [ ] Section 10.2, Wednesday: CRO reference still says "Doug Iverson" → should be "Brandan Rabdau"
- [ ] Verify Goldman Sachs is actually an investor vs. just recognition program
- [ ] CAKE restaurant count: ~4,500 in doc, may be 5,000+ — confirm with Don

---

## 14. Current State of the Google Doc

**URL:** https://docs.google.com/document/d/1bQeR8VA6-uOQEqNw1FMCoJhX-yBP16UPNtLUal46B9s/edit

**Last modified:** March 17, 2026

**Status:** Working draft. Fact-check corrections applied. Comments have been added for Don's review. Don has had "a few conversations" reviewing the document and Adam needs to incorporate new information from those reviews.

### Document Structure (17 sections)
1. Engagement Charter
2. The Actual Objective (5 questions)
3. Why This Works: The Translation Layer
4. Engagement Philosophy & Tone
5. Company Context & Pre-Engagement Intelligence
6. Diagnostic Framework: The Six Systems
7. Hypothesis Library (9 patterns A–I)
8. Three-Week Execution Plan
9. Week 1: Pre-Work
10. Week 2: Onsite Diagnostic Sprint
11. Interview Framework
12. Artifacts to Build During Onsite
13. Week 3: Analysis, Synthesis & Deliverables
14. AI-Augmented Execution Model
15. Compensation & Engagement Structure
16. Handling the Bruce / Investor Context
17. Defining Success

### Key Features of Current Doc
- "WORKING DRAFT" badge on title page
- "For discussion between Adam & Don" callout in Section 1
- Scope boundaries table in Session 1 (Section 9.4)
- Concierge AI (formerly Mad.x) — updated product name
- Bundled payment processing — corrected from "closed-loop"
- Expanded leadership table with fact-checked additions
- $50M described as "secured note, not equity"
- Pre-work timeline: "Now → Onsite" (not rigid "Week 1")

---

*End of context file. Update Section 13 as new information comes in from Don's review sessions.*
