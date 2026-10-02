---
doc_id: TRT-DDR-003
title: TremorTrace design for construction
project: TremorTrace
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-02'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
---

# 0003: Design for construction

- **Date:** 2026-10-02
- **Status:** Draft. The changes in Tables 1 and 2 were made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review. The items in Table 3 are Proposed, awaiting Amish.

> **Safety:** TremorTrace is a research and educational prototype, not a medical device. It carries a lithium polymer cell against the skin: use a protected cell, never charge while worn, and stop use if the pod becomes warm or swollen.

## Context

On 2026-09-30 Amish asked for every repo to have an illustrated prototype build plan and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of TRT-DDR-002 showed what TremorTrace does and that it works on paper, but several parts could not be made or fixed as drawn. Checking the concept geometry with build123d (intersections and distances between parts) found the problems in Table 1.

The changes keep what the band does: the same 30 x 40 x 12 mm pod, the same module, cell, charging receptacle, light pipe, gasket, strap and spring bars, the same 22 mm lugs and the same sensing, storage, power and data path. Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which now also runs 29 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, and parts that must not touch are apart by at least the stated clearance. All 29 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| C1 | The spring bar holes were 1.8 mm across, larger than the 1.5 mm body of a 22 mm quick-release bar. The body could enter one hole, the other tip would then leave its hole, and the strap would fall off. | 1.0 mm tip holes drilled right through each lug horn, 2 mm from the end and 3 mm up. The bar body (1.5 mm) sits between the horns; only its 0.9 mm tips enter the horns, 1.5 mm deep. | This is how a watch with drilled lugs holds its bars. Through holes let the bar be pushed out with a pin to change the strap. |
| C2 | The two M2 lid screws sat on the centre line, directly above the strap notches. Their pilot holes ran down to the notch ceiling, leaving no plastic below the screw (0 mm), and the screw tip ended 0.85 mm from the strap loop. | Four M2 x 6 countersunk thread-forming screws, one in each lug horn (the solid corner beside each notch), 13 mm each side of the centre along the forearm and 2.6 mm in from the end. Each has 4 mm of thread in solid plastic, 2 mm above the spring bar hole. | The horns are the only solid material at full height. Four corner screws also squeeze the gasket at all four corners instead of two ends, which helps the splash seal (R7). Countersunk heads sit flush, so the pod stays 12 mm high, as the 2026-09-26 review recommended for the appearance model. |
| C3 | The strap end looped round the spring bar (a 1.4 mm strap round a 1.5 mm bar is 4.3 mm across) overlapped the inner face of the 4.0 mm deep notch by 0.15 mm. | Notch 4.5 mm deep (was 4.0). The loop now clears the notch face by 0.35 mm and the horns by 0.2 mm. | The smallest change that lets the strap swing. The cavity across the wrist shrinks from 29.6 to 28.6 mm, which still leaves the cell 0.3 mm clear. |
| C4 | The charging receptacle sat in a hole in the 1 mm floor with nothing to hold it or seal round it. | A printed collar, 0.8 mm thick and 2 mm high, round the opening on the inside of the floor. The receptacle is pushed up through the opening with its contacts flush underneath and set in two-part epoxy that fills the collar. | The collar gives the epoxy a cup to fill, so the joint is both the fixing and the seal at the one hole through the skin side of the pod. |
| C5 | Nothing located the cell: it could slide 6.95 mm along the forearm and 1.8 mm across. | Three ribs printed on the floor, 1.5 mm high and 1 mm wide: one at the charging end and one along each long side. With the end wall they make a pocket 0.3 mm larger than the cell all round. | No glue on the cell, so it can be lifted out; the wires run in the gaps beside it. |
| C6 | The module floated on its foam pad with a 1.7 mm gap to the lid. | An upper foam pad cut from 2 mm closed-cell foam, with a 4 mm hole over the status LED, which the lid squeezes to 1.7 mm. The lower 0.5 mm adhesive foam pad is now in the model too. | The lid clamps the whole stack (cell, pad, module, pad), so nothing rattles and no screw or bracket is needed inside. |
| C7 | The cell's plug (JST-PH, about 8 x 4.5 x 6 mm) has no room anywhere in the 9.5 mm high cavity beside the stack. | The plug is cut off one lead at a time and the leads are soldered to the module's battery pads. | The module has battery pads for exactly this; a plug-in cell is not needed in a sealed pod. |
| C8 | The light pipe was a bore in the lid with no part in it. | A 2 mm length of 2 mm clear acrylic rod, pushed in from underneath until flush with the top and set with clear epoxy; it stands 0.5 mm below the lid, 1.2 mm above the module. | The pipe is now in the model, so its clearance to the module and the foam is checked. |
| C9 | The gasket was drawn at its squeezed thickness only and had holes for two screws. | Printed 0.8 mm thick in TPU 95A, squeezed to 0.5 mm, with four screw holes. | A 0.5 mm ring would not seal once squeezed; 0.8 mm gives 0.3 mm of squeeze. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | 26.2 g (was 25.4 g), 3.8 g under the R6 limit of 30 g (TRT-CAL-001 v0.3, section 7). | Two more screws, the upper foam pad, epoxy, and the ribs and collar in the base. |
| Cost | BOM lines 2, 4, 5, 7, 8, 9 and 11 updated; line 9 is now four screws. Estimated cost of the constructable design: USD 43.69 (was USD 43.19), USD 106.31 under the USD 150 value-engineering target (`budget_usd`, unchanged). | Parts added for construction. |
| Drawings | TRT-DWG-002 Rev P3 (was P2); making sketches TRT-DWG-101 to 104 added. | Follows the model. |
| Documents | TRT-CAL-001 v0.3, TRT-REQ-001 v0.5, TRT-PRC-001 v0.6: mass, cost and component figures updated. No requirement changed status. New: TRT-BLD-001 (build plan) and TRT-DEC-001 (design decisions register). | Follows the model. |
| Media | Concept media regenerated from the model (`cad/src/concept_media.py`). | Follows the model. |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | Once the lid is on, the module's USB-C socket is sealed inside the pod, so firmware cannot be loaded through it without opening the pod (and replacing the gasket). | (a) load firmware over Bluetooth with the nRF52840's over-the-air bootloader; (b) open the pod for each update. | (a), keeping (b) for recovery. It changes how the band is maintained, so it is Amish's decision. |
| A2 | The charging receptacle's two contacts touch the skin while the band is worn. They are wired to the module's 5 V and ground pins, which should carry no voltage when no charger is attached, but this depends on the module's circuit. | (a) confirm on the bought module that the 5 V pin is dead with the cell connected and no charger, and add nothing; (b) add a small Schottky diode in the receptacle's positive lead in any case. | (a), with (b) if the pin is found live. This touches the safety case, so it is Amish's decision. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan TRT-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status is unchanged: nine met, two not verifiable at TRL 3 (R7, R8), none at risk, none not met (TRT-CAL-001 v0.3).
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show two pan-head lid screws on the centre line. They need updating on Amish's Mac, where Blender is.
- The module's status LED position, its height and the charging receptacle's size are assumed; they are confirmed when parts are bought (TRT-DEC-001).
- TRL 4 remains on hold by Amish's instruction; nothing was built, bought or tested.
