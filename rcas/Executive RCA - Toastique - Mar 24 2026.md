**<u>Executive RCA – CAKE System Production Incident</u>**

Date: March 24, 2026

Prepared By: James O, Michael L, Megan M., Alexis M

Reviewed and approved By: Chathura R and Bill L (GM)

Systems Impacted:

- Cake OLO via Paytronix

**1. Overview**

On March 20<sup>th</sup>, the Cake Support team was notified of an issue
with orders being visibile in Paytronix but not reaching the POS for a
specific toastique location. The orders were being rejected by the POS
system. This caused an issue as the location was scheduled to open for
business on March 21<sup>st</sup>.

**Teams Involved**

- Level 1 Cake Support

- Level 2 Cake Support

- CSM

**Incident Owner:** James Oliver

Start time: March 20<sup>th</sup>, 2026 at 2:31PM

End time: March 23<sup>rd</sup>, 2026 at 3:30PM

**2. Business Impact**

- **OLO Orders via Paytronix**

  - All orders were being rejected by the POS. This was a new location
    onboarding and revenue could have been impacted as a result.

- **Duration:** ~ \[3 days\].

- **Resolution:**

  - March 20, 2026 at 2:31pm – Cake Support first notified of an issue
    affecting Paytronix orders from being placed successfully.

  - March 20, 2026 at 3:39pm – Cake Support noted that the Zyxel router
    had been offline for 127 days and the setup must have not been
    using. The merchant was unaware of any Zyxel router on the premises.
    There was a change of ownership and the new owner was not aware of
    the Zyxel. A new router has subsequently been shipped

  - March 20, 2026 at 4:46pm – Cake L2 confirmed that the network was
    not setup correctly. To this day, the store remains on a non-Cake IP
    address indicating a non-standard setup. L1 communicated back to
    Toastique that this was a Paytronix issue and to work with their
    support.

> At this point in the process, the Cake Support team was assuming that
> the Toastique team was working on correcting the network setup as well
> as speaking with Paytronix to correct the issue. No further action
> took place until we heard back from Toastique

- March 22, 2026 at 12:15pm – Toastique called back into the support
  line to let us know that they still were not getting any orders to the
  location.

- March 22, 2026 at 12:55pm – L2 observed that there was an issue with
  the order and taxes that were configured for the merchant

- March 22, 2026 at 1:15pm – L2 advised merchant to reach out to
  Paytronix about the tax issue we were seeing. Support spoke to
  Toastique to have them ask Paytronix if the active taxes had been set
  up.

- March 23, 2026 at 2:50am – Saw an error being returned because of an
  error retrieving taxes for a specific modifier. The L2 team at this
  point did fix a configuration issue with the MC status flag. L2 was
  unable to test the fix at this point because the location was closed.
  Advised toastique to try out a test transaction when the location was
  open.

- March 23, 2026 at 7:20am – Ask to toastique to please test a
  transaction.

- March 23, 2026 at 11:32am – Merchant confirmed to us that the issue
  was still occuring

- March 23, 2026 at 12:29pm – Cake L2 support identified the root cause
  – a misconfiguration of the “Coffee Extras” modfiier group. OLO was
  not enabled for the modifier group.

- March 23, 2026 at 1:04pm – Cake Support completed testing with the
  merchant and confirmed that the issue was resolved.

**3. Root Cause / Followup**

- A misconfiguration of the menu had occured that prevented the orders
  from properly accepting. The modifier group “coffee extras” was not
  configured for OLO, so orders that included a modifier from this group
  were rejecting.

> What was the issue on Friday? The account recently became under new
> ownership. The merchant was not aware of any Zyxel router and
> therefore is on a non-standard Cake setup. The team thought the issue
> was being caused by a Paytronix issue. On Sunday was when the issue
> was re-presented to the team and we began looking for other sources of
> the issue.
>
> Were they set-up properly? No.
>
> Why did we go back and say it’s not an issue on our side? After
> triaging the issue, we suspected the issue might be on their side.
>
> What did we finally fix yesterday? Yesterday L2 updated the modifier
> group to include it as an OLO enabled.

**4. Resolution Summary**

- Configuration for the modifier group was resolved and orders began
  flowing through.

**5. Preventive Actions**

| **Category** | **Action** | **Status** |
|--------------|------------|------------|
|              |            |            |
|              |            |            |

**6. Current Status**

✅ **All systems operational**
