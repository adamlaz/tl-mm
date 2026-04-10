**<u>Executive RCA – CAKE POS at Fish Seafood and Raw Bar</u>**

Date: March 14, 2026 - March 15, 2026

Prepared By: James Oliver, Zubair Syed, Michael Lee

Reviewed and approved By: Chathura R and Bill Lodes

Systems Impacted: Cake POS

**1. Overview**

Beginning on March 14<sup>th</sup> at around 4:46pm Cake Support was
notified of an issue happening at Fish Seafood and Raw Bar,
c0060-10930527, where the POS machines were stuck at an initializing
screen. Prior to this, there were no associated cases or change
management tickets executed by the Mad Mobile team for this merchant.

- Saturday, 3/14/2026 at 4:46pm EST – The merchant called into Cake
  Support to notify of us an issue. L1 was informed that the merchant
  was having issues with power followed by a subsequent network reboot.

- Saturday, 3/14/2026 at 6:56pm EST – L1 support continued to work with
  the merchant after the network reboot to get the machines online. At
  this time it was noted that 5 of the 6 machines were stuck at the
  loading screen while the 6<sup>th</sup> machine was showing a LAN
  connection error. A long time was spent tracing cables but there was
  no clear way to understand where the connectivity issues could be at.
  This is a managed network that would require getting an onsite IT tech
  to troubleshoot the network.

<img
src="Executive Incident Review - Fish Seafood and Raw Bar-assets/media/image1.png"
style="width:4.30826in;height:5.74205in" />

- Saturday, 3/14/2026 at 5:28pm EST – L1 paged the on-call L2 resource
  to enlist help

- Saturday, 3/14/2026 at 6:00pm EST – L2 responded to page and began
  troubleshooting the issue with L1

- Saturday, 3/14/2026 at 6:10pm EST – L2 identified that all of the
  machines had expired bissa certificates. Updated the certificates on
  the 5 machines we could access

- Between 6:10pm and 7:40pm, the following was observed

  - The 5 online POS machines were showing that they were stuck at the
    UPGRADE_STEP

  - Some devices showed that they were in a failed upgrade state

  - The devices document had 10 devices in CouchDB, despite only having
    6 at the location. In addition, we found devices in pulse onboarded
    to the merchant that were not in the devices document. Actioned on
    this document to remove all the machines from the document that were
    not present at the location

  - Updated settings document to fix the incongruities of the
    actual_version/client_version to match the versions that were
    deployed

  - Several reboots along the way

- Saturday, 3/14/2026 at 7:40pm EST – Additional SL L2 was engaged to
  help with the incident

- Saturday, 3/14/2026 at 7:30pm EST – The team noted that several
  devices were missing in pulse and were intermittently showing up and
  disappearing

- Saturday, 3/14/2026 at 7:45pm EST – Noticed in CouchDB that 2 devices
  were present in the devices document, while 4 were in the deviceID
  documents. The missing 2 devices were added to the device document

- Saturday, 3/14/2026 at 8:00pm EST – By deviceID document in CouchDB
  was showing the incorrect software versions for some devices. Manually
  corrected that document to have the correct versions

- Saturday, 3/14/2026 at 8:30pm EST – Register 14 became available for
  the merchant. The merchant immediately took over this machine and
  began to process orders

- Saturday, 3/14/2026 at 9:30pm EST – In the logs the location showed
  both static and dynamic master = false. Changed the configuration to
  be a static master and used the working register 14 as the master.
  Advised the merchant we would need help rebooting the network for the
  change to take affect. Merchant advised they may not be able to get
  anyone till the following day

- Sunday, 3/15/2026 at 12:20am EST – Merchant advised they were able to
  get an IT Technician on site. The tech had moved register 17 directly
  to the router. We asked them to instead use register 14 since it was
  the master. Once connected it took a long time to load. We recommended
  doing a DB clean up overnight.

  - Note that at the onset of the incident we had noted high revision
    counts in CouchDB but were unable to address in the middle of dinner
    service

- Sunday, 3/15/2026 at 2:20am EST – IT Technician was finally able to
  get all devices connected to the network again. DB maintenance was
  green lit to begin

- Sunday, 3/15/2026 at 4:30am EST – DB Cleanup completed. LAN connection
  issue persisted

- Sunday, 3/15/2026 at 5:30am EST – Code Blue started. L3 was engaged to
  assist with the issue

- Sunday, 3/15/2026 at 5:45am EST to 8:45am EST – More inconsistencies
  were found in the settings, devices, device upgrade info documents in
  CouchDB. L3 got clean copies of the documents and manually rebuild all
  the documents.

- Sunday, 3/15/2026 at 9:22am EST – All registers were successfully
  onboarded again and available for merchant use

**2. Business Impact**

> During the duration of the outage from Saturday 4:46pm EST till close,
> the merchant was unable to use ALL 6 registers at the location. All
> registers were back online prior to the start of the business day on
> Sunday.

**3. Root Cause / Followup**

To start the event, a power outage triggered a full network reboot. It
is unclear at this point why this may have precipitated so many issues
with the CouchDB documents. More investigation is required to find the
root cause

Follow-ups:

- Review syncing events for the cluster during this time period to
  investigate how the CouchDB documents ended up in such a corrupted
  state

- Confirm the merchant is now transacting successfully and the volume of
  transactions on Sunday match the prior Sunday

**4. Resolution Summary**

The merchant is presently back online and appears to not have any
further issues. The merchant was without their POS system for
approximately 4 hours on Saturday night. After the system became online
again, it does appear that the merchant began processing orders in the
system and paying for them by manually keying in card numbers.

**5. Preventive Actions**

| **Category** | **Action** | **Status** |
|--------------|------------|------------|
|              |            |            |
|              |            |            |

**6. Current Status**

Resolved pending further investigation into the root cause
