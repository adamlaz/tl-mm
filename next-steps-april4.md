# Next Steps & Open Items — April 4, 2026

**For Adam's eyes only.** Working list of what's left before the onsite.

---

## Data Gaps to Close (Before April 11)

- [ ] **Jira incident query**: Search for issue types "Incident", "Code Red", "Service Interruption" in 2024–2026 to fill the RCA timeline gap. The Confluence post-mortem trail dies after 2023 — Jira may have the missing recent data.
- [ ] **Root Cause Category field #2**: We queried `customfield_10382` ("Probable/Actual Root Cause Category") which was 0% populated. There's also `customfield_10590` ("Root Cause Category", type: array) that wasn't queried — could be the active one. Re-run the custom fields script targeting this field.
- [ ] **CloudTrail access escalation**: Ask Ana/Matias if the audit role can get `cloudtrail:LookupEvents` added, or if there's a CloudTrail S3 bucket we can read directly. Deployment frequency from AWS is the one DORA metric we're completely missing.
- [ ] **Grafana access**: Still pending. If it comes through before onsite, capture dashboard inventory, alert rules, and data source configuration. This is the primary observability layer.
- [ ] **Branch protection validation**: 0/30 repos showed restrictions. Check whether Bitbucket uses project-level branch permissions instead of repo-level. The API endpoint may differ.
- [ ] **Pipeline coverage expansion**: Currently only top 30 repos. Consider running for all 789 active repos to get a more representative success rate, or at least the top 100.

## Docs to Finalize (Before April 7)

- [ ] **Send Ana coordination email** — `ana-request.md` is ready. Includes interview calendar, conference room, pre-read folder.
- [ ] **Finish all 5 surveys in Microsoft Forms** — DevEx draft is live, need DORA, Westrum, Pragmatic Engineer, AI Adoption & Tooling.
- [ ] **Update Chathura survey intro message** — needs to reference 5 surveys instead of 4.
- [ ] **Finalize interview schedule grid** — send to Ana for calendar booking. Post-reorg schedule is defined in the state doc.
- [ ] **Update `interview-prep-with-data.md`** — add V7 data-backed questions (epic completion, incident timeline, reviewer bottlenecks, health checks, priority inflation, estimation discipline).

## Don Call (April 3 or ASAP)

- [ ] **Call Don** using `don-call-guide-april3.md` — 13 questions across reorg, board deliverable, onsite prep. Updated with V7 data.
- [ ] Key question: Kennedy's future (shapes board deck framing)
- [ ] Key question: Strainick — promote-to-fit or promote-to-move?
- [ ] Key question: Board deck transparency level (we now have significantly more damaging quantitative evidence)
- [ ] Flag the incident timeline gap — Don may know if RCA practice moved or died

## Analysis to Run (Before Onsite)

- [ ] **Theme-analyze the 30 sprint retrospectives** — extract recurring "what didn't go well" themes across teams. Look for: deploy friction, scope change, dependency waits, tooling gaps, testing bottlenecks.
- [ ] **Deep-read the 2 recent Team Tesla RCAs** — SQS Retry Storm (Dec 2025) and Menu Core API Retry Loop (Sept 2025). These are the most current operational evidence. Understand root causes and whether fixes were implemented.
- [ ] **Map top 5 reviewer bottleneck repos to teams** — who owns the repos where John Harre, Holly Culver, etc. are bottlenecks? Match to interview subjects.
- [ ] **Review the auto-generated C4 diagrams** — validate `mad-mobile-c4-context.mmd` and `mad-mobile-c4-container.mmd` for accuracy. Print for onsite architecture whiteboard sessions.
- [ ] **Scan extracted Confluence architecture pages** — the 94 pages from V5 + the 321KB diagram catalog from V7. Identify which ones to reference in specific interviews.

## Onsite Prep (April 11–12)

- [ ] **Survey analysis** — surveys close April 11. Analyze results same day. Feed into interview questions.
- [ ] **Final hypothesis scorecard update** — score each hypothesis A–I based on all pre-work evidence.
- [ ] **Print/prep onsite materials** — C4 diagrams, org chart, key metrics one-pager, interview question sheets.
- [ ] **Pre-onsite briefing with Don** (April 10–11) — final alignment session. Review survey results, confirm interview schedule, identify 5 real cases to trace.
- [ ] **Travel logistics** — Uber from St. Pete to Tampa HQ, confirm room booking with Ana.

## Key Onsite Questions Sharpened by V7

These are the questions the V7 data makes possible that V6 data couldn't:

1. **Chathura**: "Epic completion is 27.7%. REST has 260 open epics. How do you decide what gets worked on and what sits?"
2. **Chathura**: "89% of your issues are 'High' priority with no other levels in use. How does your team triage?"
3. **Chathura/Randy**: "I see structured post-mortems through 2023, then they largely stop. Where do incident reviews happen now?"
4. **Randy Brown**: "Payments had 19 incidents in our RCA data, most in 2021–2022. The peak was 26 incidents in 2022. Has reliability actually improved, or did the documentation practice just stop?"
5. **Randy/Zubair**: "90% of your ECS services have no health checks. Is that a conscious decision or an oversight?"
6. **Akshay Bhasin**: "The payments codebase has 87% CI/CD coverage and the cleanest architecture. How does your team's process differ from CAKE and Enterprise?"
7. **Engineering ICs**: "One reviewer handles 581 code reviews across your org. Who do you wait on for reviews, and how long?"
8. **Engineering ICs**: "Zero repos have branch protection — no required approvals, no required passing builds. Is that intentional?"
9. **Engineering ICs**: "Story points are on 9% of stories. Do you estimate? If not, how do you predict delivery?"
10. **Engineering ICs**: "Your pipeline success rate is 60.7% — nearly 40% of builds fail. What's the most common failure?"

---

## SOW / Business

- [ ] Mercury banking setup for Translation Layer LLC
- [ ] EIN pending from Northwest
- [ ] SOW draft — scope, deliverables, timeline, confidentiality, IP ownership, liability
- [ ] Invoice structure — $10K deferred, payment terms TBD
