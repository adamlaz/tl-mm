**Subject:** Re: Pre-onsite updates + one new access request

Hi Ana,

Hope you're having a good weekend. A few updates and one new request.

**Status update:** The pre-work analysis is going well. I've now completed a comprehensive cross-system people map — 499 unique individuals identified across Bitbucket, Jira, Confluence, and AWS, merged with the org chart data from Don and Chathura. I have team assignments, collaboration networks, and risk analysis ready for the onsite. This will make every interview much more targeted.

---

**1. Grafana access** — Monday still works great. Looking forward to seeing the monitoring setup.

**2. Enterprise Solutions org** — Still the biggest gap. Chathura's PDF had Zubair's page mostly blank. This is the largest org (~58 people) and I currently have zero names below Zubair. If there's a version with that team's structure, or if Zubair can send one directly, that would be extremely helpful before the onsite.

**3. Pre-read documents** — Looking forward to whatever lands Monday. Retail and Neo/AI roadmaps especially, per Don's scope confirmation.

**4. Interview scheduling** — I'll have the full grid to you early this week. Updated for the April 3 reorg — Siegel removed, Strainick refocused as COO, Akshay and Guilarte added.

**5. Conference room** — Yes, a TV/screen would be very helpful. I'll be showing interactive charts and data during several conversations.

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

None of this is blocking the onsite — I can work with what I have — but items 6, 7, and 8 would meaningfully improve the depth of the analysis.

Thanks,
Adam
