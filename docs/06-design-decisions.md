---
doc_id: TRT-DEC-001
title: TremorTrace design decisions register
project: TremorTrace
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-02'
  author: Amish Chadha
  change: Register opened; open decisions from the review note, the decision records and the build plan work
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: Amish approved the recommendations for open items 1 to 10 on 2026-10-02 (TRT-DDR-003 accepted, with A1 and A2); moved to decisions made
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Cost restated with the diode (BOM line 12): USD 43.79'
---

# TremorTrace design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in the review note (`docs/REVIEW.md`); this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

> **Safety:** TremorTrace is a research and educational prototype, not a medical device. It has not been cleared or approved by any regulator and must not be used to diagnose, treat or monitor any person.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The status LED position on the module | It sets the light pipe bore (6.5 mm from the centre on the centre line) and the hole in the upper foam pad | TRT-DDR-003, C6 and C8 |
| 2 | The module's thickness with its components (3.5 mm assumed) | It sets the squeeze on the upper foam pad; more than 4.5 mm would need a thinner pad | TRL 3 model; TRT-CAL-001, section 7 |
| 3 | The charging receptacle's body size (4 x 8 x 3 mm assumed) and whether it has a flange | It sets the floor opening and the glue collar | TRT-DDR-003, C4 |
| 4 | The spring bars' tip diameter (about 0.9 mm) | The horn holes are drilled 1.0 mm; tips over 1.0 mm need a larger drill | TRT-DDR-003, C1 |
| 5 | That the module's 5 V pin carries no voltage with the cell connected and no charger | The receptacle contacts touch the skin; a Schottky diode is fitted in any case (decided 2026-10-02), and this check decides whether it can ever be dropped | TRT-DDR-003, A2 |
| 6 | That a printed horn takes an M2 thread-forming screw without splitting (1.2 mm of plastic round the screw) | If it splits, print the horns hotter or use M1.6 screws | TRT-DDR-003, C2 |
| 7 | The textile strap's mass (8 g assumed) and that its ends loop round a 1.5 mm bar inside a 4.5 mm notch | Mass margin under R6 is 3.8 g; the loop clearance is 0.35 mm | TRT-CAL-001, section 7; TRT-DDR-003, C3 |
| 8 | The IMU sample-rate tolerance and the module's run current | They carry the R1 and R4 results | TRT-CAL-001, sections 2 and 5 |

## Value engineering

Value-engineering target: USD 150 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 43.79 (USD 106.21 under the target). Main cost drivers and savings worth trying:

- The largest lines are the controller and IMU module (USD 15.99), the textile strap (USD 10.00), the magnetic charging receptacle with its cable (USD 6.00) and the LiPo cell (USD 5.95); together they are USD 37.94 of the USD 43.79.
- Making the design constructable added USD 0.50 (two more lid screws); the foam pads and epoxy fall within the existing consumables allowance.
- Savings worth trying: a generic 22 mm textile strap (often under USD 5); buying the charging receptacle and cable as a bulk pair; the module price in small quantities from a distributor.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | D1 single nRF52840 module with built-in IMU, no custom PCB; D2 10 s summaries with optional raw snippets; D3 web Bluetooth page first; D4 most affected wrist first; D5 local-first data | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | TRT-DDR-001 |
| 2026-09-25 | D6 charge at the 50 mA setting; D7 woven textile strap of about 8 g | Amish: "i accept all your recommendations, go with them across all repos." | TRT-DDR-002 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan; keep open decisions out of the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The changes were accepted on 2026-10-02 (below) | TRT-DDR-003 |
| 2026-10-01 | Treat `budget_usd` as a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens" | `.kit/STANDARDS.md`, section 18 |
| 2026-10-02 | Design for construction accepted: the changes C1 to C9 of TRT-DDR-003, as made | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | TRT-DDR-003, Table 1 |
| 2026-10-02 | Firmware update route: over Bluetooth with the nRF52840's over-the-air bootloader; opening the pod, with a new gasket, is kept for recovery only | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | TRT-DDR-003, A1 |
| 2026-10-02 | Skin-side charging contacts: a small Schottky diode is fitted in the receptacle's positive lead on every band, and the bought module's 5 V pin is still checked dead with the cell connected and no charger; the diode is dropped only if measurements show the pin dead in every operating state | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | TRT-DDR-003, A2 |
| 2026-10-02 | First co-design and validation partner: the first candidate to approach is an academic movement disorders clinic with its own ethics board, introduced through the OpenRatio network, with the International Essential Tremor Foundation as the route to participants, shared with StillBand and SteadySleeve. No prototype is worn without clinical oversight and ethics approval | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | TRT-DDR-001, O1; TRT-DDR-002 |
| 2026-10-02 | OpenRatio confirmed as a named possible partner, described in soft, non-clinical wording as a research and educational network, not a clinical service | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | TRT-DDR-001, O2 |
| 2026-10-02 | Kit 1.3.1 approved: concept media for small objects show a forearm for scale instead of the 1.75 m person | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | TRT-DDR-001, O3 |
| 2026-10-02 | Strap path: the circular strap stays in the parametric model for the drawing and mass; the elliptical wrist path is used in renders only | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | `docs/REVIEW.md`, 2026-09-26, item 1 |
| 2026-10-02 | Lid mark and grip ribs kept as printed-in features at no cost, with the mark debossed 0.4 mm (two 0.2 mm layers) into the 1.5 mm lid | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | `docs/REVIEW.md`, 2026-09-26, item 3 |
| 2026-10-02 | Module detail and charging lead in the renders accepted as illustration only | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | `docs/REVIEW.md`, 2026-09-26, item 4 |
| 2026-10-02 | Tremor during a reach: the separate activity flag is kept and tremor is reported both with and without it; a classifier is chosen at TRL 4 from recorded data | Amish: "APPROVED: The open decisions from the last wave (TremorTrace to ZeerBox) came in after the review and aren't on the page either." | TRT-CAL-001, section 4; TRT-PRC-001 |
