# Review note: TremorTrace

## Session 2026-09-24: /populate to a strong TRL 2 (pilot run from Cowork)

### What was done

- `docs/01-problem.md` (TRT-PRB-001 v0.2): users and context, constraints, out of scope, prior research with links.
- `docs/03-requirements.md` (TRT-REQ-001 v0.2): 11 measurable requirements (R1 to R11) with targets and planned verification.
- `docs/02-concept.md` (TRT-PRC-001 v0.2): how it works, main components, first-order numbers, design choices, safety, open questions.
- `cad/src/concept_media.py`: massing model (strap, enclosure, module, LiPo cell, contacts) with a forearm and hand for scale.
- `media/`: hero, blueprint sheet (PNG and PDF), cutaway, exploded view with BOM callouts, data flow diagram, `model.glb` and `viewer.html`.
- `bom/bom.csv`: seven lines with indicative prices, numbered to match the exploded view; `bom/bom-notes.md`.
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Frequency resolution | 0.1 Hz (10 s window at 104 Hz) | R1 met |
| Battery life | about 4 days on 150 mAh | R4 met, thin margin |
| On-band history | about 10 days of summaries | R5 met |
| Mass | about 22 g with strap | R6 met |
| Parts cost | about $40 | R10 met |

No requirement is known to be missed. R4 depends on IMU current in the chosen module, which is unverified.

### Proposed, awaiting Amish

1. Controller: a single nRF52840 module with built-in IMU (Seeed XIAO nRF52840 Sense class). Alternative: separate nRF52 module and IMU breakout (more wiring, more flexibility). Decided by Amish, 2026-09-25: go with recommendation (TRT-DDR-001).
2. Store 10-second summaries rather than raw data, with optional raw snippets for research. Decided by Amish, 2026-09-25: go with recommendation (TRT-DDR-001).
3. Phone route: a web Bluetooth page first, native app later. Decided by Amish, 2026-09-25: go with recommendation (TRT-DDR-001).
4. Wear on the most affected wrist first; both wrists later. Decided by Amish, 2026-09-25: go with recommendation (TRT-DDR-001).
5. First co-design and validation partner: a movement disorders clinic, a patient association, or the OpenRatio network.

### Safety concerns

- Not a medical device; the documents say so and must keep saying so.
- LiPo cell against skin: protected cell, no charging while worn.
- Tremor data is health data: local-first design, owner-controlled sharing.

### Recommended next step

Review this note and the media. If approved, run `/advance-trl3` to verify the power budget, frequency analysis and activity flag by calculation and produce the parametric model and drawing sheet.

## Session 2026-09-24: review fixes

At Amish's request, after a review of commits `15c42b7` and `5091eea`:

- `cad/src/concept_media.py`: the massing pod had no side walls between base and lid, and stacked to 13.5 mm against the 12 mm in TRT-PRC-001. The base walls now enclose the cell and module, and the pod is 12.0 mm overall. All media regenerated.
- The concept sheet is renumbered TRT-DWG-001 (it was TRT-DWG-010); drawing numbers start at 001 (`.kit/STANDARDS.md`, section 1).
- TRT-PRC-001 v0.3: "One module, no custom PCB" and "Local-first data" are now marked "Proposed, awaiting Amish", as `CLAUDE.md` section 2 requires.

Still awaiting Amish: approval of kit 1.3.1, whose forearm-for-scale rule for small objects replaces the 1.75 m person that `/populate` asks for, and confirmation of "OpenRatio" as a possible co-design partner.


## Session 2026-09-25: TRL 3

Authority: on 2026-09-25 Amish wrote "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." This session advanced TremorTrace from TRL 2 to TRL 3 and stopped there.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (TRT-DDR-001 v0.1): the TRL 2 review decisions, and the items still open.
- `docs/04-calcs/01-sizing.md` (TRT-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: sampling, noise and range, a synthetic check of the 10 s window algorithm and the activity flag, power budget, storage, size and mass (read from the model), and cost (read from the BOM).
- `cad/src/model.py`: parametric build123d model (pod base with integrated 22 mm lugs, gasket, lid, cell, module, charging connector, spring bars, strap). Exports `cad/step/tremortrace-{pod-assembly,on-strap,base,lid,gasket}.step` and `cad/stl/tremortrace-{pod-assembly,base,lid,gasket}.stl`.
- `cad/src/sheets.py` and `cad/drawings/TRT-DWG-002.{svg,pdf,png}`: general arrangement at Rev P1, 2:1, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION".
- `bom/bom.csv`: 11 lines, every line priced, $41.19 per band; `bom/bom-notes.md` updated.
- `cad/src/concept_media.py` now builds the media from `model.py`; all media regenerated and inspected (hero, blueprint TRT-DWG-001, cutaway, exploded view with items 1 to 8, flow, `model.glb`).
- TRT-REQ-001 v0.3, TRT-PRB-001 v0.3 and TRT-PRC-001 v0.4 updated for the decisions and the calculated numbers. The precis was already at v0.3, so it moved to v0.4 rather than 0.3.
- `project.yaml`: `trl: 3`, `trl_target: 3`, evidence listed. `README.md`: TRL 3 badge and status.

### Requirement status (TRT-CAL-001)

Not met: none. At risk and not verifiable first:

| ID | Status | Value |
| --- | --- | --- |
| R6 | At risk (mass); size met | 29.4 g against 30 g, strap assumed 12 g; pod 40 x 30 x 12 mm |
| R7 | Not verifiable at TRL 3 | Gasketed pod; IP54 needs a test |
| R8 | Not verifiable at TRL 3 | Summary record defined; notebook not written |
| R1 | Met, conditional | 0.100 Hz bins; needs sample-rate correction against the 32.768 kHz crystal (up to 0.30 Hz error otherwise) |
| R4 | Met, conditional | 6.3 days nominal, 4.5 days conservative; 0.69 days if the firmware never sleeps |
| R5 | Met | 9.7 days; 6.4 days if the band logged 24 h per day |
| R2, R3, R9, R10, R11 | Met | Noise floor 0.31 mg RMS; 104 Hz; local-first; $41.19; LED and web Bluetooth page |

Corrections to TRL 2 numbers: the summary-to-raw ratio is 390, not about 1,000; firmware sits in the nRF52840's internal flash, so all 2 MB of external flash holds data; the mass estimate rose from 22 g to 29.4 g once the enclosure was modeled (7.0 g, not 5 g) and the cell mass taken from its listing (4.65 g).

Finding: the simple activity flag (low-frequency power greater than tremor-band power) marks tremor during a reach as activity in synthetic data, which would undercount action tremor in essential tremor. The design now keeps tremor values in every record and stores the flag separately.

### Decisions recorded (TRT-DDR-001)

Decided by Amish, 2026-09-25, going with the recommendation: D1 single nRF52840 module with built-in IMU, no custom PCB; D2 summaries with optional raw snippets; D3 web Bluetooth page first; D4 most affected wrist first; D5 local-first data. No budget or pitch change was recommended, so `budget_usd` stays at 150 and the pitch is unchanged.

### Still awaiting Amish

1. First co-design and validation partner (clinic, patient association or OpenRatio network). No recommendation was made.
2. Confirmation of OpenRatio as a possible partner.
3. Approval of kit 1.3.1 (forearm-for-scale rule for small objects). No recommendation was stated.
4. New: charge current 50 mA (recommended; 0.33 C, about 65 mW charger heat) or 100 mA. Decided by Amish, 2026-09-25: go with recommendation (TRT-DDR-002).

### Safety concerns

- Not a medical device; every document says so.
- LiPo cell against the skin: protected cell, never charge while worn, charge at or below the cell's 150 mA limit. The linear charger dissipates about 65 mW at 50 mA and 130 mW at 100 mA inside a sealed pod.
- Tremor data is health data; the design has no cloud path.

### Citations

The TRL 2 note listed no unchecked citations. This session checked the LSM6DS3TR-C figures (ST product page and datasheet), the XIAO nRF52840 figures (Seeed wiki) and the Adafruit 1317 cell (product page) on the web and cites them in TRT-CAL-001, section 9. The XIAO unit price could not be confirmed and stays indicative. Values marked "assumed" in TRT-CAL-001 have no source.

### TRL 4 material

None found. `build-log/` holds only its README; `electronics/` and `firmware/` are empty.

### Recommended next step

TRL 4 is on hold by Amish's instruction; do not start it. Paper work that remains within TRL 3: decide the four open items above, and choose a lighter strap (textile, about 8 g) to restore mass margin under R6 if Amish agrees. Decided by Amish, 2026-09-25: go with recommendation (TRT-DDR-002).

For reference only, TRL 4 would need: a built band, a bench shaker test of frequency and amplitude against a reference sensor (R1, R2), a measured current profile (R4), a splash test (R7), the analysis notebook run on recorded data (R8), weighing (R6), a lab test report (TST with `environment: lab`) and build log entries.


## Session 2026-09-25: recommendations accepted

Authority: on 2026-09-25 Amish wrote "i accept all your recommendations, go with them across all repos." Every open item with a recommendation is now "Decided by Amish, 2026-09-25: go with recommendation" and is recorded in `docs/decisions/0002-recommendations-accepted.md` (TRT-DDR-002 v0.1).

### Decisions applied and what changed

| # | Decision | Before | After |
| --- | --- | --- | --- |
| D6 | Charge current 50 mA (was TRT-DDR-001 O4) | Proposed, 50 or 100 mA | 50 mA as a firmware rule; about 3.6 h, about 65 mW charger heat |
| D7 | Woven textile strap, 22 mm | Silicone, 12 g, $8.00, 2.5 mm thick in the model | Textile, 8 g, $10.00, 1.4 mm thick in the model |
| | Resulting mass (R6) | 29.4 g, 0.6 g margin, at risk | 25.4 g, 4.6 g margin, met |
| | Parts cost (R10) | $41.19 | $43.19 |
| | Budget (`project.yaml`) | $150 | $150 (no change recommended) |

Files changed: `bom/bom.csv`, `bom/bom-notes.md`, `cad/src/model.py` (STEP and STL re-exported), `cad/src/sheets.py` (TRT-DWG-002 Rev P1 to P2), `cad/src/concept_media.py` (media regenerated), `docs/04-calcs/sizing.py`, TRT-CAL-001 v0.1 to v0.2, TRT-REQ-001 v0.3 to v0.4, TRT-PRC-001 v0.4 to v0.5, TRT-DDR-001 v0.1 to v0.2 (O4 marked decided), new TRT-DDR-002 v0.1, `project.yaml` (DDR-002 added to TRL evidence), `README.md`.

Also in this session: all generated files (document PDFs, drawing sheets, concept media) were regenerated so the footers carry designmolecule.com, and the README gained the sections "Concept rationale", "Burning platform", "Where it could be used" and "What sparked the idea". The inspiration point is the Parkinson's disease home diary of Hauser et al. (2000), with cited sources.

### Requirement status (TRT-CAL-001 v0.2)

Not met: none. At risk: none.

| ID | Status | Value |
| --- | --- | --- |
| R7 | Not verifiable at TRL 3 | Gasketed pod; IP54 needs a test |
| R8 | Not verifiable at TRL 3 | Summary record defined; notebook not written |
| R1 | Met, conditional | 0.100 Hz bins; needs sample-rate correction against the crystal |
| R4 | Met, conditional | 6.3 days nominal, 4.5 days conservative, if the firmware sleeps |
| R6 | Met | 25.4 g against 30 g; pod 40 x 30 x 12 mm |
| R2, R3, R5, R9, R10, R11 | Met | 0.31 mg noise floor; 104 Hz; 9.7 days; local-first; $43.19; LED and web Bluetooth page |

### Still awaiting Amish (no recommendation was made)

1. O1: first co-design and validation partner (clinic, patient association or OpenRatio network).
2. O2: confirmation of OpenRatio as a possible partner.
3. O3: approval of kit 1.3.1 (forearm-for-scale rule for small objects).

### Cross-repo actions

None. Neither decision needs a change in another repo.

### Safety concerns

Unchanged: not a medical device; protected LiPo cell, never charged while worn, charged at the 50 mA setting; tremor data stays local. A textile strap absorbs sweat and should be washable and checked for skin irritation.

### TRL 4

TRL 4 remains on hold by Amish's instruction. Nothing was built, bought, tested or programmed. `trl: 3` and `trl_target: 3` are unchanged.
