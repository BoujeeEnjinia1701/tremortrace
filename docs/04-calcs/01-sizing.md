---
doc_id: TRT-CAL-001
title: TremorTrace sizing calculations
project: TremorTrace
doc_type: Calculation note
version: "0.4"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First-principles sizing for TRL 3 against TRT-REQ-001 v0.3
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Design for construction (TRT-DDR-003): mass 26.2 g, cost USD 43.69; budget treated as a value-engineering target'
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Schottky diode added to the cost (USD 43.79 over 12 lines) and the mass; no requirement status changed'
---

# TremorTrace sizing calculations

The design meets nine of the eleven requirements in TRT-REQ-001 by calculation or design review and two cannot be verified at TRL 3 (R7 splash resistance and R8 daily profile notebook). R6 mass, at risk in v0.1 at 29.4 g, is met at 26.2 g with the textile strap adopted in TRT-DDR-002 and the parts added to make the design buildable (TRT-DDR-003). No requirement is shown to be not met. Two conditions carry the result: the firmware must measure the IMU's true sample rate against the module's crystal (R1), and it must sleep between samples (R4).

Every number in this note is printed by `docs/04-calcs/sizing.py` (run `python docs/04-calcs/sizing.py` from the repo root). Size and mass read the geometry directly from `cad/src/model.py`; cost reads `bom/bom.csv`.

> **Safety:** TremorTrace is a research and educational prototype, not a medical device. It carries a lithium polymer cell against the skin: use a protected cell, never charge while worn, and stop use if the pod becomes warm or swollen.

## 1. Results against requirements

Table 1 lists every requirement. Status is one of met, not met, at risk, or not verifiable at TRL 3.

Table 1. Requirement status at TRL 3.

| ID | Target | Value from this note | Status |
| --- | --- | --- | --- |
| R7 | Silicone or textile strap, no exposed electronics, IP54 target | Sealed PETG pod with TPU gasket, contacts through the floor; no ingress test possible on paper | Not verifiable at TRL 3 |
| R8 | Open notebook producing a daily profile | Summary record defined (Table 4); notebook not yet written | Not verifiable at TRL 3 |
| R1 | 3 to 15 Hz band, resolution 0.2 Hz or better | 0.100 Hz bins, 52 Hz Nyquist; synthetic worst error 0.002 Hz | Met, if the sample rate is corrected against the crystal |
| R6 | Mass 30 g or less with strap; pod within 45 x 35 x 14 mm | 26.2 g (3.8 g margin, textile strap mass assumed 8 g); pod 40 x 30 x 12 mm | Met |
| R2 | Acceleration and angular velocity RMS in band, per window | Noise floor 0.31 mg and 0.017 dps RMS in band; ranges +/-8 g and +/-2000 dps; synthetic amplitude error 0.6 % or less | Met |
| R3 | 6-axis IMU at 100 Hz or more | LSM6DS3TR-C at 104 Hz | Met |
| R4 | 3 days or more at 16 h of wear per day | 6.3 days nominal, 4.5 days conservative | Met, if the firmware sleeps (0.69 days if it never sleeps) |
| R5 | 7 days of summaries at 16 h per day, with raw snippet reserve | 9.7 days after a 256 kB raw reserve | Met (6.4 days if the band logs 24 h per day) |
| R9 | Local storage, owner-controlled export, no cloud | Architecture has no cloud path; web Bluetooth page reads locally | Met (design review) |
| R10 | Parts cost against the USD 150 value-engineering target, no custom PCB | USD 43.79 over 12 BOM lines, USD 106.21 under the target; module plus hand wiring | Met |
| R11 | LED and web Bluetooth page show battery, recording and sync state | RGB LED on the module under a 2 mm light pipe; page defined in TRT-PRC-001 | Met (design review) |

## 2. Sampling and frequency resolution (R1, R3)

Assumptions: the IMU runs at an output data rate of 104 Hz; each summary covers a 10 s window; the tremor band is 3 to 15 Hz.

- Samples per window N = 104 x 10 = 1,040. Bin spacing is 104 / 1,040 = 0.100 Hz, half the 0.2 Hz target. The Nyquist limit is 52 Hz, more than three times the top of the band. The band spans 120 bins.
- The IMU's own oscillator sets the sample rate. Its tolerance is not in the figures used here; this note assumes up to 2 % (to be confirmed). Left uncorrected, 2 % gives up to 0.30 Hz error at 15 Hz, which would miss R1. If the firmware counts samples against the nRF52840's 32.768 kHz crystal (20 ppm), the error falls to 0.30 mHz. R1 is therefore met on the condition that the firmware applies this correction.

A synthetic check ran the window algorithm (mean removal, Hann window, FFT, parabolic peak interpolation, band-limited RMS) on six off-bin tremor frequencies from 3.33 to 14.61 Hz at 0.05 m/s² RMS with the datasheet accelerometer noise added. The worst frequency error was 0.002 Hz and the worst amplitude error was 0.6 %. This checks the arithmetic of the method, not real tremor, which drifts in frequency and amplitude within a window.

## 3. Amplitude noise floor and range (R2)

Assumptions: accelerometer noise density 90 µg/√Hz and gyroscope rate noise density 5 mdps/√Hz (LSM6DS3TR-C datasheet, high-performance mode); a detection floor at three times the in-band noise.

- In a 12 Hz band the accelerometer noise is 90 µg x √12 = 0.31 mg RMS and the gyroscope noise is 0.017 dps RMS.
- The detection floor is 0.94 mg RMS, about 9.3 µm RMS of wrist displacement at 5 Hz. Clinically visible tremor is in the millimeter range, so the floor is not a constraint.
- Range sets the upper limit. A severe tremor of 5 mm peak at 12 Hz is 2.90 g peak; with gravity the sensor sees 3.90 g, too close to a +/-4 g range. The design uses +/-8 g (0.244 mg per LSB). Rotation of +/-20 degrees at 8 Hz is 1,005 dps peak, so the gyroscope uses +/-2000 dps (70 mdps per LSB).

## 4. Activity flag (supporting analysis)

The concept flags a window as voluntary activity when the power below 3 Hz exceeds the power in the tremor band. Four synthetic cases (Table 2) show that the ratio separates rest tremor from a slow reach and from walking with heel strikes, but it also marks tremor during a reach as activity. That would undercount action and postural tremor, the main form in essential tremor.

Table 2. Band-to-low-frequency power ratio in synthetic 10 s windows (flag threshold 1.0).

| Case | Ratio | Flag |
| --- | --- | --- |
| Rest tremor, 5 Hz, 0.3 m/s² | 40,156 | Tremor |
| Voluntary reach, 0.8 Hz, 1.5 m/s² | 0.00 | Activity |
| Walking arm swing plus heel strikes | 0.24 | Activity |
| Tremor at 5 Hz during a reach | 0.04 | Activity |

Consequence for the design: every summary record keeps the tremor-band RMS and dominant frequency whatever the flag says, and the flag is stored as a separate field. The notebook can then report tremor at rest and tremor during activity separately rather than discarding windows. A better classifier is an open question for later work; it cannot be validated on paper.

## 5. Power budget (R4)

Assumptions (Table 3): 16 h per day worn and recording, 8 h off the wrist with the accelerometer in a low-rate wear-detection mode; a 150 mAh protected cell with 85 % usable above a 3.5 V firmware cutoff and a further 90 % for ageing and cold, giving 115 mAh usable.

The MCU duty is estimated from first principles for each 10 s window: reading 1,040 six-axis samples (12,480 bytes) over I²C at 400 kHz takes 281 ms if the CPU waits on the bus; filtering and six 1,024-point FFTs take about 16 ms at 64 MHz; ten FIFO wake-ups take 5 ms. That is a 3.02 % duty, or 0.195 mA average at an assumed 6.3 mA run current plus the module's standby current of less than 5 µA (Seeed wiki).

Table 3. Recording current, mA.

| Load | Nominal | Conservative | Basis |
| --- | --- | --- | --- |
| IMU, accelerometer and gyroscope | 0.90 | 0.90 | ST figure for combined high-performance mode |
| MCU | 0.195 | 0.50 | Duty estimate above; conservative allows untuned firmware |
| BLE advertising, 1 s interval | 0.015 | 0.10 | Assumed |
| QSPI flash writes | 0.005 | 0.02 | Assumed |
| Status LED | 0.002 | 0.01 | 2 mA blink, 10 ms every 10 s |
| Cell protection circuit | 0.003 | 0.005 | Assumed |
| **Total recording** | **1.120** | **1.535** | |
| Off-wrist | 0.050 | 0.080 | Assumed |

Daily use is 18.4 mAh nominal and 25.2 mAh conservative (including a daily sync of 184 kB at an assumed 10 kB/s and 5 mA), so one charge lasts 6.3 days nominal and 4.5 days conservative. R4 is met in both cases. Firmware that never lets the CPU sleep draws 166 mAh per day and lasts 0.69 days, which fails R4; sleep discipline is a firmware requirement, not an option.

Charging: the module's BQ25101 charger has 50 mA and 100 mA settings. At 50 mA the cell charges at 0.33 C in about 3.6 h, and the linear charger dissipates about 65 mW. At 100 mA it charges at 0.67 C in about 1.8 h and dissipates about 130 mW. Both are under the cell's 150 mA limit. This note uses the 50 mA setting to keep the pod cool; decided by Amish, 2026-09-25 (TRT-DDR-002). The firmware must select the 50 mA setting.

## 6. Storage (R5)

Table 4 defines the 32-byte summary record.

Table 4. Summary record, one per 10 s window.

| Field | Bytes |
| --- | --- |
| Timestamp, s | 4 |
| Dominant frequency, 0.01 Hz steps | 2 |
| Tremor-band acceleration RMS and angular velocity RMS | 4 |
| Total acceleration RMS and angular velocity RMS | 4 |
| Band-to-low-frequency power ratio and peak width | 4 |
| Dominant tremor axis, three signed components | 6 |
| Flags (worn, activity, charging) and battery level | 2 |
| Reserved | 4 |
| CRC | 2 |
| **Total** | **32** |

Assumptions: 16 h of wear per day, with no records while off the wrist (a wear-state marker only); the module's 2 MB QSPI flash holds data only, since the firmware lives in the nRF52840's internal flash; 256 kB reserved for on-demand raw snippets; 3 % overhead for sector headers and wear leveling.

- 5,760 records per day x 32 bytes = 184.3 kB per day.
- 1,780 kB is available, which holds 9.7 days at 16 h per day. If wear detection failed and the band logged all 24 h, the history would fall to 6.4 days, under the 7-day target.
- A raw 10 s window is 12,480 bytes, so a summary is 390 times smaller. (The TRL 2 precis said about 1,000 times; corrected in TRT-PRC-001 v0.4.) The raw reserve holds 21 snippets.

## 7. Size and mass (R6)

The pod in `cad/src/model.py` is 40 mm across the wrist, 30 mm along it and 12 mm high, inside the 45 x 35 x 14 mm limit. The internal stack (3.8 mm cell, 0.5 mm foam, 3.5 mm module) is 7.8 mm in a 9.5 mm cavity. The remaining 1.7 mm is filled by an upper foam pad cut from 2 mm foam, so the lid clamps the stack (TRT-DDR-003); wires run down the 1.3 mm gaps beside the cell.

Table 5. Mass estimate.

| Part | Mass, g | Basis |
| --- | --- | --- |
| Enclosure base, PETG | 4.85 | Model volume at 1.27 g/cm³ (ribs, collar and deeper notches added, TRT-DDR-003) |
| Enclosure lid, PETG | 2.22 | Model volume at 1.27 g/cm³ |
| Gasket, TPU | 0.24 | Model volume at 1.21 g/cm³ |
| Textile strap, 22 mm | 8.00 | Assumed |
| Controller and IMU module | 3.00 | Assumed |
| LiPo cell, 150 mAh | 4.65 | Adafruit 1317 listing |
| Charging connector receptacle | 1.00 | Assumed |
| Spring bars, 2 | 0.60 | Assumed |
| M2 x 6 countersunk screws, 4 | 0.60 | Assumed |
| Wire, two foam pads, light pipe, epoxy | 1.00 | Assumed |
| **Total** | **26.2** | |

The total is 3.8 g under the limit, so R6 is met. The strap is still the largest and least certain item: v0.1 of this note used a 12 g silicone strap, which gave 29.4 g and only 0.6 g of margin, so TRT-DDR-002 replaced it with a woven textile strap of about 8 g. A heavier 10 g textile strap would still give 28.2 g. The first TRL 2 estimate (22 g) assumed a 5 g enclosure and a 10 g strap; the model shows the enclosure at 7.3 g. Making the design buildable (TRT-DDR-003) added 0.8 g: two more screws, the upper foam pad, epoxy, and the ribs and collar in the base.

## 8. Cost (R10)

Value-engineering target: USD 150 (`budget_usd`, a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 43.79 (USD 106.21 under the target), over 12 priced lines in `bom/bom.csv`. The Schottky diode in the charging receptacle's positive lead (TRT-DDR-003 A2) adds USD 0.10 and 0.02 g. The textile strap is priced at USD 10.00 against USD 8.00 for the silicone strap in v0.1, and two more lid screws added USD 0.50 under TRT-DDR-003. The cell price and size were checked against the Adafruit listing on 2026-09-25; the other prices are indicative and are confirmed at order.

## 9. Sources

- STMicroelectronics, [LSM6DS3TR-C product page](https://www.st.com/en/mems-and-sensors/lsm6ds3tr-c.html) and [datasheet](https://www.st.com/resource/en/datasheet/lsm6ds3tr-c.pdf): 0.90 mA combined high-performance current, 90 µg/√Hz, 5 mdps/√Hz, full-scale ranges and sensitivities.
- Seeed Studio, [XIAO nRF52840 Series wiki](https://wiki.seeedstudio.com/XIAO_BLE/): 21 x 17.8 mm, 2 MB flash, LSM6DS3TR-C, BQ25101 charger at 50 or 100 mA, standby under 5 µA.
- Adafruit, [Lithium Ion Polymer Battery 3.7 V 150 mAh, product 1317](https://www.adafruit.com/product/1317): 19.75 x 26.02 x 3.8 mm, 4.65 g, protection circuit, charge at 150 mA or less, $5.95.

Values marked "assumed" in this note have no source and are to be confirmed when hardware work is authorized.
