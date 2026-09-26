---
doc_id: TRT-DDR-002
title: TremorTrace recommendations accepted
project: TremorTrace
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's acceptance of all open recommendations (2026-09-25)
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted (items D6 and D7); items O1 to O3 remain proposed

## Context

After the TRL 3 session, two recommendations were still waiting for Amish: the charge current (TRT-DDR-001, item O4) and a lighter strap to restore mass margin under R6 (`docs/REVIEW.md`, TRL 3 session, recommended next step). On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item that carried a recommendation is therefore decided as recommended. Items without a recommendation stay open. TRL 4 remains on hold.

## Decision

Table 1. Items decided by this record.

| # | Item | Options | Decision |
| --- | --- | --- | --- |
| D6 | Charge current (was TRT-DDR-001 O4) | 50 mA (0.33 C, about 3.6 h, about 65 mW charger heat) or 100 mA (0.67 C, about 1.8 h, about 130 mW) | Decided by Amish, 2026-09-25: go with recommendation. 50 mA; the firmware selects the 50 mA setting |
| D7 | Strap | 12 g silicone strap (TRL 3 baseline) or a woven textile strap of about 8 g | Decided by Amish, 2026-09-25: go with recommendation. Woven textile two-piece quick-release strap, 22 mm, about 8 g |

Budget and pitch: no recommendation proposed a change to either, so `budget_usd` stays at $150 and the pitch and problem lines are unchanged. The parts total rose from $41.19 to $43.19, well inside the budget.

## What changed in the repo

- **D6.** TRT-CAL-001 v0.2, section 5: the 50 mA setting is recorded as decided and as a firmware rule. TRT-REQ-001 v0.4, R4 names the 50 mA recharge setting. TRT-PRC-001 v0.5 records the decision. Drawing TRT-DWG-002 Rev P2 notes "Charge at 50 mA". `docs/04-calcs/sizing.py` marks the setting as decided.
- **D7.** `bom/bom.csv` item 1 is now a woven textile strap, about 8 g, $10.00 (was silicone, about 12 g, $8.00); parts total $43.19 (was $41.19). `cad/src/model.py` strap thickness 1.4 mm (was 2.5 mm); STEP and STL re-exported. `docs/04-calcs/sizing.py` strap mass 8 g (was 12 g). TRT-CAL-001 v0.2: mass 25.4 g (was 29.4 g), margin 4.6 g (was 0.6 g), R6 met (was at risk). TRT-REQ-001 v0.4: R6 met. TRT-PRC-001 v0.5: component table, key numbers and design choices updated. TRT-DWG-002 Rev P2 (was P1): parts list names the textile strap. Concept media regenerated with the new key figures.

## Items still open

These carried no recommendation, so they stay "Proposed, awaiting Amish":

- **O1.** First co-design and validation partner: a movement disorders clinic, a patient association, or the OpenRatio network. Proposed, awaiting Amish.
- **O2.** Confirmation of "OpenRatio" as a possible partner (part of O1). Proposed, awaiting Amish.
- **O3.** Approval of kit 1.3.1 (forearm-for-scale rule for small objects in the concept media). Proposed, awaiting Amish.

## Consequences

- Requirement status: nine met, two not verifiable at TRL 3 (R7, R8), none at risk, none not met.
- No cross-repo action arises from these decisions.
- TRL 4 work (building a band, weighing it, measuring charge temperature, writing firmware) is on hold by Amish's instruction. The design stays at TRL 3.
