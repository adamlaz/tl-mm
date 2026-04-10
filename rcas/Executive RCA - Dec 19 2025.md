**<u>Executive RCA – CAKE System Production Incident (Admin Portal ,
Online Ordering and Payment Portal)</u>**

Date: December 19, 2025

Prepared By: James O, Zubair, Mati

Reviewed and approved By: Chathura R and Bill L (GM)

Systems Impacted: Admin Portal

**1. Overview**

On **December 19th**, Mad Mobile identified and resolved production
issues affecting the CAKE ecosystem where the admin portal was
affected.The issue has been resolved, and systems stabilized and
enhanced monitoring implemented to prevent recurrence.

**Teams Involved**

- DevOps

- Operations / Support

- CAKE Engineering

**Incident Owner:** Joel M.

Start time: 9:55 am

End time: 10:37 am

**2. Business Impact**

- **Incident - Admin Portal Issue**

  - All user base impacted and all functionality within admin portal
    unavailable.

  - Outage caused by an increased CPU utilization on the ESB services.

  - Customer Impact: temporary loss of access to Restaurant Admin to
    administrate their business.

- **Duration:** ~ \[42 mins total\].

- **Resolution:**

  - The ESB servers that had the cpu utilization issue were restarted to
    restore services. Once the servers were restarted, we saw a drop in
    the cpu utilization.

  - Approximately 1 hour later while continuing to closely monitor the
    situation, the precursor symptoms to the issue were identified
    again. The team reacted quickly before any customers were impacted
    and restarted the services again.

  - The team reviewed all available information at the time to document
    any/all possible cause for the issue. While no determination was
    able to be made on the call, the team identified several potential
    causes that need to be reviewed with the L3 team.

  - The team continues to closely monitor the issue to ensure system
    stability moving forward.

**3. Root Cause / Followup**

- **Added New ESB Instances**

  - Observed a significant increase in traffic on one of the ESB ALBs.

  - Added two new ESB instances to handle the increased load.

- **Analysis of ESB ALB Logs**

  - Identified an invalid access token request loop originating from POS
    devices.

  - Observed an increase in HTTP 500 errors from the Operator API.

  - Detected invalid requests originating from the Guest Manager
    servers.

- **Increased POS User Access Token Validity Period**

  - To reduce the likelihood of POS devices entering an invalid token
    request loop, the access token validity period was increased from
    **30 minutes to 6 hours**.

  - Retry loops were not observed after increasing the token validity
    period.

- **Offloading Frequent Invalid Requests at ALB Level**

  - Added ALB rules to the **connect.cake.net** load balancer to return
    HTTP 500 responses for the identified invalid request patterns.

- **Added WAF Rule (Count Mode)**

  - Introduced a WAF rule in **count mode** to monitor and throttle POS
    user access token requests in the event of retry loops.

- **Introduced New EC2 Instance Type for ESB**

  - The current EC2 instance type is a legacy/retired generation and is
    not recommended for ESB workloads.

  - Evaluated suitable upgrade options with similar or lower cost.

  - Introduced a new ESB server using the selected EC2 instance type and
    are currently monitoring its performance.

- **Continuous ESB Monitoring**

  - Continuously monitoring the ESB servers and restarting them as
    required.\
    Capturing snapshots and analyzing them for further insights.

**4. Resolution Summary**

- ESB servers were restarted several times to resolve the CPU
  utilization issue

- Restored Admin Portal and other related services and verified
  end-to-end service health.

- Observations made during the process so if the problem happens again
  we will know how to address the issue

- Created some new dashboards to help monitor the specific issue

- Root cause analysis underway

**5. Preventive Actions**

| **Category** | **Action** | **Status** |
|----|----|----|
| **Monitoring** | Enhanced monitoring to detect similar issues | ⚙️ In Progress |
| **Investigation** | Team to investigate a root cause week of 12/22 | 📅 Scheduled ETA – 12/22 |

**6. Current Status**

✅ **All systems operational**
