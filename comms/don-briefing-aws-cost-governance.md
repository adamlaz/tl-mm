# Don Briefing -- AWS Cost Governance

**For:** Don Session 3 (pre-onsite briefing)
**Source:** Ana Chambers' AWS Cost Savings spreadsheet (received April 9) + TL AWS inventory scan
**Bottom line:** The board's $50K/month AWS target is achievable. 60% is already done. The remaining gap is one account. But the process that got it there is person-dependent and has no owner going forward.

---

## THE NUMBERS

| Metric | Value |
|--------|-------|
| Board target | $50K/month AWS reduction by June 1 |
| Already achieved | $30.6K/month ($367K/yr) -- 71 initiatives, Sept 2025 to Apr 2026 |
| Gap to target | ~$19.4K/month |
| Monvia account | $25.9K/month -- single initiative closes the entire gap |
| Total AWS spend | ~$383K/month (March 2026, Cost Explorer) |

The $367K/year was real, verified work -- 12 closed accounts, 6 environment decommissions (TST2, TST3, POS2, Sandbox), 9 K8s extended support fixes, arm64 EKS migrations, tool removals (Sentry $21K/yr, Prismatic $24K/yr). Jira tickets exist for most of it. This is not aspirational -- it's done.

---

## THE STORY FOR DON

**Good news:** Engineering has capability. Ana and Matias self-directed $367K/year in AWS cost reductions through 71 bottom-up initiatives over 7 months. That's an 8% reduction against total AWS spend. Account closures, tool removals, environment decommissions, K8s support fee elimination -- disciplined, systematic work.

**The caveat:** It was person-dependent, not process-driven.

- Ana and Matias tracked it in a personal spreadsheet
- No formal cost review cadence
- No automated cost alerting or anomaly detection
- No budget target ownership (the board's $50K/month target doesn't appear to connect to the people doing the work)
- No executive review of what's been achieved or what remains

With Ana's role change to Chief of Staff, the operational owner of cost optimization is unclear. Matias may be carrying it forward solo -- one of my follow-up questions to Ana.

**The opportunity:** The remaining gap to the board target ($19.4K/month) is smaller than the Monvia account alone ($25.9K/month). Monvia runs legacy m1 hardware, contains a Leapset-era SVN instance, and was not in Ana/Matias' savings spreadsheet. Shutting it down or migrating it would exceed the board target in a single move.

Beyond Monvia, estimated remaining opportunity is $500K-$1M/year:

| Target | Est. Annual Savings |
|--------|-------------------|
| Monvia (legacy m1 hardware) | $311K |
| Marketplace SaaS subscriptions | ~$180K |
| Mgmt account RDS/ElastiCache/CloudWatch | ~$55K/month |
| Graviton migration (83% pre-Graviton EC2) | ~$80K |
| Lambda EOL runtime cleanup | ~$12K |

---

## HOW THIS MAPS TO HYPOTHESES

This finding maps directly to two hypotheses from the assessment framework:

- **Hypothesis F (Legacy Gravity):** Infrastructure accumulates waste because nobody inspects it on a schedule. 83% pre-Graviton EC2, m1 hardware from 2012, CloudFormation stacks from 2016 -- all still running. The cost savings work confirms the pattern and proves it's fixable.
- **Hypothesis G (Missing Cadence):** The cost optimization work succeeded precisely because Ana and Matias created their own cadence. But it was personal discipline, not organizational process. When Ana moved to Chief of Staff, the cadence left with her.

---

## WHAT TO DO WITH THIS ONSITE

1. **Matias interview** -- requested Ana add him to the PREFERRED batch. He knows the AWS estate at the operational level. Key questions: Monvia ownership, Savings Plan utilization, cost decision framework, remaining backlog.
2. **Chathura interview** -- ask whether he plans to formalize infrastructure cost management as CDO. The board's $50K/month target needs an owner in his org.
3. **Don's framing** -- this is a "capability exists, governance doesn't" finding. The savings work is genuinely impressive and should be recognized. The recommendation is structural: formalize a monthly cost review, assign ownership (likely Matias with Chathura oversight), implement automated alerting.

---

## 30/60/90 IMPLICATION

**Day 30:** Formalize monthly AWS cost review cadence. Assign ownership to Matias (or equivalent) with Chathura as exec sponsor. Set up automated cost anomaly alerting via AWS Budgets or Cost Anomaly Detection. Initiate Monvia investigation -- what runs there, who owns it, what's the shutdown/migration plan.

**Day 60:** Monvia shutdown or migration complete. Savings Plan review done. Board target of $50K/month confirmed achieved. Begin Graviton migration planning.

**Day 90:** First Graviton migration wave complete. Marketplace SaaS subscription review done. Monthly cost governance cadence has run 3 cycles and is self-sustaining.

---

## DELIVERABLE INTEGRATION

- **CEO Operating Brief:** Cost governance gap as a finding, Monvia as a quick win
- **Friction Register:** "Person-dependent cost optimization" as structural friction
- **30/60/90 Plan:** Cost governance cadence as Day 30 action
- **Board Deck:** $367K already saved (positive signal), path to $600K target, governance gap as risk/opportunity
