# Executive RCA Pattern Analysis — Onsite Reference

**Generated:** April 9, 2026
**Source:** 5 Executive RCA documents from Chathura (Dec 2025 – Mar 2026)
**Purpose:** Case trace reference material for onsite interviews (April 13–15)

---

## Incident Summary

| # | Date | Incident | Duration | Severity | Owner | Root Cause |
|---|------|----------|----------|----------|-------|------------|
| 1 | Dec 19, 2025 | Admin Portal outage | 42 min | Platform-wide | Joel M. | POS token retry loop → ESB CPU spike |
| 2 | Feb 8–19, 2026 | Sea Grill cascading failure | ~12 days | Single merchant | James Oliver | CouchDB revision bloat + new device sync |
| 3 | Feb 27, 2026 | Multi-system outage (Code Red) | 96 min | Platform-wide | James Oliver | POS query flood → DB CPU 100% |
| 4 | Mar 14–15, 2026 | Fish Seafood POS failure (Code Blue) | ~17 hours | Single merchant | James Oliver | Expired certs + CouchDB corruption |
| 5 | Mar 24, 2026 | Toastique OLO failure | 3 days | Single location | James Oliver | Modifier group not OLO-enabled |

---

## Failure Class 1: ESB / Database Overload (Dec 19, Feb 27)

**Pattern:** POS devices generate excessive request volume that overwhelms the platform's ESB and database layers. Same failure mode, 70 days apart.

### Dec 19, 2025 — Admin Portal (42 min)

| Time | Event |
|------|-------|
| 9:55 AM | Start. ESB CPU spike. |
| 10:37 AM | End. ESB servers restarted. |
| +1 hour | Precursor symptoms return; team restarted before customer impact. |

**Root cause:** POS devices entered invalid access token request loop. Generated excessive load on ESB ALBs. Operator API returning HTTP 500. Guest Manager servers sending invalid requests.

**Fix applied:**
- Token validity extended 30 min → 6 hours
- WAF rule added in count mode (monitor/throttle POS token requests)
- ALB rules on connect.cake.net to return HTTP 500 for known invalid patterns
- 2 new ESB instances added
- New EC2 instance type evaluated (legacy type is retired generation)

**Incident owner:** Joel M. (not James Oliver — identity/role unknown)

### Feb 27, 2026 — Multi-System (96 min, Code Red)

| Time | Event |
|------|-------|
| 6:32 PM | Start. High SQL wait times. DB CPU 100%. |
| 6:41 PM | Runbook executed: restart DB, Leapset API, Operator API, Aggregator API. |
| 6:50 PM | Partial recovery only. |
| 7:00 PM | Keycloak timeout suspected. Keycloak restarted — no improvement. |
| 7:41 PM | ESB servers up but not processing traffic. All ESB restarted. |
| 8:00 PM | DB CPU 100% again. |
| 8:08 PM | Full restart: DB + ESB + Leapset + Operator + Aggregator. **All restored.** |
| 8:30 PM | Query analysis: problematic query running thousands of times from hundreds of merchants. |
| 9:30 PM | Query originates from POS. Fix requires POS version update. Logs to engineering. |
| 10:30 PM | Plan: ESB 4→7 nodes, double DB capacity. Sri Lanka team executes overnight. |

**Root cause:** POS-originated query running thousands of times across hundreds of merchants → DB CPU 100% → cascade to all dependent services.

**Fix applied:**
- Multiple service restarts (reactive)
- ESB scaled from 4 to 7 nodes
- DB capacity doubled (downtime required, SL team overnight maintenance window)
- POS version fix needed — **status unknown**
- Investigation scheduled week of 3/2 — **no documented resolution**

**Systems impacted:** Restaurant Admin, PAC, Guest Manager, Online Ordering, Cake Payments (slow but working), Keycloak, ESB, Leapset API, Operator API, Aggregator API.

### Cross-reference: Historical Confluence RCAs

- **DE-98472 (Aug 2022):** 502 on admin.cake.net, 432 min, Cloud Services — same Admin Portal surface
- **DE-98499 (May 2022):** market.cake.net down, EC2 status check failure — same infrastructure class
- **DE-98448 (Jul 2022):** Pulse 503, 322 min — ESB overload pattern

### Key question for onsite

> "The Dec 19 and Feb 27 incidents are the same failure class — POS devices overwhelming ESB/DB. The Dec fix (token validity, WAF rules) didn't prevent the Feb recurrence. The Feb investigation was scheduled for 3/2. **What happened?** Did the POS version fix ship?"

Ask: James Oliver (T6), Chathura (M), Zubair (T), Randy Brown (T)

---

## Failure Class 2: CouchDB Document Corruption (Sea Grill, Fish Seafood)

**Pattern:** CouchDB — the local POS sync layer — enters a corrupted state with high revision counts, phantom device entries, and document inconsistencies. Sync storms collapse local restaurant networks during peak hours.

### Sea Grill (Feb 8–19, 2026, ~12 days)

Merchant ID: c0060-11524105

| Date/Time (EST) | Event |
|-----------------|-------|
| Sun 2/8, 11:13 AM | Payment cube issue on register 6. |
| Sun 2/8, 11:17 AM | Register 5 froze mid-service. |
| Mon 2/10, 7:13 AM | Network adapter failure diagnosed on register 5. |
| Thu 2/12, 2:01 PM | Replacement POS shipped (UPS 1ZXV41900196186455). |
| Fri 2/13 | UPS delivery attempted — restaurant closed. Merchant declined pickup. |
| Sat 2/14, ~11:25 AM | Replacement POS received. Upgrade required. ~1 PM operational. |
| Sat 2/14, 5:45 PM | **Unable to take payments.** 5/6 machines offline in Pulse. Registered in NinjaOne. Spectrum ISP rebooted network. |
| Sat 2/14, 10:57 PM | All devices offline in Pulse again. CouchDB traffic spike. Suspected new register causing sync storm. |
| Sun 2/15, 12:45 AM | Registers 1–4 up. Advise bring up 5 and 7 one at a time. |
| Sun 2/15, 8:54 AM | Merchant reports **80 walkouts** previous night. |
| Sun 2/15, 12:03 PM | **$100K payment limit hit.** Altaaf (SL) raised 250%. |
| Sun 2/15, 1:10 PM | Registers 5 & 7 stuck indexing (merchant powered on against advice). |
| Mon 2/16, 3:33 PM | DB cleanup planned. Machine not online — cleanup failed. |
| Tue 2/17, 3:57 PM | Non-CAKE devices found: 6 devices, 3 switches, 3 cameras. |
| Wed 2/18, 12:15 AM | DB maintenance. POS 7 still offline. Decision: remove and replace. |
| Wed 2/18, 11:00 AM | DB maintenance confirmed successful. |
| Thu 2/19, 2:15 PM | Replacement hardware follow-up. Merchant rescheduled setup. |

**Root cause:** CouchDB high revision count. New replacement POS triggered sync storm during peak hours, collapsing local network. Payment limit exceeded due to extended outage.

**Notable details:**
- Pulse showed devices offline when they were actually online (trust issue)
- NinjaOne used as backup when Pulse was unreliable
- Non-CAKE devices on network violating recommended setup
- Investigation suspended prematurely after Spectrum ISP fix
- **Preventive Actions: EMPTY**

### Fish Seafood and Raw Bar (Mar 14–15, 2026, ~17 hours)

Merchant ID: c0060-10930527

| Time (EST) | Event |
|------------|-------|
| Sat 3/14, 4:46 PM | Support notified. Power outage + network reboot. |
| Sat 3/14, 5:28 PM | **L1 paged on-call L2.** |
| Sat 3/14, 6:00 PM | L2 responded. |
| Sat 3/14, 6:10 PM | **Expired Bissa certificates** found on 5 machines. Updated. |
| Sat 3/14, 6:10–7:40 PM | 5/6 stuck at UPGRADE_STEP. CouchDB: 10 devices vs 6 physical. Cleaned. Settings doc version mismatches fixed. Reboots. |
| Sat 3/14, 7:30 PM | Devices intermittent in Pulse. |
| Sat 3/14, 7:40 PM | **SL L2 engaged.** |
| Sat 3/14, 7:45 PM | CouchDB: 2 in devices doc vs 4 in deviceID docs. Fixed. |
| Sat 3/14, 8:00 PM | deviceID doc: wrong software versions. Manually corrected. |
| Sat 3/14, 8:30 PM | Register 14 available. Merchant began processing. |
| Sat 3/14, 9:30 PM | Static/dynamic master both false. Set static master = register 14. |
| Sun 3/15, 12:20 AM | IT on site. DB cleanup recommended. High revision counts. |
| Sun 3/15, 2:20 AM | All devices on network. DB maintenance started. |
| Sun 3/15, 4:30 AM | DB cleanup done. LAN issue persisted. |
| Sun 3/15, 5:30 AM | **Code Blue. L3 engaged.** |
| Sun 3/15, 5:45–8:45 AM | L3 rebuilt settings, devices, device upgrade info docs from clean copies. |
| Sun 3/15, 9:22 AM | **All registers onboarded. Resolved.** |

**Root cause:** Power outage triggered CouchDB document corruption. Compounded by expired Bissa certificates, phantom device entries (10 vs 6), version mismatches, and master assignment failure.

**Escalation path (most detailed in the set):**
L1 (4:46 PM) → page L2 (5:28 PM, 42 min) → SL L2 (7:40 PM, 2.5 hrs) → Code Blue / L3 (5:30 AM, ~13 hrs from start)

**Notable details:**
- Each escalation tier discovered new problems previous tiers missed
- Merchant processed orders with manual card keying during partial outage
- Both merchants are cluster c0060 — investigate if cluster is particularly fragile
- **Preventive Actions: EMPTY**

### Cross-reference: Historical Confluence RCAs

- **DE-98497 (Sep 2022):** Expired certificate on HA Proxy broke CouchDB-to-Merchant API sync. Same class as Fish Seafood Bissa cert expiry. **3.5 years, same root cause class.**
- **DE-98480 (Aug 2022):** CouchDB failover replication issue, C30 cluster, 220 min
- **DE-98474 (Aug 2022):** Report sync stopped for C30 cluster, 74 min
- **DE-98449 (Jul 2022):** Report sync stopped for C30 cluster, 330 min
- **DE-98445 (Jun 2022):** Report sync stopped for merchants, 90 min

**CouchDB fragility is a 4-year pattern.** The 2022 incidents were cluster-level sync failures. The 2026 incidents are merchant-level document corruption. Same underlying system, different failure modes.

### Key question for onsite

> "CouchDB is the local POS sync layer and has been the root cause in at least 7 incidents across 4 years. Is revision count monitoring automated? Is there a CouchDB health check in the deployment pipeline?"

Ask: Randy Brown (T), James Oliver (T6), Chathura (M)

---

## Failure Class 3: Configuration / Onboarding (Toastique)

### Toastique (Mar 20–23, 2026, 3 days)

| Time | Event |
|------|-------|
| Mar 20, 2:31 PM | Start. Paytronix orders rejected by POS. New location onboarding. |
| Mar 20, 3:39 PM | Zyxel router offline 127 days. Merchant unaware (ownership change). |
| Mar 20, 4:46 PM | L2: non-standard network. **L1 told merchant it was a Paytronix issue.** |
| Mar 20–22 | **No action.** Assumed merchant fixing network + working with Paytronix. |
| Mar 22, 12:15 PM | Merchant called back. Still no orders. |
| Mar 22, 12:55 PM | L2: order/tax config issue found. |
| Mar 23, 2:50 AM | Tax error on modifier. MC status flag fixed. |
| Mar 23, 12:29 PM | **Root cause: "Coffee Extras" modifier group not OLO-enabled.** |
| Mar 23, 1:04 PM | Resolved. |

**Response issues:**
- L1 misattributed to Paytronix. Root cause was CAKE config.
- 2-day communication gap (assumed merchant was fixing the issue)
- Multiple issues found sequentially (network, taxes, MC flag, modifier group) — no holistic diagnostic

**Cross-reference:**
- **DE-98431 (Mar 2022):** "Paytronix Orders Did Not Push to the POS" at Ike's — same integration surface, same class
- **DE-98434 (Apr 2022):** Guest Manager stuck on loading screen — similar merchant-facing POS failure

### Key question for onsite

> "On the Toastique incident, L1 told the merchant it was a Paytronix issue and paused for 2 days. The root cause was a CAKE modifier group config. How does L1 decide when to close vs. escalate?"

Ask: James Oliver (T6), Michael Lee (W6)

---

## Broken Learning Loop — Preventive Actions Analysis

| Incident | Preventive Actions Status |
|----------|--------------------------|
| Dec 19 | Enhanced monitoring: "In Progress." Investigation ETA 12/22: "Scheduled." |
| Sea Grill | **EMPTY TABLE** |
| Feb 27 | Investigation week of 3/2: "Scheduled ETA 3/3." |
| Fish Seafood | **EMPTY TABLE** |
| Toastique | **EMPTY TABLE** |

**Zero completed preventive items across all 5 documents.**

The RCA template is being used consistently — all 5 follow the same 6-section structure (Overview, Business Impact, Root Cause, Resolution Summary, Preventive Actions, Current Status). The problem is not template adoption; it's follow-through.

This corroborates:
- 0% Jira Root Cause Category field population (customfield_10382)
- Confluence RCA process largely stopping after 2023 (Taurus space)
- Sprint retrospectives extracted but action items not tracked

---

## Technology Systems Discovered

| System | Type | Notes from RCAs |
|--------|------|-----------------|
| ESB | Enterprise Service Bus | Instance counts: 4→7 after Feb 27. Legacy EC2 instance type. |
| Keycloak | Identity/auth | Timeout observed Feb 27. Only appearance in RCA set. |
| Leapset API | Legacy service | Still in production (Feb 27 restart sequence). |
| Operator API | Service | HTTP 500 errors during Dec 19 overload. |
| Aggregator API | Service | Part of Feb 27 restart sequence. |
| CouchDB | Edge database | Local POS sync. Device docs, deviceID docs, settings docs, upgrade info docs. |
| Pulse | Remote management | Showed devices offline when actually online (trust issue). |
| NinjaOne | Backup remote mgmt | Used when Pulse unreliable. Third-party. |
| Bissa certificates | POS cert system | Expired on Fish Seafood machines. No automated renewal detected. |
| connect.cake.net | ALB | POS-to-cloud connectivity. ALB rules added Dec 19. |
| Zyxel | Edge networking | Router offline 127 days at Toastique. |

---

## Onsite Case Trace Candidates (Ranked)

### 1. Feb 27 → Dec 19 Recurrence (STRONGEST)

**Why:** Same failure class, 70 days apart, no root cause fix documented. Investigation scheduled 3/2 with no follow-up. POS version fix identified as needed but status unknown. Perfect for tracing: "What happened after this RCA?"

**Ask:** James Oliver (T6), Zubair (T), Chathura (M), Randy Brown (T)

### 2. Fish Seafood Code Blue (MOST COMPLEX ESCALATION)

**Why:** Full L1→L2→SL L2→Code Blue/L3 escalation documented minute-by-minute. Each tier found new problems. L3 manually rebuilt CouchDB from clean copies. Tests whether escalation process works or each tier starts fresh.

**Ask:** James Oliver (T6), Michael Lee (W6)

### 3. CouchDB Systemic Pattern (4-YEAR PATTERN)

**Why:** CouchDB incidents in 2022 (4+ cluster-level sync failures) and 2026 (2 merchant-level corruption events). Same underlying system, different failure modes. Tests whether the architecture can evolve or is frozen.

**Ask:** Randy Brown (T), Chathura (M), Kyle Budd (T7)

### 4. Toastique Onboarding Failure (CUSTOMER EXPERIENCE)

**Why:** New location onboarding failed due to config issue. L1 misattributed. 3-day resolution. Tests onboarding quality and support diagnostic accuracy.

**Ask:** James Oliver (T6), Michael Lee (W6), Strainick (M, COO — owns onboarding)

---

## Open Questions for Onsite

1. What happened with the Feb 27 investigation scheduled for week of 3/2?
2. Did the POS version fix (identified Feb 27) ship?
3. Is CouchDB revision count monitoring automated?
4. What triggers Code Red vs Code Blue? Different severity or inconsistent naming?
5. Who is Joel M. (Dec 19 incident owner)?
6. Are Bissa certificate renewals automated or manual?
7. Both Sea Grill and Fish Seafood are cluster c0060 — is that cluster particularly fragile?
8. How does the team track RCA preventive actions to completion?
9. Where did the RCA process go after Taurus space stopped in 2023?
10. Does Bill Lodes (outgoing CRO, reviewed all 5) still participate in incident review as a consultant?
