"""TremorTrace parametric model (build123d), constructable design (TRT-DDR-003).

Run from the repo root:
    python cad/src/model.py            export STEP and STL into cad/step and cad/stl, print the checks
    python cad/src/model.py --check    print the constructability checks only

Axes: X along the forearm (toward the hand is +X), Y across the wrist, Z up
(away from the skin). The pod underside rests on the skin at Z = 0.

Detail level: every part that is made or fitted in the prototype build plan
(TRT-BLD-001), with its fixing: base with lug horns, spring bar tip holes, cell
locating ribs and a glue collar for the charging receptacle; gasket; lid with four
countersunk screw seats and a light pipe; foam pads; spring bars with tips; strap
ends looped round the bars. PRELIMINARY, NOT FOR FABRICATION.
"""
import sys
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
    "gasket_t": 0.5,          # compressed TPU gasket thickness (printed 0.8 mm)
    "corner_r": 3.0,          # plan-view corner radius
    # Strap interface (standard 22 mm watch strap, quick-release spring bars)
    "strap_w": 22.0,          # lug width between the horns
    "lug_notch_d": 4.5,       # notch depth into each Y end, under the spring bar (DDR-003 C2; was 4.0)
    "lug_notch_h": 6.0,       # notch height from the underside
    "bar_d": 1.0,             # spring bar tip hole through each horn (DDR-003 C1; was 1.8)
    "bar_body_d": 1.5,        # spring bar body
    "bar_tip_d": 0.9,         # spring bar tip
    "bar_tip_len": 1.5,       # tip engagement in each horn
    "bar_z": 3.0,             # spring bar axis height above the skin
    "bar_inset": 2.0,         # spring bar axis distance from the pod Y end
    # Internal parts (envelopes)
    "cell": (19.75, 26.02, 3.8),   # 150 mAh protected LiPo, X, Y, Z (Adafruit 1317 class)
    "module": (17.8, 21.0, 3.5),   # XIAO nRF52840 Sense class, X, Y, Z (height assumed)
    "foam_t": 0.5,            # adhesive foam pad between cell and module
    "top_foam_t": 1.7,        # foam pad between module and lid, compressed (DDR-003 C5; cut from 2 mm)
    "pogo": (4.0, 8.0, 3.0),  # magnetic 2-pin charging receptacle, X, Y, Z
    "diode": (1.6, 2.7, 1.1),  # Schottky diode, SOD-123 body, X, Y, Z (decided 2026-10-02, TRT-DDR-003 A2)
    "diode_y": 8.5,           # diode centre across the wrist, beside the receptacle collar, on the base floor
    "mark_depth": 0.4,        # lid mark debossed into the lid (two 0.2 mm layers, decided 2026-10-02)
    "mark_w": 0.6,            # line width of the mark
    "led_d": 2.0,             # light pipe bore in the lid
    "pipe_len": 2.0,          # light pipe length (top flush with the lid)
    "led_hole_d": 4.0,        # hole in the top foam pad round the LED and light pipe
    "cell_gap": 0.3,          # clearance round the cell in its pocket
    "rib_w": 1.0,             # cell locating rib width (DDR-003 C4)
    "rib_h": 1.5,             # rib height above the floor
    "collar_w": 0.8,          # glue collar wall round the charging receptacle (DDR-003 C3)
    "collar_h": 2.0,          # collar height above the floor
    # Lid screws: four M2 x 6 countersunk thread-forming, one in each lug horn (DDR-003 C2)
    "screw_d": 1.6,           # pilot hole (thread core)
    "screw_clear_d": 2.2,     # clearance hole in the lid and gasket
    "screw_len": 6.0,         # overall length, head included
    "head_d": 3.8,            # countersunk head diameter
    "head_h": 1.1,            # countersunk head depth
    "screw_inset_y": 2.6,     # screw axis distance from the pod Y end
    # Context
    "wrist_r": 32.0,          # wrist radius used for the strap loop
    "strap_t": 1.4,           # woven textile quick-release strap, about 8 g (DDR-002 D7)
    "strap_clear": 0.2,       # strap side clearance to each horn
}


def _derived(p):
    d = dict(p)
    d["base_h"] = p["pod_h"] - p["lid_t"] - p["gasket_t"]
    d["lid_z"] = d["base_h"] + p["gasket_t"]
    d["cav_x"] = p["pod_x"] - 2 * p["wall"]
    # The cavity stops short of the lug notches so the notch walls stay closed.
    d["cav_y"] = p["pod_y"] - 2 * (p["lug_notch_d"] + 1.2)
    d["cav_h"] = d["base_h"] - p["floor"] + p["gasket_t"]   # floor to lid underside
    # Screws sit in the middle of each lug horn (the solid corner between notch and side face).
    d["screw_x"] = p["strap_w"] / 2 + (p["pod_x"] - p["strap_w"]) / 4
    d["screw_y"] = p["pod_y"] / 2 - p["screw_inset_y"]
    d["screw_engage"] = p["screw_len"] - p["lid_t"] - p["gasket_t"]
    cx, cy, cz = p["cell"]
    d["cell_x0"] = -d["cav_x"] / 2 + p["cell_gap"]         # cell against the -X wall
    d["cell_cx"] = d["cell_x0"] + cx / 2
    d["pogo_cx"] = d["cav_x"] / 2 - p["pogo"][0] / 2 - 0.4  # connector beside the cell, +X side
    d["mod_z0"] = p["floor"] + cz + p["foam_t"]
    d["mod_top"] = d["mod_z0"] + p["module"][2]
    d["bar_y"] = p["pod_y"] / 2 - p["bar_inset"]
    return d


def _b():
    import build123d as b
    return b


def _xcyl(r, length, x, y, z):
    b = _b()
    return b.Pos(x, y, z) * b.Rot(0, 90, 0) * b.Cylinder(r, length)


def _rbox(x, y, h, r, z0, cx=0.0, cy=0.0):
    """Box with vertical edges rounded, from z0 up."""
    b = _b()
    s = b.Pos(cx, cy, z0 + h / 2) * b.Box(x, y, h)
    return b.fillet(s.edges().filter_by(b.Axis.Z), r)


def mark_points(n=26):
    """Centre line of the tremor-trace mark on the lid (x, y in mm): a short decaying wave."""
    import math
    pts = []
    for k in range(n + 1):
        x = -9.0 + 18.0 * k / n
        amp = 2.4 * math.exp(-((x + 1.0) / 6.0) ** 2)
        pts.append((x, 4.0 + amp * math.sin(2 * math.pi * (x + 9.0) / 4.5)))
    return pts


def _mark_cutter(p, top):
    """Solid that is removed from the lid top to deboss the mark."""
    import math
    b = _b()
    pts = mark_points()
    d, w = p["mark_depth"], p["mark_w"]
    segs = []
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
        segs.append(b.Pos((x0 + x1) / 2, (y0 + y1) / 2, top - d / 2 + 0.05) * b.Rot(0, 0, ang) * b.Box(L + 0.01, w, d + 0.1))
        segs.append(b.Pos(x1, y1, top - d / 2 + 0.05) * b.Cylinder(w / 2, d + 0.1))
    segs.append(b.Pos(pts[0][0], pts[0][1], top - d / 2 + 0.05) * b.Cylinder(w / 2, d + 0.1))
    out = segs[0]
    for sg in segs[1:]:
        out = out + sg
    return out


def build_parts(params=None):
    """Return a dict of named build123d solids for the assembly."""
    b = _b()
    Box, Cylinder, Cone, Pos = b.Box, b.Cylinder, b.Cone, b.Pos
    p = _derived(params or PARAMS)
    X, Y, H = p["pod_x"], p["pod_y"], p["base_h"]
    sx_, sy_ = p["screw_x"], p["screw_y"]
    corners = [(i * sx_, j * sy_) for i in (-1, 1) for j in (-1, 1)]

    # Enclosure base: rounded box, cavity, lug notches, spring bar tip holes, screw pilots, receptacle opening
    base = _rbox(X, Y, H, p["corner_r"], 0)
    base -= Pos(0, 0, p["floor"] + H / 2) * Box(p["cav_x"], p["cav_y"], H)
    for s in (-1, 1):
        d = p["lug_notch_d"]
        base -= Pos(0, s * (Y / 2 - d / 2 + 0.5), p["lug_notch_h"] / 2 - 0.5) * Box(p["strap_w"], d + 1.0, p["lug_notch_h"] + 1.0)
        base -= _xcyl(p["bar_d"] / 2, X + 2, 0, s * p["bar_y"], p["bar_z"])
    for (x, y) in corners:
        dep = p["screw_engage"] + 0.5
        base -= Pos(x, y, H - dep / 2) * Cylinder(p["screw_d"] / 2, dep)
    # Cell locating ribs (printed with the base): one on the +X side, one along each Y side
    cx, cy, cz = p["cell"]
    rz = p["floor"] + p["rib_h"] / 2
    x_end = p["cell_x0"] + cx
    ribs = Pos(x_end + p["cell_gap"] + p["rib_w"] / 2, 0, rz) * Box(p["rib_w"], 20.0, p["rib_h"])
    y_in = cy / 2 + p["cell_gap"]
    for s in (-1, 1):
        w = p["cav_y"] / 2 - y_in
        ribs += Pos(-3.5, s * (y_in + w / 2), rz) * Box(17.0, w, p["rib_h"])
    base += ribs
    # Glue collar round the charging receptacle, then the opening through the floor
    px, py, pz = p["pogo"]
    cw = p["collar_w"]
    x0c = p["pogo_cx"] - px / 2 - cw
    x1c = p["cav_x"] / 2 + 0.01
    collar = Pos((x0c + x1c) / 2, 0, p["floor"] + p["collar_h"] / 2) * Box(x1c - x0c, py + 2 * cw, p["collar_h"])
    base += collar
    base -= Pos(p["pogo_cx"], 0, (p["floor"] + p["collar_h"]) / 2) * Box(px, py, p["floor"] + p["collar_h"] + 0.2)

    # Gasket: perimeter ring on the base rim, with the four screw holes
    gz = H + p["gasket_t"] / 2
    gasket = _rbox(X, Y, p["gasket_t"], p["corner_r"], H) - Pos(0, 0, gz) * Box(p["cav_x"], p["cav_y"], p["gasket_t"] + 1)
    for (x, y) in corners:
        gasket -= Pos(x, y, gz) * Cylinder(p["screw_clear_d"] / 2, 2)

    # Lid: plate with four countersunk screw seats and the light pipe bore
    lz = p["lid_z"]
    lid = _rbox(X, Y, p["lid_t"], p["corner_r"], lz)
    top = lz + p["lid_t"]
    hr, hh = p["head_d"] / 2, p["head_h"]
    for (x, y) in corners:
        lid -= Pos(x, y, lz + p["lid_t"] / 2) * Cylinder(p["screw_clear_d"] / 2, p["lid_t"] + 1)
        lid -= Pos(x, y, top - hh / 2) * Cone(p["screw_d"] / 2, hr, hh)
        lid -= Pos(x, y, top + 0.25) * Cylinder(hr, 0.5)
    led_xy = (0.0, -p["module"][1] / 2 + 4.0)
    lid -= Pos(led_xy[0], led_xy[1], lz + p["lid_t"] / 2) * Cylinder(p["led_d"] / 2, p["lid_t"] + 1)
    # Tremor-trace mark: a short decaying wave debossed into the lid top (appearance in product_model.py)
    mark = _mark_cutter(p, top)
    lid -= mark

    # Screws: countersunk head in the lid seat, shank at core diameter in the pilot hole
    screws = None
    for (x, y) in corners:
        sc = Pos(x, y, top - hh / 2) * Cone(p["screw_d"] / 2, hr, hh)
        L = p["screw_len"] - hh
        sc += Pos(x, y, top - hh - L / 2) * Cylinder(p["screw_d"] / 2, L)
        screws = sc if screws is None else screws + sc

    # Light pipe, glued in the lid bore, top flush with the lid
    pipe = Pos(led_xy[0], led_xy[1], top - p["pipe_len"] / 2) * Cylinder(p["led_d"] / 2, p["pipe_len"])

    # Internal parts
    cell = Pos(p["cell_cx"], 0, p["floor"] + cz / 2) * Box(cx, cy, cz)
    foam = Pos(0, 0, p["floor"] + cz + p["foam_t"] / 2) * Box(p["module"][0], p["module"][1] - 2.0, p["foam_t"])
    mx, my, mz = p["module"]
    module = Pos(0, 0, p["mod_z0"] + mz / 2) * Box(mx, my, mz)
    tf = p["top_foam_t"]
    top_foam = Pos(0, 0, p["mod_top"] + tf / 2) * Box(mx - 1.8, my - 2.0, tf)
    top_foam -= Pos(led_xy[0], led_xy[1], p["mod_top"] + tf / 2) * Cylinder(p["led_hole_d"] / 2, tf + 1)
    pogo = Pos(p["pogo_cx"], 0, pz / 2) * Box(px, py, pz)
    # Schottky diode in the receptacle's positive lead: lies on the floor beside the collar, long side across the wrist
    dx_, dy_, dz_ = p["diode"]
    diode = Pos(p["pogo_cx"], p["diode_y"], p["floor"] + dz_ / 2) * Box(dx_, dy_, dz_)

    # Spring bars: body between the horns, tips into the horn holes
    bars = None
    for s in (-1, 1):
        y = s * p["bar_y"]
        bar = _xcyl(p["bar_body_d"] / 2, p["strap_w"], 0, y, p["bar_z"])
        L = p["strap_w"] + 2 * p["bar_tip_len"]
        bar += _xcyl(p["bar_tip_d"] / 2, L, 0, y, p["bar_z"])
        bars = bar if bars is None else bars + bar

    # Strap: two ends looped round the spring bars, each running down out of the notch and on
    # round the wrist (the buckle side under the wrist is not drawn in detail)
    R, T = p["wrist_r"], p["strap_t"]
    sw = p["strap_w"] - 2 * p["strap_clear"]
    zc = -R + 0.5
    loop = Pos(0, 0, zc) * b.Rot(0, 90, 0) * (Cylinder(R + T, sw) - Cylinder(R, sw + 1))
    yb = p["bar_y"]
    ro = p["bar_body_d"] / 2 + T
    loop -= Pos(0, 0, 10) * Box(sw + 2, 2 * (yb + ro - T) , 60)
    strap = loop
    for s in (-1, 1):
        y = s * yb
        ring = _xcyl(ro, sw, 0, y, p["bar_z"]) - _xcyl(p["bar_body_d"] / 2, sw + 1, 0, y, p["bar_z"])
        ytail = s * (yb + p["bar_body_d"] / 2 + T / 2)
        tail = Pos(0, ytail, (p["bar_z"] - 9.0) / 2) * Box(sw, T, p["bar_z"] + 9.0)
        strap += ring + tail

    return {"strap": strap, "lid": lid, "module": module, "cell": cell, "base": base,
            "pogo": pogo, "gasket": gasket, "bars": bars, "screws": screws, "pipe": pipe,
            "foam": foam, "top_foam": top_foam, "diode": diode, "_mark": mark, "_p": p, "_led": led_xy}


POD_KEYS = ("base", "gasket", "lid", "screws", "pipe", "cell", "foam", "module", "top_foam", "pogo", "diode", "bars")


def build(params=None):
    """Pod assembly without the strap (the object on the general arrangement drawing)."""
    from build123d import Compound
    parts = build_parts(params)
    return Compound(children=[parts[k] for k in POD_KEYS])


# ---------------------------------------------------------------- constructability checks
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def checks(params=None):
    """Pairs of parts: either they must touch (no overlap, gap 0) or be apart by a stated
    clearance. Returns (description, overlap mm3, gap mm, expectation, ok)."""
    P = build_parts(params)
    rows = []

    def chk(desc, a, b_, expect):
        v = _vol(P[a] if isinstance(a, str) else a, P[b_] if isinstance(b_, str) else b_)
        gp = (P[a] if isinstance(a, str) else a).distance_to(P[b_] if isinstance(b_, str) else b_)
        ok = v < 1e-3 and (gp < 0.02 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    chk("Cell on the base floor", "cell", "base", "touch")
    chk("Charging receptacle in its collar and floor opening", "pogo", "base", "touch")
    chk("Charging receptacle clear of the cell", "pogo", "cell", 1.0)
    chk("Lower foam pad on the cell", "foam", "cell", "touch")
    chk("Module on the lower foam pad", "module", "foam", "touch")
    chk("Module clear of the base (walls, ribs, collar)", "module", "base", 1.0)
    chk("Module clear of the charging receptacle", "module", "pogo", 1.0)
    chk("Lower foam pad clear of the base", "foam", "base", 1.0)
    chk("Upper foam pad on the module", "top_foam", "module", "touch")
    chk("Upper foam pad against the lid underside", "top_foam", "lid", "touch")
    chk("Upper foam pad clear of the base", "top_foam", "base", 0.5)
    chk("Light pipe in the lid bore", "pipe", "lid", "touch")
    chk("Light pipe clear of the module (LED below)", "pipe", "module", 0.5)
    chk("Light pipe clear of the upper foam pad", "pipe", "top_foam", 0.5)
    chk("Gasket on the base rim", "gasket", "base", "touch")
    chk("Lid on the gasket", "lid", "gasket", "touch")
    chk("Lid clear of the base (gasket gap)", "lid", "base", 0.4)
    chk("Cell clear of the lid", "cell", "lid", 1.0)
    chk("Screws in their lid seats", "screws", "lid", "touch")
    chk("Screws in their pilot holes in the horns", "screws", "base", "touch")
    chk("Screws clear of the gasket", "screws", "gasket", 0.2)
    chk("Screws clear of the spring bars", "screws", "bars", 1.0)
    chk("Screws clear of the strap", "screws", "strap", 0.5)
    chk("Spring bar tips in the horn holes", "bars", "base", "touch")
    chk("Strap looped on the spring bars", "strap", "bars", "touch")
    chk("Strap clear of the base (notch faces and horns)", "strap", "base", 0.15)
    chk("Strap clear of the charging receptacle", "strap", "pogo", 1.0)
    chk("Diode lies on the base floor", "diode", "base", "touch")
    chk("Diode clear of the charging receptacle (lead run 3 mm or more)", "diode", "pogo", 3.0)
    chk("Diode clear of the module", "diode", "module", 1.0)
    chk("Diode clear of the cell", "diode", "cell", 1.0)
    chk("Diode clear of the upper foam pad", "diode", "top_foam", 1.0)
    chk("Diode clear of the lid", "diode", "lid", 1.0)
    chk("Lid mark clear of the light pipe bore", "_mark", "pipe", 1.0)
    chk("Lid mark clear of the screw seats", "_mark", "screws", 1.0)
    # The cell sits in its pocket with a stated clearance to every rib and wall
    b = _b()
    p = P["_p"]
    cx, cy, cz = p["cell"]
    ring = b.Pos(p["cell_cx"], 0, p["floor"] + 0.75) * b.Box(cx + 2 * p["cell_gap"] - 0.02, cy + 2 * p["cell_gap"] - 0.02, 1.4)
    pocket = P["base"] & ring
    rows.append(("Cell pocket: ribs and wall 0.3 mm from the cell", pocket.volume if pocket else 0.0,
                 p["cell_gap"], 0.3, (pocket.volume if pocket else 0.0) < 1e-3))
    ok = p["lid_t"] - p["mark_depth"] >= 1.0
    rows.append(("Lid keeps 1.0 mm or more under the 0.4 mm deboss", 0.0, p["lid_t"] - p["mark_depth"], 1.0, ok))
    # Bars must not be able to slide out: body longer than the hole diameter allows
    ok = p["bar_body_d"] > p["bar_d"] + 0.3
    rows.append(("Spring bar body cannot enter the 1.0 mm tip hole", 0.0, p["bar_body_d"] - p["bar_d"], 0.3, ok))
    return rows


def print_checks(params=None):
    rows = checks(params)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:54s} overlap {v:7.3f} mm3  gap {gp:6.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


def export(out=None):
    from build123d import Compound, export_step, export_stl
    out = Path(out) if out else Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    pod = build()
    export_step(pod, str(out / "step" / "tremortrace-pod-assembly.step"))
    export_stl(pod, str(out / "stl" / "tremortrace-pod-assembly.stl"), tolerance=0.05)
    fresh = build_parts()   # a shape can only have one parent, so the strap assembly uses fresh copies
    full = Compound(children=[fresh[k] for k in POD_KEYS + ("strap",)])
    export_step(full, str(out / "step" / "tremortrace-on-strap.step"))
    for name in ("base", "lid", "gasket"):
        export_step(parts[name], str(out / "step" / f"tremortrace-{name}.step"))
        export_stl(parts[name], str(out / "stl" / f"tremortrace-{name}.stl"), tolerance=0.02)
    return parts


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    parts = export()
    bb = build().bounding_box()
    print(f"Pod assembly envelope: {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm (X x Y x Z)")
    for k in ("base", "lid", "gasket"):
        print(f"{k:7s} volume {parts[k].volume / 1000:.2f} cm3")
    print_checks()
