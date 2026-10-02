---
doc_id: TRT-DEC-001
title: TremorTrace design decisions register
project: TremorTrace
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-02'
  author: Amish Chadha
  change: Register opened; open decisions from the review note, the decision records and the build plan work
---

# TremorTrace design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in the review note (`docs/REVIEW.md`); this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

> **Safety:** TremorTrace is a research and educational prototype, not a medical device. It has not been cleared or approved by any regulator and must not be used to diagnose, treat or monitor any person.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design-for-construction changes C1 to C9 (spring bar tip holes, four corner screws, deeper notch, glue collar, cell ribs, foam pads, cell plug removed, light pipe, 0.8 mm gasket) | Accept; accept some; revert to the concept | Accept: each keeps what the band does and makes a part buildable | The whole build plan follows them | TRT-DDR-003, Table 1 |
| 2 | Firmware update route once the pod is sealed | (a) over Bluetooth with the nRF52840's over-the-air bootloader; (b) open the pod for each update | (a), keeping (b) for recovery | Whether firmware must be loaded before step 8 of the build plan only once, or every time | TRT-DDR-003, A1 |
| 3 | Protection for the skin-side charging contacts | (a) confirm the module's 5 V pin is dead with no charger and add nothing; (b) add a Schottky diode in the positive lead in any case | (a), with (b) if the pin is found live | Wiring step 3 (one more part in one lead) | TRT-DDR-003, A2 |
| 4 | First co-design and validation partner | A movement disorders clinic, a patient association, or the OpenRatio network | None made | Not part of the TRL 3 build | TRT-DDR-001, O1; TRT-DDR-002 |
| 5 | Confirmation of OpenRatio as a possible partner | Confirm; do not name | None made | None | TRT-DDR-001, O2 |
| 6 | Approval of kit 1.3.1, the forearm-for-scale rule for small objects in concept media | Approve; keep the 1.75 m person | None stated | Concept media only | TRT-DDR-001, O3 |
| 7 | Strap path in the appearance model | Keep the circular strap of `model.py` for the drawing and mass; follow the elliptical clay wrist only in renders | Keep the circle in `model.py`; elliptical path for renders only | None | `docs/REVIEW.md`, 2026-09-26, item 1 |
| 8 | Lid marking and grip ribs shown in the renders but not in the model or BOM | Keep as printed-in features; drop | Keep, with the mark raised or debossed 0.14 mm; no cost change | Lid and base prints, if adopted | `docs/REVIEW.md`, 2026-09-26, item 3 |
| 9 | Module detail and charging lead in the renders (not taken from a datasheet) | Accept as illustration only; model from datasheets | Accept as illustration only | None | `docs/REVIEW.md`, 2026-09-26, item 4 |
| 10 | How the analysis separates tremor during a reach from voluntary movement | Keep the separate activity flag and report both (current); a better classifier later | Keep the current record and decide the classifier with recorded data at TRL 4 | Firmware and notebook only | TRT-CAL-001, section 4; TRT-PRC-001 |

Item 2 of the 2026-09-26 appearance review (pan-head screws standing above the lid) is answered by change C2 of TRT-DDR-003 (countersunk screws, flush), which is itself open as item 1.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The status LED position on the module | It sets the light pipe bore (6.5 mm from the centre on the centre line) and the hole in the upper foam pad | TRT-DDR-003, C6 and C8 |
| 2 | The module's thickness with its components (3.5 mm assumed) | It sets the squeeze on the upper foam pad; more than 4.5 mm would need a thinner pad | TRL 3 model; TRT-CAL-001, section 7 |
| 3 | The charging receptacle's body size (4 x 8 x 3 mm assumed) and whether it has a flange | It sets the floor opening and the glue collar | TRT-DDR-003, C4 |
| 4 | The spring bars' tip diameter (about 0.9 mm) | The horn holes are drilled 1.0 mm; tips over 1.0 mm need a larger drill | TRT-DDR-003, C1 |
| 5 | That the module's 5 V pin carries no voltage with the cell connected and no charger | The receptacle contacts touch the skin; see open decision 3 | TRT-DDR-003, A2 |
| 6 | That a printed horn takes an M2 thread-forming screw without splitting (1.2 mm of plastic round the screw) | If it splits, print the horns hotter or use M1.6 screws | TRT-DDR-003, C2 |
| 7 | The textile strap's mass (8 g assumed) and that its ends loop round a 1.5 mm bar inside a 4.5 mm notch | Mass margin under R6 is 3.8 g; the loop clearance is 0.35 mm | TRT-CAL-001, section 7; TRT-DDR-003, C3 |
| 8 | The IMU sample-rate tolerance and the module's run current | They carry the R1 and R4 results | TRT-CAL-001, sections 2 and 5 |

## Value engineering

Value-engineering target: USD 150 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 43.69 (USD 106.31 under the target). Main cost drivers and savings worth trying:

- The largest lines are the controller and IMU module (USD 15.99), the textile strap (USD 10.00), the magnetic charging receptacle with its cable (USD 6.00) and the LiPo cell (USD 5.95); together they are USD 37.94 of the USD 43.69.
- Making the design constructable added USD 0.50 (two more lid screws); the foam pads and epoxy fall within the existing consumables allowance.
- Savings worth trying: a generic 22 mm textile strap (often under USD 5); buying the charging receptacle and cable as a bulk pair; the module price in small quantities from a distributor.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | D1 single nRF52840 module with built-in IMU, no custom PCB; D2 10 s summaries with optional raw snippets; D3 web Bluetooth page first; D4 most affected wrist first; D5 local-first data | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | TRT-DDR-001 |
| 2026-09-25 | D6 charge at the 50 mA setting; D7 woven textile strap of about 8 g | Amish: "i accept all your recommendations, go with them across all repos." | TRT-DDR-002 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan; keep open decisions out of the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The resulting changes are open as item 1 | TRT-DDR-003 |
| 2026-10-01 | Treat `budget_usd` as a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens" | `.kit/STANDARDS.md`, section 18 |
