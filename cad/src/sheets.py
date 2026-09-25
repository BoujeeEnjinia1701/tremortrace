"""TremorTrace drawing sheets.

Run from the repo root:  python cad/src/sheets.py
Builds TRT-DWG-002 (general arrangement, Rev P1) in cad/drawings/ from cad/src/model.py.
TRT-DWG-001 is the concept sheet made by cad/src/concept_media.py.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(ROOT / "cad" / "src"))
from drawing import Sheet, project_views  # noqa: E402
import model  # noqa: E402

p = model.build_parts()["_p"]
pod = model.build()
work = ROOT / "cad" / "drawings" / "_views"
views = project_views(pod, work)

s = Sheet(project="TremorTrace", title="Wrist pod general arrangement", dwg_no="TRT-DWG-002", rev="P1",
          author="Amish Chadha", date="2026-09-25", scale=2.0, concept=True,
          material="Base and lid PETG, gasket TPU 95A; bought parts per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
          revisions=[("P1", "General arrangement for TRL 3 (TRT-CAL-001)", "2026-09-25", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 32, 140, 78, label="Isometric view", sublabel="Not to scale; strap omitted")
cx, cy, cz = p["cell"]
mx, my, mz = p["module"]
s.add_notes("Main dimensions (mm)", [
    f"Pod envelope {p['pod_y']:.0f} across wrist x {p['pod_x']:.0f} along forearm x {p['pod_h']:.0f} high",
    f"Base {p['base_h']:.1f} high, wall {p['wall']:.1f}, floor {p['floor']:.1f}; lid {p['lid_t']:.1f}",
    f"Gasket {p['gasket_t']:.1f} compressed; corner radius {p['corner_r']:.0f}",
    f"Cavity {p['cav_x']:.1f} x {p['cav_y']:.1f} x {p['cav_h']:.1f}",
    f"Lugs: {p['strap_w']:.0f} between horns, notch {p['lug_notch_d']:.0f} deep x {p['lug_notch_h']:.0f} high",
    f"Spring bar holes {p['bar_d']:.1f} dia, {p['bar_inset']:.0f} from end, {p['bar_z']:.0f} above skin",
    f"Lid screws 2 x M2 x {p['screw_len']:.0f} on centerline, {p['screw_y']:.1f} from center",
    f"Cell {cx:.2f} x {cy:.2f} x {cz:.1f}; module {mx:.1f} x {my:.0f} x {mz:.1f}",
    f"Charging opening {p['pogo'][0]:.0f} x {p['pogo'][1]:.0f} in floor; LED bore {p['led_d']:.0f} dia",
], x=276, y=124, width=140)
s.add_notes("Parts list (items match bom/bom.csv)", [
    "1 Silicone strap, 22 mm (not shown)",
    "2 Enclosure lid, PETG",
    "3 Controller and IMU module (XIAO class)",
    "4 LiPo cell, 150 mAh protected",
    "5 Enclosure base, PETG",
    "6 Magnetic 2-pin charging connector",
], x=20, y=222, width=100)
s.add_notes("Parts list, continued", [
    "7 TPU gasket",
    "8 Spring bars, 22 mm",
    "9 Lid screws, 2 x M2 x 6",
    "10 Light pipe, 2 mm",
    "11 Consumables",
    "Not a medical device. Never charge while worn.",
], x=124, y=222, width=100)
s.save(ROOT / "cad" / "drawings" / "TRT-DWG-002")
shutil.rmtree(work, ignore_errors=True)
print("Wrote cad/drawings/TRT-DWG-002.svg, .pdf and .png")
