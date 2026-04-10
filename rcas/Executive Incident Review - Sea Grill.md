**<u>Executive RCA – CAKE POS at Sea Grill LLC</u>**

Date: February 18, 2026

Prepared By: James Oliver, Zubair Syed, Michael Lee

Reviewed and approved By: Chathura R and Bill Lodes

Systems Impacted: Cake POS

**1. Overview**

Beginning on February 8<sup>th</sup> and continuing through February
19<sup>th</sup>, the merchant Sea Grill (c0060-11524105) experienced
numerous issues causing disruption to their business.

- Sunday, 2/8 at 11:13am EST – First notified of an issue with the
  payment cube on register 6. It took till 2/9 to get an understanding
  of which payment cube was the issue from the merchant. On 2/9 the
  technical operations team prescribed a replacement of the device.
  Could not reach the merchant again until 2/11 when he was informed we
  need to replace the cube but it would take some time.

- Sunday, 2/8 at 11:17am EST – First notified of an issue where register
  5 locked up/froze in the middle of service. In addition, they were
  seeing an issue where tickets were not closing out. On 2/10 at 7:13am
  EST, the technical operations team diagnosed an issue with the network
  adapter on the POS failing. The recommendation was to first try
  rebooting the network to try to resolve the issue happening on
  register 5, but ultimately we would have to replace the device to
  resolve the hardware issue if the reboot was not successful. On
  February 11<sup>th</sup> a hardware replacement case was created to
  replace the POS.

- Thursday, 2/12 at 2:01pm EST – POS replacement processed and shipped
  out via UPS, scheduled for delivery on Friday 2/13 (tracking ID
  1ZXV41900196186455).

  - UPS attempted delivery Friday 2/13 but the restaurant was closed.
    CAKE contacted UPS to confirm the option for pickup at UPS location
    on Friday 2/13, then informed the merchant afterwards.

  - Merchant (Richard) declined pickup on Friday, and instead opted to
    wait for UPS to retry delivery on Saturday 2/14.

- Saturday, 2/14 at 11:25am EST - Merchant received a replacement POS
  that needed an upgrade to match the rest of his POS. Around 1pm EST
  technical operations team was able to help the register get past the
  upgrade and the register started indexing.

- Saturday, 2/14 at 5:45pm EST - Merchant called back in stating they
  were unable to take payments. 

  - Technical operations team reviewed and 5 out of 6 of their machines
    were offline in pulse

  - Found despite being offline in pulse, they were online, so we
    registered all of them in NinjaOne in case the last one went down in
    pulse too

  - After reviewing the network, merchant informed us everything started
    working again. He had also called Spectrum ISP and they had rebooted
    his network

  - Because the merchant had informed us that everything was operational
    after rebooting, investigations suspended

- Saturday, 2/14 at 10:57pm EST - Merchant called back into support
  again. 

  - All devices offline in pulse again

  - Significant network traffic updating couchDB documents

  - Technical operations team recommended powering off all the registers
    but 1 and allowing that one to come up. 

    - We suspected the new register they just got was causing issues
      trying to initialize, bringing down the local network

    - Technical Support team noted huge revision count and recommended
      couchDB cleanup procedure

    - Around Sunday, 12:45am EST we had registers 1-4 up and recommended
      bringing up registers 5 and 7 one at a time

- Sunday, 2/15 at 8:54am EST - Merchant called back into support again
  asking if they would experience issues

  - Expressed they had 80 walkouts the night before 

  - All registers were online and functioning at that time so advised
    them they should be ok but we would monitor closely

- Sunday, 2/15 at 9:40am EST - Merchant called back again with concern.
  Said there were 2 closed cash sequences

  - Although this fix could have waited, we paged on call and resolved
    the sequences

  - Technical operations team resolved the issue around 10:13am EST. Ran
    a health check on the network and reviewed payment logs and the
    merchant’s system was healthy

  - Advised the merchant to keep register 5 and 7 offline for the day.
    Close cash for the night and then turn them on before they leave for
    the day

- Sunday, 2/15 at 12:03pm EST - Merchant called back in unable to take
  payments due to the 24 hour payment limit

  - 12:50pm EST - merchant confirmed after Altaaf adjusted the limits he
    could take payments again

- Sunday, 2/15 at 1:10pm EST - Merchant called back again to tell us
  registers 5 and 7 were stuck on indexing (the ones we told him not to
  power on till after shift)

  - Advised him there was a lot of data and the recommendation was to
    handle overnight

  - Merchant said he really needed register 5 but would power down 7

  - The technical operations team monitored register 5 and it eventually
    powered on after churning through all the data

- Monday, 2/16 at 3:33pm EST - Merchant having issues closing cash

  - Advised him the team would handle it overnight. Please turn on
    register 7 at COB and the team would take care of everything for him
    overnight

    - When the technical operations team went to perform DB cleanup, the
      machine was not online so we could not proceed

- Tuesday, 2/17 at 3:57pm EST – Merchant advised to turn on register 7
  at COB so we could perform DB cleanup overnight.

  - Merchant advised of non-CAKE devices seen within the network, which
    is against the recommended CAKE setup – 6 devices, 3 switches, and 3
    security/camera devices

- Wednesday 2/18 at 12:15am EST – Db maintenance underway. POS 7 was
  still offline. According to the merchant the machine was powered on.
  Decision made to remove the device from the store and replace it. DB
  maintenance proceeded overnight and completed around 6am

  - Merchant was informed of this decision, and a follow up call was set
    for 11am EST on Wednesday 2/18.

- Wednesday 2/18 at 11am EST – Technical operations team contacted
  merchant to confirm that DB maintenance was successful

  - It was also confirmed that merchant will receive shipments
    containing a replacement printer, payment cube, and ELO POS on
    Thursday 2/19

- Thursday 2/19 at 2:15pm EST – Technical operations team followed up
  with merchant to confirm receipt of replacement printer, payment cube,
  and ELO POS and to assist with setup before the weekend.

  - Merchant (Tatyana) was not available to set up the hardware and
    instead rescheduled set up of the new hardware on Friday 2/20 at
    3:00pm EST (restaurant service also begins at this time)

**2. Business Impact**

**3. Root Cause / Followup**

When the initial research surrounding the case on 2/8 was done, it was
found that a replacement POS device was needed. That device was supplied
to the merchant in the following days. It is unknown at that point in
time if the CouchDB revision count was high, however by the time the
merchant plugged the new machine in when they received it the revision
count very likely was high.

Because of the high revision count, the new machine when it was brought
on board creating instability on the network as it began to sync all the
couch documents. Because this operation was happening in the middle of
the busy times for the merchant, it caused disruption for the merchant.
Once the new register was removed and the network stabilized, the issues
started going away.

The closed cash issue does happen from time to time, however the
technical operations team was able to handle this on behalf of the
merchant without any impact to business.

The issue with the payments being blocked occurred because the merchant
had exceeded pre-definited credit card processing limits for the
merchant in a 24 hour period. The limit was set to \$100,000 and the
merchant had exceeded that. The limit was raised by 250% to ensure this
would not occur again for the merchant.

The team is waiting on the original POS that needed to be replaced on
2/8, and the subsequent replacement POS to be returned to run full
diagnostics to understand why they failed.

**4. Resolution Summary**

CouchDB maintenance was completed and a replacement POS was sent again
to the merchant. The replacement was already onboarded to ensure when
the merchant opened the box all they would have to do is plug in the
machine and it would already be operational.

**5. Preventive Actions**

| **Category** | **Action** | **Status** |
|--------------|------------|------------|
|              |            |            |
|              |            |            |

**6. Current Status**
