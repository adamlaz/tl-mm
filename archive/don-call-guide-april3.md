# Don Call Guide — April 3, 2026

**Purpose:** Status update + align on how the reorg reshapes the onsite and board deliverable. Recording + transcribing.

---

## OPEN (2 min)

Congrats on the reorg — big moves, clean execution. Friday announcement, all-hands midday — you've done this before.

---

## STATUS UPDATE — What I've Done So Far (5 min)

*Keep this tight. Don doesn't need the methodology — he needs to know you've been productive and you have real data.*

**Systems access:** Everything is working. Ana and the team turned it around fast — Bitbucket, Jira, Confluence, 18 AWS accounts, all with API access.

**Automated inventory (V1–V7):** Seven rounds of programmatic analysis, including a "sponge mode" deep collection. 94 JSON inventory files, 124 extracted documents, 31 interactive charts, 44 scripts. Here's what I have:

- **3,191 repos** across 4 Bitbucket orgs. 75% are stale. Four distinct code lineages — confirms the CAKE acquisition integration was never completed.
- **141 Jira projects**, 18,583 open issues, 72% over a year old. Median cycle time for engineering is **59 days** from In Progress to Done. Sprint velocity declining on multiple boards.
- **Epic completion rate: 27.7%.** 481 engineering epics in the last 12 months, only 133 resolved. The REST project (CAKE Restaurant) has 260 epics and an 18.5% completion rate. NEO project: 12.5%.
- **Priority is meaningless.** 89.4% of open engineering issues are "High." No other priority level in active use. They can't triage because everything looks the same.
- **Estimation discipline: 9%.** Only 27 of 300 resolved stories have Story Points. Root Cause Category field exists in Jira but is populated on 0% of bugs — the process is documented but not followed.
- **18 AWS accounts**, ~$383K/month. 201 running EC2 instances, 83% on pre-Graviton hardware. 21% of Lambda functions on end-of-life runtimes.
- **90% of ECS containers have no health checks.** 61 of 68 production services can be unhealthy without detection. This is a reliability finding for the board deck.
- **2 EKS clusters** running K8s 1.30/1.32 (modern). 8 RDS instances — MySQL 5.7 still running in 3 of them.
- **Incident timeline reconstructed.** 50 post-mortems parsed from Confluence. Peak incident year: **2022 (26 incidents)**. Top system: Payments (19), Reports (11), Menu (10). Root causes split between app bugs, infrastructure, payment providers, and database issues.
- **Pipeline success rate: 60.7%.** Nearly 40% of builds fail across 30 active repos. 1,563 pipeline runs analyzed.
- **Code review bottlenecks identified.** 1,464 reviewer relationships mapped across 217 people. **John Harre alone handles 581 code reviews.** 57 people have 100+ reviews. 17 repos have a single reviewer handling >50% of all PRs.
- **Branch protection: zero repos.** None of the 30 active repos checked have required approvals or passing builds. 201 open PRs, 175 older than 30 days, 167 with zero comments.
- **168 unique users** across all systems. 39% are inactive but still have access.
- **No production AI infrastructure.** SageMaker artifacts in R&D only. No dedicated Neo/AI account.
- **30 sprint retrospectives extracted** from 6 teams — teams are documenting what's broken in their own words. Ready for theme analysis.

**Surveys:** Building 5 surveys in Microsoft Forms on my MM account right now. Chathura sending the intro Monday. Closing April 11.

**Pre-reads:** Got org chart and restaurant update deck. Pulled 94 key pages from Confluence directly. Still waiting on Concierge/Retail and Neo/AI roadmaps, revenue breakdown.

**31 interactive charts** ready — including a PR review network graph and updated analysis — backlog trends, velocity, cycle time distributions, repo activity, AWS spend breakdowns, user access patterns.

**One gap to flag:** The incident/RCA documentation in Confluence largely stops after 2023. I have 50 structured post-mortems, but the formal RCA process in the Taurus space ran 2020–2023, then mostly died. Team Tesla wrote two RCAs in 2025 (SQS Retry Storm, Menu Core Retry Loop), but there's a clear gap in 2024. Either they stopped doing post-mortems, the practice moved to Teams/Slack/Guru, or incidents genuinely dropped. **I'll be asking Chathura and Randy about this onsite.** Also: the AWS audit role doesn't include CloudTrail, so I can't measure deployment frequency from the AWS side — only from Bitbucket pipelines.

---

## KEY QUESTIONS FOR DON

### The Reorg (10 min)

**1. "What's the real story on Kennedy?"**
- Is this a graceful transition toward an exit, or does he have a genuine mandate to build AI?
- Because the systems tell me there's almost nothing behind the AI marketing right now — no production infra, no dedicated account, SageMaker experiments in R&D only.
- **Why this matters:** It changes how I write the board deliverable. If Kennedy's lane is real, I frame the AI gap as "investment needed." If it's transitional, I frame it as "strategy clarification needed."

**2. "Where does Kennedy land in 90 days?"**
- Don may not want to answer this directly — that's fine. But his reaction tells you a lot.
- If he deflects → Kennedy's future is uncertain, frame accordingly
- If he's direct → you know exactly how to handle the onsite interview

**3. "How do you want me to handle Kennedy in the interview?"**
- I have 60 minutes with him on Monday. He just watched his operational scope get carved out.
- Options: (a) Focus entirely on AI vision and let him own it, (b) Probe gently on what the transition looks like, (c) Ask Don to give Kennedy a heads-up that I'll be asking about AI infrastructure specifics
- **Recommendation:** Option (a) with a little (c). Let Kennedy own the AI narrative. Don't make him defend what he lost.

**4. "Chathura's scope is massive — does he know what he's inheriting?"**
- All engineering + product + design + PMO + customer support. That's 94+ people.
- Has Don had a candid conversation with Chathura about capacity, priorities, and what he can realistically change in the first 90 days?
- My surveys and onsite interviews will give Chathura real data to work with. Does Don want me to position the deliverables partly as tools for Chathura?

**5. "Is the Bhasin move what it looks like?"** *(PARTIALLY RESOLVED)*
- March chart: Akshay Bhasin = QE Lead with 7 people
- April chart: Akshay Bhasin = Payments with 18 people
- **CDO org chart (April 3) confirms:** VP Payments Engineering with 20+ people. Payments R&D (Kevin Reyes as Director, 9 people), Restaurant QE (7), Biz Operations (Andy Honnold + 3), PCI counterparts (Maltes, Freid, Riglos, Keye). Much larger than "18."
- **Remaining question:** Was Restaurant QE always under Payments, or was this a consolidation? Having QE for Restaurant under the Payments VP (not the Restaurant VP) is unusual.
- **New question:** Andy Honnold appears under Akshay in Chathura's chart but under Garcia (CFO) in Don's. Dual reporting?

**6. "Talk to me about Strainick — is COO a promote-to-fit or a promote-to-move?"**
- He went from Chief People Officer to COO. That's not a lateral — it's a lane change.
- If Don moved him because he wasn't the right person for HR/culture but trusts him on operational execution → that's a "promote to fit" and Strainick is a real COO you take seriously in interviews
- If Don moved him because he needed to clear the HR seat and COO was an available landing spot → that's a "promote to move" and you calibrate how much weight to put on his inputs
- **Why this matters for the onsite:** Strainick now owns Account Management, Onboarding, Delivery, and IT — that's the entire customer operations chain. If he's strong, he's a key ally for execution improvements. If he's parked, you're interviewing someone who won't be in the seat long.
- Don't ask it this bluntly — try: "What made you pick David for the COO role specifically?" and listen for conviction vs. logistics in the answer.

**7. "What's the story on Bailey Shatney?"**
- New name — wasn't on the March org chart at all. Where did she come from?
- She's stepping into HR at a company with a 2.4 Glassdoor, culture erosion from layoffs, shifted bonuses, forced RTO, and a Houston office shutdown. That's a brutal seat.
- Is she an internal promotion or an outside hire? How much runway does Don expect before she can actually move the culture needle?
- **Why this matters:** If Bailey is new and still ramping, the culture/retention data from your surveys and interviews is even more important — she won't have her own baseline yet. Your deliverables could be a gift to her.

### The Board Deliverable (5 min)

**8. "What questions are Morgan Stanley and Western Alliance asking that you can't answer yet?"**
- This is the single most important question. It tells you exactly what the board deck needs to address.
- Likely areas: technology scalability, AI strategy credibility, tech debt quantification, team capacity, CAKE reliability
- **Listen for:** What makes Don uncomfortable when investors ask about technology

**9. "How transparent do you want the board deck to be?"**
- I now have quantitative evidence of significant issues: 27.7% epic completion, 89.4% priority inflation, 9% estimation discipline, 60.7% pipeline success rate, 90% of containers with no health checks, 59-day cycle time, 72% stale backlog, zero branch protection, 201 stale open PRs, no AI production infra, $25.9K/month on a mystery legacy account, 83% pre-Graviton EC2
- Options: (a) Full transparency — the data is the data, (b) Selective transparency — lead with strengths and frame gaps as "investment opportunities", (c) Two versions — one for internal action, one for external audiences
- **Recommendation:** Full transparency with Don's internal brief, calibrated framing for the board deck. Investors respect honesty more than spin, and they'll find the gaps anyway in diligence.

**10. "With Siegel and Lodes gone, who owns the revenue data I need?"**
- Revenue breakdown by product line (CAKE vs Concierge vs Neo vs Payments) — this was on my pending list
- Siegel had data/analytics and revenue ops. That's now split: Garcia has RevOps, Strainick has account management
- Who should I go to for the revenue mix?

### Onsite Prep (5 min)

**11. "I've added a 5th survey — AI & Tooling. Good with you?"**
- Quick pitch: Maps actual AI adoption vs. perception, identifies tooling sprawl and gaps, feeds directly into board deliverable and vendor rationalization
- Everyone in eng + product takes it. ~5 min.

**12. "I'm restructuring the interview schedule. Any names you want me to add or avoid?"**
- Added: Mark Guilarte (PMO), Bailey Shatney (VP HR), customer support lead (TBD)
- Removed: Siegel
- Deprioritized: Lodes (optional, consulting transition only)
- Changed: Strainick from HR → COO operations, Kennedy from 90 → 60 min
- **Ask specifically:** Is there anyone in Chathura's expanded org I should prioritize? Any landmines?

**13. "Any topics I should stay away from onsite?"**
- The reorg is 10 days old by the time I arrive. Some people may be raw.
- Are there conversations Don wants me to *not* have, or things he'd rather surface himself?

---

## CLOSE (2 min)

- Confirm call with Don again before onsite (targeting April 10–11 for final alignment)
- Remind him: surveys go out Monday from Chathura, close Friday April 11
- I'll have the interview grid to Ana by Tuesday
- Ask: anything else on his mind that I should be looking at?

---

## NOTES DURING CALL

*(Space for live notes — fill in during/after)*

**Kennedy real story:**


**Kennedy 90-day outlook:**


**Kennedy interview approach:**


**Chathura capacity/priorities:**


**Bhasin scope clarification:**
*PARTIALLY RESOLVED via CDO org chart: VP Payments Eng, 20+ people. Still ask about Restaurant QE reporting under Payments and Andy Honnold dual-report.*

**L&D reporting discrepancy (NEW):**
*Chathura's chart puts Adriana Z. and Ayodele L. under Dulanjan/Product L&D. Don's chart puts them under Shatney/HR. Which is correct? Matrix situation?*

**Strainick — promote to fit or promote to move?**


**Bailey Shatney — background and runway:**


**Board questions from investors:**


**Board deck transparency level:**


**Don scope confirmation (from April 3 email):**
*"Retail and Neo/AI in scope please with main focus obviously restaurant." — Updated all docs. Concierge/Retail and Neo/AI roadmaps explicitly requested.*

**Jorge Maltes (RESOLVED):**
*Not departed. Confirmed in CDO org chart as Dir. IT under PCI DSS Compliance counterparts (Payments). Rosen Georgiev handles day-to-day IT ops under COO.*

**Revenue data owner:**


**Survey 5 approved?**
*NOTE: Chathura's survey email only references 4 surveys. He dropped AI & Tooling. Need to either ask Don to push for it or accept 4.*


**Interview adds/removes/landmines:**


**Off-limits topics:**


**Other:**

