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

1. Controller: a single nRF52840 module with built-in IMU (Seeed XIAO nRF52840 Sense class). Alternative: separate nRF52 module and IMU breakout (more wiring, more flexibility).
2. Store 10-second summaries rather than raw data, with optional raw snippets for research.
3. Phone route: a web Bluetooth page first, native app later.
4. Wear on the most affected wrist first; both wrists later.
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

