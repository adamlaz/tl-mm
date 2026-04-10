**<u>Executive RCA – CAKE System Production Incident</u>**

Date: February 27, 2026

Prepared By: James O, Zubair, Mati

Reviewed and approved By: Chathura R and Bill L (GM)

Systems Impacted:

- Cake POS Payments

- Online Ordering Sites

- Restaurant Admin

- Payment Admin Console

- Guest Manager

**1. Overview**

On February 27<sup>th</sup>, the MadMobile team was notified of an issue
with Restaurant Admin not allowing users to login. Upon further review,
it was determined that in addition to Restaurant Admin a multitude of
other systems were also impacted. The team immediately convenied a Code
Red to resolve the matter.

**Teams Involved**

- AWS support

- Operations / Support

- CAKE Engineering

**Incident Owner:** James Oliver

Start time: 6:32 pm

End time: 8:08 pm

**2. Business Impact**

- **Restaurant Admin / PAC / Guest Manager**

  - All user base impacted and all functionality within aforementioned
    systems unavailable

- Cake Payments

  - Payments during this time period were processing slowly, but were
    still working

- **Duration:** ~ \[96 mins total\].

- **Resolution:**

  - The incident began at approximately 6:32pm. The team observed high
    SQL wait times, resulting in 100% cpu utilization on one of the
    primary databases in AWS\
    \
    <img src="Executive RCA - Feb 27 2026-assets/media/image1.png"
    style="width:5.53077in;height:2.13608in"
    alt="A graph with purple lines AI-generated content may be incorrect." />

  - At 6:41 pm, the team proceeding to execute our known runbook for
    resolving this issue. Runbook that was executed:

    - Restart affected database server

    - Restart leapset API service

    - Restart operator API service

    - Restart aggregator API service

  - At 6:50 pm the team completed executing our known runbook to address
    the issue. We observed at this time that service was restored to
    some systems, but others still remained down.

  - At 7:00 pm, engineering identified that the issue could be a timeout
    between leap set API service and key cloak service. We executed a
    restart on the keycloak service, but this did not resolve the issue
    with remaining services. The team began investigating for other
    causes

  - At 7:41 pm the team observed that the ESB servers while up and not
    throwing any errors didn’t seem to be processing any traffic. All
    ESB servers were subsequently restarted

  - At 8:00 pm, the cpu utilization on the database had reached 100%
    utilization again. We restarted all services again which finally
    restored all functionality around 8:08pm

    - Restart affected database server

    - Restart ESB servers

    - Restart leapset API service

    - Restart operator API service

    - Restart aggregator API service

  - At this point **all services were restored in production** and the
    team began root cause analysis to prevent it from happening again

  - At 8:30 pm the team started analyzing the problematic query that was
    running on the database server that was eating up all the system
    resources. The query was being run thousands of times from hundreds
    of merchants

  - At 9:30 pm the team identified the query was likely being run from
    each of the merchants POS and a fix would be needed to the Cake POS
    version to address. Logs were collected to be handed off to
    engineering to address

  - At 10:30pm the team created a plan to scale the ESB servers from 4
    -\> 7 nodes to handle the additional incoming volume, and double the
    capacity of the database server to avoid it falling behind. The
    database update required downtime so the Sri Lanka team executed
    this overnight during the maintenance window.

  - The team monitored all affected services closely over the weekend
    and no additional concerns presented themselves

  - Engineering worked throughout the weekend to identify the root cause
    and present a solution.

**3. Root Cause / Followup**

- Added New ESB Instances

  - Added tree new ESB instances to handle the increased load.

- Doubled the capacity of affected DB server

  - Doubled the CPU power of the DB server to help the server handle the
    incoming volume of requests

- Working with engineering to push a fix to all affected merchants

**4. Resolution Summary**

- AWS services were restarted several times to resolve the CPU
  utilization issue on the database server

- Restored Admin Portal and other affected services were restarted and
  verified end-to-end service health.

- Observations made during the process so if the problem happens again
  we will know how to address the issue

- Root cause analysis underway

**5. Preventive Actions**

| **Category** | **Action** | **Status** |
|----|----|----|
| **Investigation** | Team to investigate a root cause week of 3/2 | 📅 Scheduled ETA – 3/3 |
|  |  |  |

**6. Current Status**

✅ **All systems operational**
