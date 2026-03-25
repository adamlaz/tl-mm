# DORA Quick Check — Mad Mobile Engineering Assessment

**What this measures:** Software delivery performance against Google's DORA research benchmarks (33,000+ professionals). Results classify teams as Elite / High / Medium / Low.

**Time:** ~3 minutes
**Who takes this:** Each engineering lead or manager — one per team/squad.
**Anonymity:** Your responses are anonymous. Only aggregate patterns are reported — nothing is attributed by name.
**Note:** This is a self-assessment. I'll cross-reference against actual system metrics during the engagement.

---

## Instructions

For each question, pick the answer that best describes your team's actual performance over the last 3 months. Be honest — there are no wrong answers, and this is not a performance review. The goal is a baseline we can measure against in 30/60 days.

---

### 1. Deployment Frequency

**How often does your team deploy code to production?**

- [ ] On-demand (multiple deploys per day)
- [ ] Between once per day and once per week
- [ ] Between once per week and once per month
- [ ] Between once per month and once every 6 months
- [ ] Fewer than once every 6 months

---

### 2. Lead Time for Changes

**How long does it typically take for a commit to reach production?**

- [ ] Less than one hour
- [ ] Between one hour and one day
- [ ] Between one day and one week
- [ ] Between one week and one month
- [ ] Between one month and six months
- [ ] More than six months

---

### 3. Change Failure Rate

**What percentage of deployments to production result in a degraded service or require remediation (hotfix, rollback, patch)?**

- [ ] 0–5%
- [ ] 6–15%
- [ ] 16–30%
- [ ] 31–45%
- [ ] 46–60%
- [ ] 61%+

---

### 4. Failed Deployment Recovery Time

**When a service incident or defect occurs in production, how long does it typically take to restore service?**

- [ ] Less than one hour
- [ ] Between one hour and one day
- [ ] Between one day and one week
- [ ] Between one week and one month
- [ ] More than one month

---

### 5. Reliability

**To what extent do you meet or exceed your reliability targets (SLAs/SLOs)?**

- [ ] We consistently meet or exceed them
- [ ] We meet them most of the time
- [ ] We meet them about half the time
- [ ] We rarely meet them
- [ ] We don't have formal reliability targets

---

## Context Questions

### 6. Team Name / Product Area
_________________________________

### 7. How many engineers are on your team?
_________________________________

### 8. What percentage of your team's time goes to maintenance/legacy work vs. new feature development?

Maintenance/Legacy: ___% | New Features: ___%

### 9. Is there anything that would significantly improve your team's delivery performance that leadership should know about?

_________________________________
_________________________________
_________________________________

---

## DORA Performance Benchmarks (for scoring)

| Metric | Elite | High | Medium | Low |
|---|---|---|---|---|
| Deploy Frequency | On-demand (multiple/day) | Weekly to monthly | Monthly to every 6 months | < once per 6 months |
| Lead Time | < 1 hour | 1 day to 1 week | 1 week to 1 month | 1 to 6 months |
| Change Failure Rate | 0–5% | 6–15% | 16–30% | 31–45% |
| Recovery Time | < 1 hour | < 1 day | < 1 week | > 1 month |
| Reliability | Meets/exceeds targets | Meets most of the time | ~Half the time | Rarely meets |

*Source: dora.dev/quickcheck — Accelerate State of DevOps Research*
