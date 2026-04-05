# Translation Layer — Writing Style Guide

How Translation Layer writes across every context: internal notes, client coordination, executive deliverables, survey instruments, and generated media. The voice is constant. The tone flexes. Every word earns its place.

This file governs **how we write**. For what we say about ourselves, see [`messaging.md`](messaging.md). For how deliverables look, see [`client-deliverable-style.md`](client-deliverable-style.md).

---

## Core Voice Attributes

Four attributes define Translation Layer's voice. They apply everywhere — landing page copy, engagement plans, coordination briefs, CEO operating briefs, survey introductions, and media scripts. The attributes are non-negotiable; the intensity modulates by context.

### Authoritative

Lead with the finding, then the reasoning — not the other way around. We do not ask for permission to be right. We have done this. We know the failure modes. We lead with what matters, then show the work.

**In practice:** "Epic completion rate is 27.7%. The portfolio is overcommitted by roughly 3x." — not "After careful analysis of the Jira data, we believe there may be an opportunity to improve epic completion rates."

### Direct

Every sentence has a subject and a verb. Passive voice is a red flag — who does what? Say the hard thing clearly before the soft thing at all. If a sentence can be shorter without losing meaning, shorten it.

**In practice:** "Engineering has no branch protection on any repository." — not "It was observed that branch protection policies have not been comprehensively implemented across the repository ecosystem."

### Specific

We do not say "significant improvement." We say "40% reduction in review cycles." We do not say "leading AI platform." We say which model, what version, what benchmark. Numbers, names, dates, versions. If you can't be specific, say so — "we don't have this data yet" is more honest and more useful than a vague assertion.

**In practice:** "50 RCAs in 12 months, 60.7% pipeline success rate, 201 stale open PRs." — not "There are various areas where engineering practices could be strengthened."

### Challenged

Question the premise before accepting the brief. If the question is wrong, the answer does not matter. We say so clearly, then offer the better question. This is not contrarianism — it is the discipline of making sure we're solving the right problem.

**In practice:** "The question isn't whether to migrate to microservices. The question is which three services are actually bottlenecked by the monolith, and whether the team has the operational maturity to run them independently."

---

## The Register

**Engineer who gives a damn.**

Not a consultant performing expertise. Not an auditor scoring failures. Not a vendor pitching services. A builder who has been in the room, seen the failure modes, and knows exactly what to do about them.

The confidence comes from experience, not title. We write as a peer — someone the CTO would want to grab a beer with after the review, not someone they endure in a conference room. We speak both business and engineering languages natively. We do not translate down; we translate across.

This register holds everywhere. It's the voice of the v12 engagement plan changelog: "Less consulting-speak, more engineer-who-gives-a-damn." It's the coordination brief that says "Ship raw over polished. Partial or dated beats 'we'll send when it's perfect.'" It's the interview framework that asks "Where does the system make it easy or hard for good people to ship?"

The register is NOT:
- Academic or theoretical ("research suggests...")
- Deferential or hedge-heavy ("it might be worth considering...")
- Performatively confident ("we are uniquely positioned to...")
- Casual to the point of unprofessional ("lol this codebase")
- Jargon-dense to signal belonging ("let's leverage our synergies to...")

---

## Tone Modulation by Context

The voice is constant. The tone flexes across five contexts. Each context has a different audience, different stakes, and different expectations for formality and warmth.

### 1. Internal Working Documents

**Audience:** Adam, collaborators, future-self reference.
**Formality:** Low. **Directness:** Maximum. **Warmth:** As needed.

The most unfiltered register. Can be blunt, fragmentary, profane if the moment calls for it. Thinking out loud is acceptable. Version tracking matters. This is where hypotheses live before they're validated, where `[PRIVATE]` tags mark things that stay between principals.

> Hypothesis D is confirmed. The April 3 reorg resolved the authority misalignment — Chathura now has formal authority over all engineering, product, design, PMO, and customer support. Kennedy narrowed to AI/innovation only. Remove `[PRIVATE]` tags; this is a finding now, not a sensitive hypothesis. Siegel and Lodes are out. Add Garcia (CFO) and Shatney (VP HR) to the interview schedule.

### 2. Client Coordination

**Audience:** Client technical leadership, operations contacts, people being asked to help.
**Formality:** Medium. **Directness:** High. **Warmth:** Collaborative, peer-level.

Treat the audience as respected technical leaders being asked to help, not as subjects of investigation. Frame asks with clear deadlines and explicit ownership. Use the "what this is / what it isn't" pattern early. Action items are specific and dated.

> I care about how work moves from idea to production, where it stalls, and what would move the needle if we fixed it. Ship raw over polished. Partial or dated beats "we'll send when it's perfect." If someone asks "Is this about me?" the answer is no. It's about how the machine runs.

### 3. Executive Deliverables

**Audience:** C-suite, board members, investors, decision-makers.
**Formality:** High. **Directness:** High. **Warmth:** Measured, professional.

Evidence first, then interpretation. Framework-credentialed assertions (name the framework: DORA, Westrum, DevEx, Value Stream Mapping, RAPID). Every claim has a number or a named source. Structure enables scanning: executive summary, then depth. The reader should be able to act on the executive summary alone and dive deeper only where they choose.

> Mad Mobile's engineering organization shows a 27.7% epic completion rate across the portfolio. Priority inflation is systemic: 89.4% of open items are marked "High." The REST project alone carries 260 open epics. These are indicators of Hypothesis A (Portfolio Sprawl) — the organization is overcommitted by roughly 3x relative to its demonstrated throughput. Recommendation: declare a portfolio freeze, score every active epic against the three criteria in Section 9, and cut to a number the team can actually finish.

### 4. Survey Instruments

**Audience:** Individual contributors, engineering managers, product leads — people giving their time.
**Formality:** Medium. **Directness:** High. **Warmth:** Respectful, brief.

Respect the respondent's time above all else. State the time commitment upfront ("under 15 minutes"). Guarantee anonymity clearly and early. Questions are unambiguous. Response scales are consistent. No leading questions. No double-barreled questions. The introduction explains why their input matters without being sycophantic.

> This survey takes approximately 3 minutes. Your responses are anonymous — only aggregate patterns are reported, never individual answers. The results help establish a baseline that Mad Mobile can re-measure at 30 and 60 days to track real improvement.

### 5. Media and Generated Content

**Audience:** Mixed — leadership teams, onboarding audiences, broader stakeholders.
**Formality:** Variable by format. **Directness:** High. **Warmth:** Conversational for audio, structured for visual.

Format-specific rules override general style:

- **Slides:** Headline + bullets, never paragraphs. Max 6 bullets per slide. If a slide has more text, split it. "Not a sales deck. An operational briefing between people who are about to work together."
- **Audio/Podcast:** Conversational, direct, peer-to-peer. Target 8–12 minutes. Orientation, not exhaustive walkthrough. "Like three experienced engineers talking about how to run a good assessment." Enthusiastic but grounded — not hype, not doom.
- **Video:** "Executive briefing deck that moves." Low text density. Visual emphasis on structure and data patterns. Confident pace, not rushed.

Across all media: do NOT speculate about findings before the work is done. Do NOT mention compensation, investor dynamics, or political context. Treat every named individual as a respected partner.

---

## Emoji, Icon, and Symbol Conventions

Emojis, icons, and symbols are precision communication tools — not decoration. Use them when they are the clearest, fastest way to convey meaning. Never use them to paper over vagueness, add false warmth, or mimic casual chat tone in professional work.

### When to Use

- Status indicators in dense tables or dashboards (severity, health, progress)
- Inline category markers that help the eye group related items during fast scanning
- Navigation wayfinding in sidebar menus or tab bars
- Visual anchors in scan-heavy documents where a symbol orients faster than text

### When Not to Use

- Multiple emojis per heading or section title
- Emoji as a substitute for clear, specific language
- Decorative filler that adds visual noise without aiding comprehension
- Mimicking casual Slack/chat tone in professional deliverables
- Softening critical findings with friendly icons

### The Test

Does removing this emoji or icon make the content harder to parse? If no, remove it. Symbols earn their place the same way every other element does: by serving comprehension.

### Technical Note

Noto Emoji and Noto Sans Symbols are the canonical rendering sources for all deliverables, ensuring cross-platform visual consistency. A status indicator in a chart tooltip renders identically on macOS, Windows, Linux, and mobile.

---

## Structural Conventions

Patterns that recur across all Translation Layer writing. These are not templates — they are disciplines.

### Tables Over Paragraphs

Structured information goes in tables. Timelines, specifications, comparison data, role assignments, action items — if it has a natural row/column structure, it belongs in a table. A well-constructed table communicates in 3 seconds what a paragraph takes 30 seconds to parse.

### Numbered Questions Over Vague Scope

"This engagement answers five specific questions" is better than "This engagement will explore various aspects of technology operations." Name the questions. Number them. Make the reader able to evaluate whether they got answered.

### "What This Is / What It Isn't"

When introducing a new engagement, process, or deliverable to an audience that may have anxiety about it, use the dual framing explicitly. Name what it is (collaborative, systems-focused, anonymous). Name what it isn't (personnel review, audit, blame exercise). This pattern builds trust in the first 30 seconds.

### Explicit Tiering

When deliverables or commitments have variable certainty, tier them: Core (guaranteed), Expected (high confidence), Stretch (if time/access allows). Honest tiering builds more trust than overpromising.

### Version Tracking

Working documents carry version numbers and changelogs. "What's Changed in v12" at the top of the document tells the reader exactly what shifted and why, without rereading 20 pages. The changelog is direct: "Scope expanded. Voice tightened. Hypothesis D confirmed."

### Ship Raw Over Polished

Partial or dated material beats "we'll send when it's perfect." This applies to pre-read packages, architecture diagrams, and internal documentation. Say so explicitly when asking for materials: "Raw over polished."

### Action Items Are Accountable

Every action item has a named owner and a hard date. "System access — by April 1" not "System access — ASAP." "Coordination: IT — Jorge Maltes" not "Coordination: IT team."

---

## Framing Principles

Philosophical guardrails that govern how Translation Layer frames its work, especially in sensitive client contexts.

### Systems-Focused, Not Blame-Focused

The question is never "who failed?" The question is "where does the system make it easy or hard for good people to ship?" This is not softness — it is precision. Blaming individuals obscures the structural root cause. Structural root causes are actionable. Individual blame is not.

### Anonymous Interviews, Pattern Reporting

Interviews are one-on-one and anonymous. Only patterns get reported, never individual comments. If someone asks "Is this about me?" the answer is always no. This commitment must be stated early and honored absolutely — a single breach destroys the entire data collection model.

### Preserve What Works

Finding problems is easy. Identifying what should be left alone is harder and more valuable. Every diagnostic includes a "leave alone" list. Calling out strengths is not diplomacy — it prevents well-intentioned leaders from breaking things that aren't broken while fixing things that are.

### Framework-Credentialed Assertions

Credibility in executive deliverables comes from named, recognized frameworks — not from opinions or "years of experience." DORA benchmarks. Westrum organizational culture typology. DevEx survey methodology. Value Stream Mapping. RAPID decision-rights framework. PE due diligence pillar scoring. Name the framework. Show how the data maps to it. Let the framework carry the authority.

### Specific Over Vague, Always

"89.4% priority inflation" not "widespread priority issues." "27.7% epic completion rate" not "low completion rates." "201 stale open PRs" not "significant PR backlog." If you don't have the number yet, say "we'll measure this during the onsite" — that's more specific than a vague assertion, and more honest.

---

## Anti-Pattern Lexicon

Words and phrases that do not appear in Translation Layer's communications. If you find yourself reaching for them, stop and say what you actually mean.

### Tier 1 — Never Use

These words are banned in all contexts. They are consulting filler, corporate camouflage, or buzzwords that have been emptied of meaning through overuse.

| Word/Phrase | What to Say Instead |
|---|---|
| synergy | name the specific collaboration or integration |
| leverage (as verb) | use, apply, build on |
| disrupt | name the specific change and who it affects |
| thought leadership | say what the actual insight is |
| best-in-class | name the benchmark and how you compare |
| world-class | name the standard and the evidence |
| cutting-edge | name the technology and its maturity |
| next-generation | name the version and what's new |
| turnkey | describe what's included and what's not |
| comprehensive | name the scope explicitly |
| robust | name what was tested and how it held |
| utilize | use |
| facilitate | run, lead, organize |
| holistic | name what's included in the scope |
| seamless | describe the integration and its failure modes |
| empower | name the specific capability being enabled |
| ideate | brainstorm, or just describe what you're doing |
| learnings | lessons, findings, observations |
| bandwidth | capacity, availability, time |
| circle back | follow up on [specific topic] by [specific date] |
| solution | name the specific thing being built or delivered |
| ecosystem | name the components and how they connect |
| journey | name the process and its stages |
| deliverables | name the specific documents, artifacts, or outputs |
| stakeholders | name the people or roles |
| value add | name the specific value and for whom |
| paradigm shift | describe the specific change |
| innovative | describe what's new and why it matters |
| transformative | describe the before and after states |

### Tier 2 — Only With Qualification

These words are acceptable when paired with specific evidence. Without qualification, they are empty. With it, they're useful.

| Word | Required Qualification |
|---|---|
| scalable | say how — "scales to 10K concurrent users on 3 nodes" |
| AI-powered | say which model, which version, which capability |
| enterprise-grade | say what standard — SOC 2, 99.99% uptime SLA, etc. |
| end-to-end | specify both ends — "from Jira ticket to production deploy" |
| platform | define the boundary — what's in, what's not |
| real-time | define the latency — "under 200ms p99" |
| automated | describe what's automated and what still requires human input |
| data-driven | name the data source, the metric, and the decision it informs |

---

## Quality Tests

Three litmus tests before any external communication leaves Translation Layer.

### 1. The CTO Test

"Would the CTO of a serious company find this impressive, or would they find it embarrassing?"

Serious CTOs read source code. They inspect network tabs. They have seen every consultant's pitch deck. They know immediately when something was written to sound impressive rather than to say something true. Write for that reader.

### 2. The Action Test

"Could someone act on this without asking a follow-up question?"

Every deliverable, every recommendation, every finding should be actionable on first read. If the reader needs to schedule a meeting to clarify what you meant, the writing failed. Named owners, specific dates, concrete next steps, explicit scope.

### 3. The Attribution Test

"If I removed the company name, could this have been written by any consulting firm?"

If yes, rewrite. Translation Layer's writing should be identifiable by its precision, specificity, and directness — not by a logo in the corner. If swapping in "McKinsey" or "Deloitte" wouldn't change the reader's experience, the voice is wrong.
