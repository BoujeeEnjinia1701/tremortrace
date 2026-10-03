---
doc_id: TRT-DDR-001
title: TremorTrace TRL 2 review decisions
project: TremorTrace
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's 2026-09-25 decisions on the TRL 2 review points
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: O1 to O3 recorded as decided by Amish on 2026-10-02
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted (items D1 to D5, and O4 through TRT-DDR-002); items O1 to O3 decided by Amish on 2026-10-02 (TRT-DEC-001)

## Context

The TRL 2 review note (`docs/REVIEW.md`, sessions of 2026-09-24) listed design choices marked "Proposed, awaiting Amish". On 2026-09-25 Amish reviewed the review points for every repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." Every item that carried a recommendation is therefore decided as recommended. Items without a recommendation stay open.

## Options considered

Table 1. Items with a recommendation.

| # | Item | Options | Recommendation |
| --- | --- | --- | --- |
| D1 | Controller | Single nRF52840 module with built-in IMU, flash and charger (Seeed XIAO nRF52840 Sense class); or a separate nRF52 module and IMU breakout | Single module, no custom PCB |
| D2 | What the band stores | 10 s summaries only; raw data only; summaries with optional raw snippets | Summaries, with optional raw snippets for research |
| D3 | Phone route | Web Bluetooth page; native app | Web Bluetooth page first, native app later |
| D4 | Which wrist | Most affected wrist; both wrists | Most affected wrist first, both later |
| D5 | Data handling | Local-first, owner-controlled export; cloud service | Local-first, no cloud dependency (as R9 requires) |

## Decision

- **D1.** Decided by Amish, 2026-09-25: go with recommendation. One nRF52840 module with built-in LSM6DS3TR-C IMU, 2 MB flash and charger; no custom PCB for the first build.
- **D2.** Decided by Amish, 2026-09-25: go with recommendation. The band stores 32-byte 10 s summaries; a 256 kB area is reserved for raw snippets captured on demand (TRT-CAL-001, section 6).
- **D3.** Decided by Amish, 2026-09-25: go with recommendation. Sync and status use a web Bluetooth page first; a native app may follow.
- **D4.** Decided by Amish, 2026-09-25: go with recommendation. One band on the most affected wrist first; both wrists later.
- **D5.** Decided by Amish, 2026-09-25: go with recommendation. Data stays on the band and the owner's own devices; the owner controls any sharing.

Budget and pitch: the TRL 2 review made no recommendation to change either, so `budget_usd` stays at $150 and the pitch and problem lines are unchanged.

Items left open on 2026-09-25 (no recommendation was made); all three were decided on 2026-10-02 (TRT-DEC-001):

- **O1.** First co-design and validation partner: a movement disorders clinic, a patient association, or the OpenRatio network. **Decided by Amish, 2026-10-02:** the first candidate to approach is an academic movement disorders clinic with its own ethics board, introduced through the OpenRatio network, with the International Essential Tremor Foundation as the route to participants, shared with StillBand and SteadySleeve.
- **O2.** Confirmation of "OpenRatio" as a possible partner (part of O1). **Decided by Amish, 2026-10-02:** confirmed, described in soft, non-clinical wording as a research and educational network.
- **O3.** Approval of kit 1.3.1, whose forearm-for-scale rule for small objects replaces the 1.75 m person in the concept media. **Decided by Amish, 2026-10-02:** approved.

New item raised at TRL 3 (not part of the 2026-09-25 decision):

- **O4.** Charge current: the 50 mA setting (0.33 C, about 3.6 h, about 65 mW charger heat) or the 100 mA setting (0.67 C, about 1.8 h, about 130 mW). Recommendation: 50 mA, to keep the pod cool. Decided by Amish, 2026-09-25: go with recommendation (TRT-DDR-002).

## Consequences

- TRT-REQ-001 v0.3: R5 now counts 7 days at 16 h of wear per day alongside a raw-snippet reserve; R11 names the LED and the web Bluetooth page; the assumptions name the most affected wrist.
- TRT-PRC-001 v0.4: D1, D2, D3 and D5 are recorded as decided; first-order numbers are replaced by TRT-CAL-001 values.
- TRT-PRB-001 v0.3: the wrist question is closed; the partner question stays open.
- The design stops at TRL 3. TRL 4 is on hold by Amish's instruction.
