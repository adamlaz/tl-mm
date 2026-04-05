# Next Steps & Open Items — April 5, 2026

**For Adam's eyes only.** Working list of what's left before the onsite.

**Last updated:** April 5 — after Don touchbase, engagement minisite expansion, ECharts chart generation.

---

## Today — April 5

- [x] **Don touchbase** — reorg alignment, V7 findings briefed, key questions on Kennedy/Strainick/board deck.
- [ ] **Send Ana + Chathura coordination update** — tonight. Updated `ana-request.md` covers all open items: Grafana Monday, Survey 5 inclusion, Enterprise Solutions org detail, interview schedule, conference room TV, pre-reads, CloudTrail access, incident process location.
- [ ] **Follow up with Chathura re: Survey 5** — his intro email only references 4 surveys. Either: (a) ask him to add the AI Adoption & Tooling survey as a 5th link, or (b) merge critical AI questions into Survey 4. Include in tonight's email.
- [ ] **Request Enterprise Solutions org detail** — Chathura's PDF had Zubair's page mostly blank. 58 people, zero names. Ask Chathura or Zubair directly. Include in tonight's email.
- [ ] **Finish building all surveys in Microsoft Forms** — DevEx draft is live, need DORA, Westrum, Pragmatic Engineer, and AI Adoption & Tooling. Target: all links ready before Monday morning so Chathura can send.

## Data Gaps to Close (Before April 11)

- [ ] **Jira incident query**: Search for issue types "Incident", "Code Red", "Service Interruption" in 2024–2026 to fill the RCA timeline gap. The Confluence post-mortem trail dies after 2023 — Jira may have the missing recent data.
- [ ] **Root Cause Category field #2**: We queried `customfield_10382` ("Probable/Actual Root Cause Category") which was 0% populated. There's also `customfield_10590` ("Root Cause Category", type: array) that wasn't queried — could be the active one. Re-run the custom fields script targeting this field.
- [ ] **CloudTrail access escalation**: Ask Ana/Matias if the audit role can get `cloudtrail:LookupEvents` added, or if there's a CloudTrail S3 bucket we can read directly. Deployment frequency from AWS is the one DORA metric we're completely missing.
- [x] ~~**Grafana access**: Still pending.~~ **CONFIRMED for Monday April 7** (Ana: Matias off for holiday weekend). When access arrives, capture dashboard inventory, alert rules, and data source configuration.
- [ ] **Branch protection validation**: 0/30 repos showed restrictions. Check whether Bitbucket uses project-level branch permissions instead of repo-level. The API endpoint may differ.
- [ ] **Pipeline coverage expansion**: Currently only top 30 repos. Consider running for all 789 active repos to get a more representative success rate, or at least the top 100.

## Docs to Finalize (Before April 7)

- [x] ~~**Update Chathura survey intro message** — needs to reference 5 surveys instead of 4.~~ **Chathura wrote his own version.** Issue: only 4 surveys. Following up tonight.
- [x] ~~**Send Ana follow-up reply**~~ Sending tonight (April 5). Updated `ana-request.md` covers all items.
- [ ] **Finalize interview schedule grid** — send to Ana for calendar booking. Post-reorg schedule is defined in the state doc and on the minisite at `/engagement/interviews`. Ana will work on this early next week.
- [ ] **Update `interview-prep-with-data.md`** — add V7 data-backed questions, fix titles/durations, remove Siegel, add Akshay/Guilarte sections, add roadmap-based questions from CDO PDF.
- [ ] **Capture product roadmap data** — the CDO PDF includes a detailed roadmap for CAKE, CAKE+Payments, Payments Ops, and Engineering. Capture into structured format for interview prep and minisite.

## Scope Update from Don

- [x] **Don confirmed (April 3 email):** "Retail and Neo/AI in scope please with main focus obviously restaurant." This explicitly expands scope beyond CAKE-primary to include Concierge/Retail and Neo/AI. Updated in state doc and engagement plan.

## CDO Org Chart — Key Corrections Applied

- [x] **Holly Bobal** — moved from Kennedy to Randy Brown (Restaurant Backend). Kennedy's team is just Jeremy Diggins.
- [x] **Akshay Bhasin** — VP Payments Engineering, 20+ people (was listed as 18). Includes Payments R&D (Kevin Reyes), Restaurant QE (7), Biz Ops, PCI counterparts.
- [x] **Randy Brown** — Restaurant Technology, 10 people (was 8). Frontend (3) + Backend (6) + Randy.
- [x] **Dulanjan W.** — VP, Product & GTM (was Sr. Dir. Product & Design). 6 named PMs, design director, open marketing role, L&D.
- [x] **Jorge Maltes** — confirmed still at company. PCI DSS Compliance counterpart under Payments.
- [x] **PMO domain assignments** — Qaiser (Restaurant), Vanessa (Payments), Ian (AI), Debbie (Ops Eng).
- [ ] **L&D discrepancy** — Chathura's chart places Adriana Z. and Ayodele L. under Dulanjan/Product. Don's chart placed them under Shatney/HR. Clarify onsite or via email.
- [ ] **Andy Honnold dual-report** — Don's chart: under Garcia (CFO). Chathura's chart: under Akshay (Payments). Clarify onsite.
- [ ] **Enterprise Solutions detail gap** — Zubair's page in the PDF was mostly blank. 58 people with no names. Need to request.

## Don Touchbase (April 5) ✅

- [x] **Touchbase with Don** — April 5. Reorg alignment, V7 findings briefed.
- [x] Key question: Kennedy's future (shapes board deck framing)
- [x] Key question: Strainick — promote-to-fit or promote-to-move?
- [x] Key question: Board deck transparency level (we now have significantly more damaging quantitative evidence)
- [x] Flag the incident timeline gap — Don may know if RCA practice moved or died
- [x] L&D reporting discrepancy — who owns Adriana/Ayodele, Dulanjan or Shatney?

## Analysis to Run (Before Onsite)

- [ ] **Theme-analyze the 30 sprint retrospectives** — extract recurring "what didn't go well" themes across teams. Look for: deploy friction, scope change, dependency waits, tooling gaps, testing bottlenecks.
- [ ] **Deep-read the 2 recent Team Tesla RCAs** — SQS Retry Storm (Dec 2025) and Menu Core API Retry Loop (Sept 2025). These are the most current operational evidence. Understand root causes and whether fixes were implemented.
- [ ] **Map top 5 reviewer bottleneck repos to teams** — who owns the repos where John Harre, Holly Culver, etc. are bottlenecks? Match to interview subjects.
- [ ] **Review the auto-generated C4 diagrams** — validate `mad-mobile-c4-context.mmd` and `mad-mobile-c4-container.mmd` for accuracy. Print for onsite architecture whiteboard sessions.
- [ ] **Scan extracted Confluence architecture pages** — the 94 pages from V5 + the 321KB diagram catalog from V7. Identify which ones to reference in specific interviews.
- [ ] **Map CDO product roadmap to team capacity** — 12+ ongoing CAKE projects + Payments integrations vs. Randy's 9 engineers + Akshay's 9 R&D engineers. Quantify the project-to-engineer ratio for onsite conversations.

## Onsite Prep (April 11–12)

- [ ] **Survey analysis** — surveys close April 10 (per Chathura's email). Analyze results same day. Feed into interview questions.
- [ ] **Final hypothesis scorecard update** — score each hypothesis A–I based on all pre-work evidence.
- [ ] **Print/prep onsite materials** — C4 diagrams, org chart (now detailed), key metrics one-pager, interview question sheets.
- [ ] **Pre-onsite briefing with Don** (April 10–11) — final alignment session. Review survey results, confirm interview schedule, identify 5 real cases to trace.
- [ ] **Travel logistics** — Uber from St. Pete to Tampa HQ, confirm room booking with Ana.

## Key Onsite Questions Sharpened by V7 + CDO Org Chart

These are the questions the V7 data and CDO org chart make possible:

1. **Chathura**: "Epic completion is 27.7%. REST has 260 open epics. How do you decide what gets worked on and what sits?"
2. **Chathura**: "89% of your issues are 'High' priority with no other levels in use. How does your team triage?"
3. **Chathura/Randy**: "I see structured post-mortems through 2023, then they largely stop. Where do incident reviews happen now?"
4. **Randy Brown**: "Your roadmap shows 12+ ongoing CAKE projects. Your team is 9 engineers — 3 frontend, 6 backend. How do you allocate across CAKEpop/Kiosk v2, Fixed POS, KDS v2, Cloud/EMS?"
5. **Randy/Akshay**: "Restaurant QE reports under Payments, not Restaurant. How does that work day-to-day? Do your QE engineers sit in the same sprints as Randy's developers?"
6. **Akshay Bhasin**: "The payments codebase has 87% CI/CD coverage and the cleanest architecture. Your org is 20+ people with Payments R&D, Restaurant QE, Biz Ops, and PCI compliance. How does your team's process differ from CAKE and Enterprise?"
7. **Akshay Bhasin**: "Kevin Reyes runs Payments R&D with 9 engineers including SL staff. How does the US/SL split work for payments development specifically?"
8. **Randy/Zubair**: "90% of your ECS services have no health checks. Is that a conscious decision or an oversight?"
9. **Engineering ICs**: "One reviewer handles 581 code reviews across your org. Who do you wait on for reviews, and how long?"
10. **Engineering ICs**: "Zero repos have branch protection — no required approvals, no required passing builds. Is that intentional?"
11. **Engineering ICs**: "Your pipeline success rate is 60.7% — nearly 40% of builds fail. What's the most common failure?"
12. **Dulanjan**: "Your roadmap has 12+ ongoing projects in CAKE alone, plus Payments integrations and Engineering platform work. With 6 PMs across those domains, who owns what?"

---

## SOW / Business

- [ ] Mercury banking setup for Translation Layer LLC
- [ ] EIN pending from Northwest
- [ ] SOW draft — scope, deliverables, timeline, confidentiality, IP ownership, liability
- [ ] Invoice structure — $10K deferred, payment terms TBD
