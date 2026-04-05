**Subject:** Re: Pre-onsite updates, requests, and next steps

Hi Ana (cc Chathura),

Quick Sunday evening update with where things stand and what I need before Monday.

**Status update:** Pre-work is in strong shape. Seven rounds of automated system analysis (V1–V7) across AWS, Bitbucket, Jira, and Confluence are complete. The engagement minisite now has 36+ interactive charts, a comprehensive people map (499 individuals across all systems), and detailed pages covering infrastructure, engineering, delivery, people, and the engagement itself — timeline, hypotheses, leadership structure, interview plan, and deliverables. Every onsite interview will lead with data.

---

**1. Grafana access** — Monday still works great. Looking forward to seeing the monitoring setup. Thank you for confirming with Matias.

**2. Enterprise Solutions org** — Still the biggest data gap. Chathura's CDO org chart PDF had Zubair's page mostly blank ("Enterprise Solution Org." with no names). This is the largest org (~58 people) and I currently have zero names below Zubair. **Chathura** — can you share the Enterprise Solutions team structure, or ask Zubair to send one directly? Even a rough list of names and roles would help. This is critical for interview prep and the people analysis.

**3. Pre-read documents** — Looking forward to whatever lands Monday. Retail and Neo/AI roadmaps especially, per Don's scope confirmation.

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

**9. Survey 5 — AI Adoption & Tooling** — **Chathura**, your survey intro email references 4 surveys. There's a 5th — AI Adoption & Tooling (16 questions, ~5 minutes, for all engineering, product, design, and QE). This feeds directly into the board deliverable and vendor rationalization assessment. Could you add it as a 5th link in your intro message? I'll have the Microsoft Forms link ready Monday morning. If you'd prefer to keep it at 4, let me know and I'll fold the most critical AI questions into the Engineering Practices survey instead.

---

None of this is blocking the onsite — I can work with what I have — but items 2, 6, 7, 8, and 9 would meaningfully improve the depth of the analysis.

Thanks,
Adam
