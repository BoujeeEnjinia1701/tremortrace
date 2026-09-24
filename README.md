# TremorTrace

**Area:** BioMedical · **Status:** Concept · **Prototype budget:** about $150 USD · **Difficulty:** 2 of 5

Wrist-worn IMU band that logs tremor frequency and amplitude continuously, with an open analysis notebook that produces a daily tremor profile.

## Problem

Tremor severity is scored during short clinic visits, which misses how it varies day to day.

## Concept

Wrist-worn IMU band that logs tremor frequency and amplitude continuously, with an open analysis notebook that produces a daily tremor profile.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- 6-axis IMU
- nRF52 BLE module
- LiPo cell
- Printed enclosure
- Silicone strap

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

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

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
