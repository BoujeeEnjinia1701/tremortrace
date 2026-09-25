# TremorTrace

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** BioMedical · **TRL:** 3 of 9 (proof of concept by calculation) · **Prototype budget:** about $150 USD · **Difficulty:** 2 of 5

Wrist-worn IMU band that logs tremor frequency and amplitude continuously, with an open analysis notebook that produces a daily tremor profile.

![TremorTrace concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Review note](docs/REVIEW.md)

## Problem

Tremor severity is scored during short clinic visits, which misses how it varies day to day.

## Concept

Wrist-worn IMU band that logs tremor frequency and amplitude continuously, with an open analysis notebook that produces a daily tremor profile.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Seeed XIAO nRF52840 Sense class module (nRF52840 BLE, 6-axis IMU, 2 MB flash, charger)
- 150 mAh protected LiPo cell
- Printed PETG enclosure with TPU gasket, 40 x 30 x 12 mm
- 22 mm silicone strap

The priced bill of materials ($41.19 in parts) is in [bom/bom.csv](bom/bom.csv).

## Status at TRL 3

Calculations in [TRT-CAL-001](docs/04-calcs/01-sizing.md) show 0.1 Hz frequency resolution, 4.5 to 6.3 days per charge and 9.7 days of on-band history. Mass is at risk at 29.4 g against a 30 g limit. The parametric model is [cad/src/model.py](cad/src/model.py) and the general arrangement is [TRT-DWG-002](cad/drawings/TRT-DWG-002.pdf). TRL 4 work is on hold.

## Safety

> This is a research and educational prototype. It is not a medical device, has not been cleared or approved by any regulator, and must not be used to diagnose, treat or monitor any person.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (TRT-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `TRT-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
