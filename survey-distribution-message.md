# Reply to Ana & Chathura — April 5, 2026 (Evening)

**Thread:** Re: Mad Mobile — Technology Operations Review \ DRAFT briefing materials
**Reply-all** (Ana, Chathura, Don, Jack on thread)

---

Ana, Chathura — thanks for the org chart and the revised survey message. A few things for each of you, plus open items for the week.

Don — noted on Retail and Neo/AI in scope, main focus restaurant. Also received the 90-day plan and cash flow forecast — thank you. The deck references the technology deep dive as still in process, which is exactly what my onsite and deliverables cover. This gives me the framing I need to make sure the technology assessment plugs directly into the plan you've presented to Morgan Stanley and Bridge Bank.

---

**Chathura — surveys**

Your survey email reads well. One addition: there's a 5th survey — **AI Adoption & Tooling** (20 questions, ~5 min, for all engineering, product, design, and QE). It feeds directly into the board deliverable and vendor assessment. Could you add it before sending Monday?

Here's the line to add:

- [Survey 5 — AI Adoption & Tooling] (everyone in engineering, product, design, and QE)

And here are all 5 response links ready to drop in:

1. **Survey 1 — Delivery Performance:** https://forms.cloud.microsoft/r/WNU3f9ryvZ
2. **Survey 2 — Team Culture:** https://forms.cloud.microsoft/r/AwEJqN022m
3. **Survey 3 — Developer Experience:** https://forms.cloud.microsoft/r/021mP98Sf9
4. **Survey 4 — Engineering Practices:** https://forms.cloud.microsoft/r/AV5BE2eKJP
5. **Survey 5 — AI Adoption & Tooling:** https://forms.cloud.microsoft/r/bPBy7MNCkS

One more ask: your CDO org chart had Zubair's Enterprise Solutions page blank. That's the largest org (~58 people) and I have zero names. Can you or Zubair share even a rough list of names and roles this week?

---

**Ana — logistics and open items**

Confirmed items (thank you):
- Grafana access Monday via Matias — perfect.
- Pre-read folder Monday — looking forward to it. Retail and Neo/AI roadmaps especially. *(Don shared the 90-day plan and cash flow forecast tonight — that covers the investor/lender framing I was looking for, so that item is resolved.)*
- Interview scheduling — I'll send the full 3-day grid (18–21 sessions, April 13–15) tomorrow for calendar booking.
- Conference room — yes, a TV/screen would be great for showing charts during interviews. Thanks for asking.

New asks for this week:

1. **Microsoft Graph API** — I need an IT admin (Rosen or Matias) to grant read-only permissions on my account (`adam.lazarus@madmobile.com`): `User.Read.All`, `People.Read`, `Calendars.Read`, `Group.Read.All`. Lets me pull the org directory and check calendar availability for interview scheduling. Read-only, engagement period only. Happy to send Rosen the exact steps.
2. **Incident/RCA docs** — Confluence post-mortems largely stop after 2023. Did the process move somewhere — Teams, Guru, Jira, PagerDuty? Who would know?
3. **CloudTrail access** — Can the audit role get `cloudtrail:LookupEvents` added, or is there a CloudTrail S3 bucket I can read directly? Routing question for Matias.
4. **SaaS vendor spend** — **(elevated priority)** The 90-day plan commits to specific technology cost reductions. My board deliverable needs to back those numbers with line-item detail. An export from finance showing annual vendor spend would be the single most impactful thing I could get this week. Top priorities: Atlassian, Wiz.io, Datadog, Five9, Salesforce, AWS contract terms. Even partial data on the top 5 helps.
5. **GitHub** — still active alongside Bitbucket, or can it be shut down?
6. **Guru** — still active? Roughly how many users?

Two items from Don's call — routing to the right people:

7. **Winmark project** — Don mentioned Jack is working on a client delivery for Winmark. Is there a Jira project, Confluence space, or Bitbucket repo for this? Want to make sure I'm not missing any active workstreams.
8. **Bloom Intelligence** — Don mentioned a potential partnership with Bloom Intelligence (Will Wilson) around POS + customer analytics. Would you check with Dulanjan if there are meeting notes or briefs from conversations with them?

---

Pre-work is in good shape. All 5 surveys are built, I've completed 7 rounds of automated analysis across Bitbucket, Jira, Confluence, and all 18 AWS accounts, and the interview grid is ready to send tomorrow. With the 90-day plan now in hand, I'll make sure the technology assessment and vendor analysis plug directly into the cost reduction and operational targets Don has laid out.

Thanks,
Adam

---

## Routing Guide (for Chathura's reference — not included in the email)

| Role | Surveys |
|------|---------|
| Engineering Manager / Lead | 1 (Delivery Performance), 2 (Team Culture), 4 (Engineering Practices), 5 (AI Tooling) |
| Senior IC / Staff Engineer | 2 (Team Culture), 3 (Developer Experience), 4 (Engineering Practices), 5 (AI Tooling) |
| Software Engineer (IC) | 2 (Team Culture), 3 (Developer Experience), 5 (AI Tooling) |
| QE / Quality Engineer | 3 (Developer Experience), 5 (AI Tooling) |
| DevOps / SRE | 3 (Developer Experience), 5 (AI Tooling) |
| Product Manager | 2 (Team Culture), 5 (AI Tooling) |
| Product Designer | 5 (AI Tooling) |

**If Chathura gets questions:**
- "Is this about me?" — No. It's about how the system runs. Only aggregate patterns are reported.
- "Who sees the results?" — Adam analyzes them. Only patterns and team-level trends go into the report. No individual answers are shared with leadership.
- "Why so many?" — Each survey measures a different dimension. Most people only take 2–3 based on role.
- "I don't know the answer" — Answer based on actual experience. "I don't know" is a valid and useful data point.
