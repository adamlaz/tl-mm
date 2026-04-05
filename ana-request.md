**Subject:** Re: Pre-onsite updates, requests, and next steps

Hi Ana (cc Chathura),

Quick Sunday evening update with where things stand and what I need before Monday.

**Status update:** Pre-work is in strong shape. Seven rounds of automated system analysis (V1–V7) across AWS, Bitbucket, Jira, and Confluence are complete. The engagement minisite now has 36+ interactive charts, a comprehensive people map (499 individuals across all systems), and detailed pages covering infrastructure, engineering, delivery, people, and the engagement itself — timeline, hypotheses, leadership structure, interview plan, and deliverables. Every onsite interview will lead with data.

---

**1. Grafana access** — Monday still works great. Looking forward to seeing the monitoring setup. Thank you for confirming with Matias.

**2. Enterprise Solutions org** — Still the biggest data gap. Chathura's CDO org chart PDF had Zubair's page mostly blank ("Enterprise Solution Org." with no names). This is the largest org (~58 people) and I currently have zero names below Zubair. **Chathura** — can you share the Enterprise Solutions team structure, or ask Zubair to send one directly? Even a rough list of names and roles would help. This is critical for interview prep and the people analysis.

**3. Pre-read documents** — Looking forward to whatever lands Monday. Retail and Neo/AI roadmaps especially, per Don's scope confirmation. Also, Don mentioned he'd share the investor/lender presentation deck — if that comes through you, that would be very helpful for framing the board deliverable.

**4. Interview scheduling** — I have the full 3-day grid ready: 18–21 sessions across April 13–15, organized by day (Monday: leadership, Tuesday: engineering deep dive, Wednesday: validation and gaps). I'll send it tomorrow for calendar booking. Updated for the April 3 reorg — Siegel removed, Strainick refocused as COO, Akshay and Guilarte added.

**5. Conference room** — Yes, a TV/screen would be very helpful. I'll be showing interactive charts and data during several conversations. Thank you for asking.

---

**6. NEW: Microsoft 365 / Azure AD access request**

For the people and organizational analysis, I need read access to the Microsoft 365 directory and calendar data via the Microsoft Graph API. This requires admin consent in your Azure AD tenant — my account (`adam.lazarus@madmobile.com`) currently can't authorize the permissions on its own due to your Conditional Access policies (which is good security practice, by the way).

**What I need approved:**

An IT admin (Rosen or Matias) to grant the following Microsoft Graph API permissions to the "Microsoft Graph Command Line Tools" app (app ID: `14d82eec-204b-4c2f-b7e8-296a70dab67e`) for my account:

- **User.Read.All** — Read the company directory (names, titles, departments, managers, office locations). This gives me the full employee list with reporting structure, which is critical for mapping the org accurately — especially Zubair's Enterprise Solutions team.
- **People.Read** — See organizational relationships and relevant contacts.
- **Calendars.Read** — Read-only access to calendars. Two purposes:
  1. **Interview scheduling**: I can check availability for the 18–21 interview slots during April 13–15 and send you a proposed schedule that avoids conflicts, rather than going back and forth on times.
  2. **Meeting pattern analysis**: Historical calendar data shows how teams actually coordinate — which groups meet regularly, where there are cross-team syncs, and where there are gaps. This feeds directly into the interaction analysis for the board deliverable.
- **Group.Read.All** or **Team.ReadBasic.All** — See which Microsoft Teams channels exist and their membership. This maps the informal communication structure.

**How to do it:** In the Azure AD portal (entra.microsoft.com), go to Enterprise Applications → search for "Microsoft Graph Command Line Tools" → Permissions → Grant admin consent. Alternatively, Rosen or Matias can run a PowerShell command — happy to provide the exact steps if that's easier.

**Scope and duration:** This is read-only access for my account only, limited to the engagement period. I won't modify any data. Happy to have the permissions revoked after April 25 when deliverables are complete.

---

**7. Incident reports / post-mortems** — I've been able to pull structured post-mortem documents from Confluence going back to 2020, and the data is excellent — 50 incidents parsed with root causes, affected systems, resolution timelines. But the trail largely stops after 2023. I found 26 structured RCAs in 2022, but only 5 in 2024 and 2 in 2025 (both in the Team Tesla space, not the original Taurus space where the earlier ones lived).

I'm hoping this means the incident review process migrated to a different tool or location rather than stopped entirely. Could you help me find out:
- **Did RCA/post-mortem documentation move somewhere?** Possible places: a Teams channel, Guru, a different Confluence space, a Jira project with an "Incident" issue type, PagerDuty, or Opsgenie?
- **Is there a current on-call or incident response tool** I should be looking at? (The Grafana/Mimir stack suggests alerting exists, but I can't see the alert rules or notification channels yet.)
- **Who would know?** If there's a specific person who owns the incident process now, I'd love to talk to them onsite — or just know where to look.

This is important for the board deliverable — incident response maturity is one of the key DORA metrics, and right now I can't tell if Mad Mobile got dramatically better at reliability (great news) or stopped documenting incidents (concerning news). Either answer is useful, but I need to know which one.

**8. CloudTrail access** — One more from the AWS side: could the audit role (`Global-Audit-RO`) get `cloudtrail:LookupEvents` permission added? Or is there a CloudTrail S3 bucket I can read directly? Deployment frequency from AWS is the one DORA metric I'm completely missing, and it would strengthen the board deliverable significantly.

---

---

**9. Survey 5 — AI Adoption & Tooling** — **Chathura**, your survey intro email references 4 surveys. There's a 5th — AI Adoption & Tooling (20 questions, ~5 minutes, for all engineering, product, design, and QE). This feeds directly into the board deliverable and vendor rationalization assessment. The survey is built and ready: https://forms.cloud.microsoft/Pages/DesignPageV2.aspx?origin=RevampFRE&subpage=design&id=ib_aDhNew0Kr1vaH6f4POuzhwTnhYKxDp5P7TQtHDhRUMDNHRTNRU05KRTdRWDJWTE41UFZEMkUxNi4u

Could you add it as a 5th link in your intro message? If you'd prefer to keep it at 4, let me know and I'll fold the most critical AI questions into the Engineering Practices survey instead.

**All 5 survey links for reference:**
- DORA Quick Check (9 questions): https://forms.cloud.microsoft/Pages/DesignPageV2.aspx?origin=RevampFRE&subpage=design&id=ib_aDhNew0Kr1vaH6f4POuzhwTnhYKxDp5P7TQtHDhRUQU9JNFJJMzg2R1dGUlhWRTYwODc1UURaVi4u
- Westrum Culture (7 questions): https://forms.cloud.microsoft/Pages/DesignPageV2.aspx?origin=RevampFRE&subpage=design&id=ib_aDhNew0Kr1vaH6f4POuzhwTnhYKxDp5P7TQtHDhRURjJXR01JU0Q5Tk8xSFNKUVFWMEIxQ1FSMC4u
- DevEx / DX Core 4 (23 questions): https://forms.cloud.microsoft/r/021mP98Sf9
- Pragmatic Engineer Test (15 questions): https://forms.cloud.microsoft/Pages/DesignPageV2.aspx?origin=RevampFRE&subpage=design&id=ib_aDhNew0Kr1vaH6f4POuzhwTnhYKxDp5P7TQtHDhRUNUtQWVRMWlZQRExUME1LMjNJM1lER0xaTC4u
- AI Adoption & Tooling (20 questions): https://forms.cloud.microsoft/Pages/DesignPageV2.aspx?origin=RevampFRE&subpage=design&id=ib_aDhNew0Kr1vaH6f4POuzhwTnhYKxDp5P7TQtHDhRUMDNHRTNRU05KRTdRWDJWTE41UFZEMkUxNi4u

---

None of this is blocking the onsite — I can work with what I have — but items 2, 6, 7, 8, 9, 14, and 15 would meaningfully improve the depth of the analysis.

---

**10. Vendor / SaaS spend data** — I've now identified **48 tools** across Mad Mobile's technology stack (up from 28 in the initial scan). The vast majority have unknown costs — only AWS and a few line items have real numbers. For the vendor rationalization section of the board deliverable, I need actual spend data.

**What would be most helpful:** An export from finance/procurement showing annual or monthly SaaS vendor spend. Even a rough summary by vendor would be transformative. The tools I'm most interested in are:

- **Atlassian** (Jira, Confluence, Bitbucket) — how many seats? Which tier (Standard/Premium/Enterprise)? Annual contract total?
- **Wiz.io** — annual contract? This is likely one of the larger non-AWS security line items ($100K–$300K range typical).
- **Datadog** — confirmed active for Concierge/Retail (app.datadoghq.com). What's the scope and annual cost?
- **Five9** — cloud contact center for CS. How many agent seats? Annual cost?
- **Salesforce** — how many licenses? Annual total?
- **Tyk API Gateway** — last renewal was 2023 at ~$35K/year. Is it current?
- **Snyk** — onboarded formally in Jan 2023 but adoption seems low. Is the contract still active? Annual cost?
- **Trend Micro Cloud One** — showing $1,438/month in the CAKE Dev AWS account. Is this intentional alongside Wiz?
- **Slack** — is the org on a paid plan alongside Microsoft Teams?
- **Figma** — how many editor seats?
- **TeamViewer** — annual cost for POS remote access?

I can provide the full 48-tool list with estimated pricing ranges if that helps the conversation with finance. Even partial data on the top 5 vendors would meaningfully strengthen the board deliverable.

**11. GitHub status** — Is the GitHub organization still active, or has everything migrated to Bitbucket? The internal Cake Engineering Tools documentation already flags this with the note "Can we get rid of this?" If Mad Mobile is still paying for GitHub alongside Bitbucket, that's an immediate savings opportunity.

**12. Observability consolidation** — I've identified **6 monitoring/observability tools**: Grafana (Mimir/Loki/Tempo), Datadog, Nagios, Munin, Graylog, and DB Cacti. Has anyone proposed consolidating these? Is there a roadmap? This is likely one of the bigger areas for both cost savings and operational simplification.

**13. Guru status** — Still active? How many users? The Restaurant deck mentions it but I can't confirm whether it's widely used or just a few teams.

---

Items 10–13 are specifically for the vendor/tooling rationalization that Don wants in the board deliverable. The estimated annual SaaS spend (excluding AWS) is somewhere in the **$350K–$800K range** based on public pricing — confirming actuals would let me narrow that to a real number with specific savings recommendations.

---

**14. Winmark project visibility** — I want to make sure I have visibility into all active development efforts ahead of the onsite. Don mentioned Jack Kennedy is working on a client delivery for Winmark — is there a Jira project, Confluence space, or Bitbucket repo I should be aware of? Just want to make sure I'm not missing any active workstreams in the analysis.

**15. Bloom Intelligence** — Don mentioned a potential partnership with Bloom Intelligence related to POS analytics and customer data. I'd like to understand what's been discussed so far so I can include it in the technology landscape assessment. **Chathura/Dulanjan** — are there any meeting notes, briefs, or evaluation materials from conversations with Bloom Intelligence (Will Wilson)? Even a quick summary of what's been discussed would be helpful.

---

Thanks,
Adam
