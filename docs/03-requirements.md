---
doc_id: TRT-REQ-001
title: TremorTrace requirements
project: TremorTrace
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-24'
  author: Amish Chadha
  change: First measurable requirements for TRL 2
---

# TremorTrace requirements

These are first-pass requirements for the concept. Targets are proposals for review and will be checked by calculation at TRL 3.

| ID | Requirement | Target | Verification (TRL 3 or later) |
| --- | --- | --- | --- |
| R1 | Measure tremor frequency across the clinically relevant band | 3 to 15 Hz, resolution 0.2 Hz or better | Calculation of sampling and window length; later bench shaker test |
| R2 | Measure tremor amplitude | Acceleration RMS and angular velocity RMS in the tremor band, reported per window | Calculation; later comparison against a reference sensor |
| R3 | Sample motion fast enough | 6-axis IMU at 100 Hz or more | Datasheet and firmware configuration |
| R4 | Run a full waking day and more | 3 days or more between charges at 16 h per day of wear | Power budget calculation |
| R5 | Store a day of results on the band | 7 days of 10 s window summaries without a phone | Storage calculation |
| R6 | Comfortable for all-day wear | Mass 30 g or less including strap; pod no larger than 45 x 35 x 14 mm | Massing model, then weighing |
| R7 | Skin-safe and wearable | Silicone or textile strap; no exposed electronics; splash resistant (IP54 target) | Design review |
| R8 | Produce a daily tremor profile | Open notebook turning window summaries into a daily chart of tremor time, frequency and amplitude | Run on sample data |
| R9 | Protect health data | Data stored locally and exported only by the owner; no cloud dependency | Design review |
| R10 | Low cost and buildable | Parts cost $150 or less per unit; no custom PCB required for the first build | Priced BOM |
| R11 | Clear status | LED or phone app shows battery, recording and sync state | Design review |

## Assumptions

- Parkinsonian rest tremor is typically about 4 to 6 Hz and essential tremor about 4 to 12 Hz; a 3 to 15 Hz band covers both with margin.
- Wear time of 16 h per day and nightly charging is acceptable, but a multi-day battery is preferred so a missed charge does not lose a day.
