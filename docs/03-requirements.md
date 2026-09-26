---
doc_id: TRT-REQ-001
title: TremorTrace requirements
project: TremorTrace
doc_type: Requirements
version: "0.4"
status: Draft
date: '2026-09-25'
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
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: 'Apply TRT-DDR-001 decisions: R5 redefined with a raw-snippet reserve, R11 names the LED and web Bluetooth page, wrist choice; status from TRT-CAL-001'
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# TremorTrace requirements

These requirements were checked by calculation in TRT-CAL-001 (TRL 3). Nine are met by calculation or design review and R7 and R8 cannot be verified on paper; none is not met. Changes in v0.3 follow Amish's decisions of 2026-09-25 (TRT-DDR-001). In v0.4, R6 moves from at risk to met because the textile strap recommended at TRL 3 was accepted (TRT-DDR-002), and R4 names the 50 mA charge setting.

Table 1. Requirements and TRL 3 status.

| ID | Requirement | Target | Verification (TRL 3 or later) | TRL 3 status (TRT-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Measure tremor frequency across the clinically relevant band | 3 to 15 Hz, resolution 0.2 Hz or better | Calculation of sampling and window length; later bench shaker test | Met, if the firmware corrects the sample rate against the crystal |
| R2 | Measure tremor amplitude | Acceleration RMS and angular velocity RMS in the tremor band, reported per window | Calculation; later comparison against a reference sensor | Met |
| R3 | Sample motion fast enough | 6-axis IMU at 100 Hz or more | Datasheet and firmware configuration | Met |
| R4 | Run a full waking day and more | 3 days or more between charges at 16 h per day of wear; recharge at the 50 mA setting | Power budget calculation | Met, 4.5 to 6.3 days, if the firmware sleeps |
| R5 | Store a week of results on the band | 7 days of 10 s window summaries at 16 h of wear per day without a phone, alongside a reserved area for on-demand raw snippets | Storage calculation | Met, 9.7 days |
| R6 | Comfortable for all-day wear | Mass 30 g or less including strap; pod no larger than 45 x 35 x 14 mm | Massing model, then weighing | Met: 25.4 g with textile strap (TRT-CAL-001 v0.2); size met |
| R7 | Skin-safe and wearable | Silicone or textile strap; no exposed electronics; splash resistant (IP54 target) | Design review | Not verifiable at TRL 3 |
| R8 | Produce a daily tremor profile | Open notebook turning window summaries into a daily chart of tremor time, frequency and amplitude | Run on sample data | Not verifiable at TRL 3 |
| R9 | Protect health data | Data stored locally and exported only by the owner; no cloud dependency | Design review | Met (design review) |
| R10 | Low cost and buildable | Parts cost $150 or less per unit; no custom PCB required for the first build | Priced BOM | Met, $43.19 |
| R11 | Clear status | Status LED on the band and the web Bluetooth page show battery, recording and sync state | Design review | Met (design review) |

## Assumptions

- Parkinsonian rest tremor is typically about 4 to 6 Hz and essential tremor about 4 to 12 Hz; a 3 to 15 Hz band covers both with margin.
- Wear time of 16 h per day and nightly charging is acceptable, but a multi-day battery is preferred so a missed charge does not lose a day.
- One band is worn on the most affected wrist (decided by Amish, 2026-09-25, TRT-DDR-001); both wrists are later work.
- The mass limit in R6 includes the strap. The strap is a woven textile strap of about 8 g (TRT-DDR-002) and remains the least certain item in the mass estimate.

> **Safety:** TremorTrace is a research and educational prototype, not a medical device. It carries a lithium polymer cell against the skin; the cell must be protected and must never be charged while the band is worn.
