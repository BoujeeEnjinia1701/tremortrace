"""TremorTrace parametric model (build123d), TRL 3 massing-plus level.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl.

Axes: X along the forearm (toward the hand is +X), Y across the wrist, Z up
(away from the skin). The pod underside rests on the skin at Z = 0.

Detail level: correct interfaces (strap lugs, spring bars, gasket seat, lid
screws, charging connector opening, LED light pipe) and main dimensions. Not
fabrication detail. PRELIMINARY, NOT FOR FABRICATION.
"""
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # Pod envelope (R6 limit: 45 x 35 x 14 mm)
    "pod_x": 30.0,            # along the forearm
    "pod_y": 40.0,            # across the wrist, including integrated lugs
    "pod_h": 12.0,            # overall height, base + gasket + lid
    "wall": 1.5,              # side wall thickness
    "floor": 1.0,             # base floor thickness
    "lid_t": 1.5,             # lid thickness
    "gasket_t": 0.5,          # compressed TPU gasket thickness
    "corner_r": 3.0,          # plan-view corner radius
    # Strap interface (standard 22 mm watch strap, quick-release spring bars)
    "strap_w": 22.0,          # lug width between the horns
    "lug_notch_d": 4.0,       # notch depth into each Y end, under the spring bar
    "lug_notch_h": 6.0,       # notch height from the underside
    "bar_d": 1.8,             # spring bar hole diameter
    "bar_z": 3.0,             # spring bar axis height above the skin
    "bar_inset": 2.0,         # spring bar axis distance from the pod Y end
    # Internal parts (envelopes)
    "cell": (19.75, 26.02, 3.8),   # 150 mAh protected LiPo, X, Y, Z (Adafruit 1317 class)
    "module": (17.8, 21.0, 3.5),   # XIAO nRF52840 Sense class, X, Y, Z (height assumed)
    "foam_t": 0.5,            # foam pad between cell and module
    "pogo": (4.0, 8.0, 3.0),  # magnetic 2-pin charging receptacle, X, Y, Z
    "led_d": 2.0,             # light pipe bore in the lid
    "screw_d": 1.6,           # M2 thread-forming screw pilot hole
    "screw_len": 6.0,
    # Context
    "wrist_r": 32.0,          # wrist radius used for the strap loop
    "strap_t": 2.5,
}


def _derived(p):
    d = dict(p)
    d["base_h"] = p["pod_h"] - p["lid_t"] - p["gasket_t"]
    d["cav_x"] = p["pod_x"] - 2 * p["wall"]
    # The cavity stops short of the lug notches so the notch walls stay closed.
    d["cav_y"] = p["pod_y"] - 2 * (p["lug_notch_d"] + 1.2)
    d["cav_h"] = d["base_h"] - p["floor"] + p["gasket_t"]   # floor to lid underside
    d["screw_y"] = p["pod_y"] / 2 - p["lug_notch_d"] / 2 - 0.6
    cx, cy, cz = p["cell"]
    d["cell_x0"] = -d["cav_x"] / 2 + 0.3                   # cell against the -X wall
    d["cell_cx"] = d["cell_x0"] + cx / 2
    d["pogo_cx"] = d["cav_x"] / 2 - p["pogo"][0] / 2 - 0.4  # connector beside the cell, +X side
    return d


def build_parts(params=None):
    """Return a dict of named build123d solids for the assembly."""
    from build123d import (Box, Cylinder, Pos, Rot, fillet, Axis)
    p = _derived(params or PARAMS)
    X, Y, H = p["pod_x"], p["pod_y"], p["base_h"]

    # Enclosure base: rounded box, cavity, lug notches, spring bar holes, screw pilots, connector opening
    base = Pos(0, 0, H / 2) * Box(X, Y, H)
    base = fillet(base.edges().filter_by(Axis.Z), p["corner_r"])
    base -= Pos(0, 0, p["floor"] + H / 2) * Box(p["cav_x"], p["cav_y"], H)
    for s in (-1, 1):
        base -= Pos(0, s * (Y / 2 - p["lug_notch_d"] / 2 + 0.5), p["lug_notch_h"] / 2 - 0.5) * Box(
            p["strap_w"], p["lug_notch_d"] + 1.0, p["lug_notch_h"] + 1.0)
        base -= Pos(0, s * (Y / 2 - p["bar_inset"]), p["bar_z"]) * Rot(0, 90, 0) * Cylinder(p["bar_d"] / 2, X + 2)
        engage = p["screw_len"] - p["lid_t"] - p["gasket_t"]      # thread engagement in the base
        base -= Pos(0, s * p["screw_y"], H - engage / 2 + 0.5) * Cylinder(p["screw_d"] / 2, engage + 1.0)
    px, py, pz = p["pogo"]
    base -= Pos(p["pogo_cx"], 0, p["floor"] / 2) * Box(px, py, p["floor"] + 0.2)

    # Gasket: perimeter ring on the base rim
    ring_out = fillet((Pos(0, 0, 0) * Box(X, Y, p["gasket_t"])).edges().filter_by(Axis.Z), p["corner_r"])
    gasket = Pos(0, 0, H + p["gasket_t"] / 2) * (ring_out - Box(p["cav_x"], p["cav_y"], p["gasket_t"] + 1))
    for s in (-1, 1):
        gasket -= Pos(0, s * p["screw_y"], H + p["gasket_t"] / 2) * Cylinder(1.1, 2)

    # Lid: plate with screw clearance holes and LED light pipe bore
    lid_z = H + p["gasket_t"]
    lid = fillet(Box(X, Y, p["lid_t"]).edges().filter_by(Axis.Z), p["corner_r"])
    lid = Pos(0, 0, lid_z + p["lid_t"] / 2) * lid
    for s in (-1, 1):
        lid -= Pos(0, s * p["screw_y"], lid_z + p["lid_t"] / 2) * Cylinder(1.1, p["lid_t"] + 1)
    led_xy = (0.0, -p["module"][1] / 2 + 4.0)
    lid -= Pos(led_xy[0], led_xy[1], lid_z + p["lid_t"] / 2) * Cylinder(p["led_d"] / 2, p["lid_t"] + 1)

    # Internal envelopes
    cx, cy, cz = p["cell"]
    cell = Pos(p["cell_cx"], 0, p["floor"] + cz / 2) * Box(cx, cy, cz)
    mx, my, mz = p["module"]
    mod_z0 = p["floor"] + cz + p["foam_t"]
    module = Pos(0, 0, mod_z0 + mz / 2) * Box(mx, my, mz)
    pogo = Pos(p["pogo_cx"], 0, pz / 2) * Box(px, py, pz)
    bars = None
    for s in (-1, 1):
        b = Pos(0, s * (Y / 2 - p["bar_inset"]), p["bar_z"]) * Rot(0, 90, 0) * Cylinder(0.75, p["strap_w"] + 3)
        bars = b if bars is None else bars + b

    # Strap: loop around the wrist, cut back where it meets the pod lugs
    R, T = p["wrist_r"], p["strap_t"]
    strap = Pos(0, 0, -R + 0.5) * Rot(0, 90, 0) * (Cylinder(R + T, p["strap_w"]) - Cylinder(R, p["strap_w"] + 1))
    strap -= Pos(0, 0, 10) * Box(p["strap_w"] + 2, Y - 2 * p["bar_inset"] - 2, 40)

    return {"strap": strap, "lid": lid, "module": module, "cell": cell, "base": base,
            "pogo": pogo, "gasket": gasket, "bars": bars, "_p": p, "_led": led_xy}


def build(params=None):
    """Pod assembly without the strap (the object on the general arrangement drawing)."""
    from build123d import Compound
    parts = build_parts(params)
    return Compound(children=[parts[k] for k in ("base", "gasket", "lid", "cell", "module", "pogo", "bars")])


def export(out=None):
    from build123d import Compound, export_step, export_stl
    out = Path(out) if out else Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    pod = build()
    export_step(pod, str(out / "step" / "tremortrace-pod-assembly.step"))
    export_stl(pod, str(out / "stl" / "tremortrace-pod-assembly.stl"))
    fresh = build_parts()   # a shape can only have one parent, so the strap assembly uses fresh copies
    full = Compound(children=[fresh[k] for k in ("base", "gasket", "lid", "cell", "module", "pogo", "bars", "strap")])
    export_step(full, str(out / "step" / "tremortrace-on-strap.step"))
    for name in ("base", "lid", "gasket"):
        export_step(parts[name], str(out / "step" / f"tremortrace-{name}.step"))
        export_stl(parts[name], str(out / "stl" / f"tremortrace-{name}.stl"))
    return parts


if __name__ == "__main__":
    parts = export()
    bb = build().bounding_box()
    print(f"Pod assembly envelope: {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm (X x Y x Z)")
    for k in ("base", "lid", "gasket"):
        print(f"{k:7s} volume {parts[k].volume / 1000:.2f} cm3")
