# NotebookLM source: Technology operations review at Mad Mobile

## Context for NotebookLM

This document describes a technology operations review engagement at Mad Mobile, Inc. The podcast should explain the engagement to Chathura Ratnayake and John Kennedy — two senior technology leaders at Mad Mobile who will be coordinating logistics on the company side. Focus on: what this engagement is, why Don is doing it, what Adam's approach looks like, what the onsite experience will be, how interviews work, and what the deliverables are. Do **not** speculate about what the diagnostic will find — that's the whole point of doing it. Keep the tone collaborative and peer-level.

---

## What this is — and why now

I'm Adam Lazarus, and I'm working with Don Salama on something pretty straightforward in intent but deep in substance: a technology operations review that gives leadership a grounded picture of how engineering and delivery actually work — not the org-chart story, not the slide-deck story, but the real flow of decisions, work, and outcomes.

Don has been Co-CEO and Acting CFO for about two years. That means he has serious visibility into financial and operational reality. What he's building next is a similarly clear view of technology: how product decisions get made, how work moves from idea to customer, where friction shows up, and what is structurally working versus structurally strained. I'm here to help him get there faster and with evidence behind it, not just anecdotes.

My background is systems and software engineering, ecommerce, enterprise platforms, and AI strategy. I've spent most of my career where business strategy and technology execution meet — Smarsh, IBM, Microsoft, CPAP.com (where I led platform migration and an AI-driven prescription system), and Legacybox as Director of Engineering across multi-brand operations. The through-line isn't a single stack or title; it's translation. I speak both sides well enough to connect them: what the business needs to hear, and what engineering needs to protect and improve.

The engagement is roughly **sixty hours over about three weeks**. That breaks into pre-work — system analysis, surveys, document review — a **three-day onsite sprint in Tampa (April 13–15)**, and then a week of synthesis and deliverables. It's intensive by design: enough contact to see patterns, not so long that we're living in your calendar forever.

**Before anyone sits down with me in Tampa**, the pre-work week is doing real work: ingesting what you can share, running the automated passes where we have access, sending surveys so we hear from a wider slice than we could possibly interview, and reading enough context that the onsite time isn't wasted on "what repo is this in?" The onsite is the amplifier; the pre-work is what makes the signal-to-noise ratio tolerable. If Chathura and Kennedy can unblock access and documents early, that week pays dividends in every conversation that follows.

---

## How the approach works — frameworks, data, and systems

This isn't a vibe check. The review is grounded in established ways of looking at how technology organizations perform and behave. We lean on things like **DORA** for delivery performance, **Westrum** for cultural traits that correlate with how safely and quickly teams can move, **value stream mapping** for how work actually flows end to end, and **RAPID**-style thinking for decision rights — who recommends, who agrees, who decides. The point isn't to paste acronyms on a whiteboard; it's to have a shared language and benchmarks so we're comparing Mad Mobile to recognized good practice, not to my personal preferences.

A big differentiator is that the work is **AI-augmented** in a very practical way. Before the first serious interview, we run automated scanning against your development and collaboration systems where we have access. That produces **quantitative baselines** — lead times, batch sizes, review patterns, whatever the tools can support — so conversations start from **data**, not from whoever spoke loudest in the last meeting. People still matter enormously; the data just keeps us honest about where to dig.

We look at **six interlocking systems**: **business direction** (strategy clarity and how it reaches teams), **product decision-making** (how priorities get chosen and communicated), **delivery** (how work is broken down, sequenced, and shipped), **technical foundations** (architecture, quality, operability, and the cost of change), **operating cadence** (rituals, communication, and how often reality gets inspected), and **accountability** (who owns outcomes versus activities, and whether feedback loops close). They're not silos. A weakness in one place almost always shows up somewhere else — for example, unclear product priorities might look like a delivery problem until you trace it upstream, or a brittle technical core might look like a people problem until you see what the system asks of them every sprint. The review is built to see those connections instead of treating symptoms in isolation.

The whole thing is **hypothesis-driven**. I arrive with a set of **named patterns to test** — structured questions about whether certain dynamics are real, how strong they are, and what evidence supports or contradicts them. Those hypotheses get validated or ruled out with interviews, artifacts, and metrics. I won't list the specific hypotheses here; naming them before we're in the room tends to create the wrong conversation. Suffice it to say they're concrete enough to guide the week and open enough that reality can correct us.

---

## The Tampa onsite — three days, high signal

The heart of the engagement is **three consecutive days onsite**, with **fifteen or more interviews**, each about **thirty to sixty minutes**. The arc is intentional:

- **Monday** tends toward leadership and strategic alignment — how direction is set, how commitments get made, how technology is expected to support the business.
- **Tuesday** goes deeper into engineering practice — how teams build, integrate, and ship; where the technical debt and integration pressure actually live.
- **Wednesday** is cross-functional tracing and validation — following threads across roles, checking whether Monday's story and Tuesday's story match what happens when real work moves through the system.

**Daily rhythm** roughly looks like: a **morning sync with Don** so priorities stay aligned; **structured interviews** through the day; **lunch with team members** when it makes sense — informal, human, often where the best nuance shows up; **afternoon sessions** for walkthroughs or deep dives; **synthesis time** so themes don't pile up untouched; and **evening processing** so the next day starts sharp. Flexibility matters — if we need to chase a critical thread, we chase it — but the backbone is that rhythm.

I use **AI-assisted note-taking** so I can stay present in the room. I'd rather ask one more good follow-up than worry about capturing every phrase. The goal is **architecture walkthroughs**, **real case tracing** (following actual work items from request to delivery where possible), and **observation** of how teams really work together, not how the process doc says they should.

If you've ever been in a review where the consultant left with a pile of sticky notes and you wondered what actually happened to them — the back half of this engagement is designed differently. Each evening I'm tightening themes, testing them against what we already saw in data, and adjusting who we need to see next. **Wednesday** especially is where the story either holds together or we go back and reconcile gaps. That's a feature, not a slip: we'd rather discover a mismatch while we're still in the building than ship a neat narrative that falls apart the following Monday.

---

## If you're being interviewed — what to expect

If you're on the calendar, here's the deal.

- **Thirty to sixty minutes**, typically **one-on-one**, **conversational**. This is not a quiz. It's not a performance review. There are no trick questions.
- I'll ask about **how work flows**, **where things stall**, **what you'd change** if you could wave a wand without blame landing on anyone, and **what "good" would look like** from your seat.
- **Individual comments are anonymous** in the outputs. I synthesize patterns and themes. Nobody gets quoted by name in the CEO-facing materials. The more specific you can be about *systems and processes*, the more useful the whole exercise is — for Don, for Chathura and Kennedy's organizations, and for everyone who lives in the tools and ceremonies every day.
- **Candor helps everyone.** If something is broken, saying so in this forum is one of the highest-leverage ways to get it on a prioritized fix list without it becoming personal. If something works really well, that's equally important — we want to **protect** what's working, not only chase problems.

---

## Tone and philosophy — how we're showing up

**Collaborative, not adversarial.** I'm working with Don as a colleague who cares about getting the technology story straight for the business — not as an outside auditor building a case against anyone.

**Systems-focused, not blame-focused.** Every finding should be readable as: *where does the system make it easy or hard for talented people to succeed?* People make choices inside structures; we care about the structures and incentives as much as the heroic exceptions.

**Preserving what works.** Mad Mobile is not a blank slate. There are **strong partnerships** — names like Sysco, Visa, Best Buy, Apple matter in the market — **real revenue**, **more than twenty-one thousand deployed locations**, and **deep bench strength** in the people building and supporting the product. Those are assets. The output of this work should make it *easier* to invest in the right places, not to tear down what's carrying the business.

One more thing worth saying plainly: **enthusiasm without denial.** I'm genuinely excited to work with organizations that operate at real scale in messy domains — that's where good systems thinking earns its keep. Grounded means we don't flatter problems away, and enthusiastic means we don't treat every rough edge as a catastrophe. The goal is a proportionate, actionable read on reality.

---

## What you'll get on the other side — deliverables

When the three weeks are done, Don gets a package meant to sit in **his** operating rhythm — something he can act on and something leadership can align around.

1. **CEO Operating Brief** — Think of it as the technology chapter of a transition and execution playbook: what's working, what's under stress, why, and what to tackle first so the business gets relief without random thrash.

2. **Prioritized friction register** — Specific findings, tied to **evidence**, with **severity** and **recommended actions**. This is the "what to fix" list with enough context that owners can argue productively about sequencing.

3. **30 / 60 / 90-day plan** — Including an explicit **"leave alone"** list. Not everything needs to change on day one; knowing what *not* to touch is as valuable as knowing what to prioritize.

4. **Board-ready presentation** — Investor-grade narrative and visuals so the technology story can be told clearly when the audience cares about risk, execution, and trajectory.

5. **Baseline survey package** — Something Mad Mobile can **re-run at 30 and 60 days** to see whether changes are moving the needle — **without** needing me back in the building. The goal is durable instrumentation, not dependency on a consultant.

Together, those artifacts answer the questions a CEO actually asks after a week like this: *What did we learn? What do we do Monday? What do we protect? How do we explain this to people who weren't in the room? How will we know if we're winning?* Those five buckets map cleanly to executive narrative when you brief others: diagnosis, backlog, plan, outward story, and measurement.

---

## How Chathura and Kennedy can help — logistics that multiply quality

If you're coordinating on the Mad Mobile side, a few things make an outsized difference:

**Access (read-only is fine):** source control, project management, cloud infrastructure, monitoring, internal documentation — whatever lets us ground the narrative in how work *actually* moves.

**Pre-reads:** roadmaps, architecture diagrams, recent incident or postmortem summaries, anything that orients the hypotheses and saves interview time for nuance instead of basics.

**Scheduling:** protecting calendar for the right people across the three days — including blocks for walkthroughs and tracing exercises — so we're not always fighting ten-minute gaps.

**Surveys:** helping **distribute the engineering surveys** Don will introduce, so participation is high and representative.

**Framing for teams:** reinforcing Don's message — **collaborative**, **systems-level**, **not a personnel review**. The emotional safety of the room directly affects signal quality.

**Encouraging candor:** seriously, this is the multiplier. The quality of the engagement scales with how willing people are to describe reality. No one is asked to be reckless — but vague politeness produces vague recommendations, and nobody benefits from that.

Small practical note: **read-only access** is enough for almost everything we need from tooling. We're not trying to move production levers from a guest account; we're trying to see how work is represented, how change flows, and where the metadata tells a story that interviews can enrich. If something truly can't be shared, say so early — we can often substitute a guided screen share or a redacted export for a given slice.

---

## Closing thought

We're not pre-writing the ending. The whole point is to **discover** what's true, **quantify** what we can, and **prioritize** what matters for Don's next chapter of leadership and for the teams doing the work. If Chathura, Kennedy, and the folks in the interviews help us see the real system — access, documents, time, honesty — we'll return a brief and a plan that respect both the complexity of the business and the people carrying it.

I'm looking forward to the week in Tampa and to being a useful translator between what the business needs to know and what engineering already knows in its bones.

— Adam
