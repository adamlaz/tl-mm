# Developer Experience (DevEx) Survey — Mad Mobile

**What this measures:** Developer experience across three dimensions — Feedback Loops, Cognitive Load, and Flow State. Results map to four executive-ready dimensions: Speed, Effectiveness, Quality, and Impact (DX Core 4).

**Time:** ~5 minutes
**Who takes this:** Individual contributors — software engineers, QE engineers, DevOps/SRE. Not managers — this captures the IC perspective.
**Anonymity:** Your responses are anonymous. Only aggregate patterns and team-level trends are reported — nothing is attributed by name.

---

## Instructions

Rate each statement based on your experience at Mad Mobile over the last 3 months. Answer based on how things actually are, not how you wish they were.

**Scale:** 1 = Strongly Disagree | 2 = Disagree | 3 = Neutral | 4 = Agree | 5 = Strongly Agree

---

## Section A: Feedback Loops

*How fast do you get signal on whether your work is correct, complete, and valuable?*

### 1. I can validate my code changes quickly through automated tests and CI/CD.

| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|

### 2. Code reviews on my team happen promptly and don't create long waiting periods.

| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|

### 3. When I deploy to production, I get clear, fast feedback on whether the deployment succeeded or caused issues.

| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|

### 4. When I have a question about requirements or scope, I can get an answer quickly without waiting days.

| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|

---

## Section B: Cognitive Load

*How much mental effort is required to navigate the codebase, tools, and processes?*

### 5. I understand the codebase(s) I work in well enough to be productive without constantly asking for help.

| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|

### 6. Our development tools and processes are well-documented and easy to set up.

| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|

### 7. I rarely have to context-switch between unrelated projects or tasks during the same day.

| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|

### 8. The number of different systems, languages, and tools I need to work with is manageable.

| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|

### 9. I don't spend excessive time on toil (manual processes, workarounds, or fighting infrastructure).

| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|

---

## Section C: Flow State

*How often can you achieve sustained, focused work without interruption?*

### 10. I can typically get 2+ hours of uninterrupted focus time during my workday.

| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|

### 11. Meetings and interruptions don't frequently break my concentration during focused work.

| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|

### 12. I feel productive most days — I can see the impact of my work.

| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|

---

## Section D: Satisfaction & Impact

### 13. I would recommend Mad Mobile as a good place to work for an engineer.

| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|

### 14. I believe the work I'm doing matters to the company's success.

| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|

---

## Context Questions

### 15. Team / Product Area
_________________________________

### 16. Role (select one)
- [ ] Software Engineer (Frontend)
- [ ] Software Engineer (Backend)
- [ ] Software Engineer (Full Stack)
- [ ] QE / Quality Engineer
- [ ] DevOps / SRE / Infrastructure
- [ ] Other: _____________

### 17. How long have you been at Mad Mobile?
- [ ] Less than 6 months
- [ ] 6 months – 1 year
- [ ] 1 – 2 years
- [ ] 2 – 4 years
- [ ] 4+ years

### 18. What is the single biggest thing that slows you down on a daily or weekly basis?

_________________________________
_________________________________
_________________________________

---

## Scoring Guide (for Adam's analysis)

**DX Core 4 Mapping:**

| Executive Dimension | Survey Questions | What It Measures |
|---|---|---|
| **Speed** | Q1, Q2, Q3 (Feedback Loops) | How fast developers get signal on their work |
| **Effectiveness** | Q5, Q6, Q8, Q9 (Cognitive Load) | How much friction exists in the development environment |
| **Quality** | Q4, Q7 (Cognitive Load + Feedback) | Whether developers have the clarity and focus to produce quality work |
| **Impact** | Q12, Q13, Q14 (Flow + Satisfaction) | Whether developers feel productive and connected to outcomes |

**Segmentation:** Score by team, tenure, and role to identify patterns. Compare CAKE/Restaurant team scores to Concierge/Retail and Neo/AI teams.

*Source: Noda, Storey, Forsgren, Greiler — "DevEx: What Actually Drives Productivity," ACM Queue, 2023*
