---
doc_id: TRT-PRB-001
title: TremorTrace problem statement
project: TremorTrace
doc_type: Problem statement
version: "0.3"
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
  change: Populate to TRL 2 (users, context, constraints, prior work)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Wrist question closed per TRT-DDR-001; partner question stays open
---

# TremorTrace problem statement

Tremor is judged from a few minutes of observation in a clinic, but it changes through the day with medication timing, fatigue, stress and activity, so the snapshot a clinician sees is often not the tremor a person lives with.

## The problem

People with Parkinson's disease and essential tremor are typically assessed with rating scales (for example the MDS-UPDRS tremor items or TETRAS) during an appointment every few months. Those scores depend on what happens in the room that day. Patients are asked to recall how their tremor behaved between visits, and recall is poor. Medication changes are therefore judged on thin evidence.

Research has shown that a wrist-worn accelerometer and gyroscope can measure tremor frequency and amplitude continuously at home ([Mahadevan et al., npj Digital Medicine](https://www.nature.com/articles/s41746-019-0217-7); [standardized accelerometry method, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9386269/); [rest tremor from the wrist, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11942689/)). Commercial systems exist, but they are closed, costly, or tied to one phone ecosystem. There is no open, low-cost, inspectable reference design that a researcher, clinic or patient group can build, audit and adapt.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Person living with tremor | Wear it all day without thinking about it; see how tremor changed and share it | At home, daily activities, 12 to 16 h of wear |
| Care partner | Understand good and bad periods of the day | Home |
| Clinician or researcher | Objective daily tremor profile between visits, in a format they can analyze | Clinic review, research studies |
| Open hardware community | A reproducible design and analysis pipeline to build on | Makerspaces, university labs |

## Constraints

- Garage-buildable prototype, about $150 USD per unit, using off-the-shelf modules and 3D-printed parts.
- Comfortable for all-day wear: light, small, skin-safe materials.
- Health data is sensitive: data stays on the device and the owner's phone by default; the owner controls any sharing.
- Research and educational use only. TremorTrace is not a medical device and must not be used to diagnose, treat or change medication.

## Out of scope

- Diagnosis or classification of disease.
- Tremor suppression or stimulation.
- Cloud services.

## Open questions

- Which users to involve first, and through which partner (a movement disorders clinic, a patient association, or OpenRatio's network)? No recommendation has been made; proposed, awaiting Amish.
- One wrist or both: closed. Decided by Amish, 2026-09-25 (TRT-DDR-001): the most affected wrist first, both wrists later.
