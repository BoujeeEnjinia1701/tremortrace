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

## Session 2026-09-26: sources strengthened

- `README.md`, "Where it could be used", India row: the row had no citation. It now cites the ICMR, PHFI and IHME release of 14 July 2021 on the India State-Level Disease Burden Initiative study of neurological disorders (1990 to 2019), which reports that the burden of non-communicable neurological disorders, including Parkinson's disease, is rising mainly through population ageing and calls for addressing the shortage of trained neurology workforce. The unsourced claim that specialist care is concentrated in cities was removed.
- All other links in the four README source sections were re-fetched and confirmed (WHO, Louis and Ferreira 2010, WFN 2017, Commonwealth Fund 2016, Qi et al. 2021, Löhle et al. 2022, which also confirms the Hauser et al. 2000 diary). The inspiration (Hauser home diary) is unchanged. No controlled documents changed.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26. This session adds an appearance model for photoreal renders; it changes no design value, requirement, calculation or controlled document.

### What was done

- New `cad/src/product_model.py` (`product_parts()`, `TITLE`, `RENDER_VIEWS`). It imports `PARAMS`, `_derived()` and `build_parts()` from `cad/src/model.py` and keeps every main dimension and interface: pod 30 x 40 x 12 mm, 22 mm lugs, spring bar axes, gasket seat, screw positions, light pipe bore, charging opening and the internal envelopes.
- `README.md`: hero image now points to `media/render-hero.png`, with a link to `media/render-exploded.png`. The render files are produced separately.

What the appearance model adds (28 parts: 15 shell, 10 internal, 2 accessory, 1 context):

- Filleted base (0.6 mm underside edge, 0.4 mm top rim) and lid (1.0 mm top edge), so the dark TPU gasket reads as the parting line.
- Three shallow grip ribs on each X face of the base.
- Pan-head M2 lid screws with a cross recess, sitting in shallow seats in the lid.
- Status light pipe shown lit (emissive), plus the module's status LED.
- A raised tremor-trace mark (a short decaying wave) on the lid in the kit accent, #0F766E.
- Visible internals: module PCB with RF shield, USB-C, ICs and castellated pads; foam pad; LiPo cell with protection tape; magnetic charging receptacle with gold contacts; separate spring bars.
- Two-piece woven strap with edge stitching, buckle and keeper, following the clay wrist and wrapping the spring bars inside the lug notches.
- Magnetic charging lead with a USB-A plug, shown in the exploded view only.
- Scale context: the shared clay forearm and left hand (`.kit/context_parts.py`, flat pose, forearm length 130 mm), tilted 6 deg so the pod sits level on the back of the wrist.

Render views: `hero` (front right, 30 deg elevation, worn on the wrist), `exploded` (front right, 28 deg) and `detail` (front right, 38 deg, pod and strap without the arm).

### Differences from model.py

1. **Strap path.** `model.py` draws the strap as a 32 mm radius circular loop centred 31.5 mm below the skin. The appearance model follows the elliptical clay wrist (about 67 x 48 mm) and shows a two-piece strap with a buckle, 21.6 mm wide so it clears the 22 mm lugs in the render. Proposed, awaiting Amish. Recommendation: keep the circle in `model.py` for the drawing and mass figures, and use the elliptical path only for renders.
2. **Screw heads above the lid.** `model.py` has no screw heads. The pan heads stand about 0.85 mm above the lid, so the pod reads about 12.9 mm tall at the screws against the 12 mm envelope (the R6 limit is 14 mm, so R6 is still met). Proposed, awaiting Amish. Recommendation: specify countersunk M2 screws at TRL 4 so the lid stays flush, or accept the pan heads and update the envelope note.
3. **Lid marking and grip ribs.** Neither is in `model.py` or the BOM. Proposed, awaiting Amish. Recommendation: keep both as printed-in features (no cost change), with the mark 0.14 mm raised or debossed.
4. **Module detail and charging lead.** Shield, USB-C position, IC placement and the charging lead shape are indicative only and are not taken from a datasheet. Proposed, awaiting Amish. Recommendation: accept as illustration only.

### Confirmation

This is an appearance model only: no tolerances, no fabrication detail, nothing past TRL 3. `trl: 3` is unchanged in `project.yaml`, and TRL 4 remains on hold.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.
