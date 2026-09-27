"""TremorTrace product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: filleted pod base and lid with the TPU gasket as a
visible parting line, pan-head lid screws, a lit status light pipe, a raised tremor-trace mark,
side grip ribs, visible internals (module, cell, foam pad, charging receptacle), spring bars, a
woven two-piece strap with stitching, buckle and keeper, a magnetic charging lead, and the shared
clay forearm and hand for scale.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.
Research and educational prototype, not a medical device.

Every main dimension and interface comes from PARAMS and _derived() in model.py.
Axes as model.py: X along the forearm (+X toward the hand), Y across the wrist, Z up (away from
the skin); the pod underside rests on the skin at Z = 0.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parents[1] / ".kit"))

from build123d import (Axis, Box, Cylinder, Ellipse, Plane, Pos, RectangleRounded, Rot, extrude,
                       fillet, loft)
from model import PARAMS, _derived as derived, build_parts

TITLE = "TremorTrace: wrist-worn motion sensor band for logging tremor"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); pod worn on the "
             "back of the left wrist, hand at right"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): lid and screws, "
             "gasket, controller and IMU module, foam pad, LiPo cell, base, charging receptacle, "
             "spring bars, two-piece strap with buckle, magnetic charging lead"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 38, "az": -30,
     "note": "Detail from the front right and above (about 38 deg elevation): lit status light pipe, "
             "tremor-trace mark, gasket parting line and quick-release strap lugs"},
]

# Colours (restrained product palette; accent from the kit)
C_BASE = "#E3E6EA"
C_LID = "#F2F3F5"
C_GASKET = "#3A3F47"
C_ACCENT = "#0F766E"
C_LIGHT = "#5EEAD4"
C_STRAP = "#2F3A40"
C_STITCH = "#8A949E"
C_METAL = "#B8BEC6"
C_STEEL = "#9AA1A9"
C_GOLD = "#C9A227"
C_PCB = "#1A1D21"
C_CHIP = "#111827"
C_POUCH = "#C7CCD3"
C_KAPTON = "#D08A2E"
C_FOAM = "#4B5563"
C_DARK = "#24282E"
C_CABLE = "#1F2328"
C_CLAY = "#A9ADB2"

# Appearance-only detail sizes (mm)
FIL_BASE_BOT = 1.0     # base underside edge
FIL_RIM = 0.4          # base top rim (one side of the parting line)
FIL_LID = 1.0          # lid top edge
STRAP_CLEAR = 0.3      # strap clearance off the clay wrist
STRAP_CUT_Y = 22.0     # strap arc removed inside this |y| near the top (the pod and lugs take over)

# Placement of the shared clay arm (left hand, flat pose). The forearm is tilted 6 deg so its top
# line runs level under the pod, and the pod sits 22 mm up the forearm from the wrist crease.
ARM_FOREARM = 130.0
ARM_BACK_X = 22.0
ARM_TILT = -6.0
ARM_DZ = -21.9
# Clay wrist cross-sections measured at the strap edges (x = -10.8 and +10.8) after placement:
# (x, half-width in Y, half-height in Z, centre z)
WRIST_SECTIONS = [(-10.8, 33.35, 24.09, -23.47), (10.8, 30.83, 21.08, -20.99)]


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _prism(L, W, r, z0, h, x=0.0, y=0.0):
    """Rounded-rectangle prism in plan, from z0 up by h."""
    r = max(min(r, min(L, W) / 2 - 0.01), 0.01)
    return Pos(x, y, z0) * extrude(RectangleRounded(L, W, r), amount=h)


def _top_edges(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom_edges(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _x_cyl(r, length, xc, y, z):
    """Cylinder along X centred at xc."""
    return Pos(xc, y, z) * Rot(0, 90, 0) * Cylinder(r, length)


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


# ---------------------------------------------------------------- context
def _clay_arm():
    from context_parts import forearm_hand
    arm = forearm_hand(side="left", pose="flat", forearm_len=ARM_FOREARM)
    return Pos(0, 0, ARM_DZ) * Rot(0, ARM_TILT, 0) * Pos(ARM_BACK_X, 0, 0) * arm


# ---------------------------------------------------------------- strap
def _wrist_section(x, grow):
    """Elliptical section of the strap path at x, grown by `grow` beyond the clay wrist."""
    (x0, a0, b0, z0), (x1, a1, b1, z1) = WRIST_SECTIONS
    t = (x - x0) / (x1 - x0)
    a, b, zc = a0 + t * (a1 - a0), b0 + t * (b1 - b0), z0 + t * (z1 - z0)
    return a + grow, b + grow, zc


def _ellipse_face(x, a, b, zc):
    return Plane(origin=(x, 0, zc), x_dir=(0, 1, 0), z_dir=(1, 0, 0)) * Ellipse(a, b)


def _band(x0, x1, g_in, g_out, pad=0.3):
    """Elliptical band hugging the clay wrist between x0 and x1, from grow g_in to g_out."""
    outer = loft([_ellipse_face(x, *_wrist_section(x, g_out)) for x in (x0, x1)])
    inner = loft([_ellipse_face(x, *_wrist_section(x, g_in)) for x in (x0 - pad, x1 + pad)])
    return outer - inner


def _strap(P, D):
    """Two-piece woven strap: halves meet under the wrist at a buckle, and each half rises into a lug
    notch and wraps the spring bar, as a quick-release watch strap does."""
    w, T = P["strap_w"] - 0.4, P["strap_t"]
    Y = P["pod_y"]
    ring = _band(-w / 2, w / 2, STRAP_CLEAR, STRAP_CLEAR + T)
    ring -= Pos(0, 0, 10) * Box(w + 4, 2 * STRAP_CUT_Y, 40)            # the pod covers the top arc
    halves = []
    for s in (1, -1):
        half = ring & Pos(0, s * 60, -20) * Box(w + 4, 120, 120)
        # tongue from the strap end up into the lug notch, and the loop around the spring bar
        by, bz = s * (Y / 2 - P["bar_inset"]), P["bar_z"]
        a, b, zc = _wrist_section(0.0, STRAP_CLEAR + T / 2)
        ey = s * (STRAP_CUT_Y + 0.4)
        ez = zc + b * math.sqrt(max(1 - (ey / a) ** 2, 0.0))
        dy, dz = ey - by, ez - bz
        L = math.hypot(dy, dz)
        ang = math.degrees(math.atan2(dz, dy))
        tongue =Pos(0, (by + ey) / 2, (bz + ez) / 2) * Rot(ang, 0, 0) * Box(w, L + 1.0, T)
        loop = _x_cyl(P["bar_d"] / 2 + 1.1, w, 0, by, bz)
        loop -= _x_cyl(P["bar_d"] / 2 - 0.1, w + 1, 0, by, bz)
        half = half + tongue + loop
        half = half.clean()
        halves.append(half)
    return halves


def _stitching(P):
    """Raised stitch lines along both edges of each visible strap arc."""
    w, T = P["strap_w"] - 0.4, P["strap_t"]
    lines = []
    for sx in (-1, 1):
        xc = sx * (w / 2 - 1.3)
        band = _band(xc - 0.25, xc + 0.25, STRAP_CLEAR + T - 0.05, STRAP_CLEAR + T + 0.12, pad=0.1)
        for sy in (-1, 1):
            keep = Pos(0, sy * (STRAP_CUT_Y + 1.5 + 9.0), -9.0) * Box(40, 18.0, 22.0)
            lines.append(band & keep)
    return _union(lines)


def _buckle_and_keeper(P):
    w, T = P["strap_w"] - 0.4, P["strap_t"]
    a, b, zc = _wrist_section(0.0, STRAP_CLEAR + T)
    z_bot = zc - b                                                    # strap outer surface, underside
    yb = 5.0
    frame = Pos(0, yb, z_bot - 0.9) * Box(w + 4.0, 7.0, 1.6)
    frame -= Pos(0, yb, z_bot - 0.9) * Box(w + 0.6, 4.2, 3.0)
    frame = _fillet_try(frame, frame.edges().filter_by(Axis.Y), [0.6, 0.4])
    frame += Pos(0, yb - 3.5, z_bot - 0.3) * Rot(0, 90, 0) * Cylinder(0.7, w + 3.0)   # hinge bar
    tongue = Pos(0, yb + 0.2, z_bot - 1.2) * Box(1.2, 7.2, 0.8)
    buckle = frame + tongue
    yk = -7.0
    keeper = Pos(0, yk, z_bot + T / 2) * Box(w + 1.6, 5.0, T + 2.2)
    keeper -= Pos(0, yk, z_bot + T / 2) * Box(w + 0.2, 6.0, T + 0.4)
    keeper = _fillet_try(keeper, keeper.edges().filter_by(Axis.Y), [0.5, 0.3])
    return buckle, keeper


# ---------------------------------------------------------------- pod
def _base(P, D, m):
    base = m["base"]
    base = _fillet_try(base, _bottom_edges(base), [FIL_BASE_BOT, 0.6, 0.3])
    base = _fillet_try(base, _top_edges(base), [FIL_RIM, 0.25])
    # shallow grip ribs on both X faces (toward the hand and toward the elbow)
    for sx in (-1, 1):
        for z in (4.0, 5.6, 7.2):
            base -= Pos(sx * P["pod_x"] / 2, 0, z) * Box(0.7, 18.0, 0.6)
    return base


def _lid(P, D, led_xy):
    X, Y, t = P["pod_x"], P["pod_y"], P["lid_t"]
    z0 = D["base_h"] + P["gasket_t"]
    lid = _prism(X, Y, P["corner_r"], z0, t)
    lid = _fillet_try(lid, _top_edges(lid), [FIL_LID, 0.8, 0.5])
    for s in (-1, 1):
        lid -= Pos(0, s * D["screw_y"], z0 + t / 2) * Cylinder(1.1, t + 1)
        lid -= Pos(0, s * D["screw_y"], z0 + t - 0.25) * Cylinder(2.05, 0.6)     # seat for the pan head
    lid -= Pos(led_xy[0], led_xy[1], z0 + t / 2) * Cylinder(P["led_d"] / 2, t + 1)
    return lid


def _trace_mark(P, D):
    """Raised tremor-trace mark on the lid: a short decaying wave (appearance only)."""
    z = D["base_h"] + P["gasket_t"] + P["lid_t"]
    pts = []
    n = 26
    for k in range(n + 1):
        x = -9.0 + 18.0 * k / n
        amp = 2.4 * math.exp(-((x + 1.0) / 6.0) ** 2)
        pts.append((x, 4.0 + amp * math.sin(2 * math.pi * (x + 9.0) / 4.5)))
    segs = []
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
        segs.append(Pos((x0 + x1) / 2, (y0 + y1) / 2, z + 0.07) * Rot(0, 0, ang) * Box(L, 0.6, 0.14))
        segs.append(Pos(x1, y1, z + 0.07) * Cylinder(0.3, 0.14))
    segs.append(Pos(pts[0][0], pts[0][1], z + 0.07) * Cylinder(0.3, 0.14))
    return _union(segs)


def _screw(P, D, y):
    z_top = D["base_h"] + P["gasket_t"] + P["lid_t"]
    head = Pos(0, y, z_top - 0.25 + 0.55) * Cylinder(1.95, 1.1)
    head = _fillet_try(head, _top_edges(head), [0.5, 0.3])
    head -= Pos(0, y, z_top + 0.85) * Box(2.2, 0.45, 0.6)
    head -= Pos(0, y, z_top + 0.85) * Box(0.45, 2.2, 0.6)
    shank_len = P["screw_len"]
    head += Pos(0, y, z_top - 0.25 - shank_len / 2) * Cylinder(P["screw_d"] / 2, shank_len)
    return head


def _module(P, D):
    """XIAO nRF52840 Sense class module: PCB, RF shield, USB-C, IMU, castellated pads, status LED."""
    mx, my, mz = P["module"]
    z0 = P["floor"] + P["cell"][2] + P["foam_t"]
    pcb_t = 1.0
    pcb = _prism(mx, my, 0.8, z0, pcb_t)
    zt = z0 + pcb_t
    shield = _prism(12.0, 11.0, 0.5, zt, 1.4, y=-0.5)
    shield = _fillet_try(shield, _top_edges(shield), [0.3, 0.15])
    usb = _prism(8.9, 7.3, 1.2, zt, 2.5, y=my / 2 - 7.3 / 2 + 0.8)
    usb -= _prism(7.6, 3.0, 0.9, zt + 0.6, 1.3, y=my / 2 + 0.2)
    chips = Pos(5.2, -6.5, zt + 0.45) * Box(2.5, 3.0, 0.9)                       # IMU
    chips += Pos(-5.4, -6.8, zt + 0.35) * Box(2.0, 2.0, 0.7)                    # flash
    chips += Pos(-5.6, 6.2, zt + 0.3) * Box(1.6, 1.6, 0.6)                      # charger
    pads = []
    for sx in (-1, 1):
        for k in range(7):
            y = (k - 3) * 2.54
            pads.append(Pos(sx * (mx / 2 - 0.6), y, zt + 0.03) * Box(1.2, 1.5, 0.06))
    led_x, led_y = 0.0, -my / 2 + 4.0
    led = Pos(led_x, led_y, zt + 0.3) * Box(1.6, 1.2, 0.6)
    return pcb, shield + usb, chips, _union(pads), led


def _cell(P, D):
    cx, cy, cz = P["cell"]
    cell = _prism(cx, cy, 1.2, P["floor"], cz, x=D["cell_cx"])
    cell = _fillet_try(cell, _top_edges(cell), [0.8, 0.5, 0.3])
    tape = Pos(D["cell_cx"], cy / 2 - 2.6, P["floor"] + cz + 0.06) * Box(cx - 3.0, 4.2, 0.12)
    return cell, tape


def _pogo(P, D):
    px, py, pz = P["pogo"]
    body = _prism(px, py, 1.0, 0.0, pz, x=D["pogo_cx"])
    pins = None
    for s in (-1, 1):
        pin = Pos(D["pogo_cx"], s * 1.8, -0.02 + 0.4) * Cylinder(0.75, 0.8)
        pins = pin if pins is None else pins + pin
    body -= pins
    return body, pins


def _charging_lead(P, D):
    """Magnetic charging plug and USB-A lead, shown below the receptacle (exploded view only)."""
    px, py, pz = P["pogo"]
    x0 = D["pogo_cx"]
    zc = -3.0
    plug = _prism(px + 2.4, py + 2.4, 1.6, zc - 2.0, 4.0, x=x0)
    plug = _fillet_try(plug, _bottom_edges(plug), [0.8, 0.5])
    relief = _x_cyl(1.6, 8.0, x0 + (px + 2.4) / 2 + 3.6, 0, zc - 0.2)
    pins = None
    for s in (-1, 1):
        pin = Pos(x0, s * 1.8, zc + 2.0 + 0.3) * Cylinder(0.55, 0.6)
        pins = pin if pins is None else pins + pin
    cable = _x_cyl(1.2, 34.0, x0 + (px + 2.4) / 2 + 7.0 + 17.0, 0, zc - 0.2)
    xa = x0 + (px + 2.4) / 2 + 7.0 + 34.0
    usb_body = Pos(xa + 9.0, 0, zc - 0.2) * Box(18.0, 15.0, 7.5)
    usb_body = _fillet_try(usb_body, usb_body.edges().filter_by(Axis.X), [1.5, 0.8])
    usb_shell = Pos(xa + 18.0 + 6.0, 0, zc - 0.2) * Box(12.0, 12.0, 4.5)
    usb_shell -= Pos(xa + 18.0 + 7.0, 0, zc - 0.2) * Box(11.0, 11.0, 3.5)
    return plug + relief + cable + usb_body, pins + usb_shell


# ---------------------------------------------------------------- assembly
def product_parts(P=PARAMS):
    D = derived(P)
    m = build_parts(P)
    led_xy = m["_led"]
    Y = P["pod_y"]
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # explode stack (mm up from assembled position)
    E_FOAM, E_CELL, E_MOD, E_GASKET, E_LID, E_SCREW = 26, 16, 34, 48, 58, 76

    # ---- shell: pod
    add("Enclosure base (PETG)", _base(P, D, m), C_BASE, "plastic", 5, "shell", (0, 0, 0))
    add("TPU gasket", m["gasket"], C_GASKET, "rubber", 7, "shell", (0, 0, E_GASKET))
    add("Enclosure lid (PETG)", _lid(P, D, led_xy), C_LID, "plastic", 2, "shell", (0, 0, E_LID))
    add("Tremor-trace mark", _trace_mark(P, D), C_ACCENT, "painted", 2, "shell", (0, 0, E_LID))
    z_lid = D["base_h"] + P["gasket_t"]
    pipe = Pos(led_xy[0], led_xy[1], z_lid + (P["lid_t"] + 0.15) / 2 - 0.25) * Cylinder(P["led_d"] / 2 - 0.05, P["lid_t"] + 0.4)
    add("Status light pipe (lit)", pipe, C_LIGHT, "emissive", 10, "shell", (0, 0, E_LID + 6))
    for i, s in enumerate((-1, 1)):
        add(f"M2 lid screw {i + 1}", _screw(P, D, s * D["screw_y"]), C_METAL, "metal", 9, "shell",
            (0, 0, E_SCREW))
    for i, s in enumerate((-1, 1)):
        bar = _x_cyl(0.75, P["strap_w"] + 2.0, 0, s * (Y / 2 - P["bar_inset"]), P["bar_z"])
        bar += _x_cyl(0.55, P["strap_w"] + 3.0, 0, s * (Y / 2 - P["bar_inset"]), P["bar_z"])
        add(f"Spring bar {i + 1}", bar, C_STEEL, "metal", 8, "shell", (0, s * 12, 0))

    # ---- shell: strap
    halves = _strap(P, D)
    buckle, keeper = _buckle_and_keeper(P)
    stitch = _stitching(P)
    add("Woven strap, buckle side", halves[0], C_STRAP, "fabric", 1, "shell", (0, 40, -4))
    add("Woven strap, tail side", halves[1], C_STRAP, "fabric", 1, "shell", (0, -40, -4))
    st_pos = stitch & Pos(0, 60, 0) * Box(60, 120, 200)
    st_neg = stitch & Pos(0, -60, 0) * Box(60, 120, 200)
    add("Strap stitching, buckle side", st_pos, C_STITCH, "fabric", 1, "shell", (0, 40, -4))
    add("Strap stitching, tail side", st_neg, C_STITCH, "fabric", 1, "shell", (0, -40, -4))
    add("Strap buckle", buckle, C_METAL, "metal", 1, "shell", (0, 40, -4))
    add("Strap keeper", keeper, C_STRAP, "fabric", 1, "shell", (0, -40, -4))

    # ---- internal
    pcb, shield_usb, chips, pads, led = _module(P, D)
    add("Module PCB", pcb, C_PCB, "plastic", 3, "internal", (0, 0, E_MOD))
    add("RF shield and USB-C", shield_usb, C_METAL, "metal", 3, "internal", (0, 0, E_MOD))
    add("IMU, flash and charger ICs", chips, C_CHIP, "plastic", 3, "internal", (0, 0, E_MOD))
    add("Castellated pads", pads, C_GOLD, "metal", 3, "internal", (0, 0, E_MOD))
    add("Status LED (lit)", led, C_LIGHT, "emissive", 3, "internal", (0, 0, E_MOD))
    foam = _prism(P["module"][0], P["module"][1] - 2.0, 0.8, P["floor"] + P["cell"][2], P["foam_t"])
    add("Foam pad", foam, C_FOAM, "rubber", 11, "internal", (0, 0, E_FOAM))
    cell, tape = _cell(P, D)
    add("LiPo cell, 150 mAh", cell, C_POUCH, "painted", 4, "internal", (0, 0, E_CELL))
    add("Cell protection tape", tape, C_KAPTON, "painted", 4, "internal", (0, 0, E_CELL))
    pogo, pogo_pins = _pogo(P, D)
    add("Magnetic charging receptacle", pogo, C_DARK, "plastic", 6, "internal", (0, 0, -14))
    add("Charging contacts", pogo_pins, C_GOLD, "metal", 6, "internal", (0, 0, -14))

    # ---- accessory: magnetic charging lead
    lead, lead_metal = _charging_lead(P, D)
    add("Magnetic charging lead", lead, C_CABLE, "rubber", 6, "accessory", (0, 0, -34))
    add("Charging lead contacts and USB-A shell", lead_metal, C_METAL, "metal", 6, "accessory", (0, 0, -34))

    # ---- context: shared clay forearm and hand
    add("Forearm and hand (clay)", _clay_arm(), C_CLAY, "clay", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:40s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:7.3f} cm3")
