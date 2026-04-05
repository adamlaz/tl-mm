# AI Adoption & Tooling Survey — Mad Mobile

**What this measures:** Current AI tool adoption, perceived effectiveness, broader tooling landscape (gaps, overlaps, friction), and readiness for AI-driven product and engineering strategy. Results feed into three deliverables: the board/investor AI strategy assessment, the vendor/tool rationalization analysis, and the 30/60/90-day action plan.

**Time:** ~5 minutes
**Who takes this:** All engineering, product, design, and QE. Managers and ICs both — this captures the full picture.
**Anonymity:** Your responses are anonymous. Only aggregate patterns and team-level trends are reported — nothing is attributed by name.

---

## Instructions

Answer based on your actual experience at Mad Mobile over the last 3 months. We're interested in what you really use, what actually helps, and what's missing — not what's aspirational.

---

## Section A: AI Tool Usage

*What AI tools do you currently use in your work at Mad Mobile?*

### 1. Which AI tools do you use at least weekly? (select all that apply)

- [ ] Cursor (AI-assisted coding)
- [ ] Claude (Anthropic) — directly or via Cursor
- [ ] ChatGPT / OpenAI
- [ ] Lovable (AI prototyping / UI generation)
- [ ] n8n AI workflows (Smart Prompts, ETL, etc.)
- [ ] Amazon Bedrock / SageMaker
- [ ] GitHub Copilot
- [ ] Gemini (Google)
- [ ] Bland.AI (customer support)
- [ ] Revenue.io (sales intelligence)
- [ ] AI features built into existing tools (Jira, Confluence, Bitbucket, etc.)
- [ ] Amazon Q Developer / CodeWhisperer
- [ ] Custom internal AI tools or scripts
- [ ] None — I don't currently use AI tools
- [ ] Other: _____________

### 2. What do you primarily use AI tools for? (select all that apply)

- [ ] Writing or generating code
- [ ] Code review and debugging
- [ ] Writing tests
- [ ] Writing documentation
- [ ] Writing user stories or requirements
- [ ] Analyzing logs or production issues (RCA)
- [ ] Data analysis or querying
- [ ] Internal communication (drafting messages, summarizing)
- [ ] Learning new technologies or codebases
- [ ] I don't currently use AI tools
- [ ] Other: _____________

---

## Section B: AI Effectiveness

**Scale:** 1 = Strongly Disagree | 2 = Disagree | 3 = Neutral | 4 = Agree | 5 = Strongly Agree

### 3. AI tools meaningfully improve my daily productivity.

| 1 | 2 | 3 | 4 | 5 | N/A — I don't use AI tools |
|---|---|---|---|---|---|

### 4. I have the training and support I need to use AI tools effectively.

| 1 | 2 | 3 | 4 | 5 | N/A |
|---|---|---|---|---|---|

### 5. My team has clear guidelines on when and how to use AI tools (e.g., code review standards, security, IP).

| 1 | 2 | 3 | 4 | 5 | N/A |
|---|---|---|---|---|---|

### 6. I trust the output from AI tools enough to use it without heavy manual review.

| 1 | 2 | 3 | 4 | 5 | N/A |
|---|---|---|---|---|---|

### 7. Mad Mobile's AI strategy for our products (CAKE, Concierge, Neo) is clear to me.

| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|

---

## Section C: Tooling Landscape

*Beyond AI — the full set of tools, platforms, and services you rely on to do your work.*

### 8. Which of these tools do you use at least weekly? (select all that apply)

- [ ] Jira
- [ ] Confluence
- [ ] Bitbucket
- [ ] VS Code
- [ ] IntelliJ IDEA
- [ ] Postman / Insomnia
- [ ] Docker
- [ ] Jenkins
- [ ] Grafana
- [ ] Datadog
- [ ] Slack
- [ ] Microsoft Teams
- [ ] Figma
- [ ] SonarQube
- [ ] Snyk
- [ ] SpiraTest / QCenter
- [ ] Salesforce
- [ ] Five9
- [ ] Other: _____________

### 8b. What are the 1–3 tools most essential to your daily work? (free text)

_________________________________

### 9. Are there tools your team pays for or has access to that you rarely or never use? If so, which ones?

_________________________________
_________________________________

### 10. Are there tools or capabilities you wish you had but don't? What would make your work significantly easier?

_________________________________
_________________________________

### 11. Rate the following statements:

**Scale:** 1 = Strongly Disagree | 2 = Disagree | 3 = Neutral | 4 = Agree | 5 = Strongly Agree

**a) I have too many tools to manage — there is overlap and redundancy in what we use.**

| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|

**b) Our tools are well-integrated — data flows between systems without manual effort.**

| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|

**c) When a new tool is introduced, I receive adequate onboarding and documentation.**

| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|

**d) I know who to ask when I have problems with a tool or need access to a new one.**

| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|

---

## Section D: AI in Our Products

### 12. How confident are you that Mad Mobile can deliver competitive AI-powered features to customers in the next 12 months?

| 1 — Not at all confident | 2 | 3 | 4 | 5 — Very confident |
|---|---|---|---|---|

### 13. What is the biggest barrier to Mad Mobile delivering on its AI product vision? (select one)

- [ ] We don't have the right infrastructure
- [ ] We don't have the right skills/talent
- [ ] Our existing tech debt prevents us from moving fast enough
- [ ] The AI strategy isn't clearly defined
- [ ] We're spread too thin across too many products
- [ ] I don't think there's a significant barrier
- [ ] Other: _____________

---

## Context Questions

### 14. Team / Product Area

_________________________________

### 15. Role (select one)
- [ ] Software Engineer (Frontend)
- [ ] Software Engineer (Backend)
- [ ] Software Engineer (Full Stack)
- [ ] QE / Quality Engineer
- [ ] DevOps / SRE / Infrastructure
- [ ] Product Manager
- [ ] Product Designer
- [ ] Engineering Manager / Lead
- [ ] Other: _____________

### 16. How long have you been at Mad Mobile?
- [ ] Less than 6 months
- [ ] 6 months – 1 year
- [ ] 1 – 2 years
- [ ] 2 – 4 years
- [ ] 4+ years

---

## Scoring Guide (for Adam's analysis)

**Three analysis dimensions:**

| Dimension | Survey Questions | What It Measures |
|---|---|---|
| **AI Adoption Maturity** | Q1, Q2, Q3, Q4, Q5, Q6 | How broadly and effectively AI tools are used today |
| **AI Strategy Clarity** | Q7, Q12, Q13 | Whether the organization has a credible, understood AI direction |
| **Tooling Health** | Q8, Q9, Q10, Q11a–d | Tooling sprawl, integration quality, gaps, and governance |

**Key cross-references:**
- Q7 (strategy clarity) vs. Q12 (delivery confidence) → Measures whether people believe in the strategy AND think they can execute it. A gap here is a credibility problem.
- Q1 (tool usage) vs. Q3 (productivity impact) → Separates adoption from value. High adoption + low impact = checkbox AI. Low adoption + high impact = untapped potential.
- Q9 (unused tools) + Q10 (missing tools) → Direct input for vendor rationalization and investment recommendations.
- Q13 (biggest barrier) → Forced-choice reveals the dominant constraint as perceived by practitioners. Compare leadership's answer in interviews vs. team's answer here.

**Segmentation:** Score by team, tenure, role, and product area. Compare CAKE/Restaurant vs. Concierge/Retail vs. Neo/AI vs. Payments teams. IC vs. manager splits on Q7 and Q12 reveal whether strategy communication is reaching the people who build.

*Note: No established academic benchmark for this instrument. Designed as a diagnostic specific to Mad Mobile's engagement context. Baseline scores become the benchmark for 30/60-day re-runs.*
