"""TremorTrace concept media from the TRL 3 parametric model.

Run from the repo root:  python cad/src/concept_media.py
Geometry comes from cad/src/model.py; not for fabrication.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build123d import Box, Cylinder, Pos, Rot
from concept import Part, render_all
import model

P = model.build_parts()
p = P["_p"]

parts = [
    Part("Silicone strap", P["strap"], "#374151", 1),
    Part("Enclosure lid", P["lid"], "#E5E7EB", 2, (0, 0, 64)),
    Part("Controller and IMU module", P["module"], "#0F766E", 3, (0, 0, 46)),
    Part("LiPo cell, 150 mAh", P["cell"], "#C2410C", 4, (0, 0, 30)),
    Part("Enclosure base", P["base"], "#D1D5DB", 5, (0, 0, 12)),
    Part("Charging connector", P["pogo"], "#D4A017", 6, (0, 0, -16)),
    Part("TPU gasket", P["gasket"], "#6B7280", 7, (0, 0, 55)),
    Part("Spring bars", P["bars"], "#9CA3AF", 8, (0, 0, 0)),
]
R = p["wrist_r"]
forearm = Pos(0, 0, -R + 0.5) * Rot(0, 90, 0) * Pos(0, 0, -15) * Cylinder(R - 0.5, 110)
hand = Pos(88, 0, -R + 0.5 - 4) * Box(62, 70, 24)
context = [Part("Forearm and hand", forearm + hand, "#C8CDD3")]

render_all(
    parts, project="TremorTrace", title="Wrist pod concept", dwg_no="TRT-DWG-001",
    date="2026-09-25",
    key_figures=["6-axis IMU at 104 Hz, 3 to 15 Hz band, 0.1 Hz bins", "10 s tremor summaries on the band",
                 "4.5 to 6.3 days per charge (TRT-CAL-001)", "About 29.4 g with strap, limit 30 g",
                 "Pod 40 x 30 x 12 mm; parts $41.19 (BOM)"],
    scale_figure=False, context=context, cut_exclude=("Silicone strap",),
    flow={"title": "data flow (local-first, no cloud)", "unit": "",
          "stages": [("Wrist motion", "6-axis, 104 Hz"), ("On-band summary", "32 B every 10 s"),
                     ("Band flash", "about 9.7 days"), ("Phone or laptop", "web Bluetooth sync"),
                     ("Daily profile", "open notebook")]},
)
