---
doc_id: TRT-PRC-001
title: TremorTrace design precis
project: TremorTrace
doc_type: Design precis
version: "0.3"
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
  change: Populate to TRL 2 (architecture, first-order numbers, safety, media)
- version: "0.3"
  date: '2026-09-24'
  author: Amish Chadha
  change: 'Review fixes: one-module and local-first choices marked proposed; massing pod closed at 12 mm; concept sheet renumbered TRT-DWG-001'
---

# TremorTrace design precis

TremorTrace is a small wrist pod on a watch strap that records wrist motion all day, turns it into 10-second tremor summaries on the band, and hands them to an open notebook that draws a daily tremor profile. First-order numbers suggest a single off-the-shelf module and a 150 mAh cell can meet every requirement for about $40 in parts.

![Hero render](../media/hero.png)

## How it works

1. **Sense.** A 6-axis IMU (accelerometer and gyroscope) samples wrist motion at 104 Hz.
2. **Summarize on the band.** Every 10 seconds the firmware band-pass filters the signal to 3 to 15 Hz, runs a spectrum, and stores a compact summary: dominant frequency, band power, acceleration and angular velocity RMS, and an activity flag so voluntary movement is not counted as tremor.
3. **Store.** Summaries go to on-board flash, so the band works for a week without a phone.
4. **Sync.** When the owner opens the phone app or a laptop script, summaries transfer over Bluetooth Low Energy. Nothing goes to the cloud.
5. **Analyze.** An open Python notebook turns summaries into a daily profile: minutes of tremor per hour, dominant frequency and amplitude over the day, and optional medication-time markers entered by the owner.

![System and data flow](../media/flow.png)

## Main components

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Strap | 22 mm silicone watch strap | Standard spring bars; skin-safe |
| 2 | Enclosure lid | 3D-printed, PETG or resin | Light pipe for the status LED |
| 3 | Controller and IMU | nRF52840 module with built-in 6-axis IMU, 2 MB flash and LiPo charger (Seeed XIAO nRF52840 Sense class) | One module, no custom PCB. Proposed, awaiting Amish |
| 4 | Battery | 150 mAh protected LiPo | See power budget |
| 5 | Enclosure base | 3D-printed with TPU gasket | Charging contacts through the base |
| 6 | Charging contacts | Magnetic 2-pin pogo connector | Keeps the enclosure sealed |

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3.

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Frequency resolution | 0.1 Hz | 10 s window at 104 Hz | R1 (0.2 Hz) met |
| Nyquist limit | 52 Hz | 104 Hz sampling | R1, R3 met |
| Average current while recording | about 1.5 mA | IMU about 0.9 mA, MCU processing about 0.5 mA, BLE about 0.1 mA | |
| Daily charge used | about 25 mAh | 16 h recording plus 8 h at about 0.05 mA | |
| Battery life | about 4 days | 150 mAh cell, 70 % usable | R4 (3 days) met, margin thin |
| Summary storage | about 185 kB per day | 32 bytes per 10 s window, 16 h | |
| On-band history | about 10 days | 2 MB flash, minus firmware space | R5 (7 days) met |
| Mass | about 22 g | Module 3 g, cell 3.5 g, enclosure 5 g, strap 10 g | R6 (30 g) met |
| Pod size | 40 x 30 x 12 mm | Module 21 x 18 mm over a 30 x 20 x 5 mm cell | R6 met |
| Parts cost | about $40 | Indicative prices, see bom/bom.csv | R10 met |

## Key design choices

- **Summaries, not raw data.** Storing 10-second summaries instead of raw samples cuts storage by about 1,000 times and keeps personal data minimal. Short raw snippets can be captured on demand for research. Proposed, awaiting Amish.
- **One module, no custom PCB.** Keeps the first build within reach of anyone with a soldering iron and a 3D printer. Proposed, awaiting Amish.
- **Local-first data.** No cloud account is needed to use or analyze the data (R9). Proposed, awaiting Amish.

![Exploded view](../media/exploded.png)

## Safety

- Research and educational prototype only. It is not a medical device, has not been cleared or approved by any regulator, and must not be used to diagnose, treat or adjust medication.
- The LiPo cell sits against the skin: use a protected cell, never charge while worn, and stop use if the pod becomes warm or swollen.
- Use skin-safe strap materials and check for irritation during long wear.
- Tremor data is health data. Keep it on the owner's devices and share only with consent.

## Open questions for TRL 3

- Validate the activity flag: how well can voluntary movement be separated from tremor with 10 s summaries?
- Confirm IMU current at 104 Hz in the chosen module and firmware.
- Choose phone app route: a simple web Bluetooth page or a native app. Proposed: web Bluetooth page, awaiting Amish.
- Identify a clinical or patient partner for co-design and eventual validation.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
