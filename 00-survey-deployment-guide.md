# Survey Deployment Guide — Mad Mobile Pre-Work

**Purpose:** Deploy four established engineering assessments before the April 13 onsite to create a quantitative baseline. These surveys are designed to be re-run at 30 and 60 days by Mad Mobile's team without Adam's involvement.

---

## Survey Summary

| Survey | Audience | Time | Questions | What It Measures |
|---|---|---|---|---|
| DORA Quick Check | Engineering leads/managers (1 per team) | ~3 min | 9 | Software delivery performance: deploy frequency, lead time, change failure rate, recovery time |
| Westrum Culture | All eng leads, managers, senior ICs, PMs | ~2 min | 7 | Organizational culture type: pathological → bureaucratic → generative |
| DevEx (DX Core 4) | Individual contributors only (engineers, QE) | ~5 min | 18 | Developer experience: feedback loops, cognitive load, flow state, satisfaction |
| Pragmatic Engineer Test | 3–5 engineering leads or senior engineers | ~2 min | 15 | Engineering culture maturity: 12 yes/no + 3 context |

**Total time per person: under 15 minutes** (most people take only 2 of the 4 surveys based on their role)

---

## Who Takes What

| Role | DORA | Westrum | DevEx | Pragmatic Eng |
|---|---|---|---|---|
| Engineering Manager / Lead | ✅ | ✅ | | ✅ |
| Senior IC / Staff Engineer | | ✅ | ✅ | ✅ |
| Software Engineer | | ✅ | ✅ | |
| QE Engineer | | ✅ | ✅ | |
| Product Manager | | ✅ | | |
| Product Designer | | ✅ | | |

---

## Deployment Timeline

| Date | Action |
|---|---|
| ~April 1–3 | Don sends introduction message to engineering (see template below) |
| ~April 3–4 | Surveys go live. Adam sends links or Don's team distributes through internal survey tool. |
| April 10 | Reminder for anyone who hasn't completed |
| April 11 | Surveys close. Adam analyzes results. |
| April 13 | Adam arrives onsite with baseline data. Uses results in interviews. |

---

## Deployment Options

### Option A: Mad Mobile's internal survey tool (preferred)
If MM has SurveyMonkey, Typeform, Google Forms, or similar — deploy through their existing infrastructure. This makes it feel like an internal initiative, not an external exercise. Adam provides the questions; MM's team sets them up.

### Option B: Adam sets up Google Forms (fallback)
If no internal tool is available or it's faster, Adam creates Google Forms for each survey and shares links. Results are private to Adam and shared only in aggregate with Don.

### Option C: Hybrid
DORA and Pragmatic Engineer go to a small group (leads only) — Adam can send directly. Westrum and DevEx go to a broader group — better deployed through internal channels with Don's framing.

---

## Introduction Message (from Don to the team)

This message should come from Don — not from Adam. It positions the surveys as part of Don's leadership onboarding, not as an external consultant's data collection.

> **Subject:** Quick surveys ahead of our technology review
>
> Team,
>
> As part of my onboarding as Co-CEO, I've asked Adam Lazarus to help me get a clear picture of how our technology and delivery systems work. Adam has deep experience translating between business and engineering, and he'll be onsite April 13–15 doing interviews and walkthroughs.
>
> Before he arrives, I'd like everyone in engineering and product to complete a short set of surveys. These take **under 15 minutes total** and are completely anonymous — no individual responses will be attributed to anyone by name.
>
> The surveys measure things like deployment speed, team culture, and developer experience using industry-standard benchmarks. The goal isn't to evaluate anyone — it's to understand where the system helps or hinders your ability to do great work.
>
> **Your honest answers matter.** The more candid you are, the more useful this will be for all of us. We plan to re-run these same surveys in 30 and 60 days so we can measure whether changes we make are actually working.
>
> Here are the links:
> - [Survey 1 — DORA Quick Check] *(engineering leads/managers only)*
> - [Survey 2 — Culture Survey] *(everyone in engineering and product)*
> - [Survey 3 — Developer Experience] *(individual contributors only)*
> - [Survey 4 — Engineering Practices] *(engineering leads and senior engineers)*
>
> Please complete by **April 10**.
>
> Thanks for your time on this — I know surveys aren't anyone's favorite thing, but this is a real opportunity to be heard.
>
> Don

---

## Analysis Plan (for Adam)

### Pre-Onsite (by April 12)
- Score each survey per the scoring guides in the individual survey files
- Segment by team/product area wherever possible (CAKE/Restaurant vs. Concierge/Retail vs. Neo/AI)
- Identify top 3 patterns from each survey
- Flag any extreme outliers (very high or very low scores)
- Prepare 2–3 "data-informed" interview questions for the onsite (e.g., "I can see your DORA lead time is X — does that match your experience?")

### Onsite (April 13–15)
- Reference survey data during interviews: "The survey data suggests X — does that resonate?"
- Use Westrum culture scores to guide which teams may be more or less candid
- Validate DORA self-reported metrics against actual system data from GitHub/Jira

### Post-Engagement Deliverable
- Package all four surveys with Mad Mobile-specific instructions, baseline scores, and comparison guidance
- Deliver as the "Baseline Survey Package (Repeatable)" so MM can re-run at 30/60 days
- Include a simple scoring template so Don's team doesn't need Adam to interpret results

---

## Files

- `01-dora-quick-check.md` — DORA Quick Check survey instrument
- `02-westrum-culture-survey.md` — Westrum Organizational Culture Survey
- `03-devex-survey.md` — Developer Experience (DX Core 4) Survey
- `04-pragmatic-engineer-test.md` — Pragmatic Engineer Test
