"""TremorTrace concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot
from concept import Part, render_all

POD_W, POD_L = 40.0, 30.0   # across the wrist (Y), along the forearm (X), mm
WRIST_R = 30.0
STRAP_W, STRAP_T = 22.0, 2.5
top = WRIST_R + STRAP_T      # outer face of the strap at the top of the wrist

strap = Rot(0, 90, 0) * (Cylinder(WRIST_R + STRAP_T, STRAP_W) - Cylinder(WRIST_R, STRAP_W + 1))
base = Pos(0, 0, top + 2.0) * (Box(POD_L, POD_W, 4.0) - Pos(0, 0, 1.0) * Box(POD_L - 3, POD_W - 3, 4.0))
battery = Pos(0, 0, top + 4.0) * Box(20.0, 30.0, 5.0)
module = Pos(0, 0, top + 8.5) * Box(18.0, 21.0, 3.5)
lid = Pos(0, 0, top + 12.0) * (Box(POD_L, POD_W, 3.0) - Pos(0, 0, -1.0) * Box(POD_L - 3, POD_W - 3, 2.0))
contacts = Pos(0, POD_W / 2 - 6, top - 0.5) * Box(8.0, 4.0, 1.5)

parts = [
    Part("Silicone strap", strap, "#374151", 1),
    Part("Enclosure lid", lid, "#E5E7EB", 2, (0, 0, 60)),
    Part("Controller and IMU module", module, "#0F766E", 3, (0, 0, 42)),
    Part("LiPo cell, 150 mAh", battery, "#C2410C", 4, (0, 0, 24)),
    Part("Enclosure base", base, "#D1D5DB", 5, (0, 0, 8)),
    Part("Charging contacts", contacts, "#D4A017", 6, (0, 0, -14)),
]
forearm = Rot(0, 90, 0) * Pos(0, 0, -15) * Cylinder(WRIST_R - 0.5, 110)
hand = Pos(88, 0, -4) * Box(62, 70, 24)
context = [Part("Forearm and hand", forearm + hand, "#C8CDD3")]

render_all(
    parts, project="TremorTrace", title="Wrist pod concept", dwg_no="TRT-DWG-010",
    key_figures=["6-axis IMU at 104 Hz, 3 to 15 Hz band", "10 s tremor summaries on the band",
                 "About 4 days per charge (estimate)", "About 22 g with strap (estimate)",
                 "About $40 in parts (indicative)"],
    scale_figure=False, context=context, cut_exclude=("Silicone strap",),
    flow={"title": "data flow (local-first, no cloud)", "unit": "",
          "stages": [("Wrist motion", "6-axis, 104 Hz"), ("On-band summary", "every 10 s"),
                     ("Band flash", "about 10 days"), ("Phone or laptop", "BLE sync"),
                     ("Daily profile", "open notebook")]},
)
