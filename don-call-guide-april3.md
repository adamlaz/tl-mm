# Don Call Guide — April 3, 2026

**Purpose:** Status update + align on how the reorg reshapes the onsite and board deliverable. Recording + transcribing.

---

## OPEN (2 min)

Congrats on the reorg — big moves, clean execution. Friday announcement, all-hands midday — you've done this before.

---

## STATUS UPDATE — What I've Done So Far (5 min)

*Keep this tight. Don doesn't need the methodology — he needs to know you've been productive and you have real data.*

**Systems access:** Everything is working. Ana and the team turned it around fast — Bitbucket, Jira, Confluence, 18 AWS accounts, all with API access.

**Automated inventory (V1–V6):** I've already run six rounds of programmatic analysis across every system. Here's what I have:

- **3,191 repos** across 4 Bitbucket orgs. 75% are stale. Four distinct code lineages — confirms the CAKE acquisition integration was never completed.
- **141 Jira projects**, 18,583 open issues, 72% over a year old. Median cycle time for engineering is **59 days** from In Progress to Done. Sprint velocity is declining on multiple boards.
- **18 AWS accounts**, ~$383K/month. 201 running EC2 instances, 83% on pre-Graviton hardware. 21% of Lambda functions on end-of-life runtimes.
- **168 unique users** across all systems. 39% are inactive but still have access.
- **No production AI infrastructure.** SageMaker artifacts in R&D only. No dedicated Neo/AI account.
- **Self-hosted Grafana** for monitoring — not Datadog or New Relic.
- **$25.9K/month on Monvia** — a legacy account nobody seems to own. MenuPad and Relate also running with no clear ownership.

**Surveys:** Building 5 surveys in Microsoft Forms on my MM account right now. Chathura sending the intro Monday. Closing April 11.

**Pre-reads:** Got org chart and restaurant update deck. Pulled 94 key pages from Confluence directly. Still waiting on Concierge/Retail and Neo/AI roadmaps, revenue breakdown.

**29 interactive charts** ready — backlog trends, velocity, cycle time distributions, repo activity, AWS spend breakdowns, user access patterns.

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

**5. "Is the Bhasin move what it looks like?"**
- March chart: Akshay Bhasin = QE Lead with 7 people
- April chart: Akshay Bhasin = Payments with 18 people
- Did he absorb the Payments engineering org, or was the March chart just incomplete?

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
- I now have quantitative evidence of significant issues: 59-day cycle time, 72% stale backlog, no AI production infra, $25.9K/month on a mystery legacy account, 83% pre-Graviton EC2
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


**Strainick — promote to fit or promote to move?**


**Bailey Shatney — background and runway:**


**Board questions from investors:**


**Board deck transparency level:**


**Revenue data owner:**


**Survey 5 approved?**


**Interview adds/removes/landmines:**


**Off-limits topics:**


**Other:**

