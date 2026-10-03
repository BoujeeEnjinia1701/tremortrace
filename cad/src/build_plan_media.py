"""TremorTrace prototype build plan pictures (TRT-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps|wiring ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_parts), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/TRT-DWG-101 to 104        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.

The pod is small (30 x 40 x 12 mm), so the shaded pictures are drawn from a copy of the
model scaled up SC times; the kit tessellates at a fixed 1 mm, which would make 1 mm parts
blocky at true size. Making sketches use the true-size model, so their dimensions are true.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
import model  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-02"
SC = 5.0
M = model.build_parts()
p = M["_p"]
LED = M["_led"]

COL = {"base": "#D1D5DB", "pogo": "#D4A017", "diode": "#111827", "cell": "#C2410C", "foam": "#FDE68A", "module": "#0F766E",
       "top_foam": "#FCD34D", "pipe": "#93C5FD", "gasket": "#374151", "lid": "#E5E7EB", "screws": "#6B7280",
       "bars": "#9CA3AF", "strap": "#1E3A8A", "wrist": "#E7D7C9"}
NAMES = {"base": "Enclosure base", "pogo": "Charging receptacle", "diode": "Schottky diode (receptacle lead)", "cell": "LiPo cell", "foam": "Lower foam pad",
         "module": "Controller and IMU module", "top_foam": "Upper foam pad", "pipe": "Light pipe",
         "gasket": "Gasket", "lid": "Lid", "screws": "Lid screws (4)", "bars": "Spring bars (2)",
         "strap": "Strap halves (2)"}
ORDER = ["base", "pogo", "diode", "cell", "foam", "module", "top_foam", "pipe", "gasket", "lid", "screws", "bars", "strap"]


def big(shape):
    """The shape scaled SC times about the model origin (build123d scales about the shape's own
    centre, so move it back to where SC times its true position puts it)."""
    import build123d as b
    a = shape.bounding_box().min
    s = shape.scale(SC)
    m = s.bounding_box().min
    return b.Pos(SC * a.X - m.X, SC * a.Y - m.Y, SC * a.Z - m.Z) * s


def part(key, name=None, shape=None, color=None, explode=(0, 0, 0), alpha=1.0):
    s = M[key] if shape is None else shape
    return Part(name or NAMES[key], big(s), color or COL[key], None, tuple(SC * v for v in explode), alpha)


def win(shape, x0, x1, y0, y1, z0, z1):
    import build123d as b
    return shape & (b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0))


def wrist():
    import build123d as b
    R = p["wrist_r"]
    return b.Pos(0, 0, -R + 0.5) * b.Rot(0, 90, 0) * b.Cylinder(R - 0.3, 46)


# ----------------------------------------------------------------- overview
def overview():
    off = {"base": (0, 0, 0), "pogo": (38, 0, 2), "diode": (38, 12, 14), "cell": (0, 0, 14), "foam": (0, 0, 24), "module": (0, 0, 32),
           "top_foam": (0, 0, 42), "pipe": (-34, 0, 64), "gasket": (0, 0, 52), "lid": (0, 0, 62), "screws": (0, 0, 78),
           "bars": (0, 0, -12), "strap": (0, 0, -26)}
    ends = win(M["strap"], -20, 20, -30, 30, -9, 10)      # the strap ends only; the rest goes round the wrist
    parts = [part(k, NAMES[k], shape=ends if k == "strap" else None, explode=off[k]) for k in ORDER]
    return bv.overview(parts, OUT / "overview.png", "TremorTrace prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the front right and above; only the looped ends of the strap halves are drawn",
                       elev=22, azim=-55, size=(10, 9), dpi=150, key=False)


# ----------------------------------------------------------------- making sketches
def sheets():
    import build123d as b
    base_ctx = [part("cell"), part("pogo"), part("bars"), part("diode")]
    common = dict(project="TremorTrace", date=DATE)
    out = []
    cx = p["cell"][0]
    pocket_len = cx + 2 * p["cell_gap"]
    out.append(bv.component_sheet(
        part("base"), base_ctx, dwg_no="TRT-DWG-101", title="TremorTrace enclosure base: making sketch",
        material="PETG, 3D printed; lug horns solid (100 % infill)", view_shape=M["base"],
        inset_view=(35, -55),
        notes=["Print open side up, 0.2 mm layers; 30 long x 40 wide x 10 high, corners R3.",
               "Inside: 27 x 28.6, floor 1. Strap notch at each strap end (30 mm face): 22 wide,",
               "  4.5 deep, 6 high from the underside; it bridges, no support needed.",
               "Spring bar holes: print, then drill 1.0 mm right through each horn",
               "  (the solid corner beside the notch), 2 from the end, 3 up.",
               "Screw holes: one per horn, 13 each side of centre along the 30 mm",
               "  length and 2.6 in from the end; open to 1.6 mm, 4.5 deep.",
               f"Cell pocket: ribs 1.5 high leave {pocket_len:.2f} x {p['cell'][1] + 2 * p['cell_gap']:.2f}, 0.3 mm round the cell.",
               "Charging opening 4 x 8 through the floor, 0.4 from the end wall,",
               "  in a collar 0.8 thick and 2 high that holds the glue.",
               "Diode spot: on the floor 8.5 to one side of the opening, clear of the collar.",
               "Check: a 1.0 mm drill passes each bar hole; the cell drops into its",
               "  pocket by its own weight; nothing is left in the notch."], **common))
    lid_view = M["lid"] + M["pipe"]
    out.append(bv.component_sheet(
        part("lid", shape=M["lid"] + M["pipe"]), [part("base"), part("gasket"), part("module")],
        dwg_no="TRT-DWG-102", title="TremorTrace lid with light pipe: making sketch",
        material="PETG, 3D printed; light pipe 2 mm clear acrylic rod", view_shape=lid_view, inset_view=(35, -55),
        notes=["Print top face down on a smooth bed: 30 x 40 x 1.5, corners R3.",
               "Four screw holes 2.2 mm at the horn positions (13 and 17.4 each",
               "  side of centre), each with a 90 degree countersink 3.8 across.",
               "Light pipe bore: drill 2.0 mm on the centre line, 6.5 from the",
               "  centre toward one strap end, over the module's status LED.",
               "  Check the LED position on the module you buy and move it to suit.",
               "Light pipe: cut 2 mm off the rod, square and polish both ends,",
               "  press in flush with the top, a drop of clear epoxy underneath.",
               "  It stands 0.5 mm below the lid, 1.2 mm above the module.",
               "Fit: lies on the gasket; four M2 x 6 countersunk screws into the horns.",
               "Mark: a short wave debossed 0.4 deep (two 0.2 mm layers) on the top face,",
               "  clear of the light pipe and screws; the lid keeps 1.1 mm under it.",
               "Check: the screw heads sit flush or just below the top face."], **common))
    out.append(bv.component_sheet(
        part("gasket"), [part("base"), part("lid")], dwg_no="TRT-DWG-103",
        title="TremorTrace gasket: making sketch", material="TPU 95A, 3D printed", view_shape=M["gasket"],
        inset_view=(35, -55),
        notes=["Print flat in TPU 95A, 0.8 mm thick (four 0.2 mm layers).",
               "  It squeezes to 0.5 mm when the lid screws are tight.",
               "Outline the same as the pod: 30 x 40, corners R3.",
               "Opening 27 x 28.6, the same as the base cavity.",
               "Four 2.2 mm holes at the screw positions (13 and 17.4 each side",
               "  of centre) so the screws pass without tearing it.",
               "Fit: lies on the base rim, inside edge flush with the cavity wall.",
               "Check: it lies flat with no stringing across the opening;",
               "  print a spare, since the gasket is replaced if the pod is opened."], **common))
    lo = M["foam"]
    up = b.Pos(22, 0, -(p["mod_top"] - (p["floor"] + p["cell"][2]))) * M["top_foam"]
    out.append(bv.component_sheet(
        Part("Foam pads", big(M["foam"] + M["top_foam"]), COL["foam"]), [part("cell"), part("module"), part("base")],
        dwg_no="TRT-DWG-104", title="TremorTrace foam pads (lower and upper): cutting sketch",
        material="Lower: 0.5 mm double-sided adhesive foam. Upper: 2 mm closed-cell foam", view_shape=lo + up,
        inset_view=(35, -55),
        notes=["Drawn side by side (39 is both pads together): lower pad left, upper right.",
               "  The upper pad is drawn squeezed, 1.7 thick; cut it from 2 mm foam.",
               "Lower pad: 17.8 x 19 from 0.5 mm double-sided adhesive foam.",
               "  It holds the module on the cell and keeps its pads off the cell.",
               "Upper pad: 16 x 19 from 2 mm closed-cell foam, with a 4 mm hole",
               "  centred 3 mm in from one short end, over the status LED.",
               "  The lid squeezes it to 1.7 mm and so clamps the stack.",
               "Cut with a sharp knife on a cutting mat; punch the hole.",
               "Check: the upper pad covers the module but not the light pipe;",
               "  the lower pad does not reach the module's battery pads."], **common))
    return out


# ----------------------------------------------------------------- joints
def joints():
    out = []
    # 01 receptacle in its collar, cut through the middle
    w = (5, 15, -6, 6, -1, 5)
    out.append(bv.joint([
        part("base", "Base floor and glue collar", shape=win(M["base"], *w)),
        part("pogo", "Charging receptacle", shape=win(M["pogo"], *w)),
        part("cell", "LiPo cell end", shape=win(M["cell"], *w))],
        OUT / "joint-01.png", "Joint 1: charging receptacle in the floor (cut through its middle)",
        subtitle="Seen from the front, a little below the floor: contacts flush with the underside; epoxy fills the collar round it",
        cut="+Y", elev=-14, azim=-75, size=(8, 6)))
    # 02 the stack, cut across the pod
    ly = LED[1]
    w = (-16, 16, ly - 13, ly + 13, -1, 13)          # centred on the light pipe, so the cut passes through it
    keys = ["base", "cell", "foam", "module", "top_foam", "gasket", "lid", "pipe"]
    names = {"base": "Base", "cell": "LiPo cell", "foam": "Lower foam pad", "module": "Module",
             "top_foam": "Upper foam pad (squeezed to 1.7 mm)", "gasket": "Gasket", "lid": "Lid",
             "pipe": "Light pipe", "pogo": "Charging receptacle"}
    out.append(bv.joint([part(k, names[k], shape=win(M[k], *w)) for k in keys],
                        OUT / "joint-02.png", "Joint 2: the inside stack (cut along the forearm through the light pipe)",
                        subtitle="Seen square from the front. Cell on the floor, foam, module, foam, lid: the lid clamps the stack so nothing rattles",
                        cut="+Y", elev=0, azim=-90, size=(9, 5)))
    # 03 corner screw through lid and gasket into the horn
    sx, sy = p["screw_x"], p["screw_y"]
    w = (sx - 2, sx + 2, sy - 6, sy + 2.6, 0, 12.5)
    out.append(bv.joint([
        part("base", "Lug horn (solid), with the spring bar hole", shape=win(M["base"], *w)),
        part("gasket", "Gasket", shape=win(M["gasket"], *w), color="#111827"),
        part("lid", "Lid (blue), countersunk", shape=win(M["lid"], *w), color="#93C5FD"),
        part("screws", "M2 x 6 countersunk screw", shape=win(M["screws"], *w), color="#B45309")],
        OUT / "joint-03.png", "Joint 3: lid screw in a lug horn (cut across the pod through the screw)",
        subtitle="Seen from the elbow end. 4 mm of thread in solid plastic, 2 mm above the 1.0 mm spring bar hole",
        cut="+X", elev=6, azim=-172, size=(8, 6)))
    # 04 spring bar and strap loop in the notch
    by = p["bar_y"]
    w = (5, 16, by - 2, by + 2, -3, 8)     # symmetric about the bar axis, so the cut passes through the bar and tip
    out.append(bv.joint([
        part("base", "Lug horn (grey), lid screw hole above", shape=win(M["base"], *w)),
        part("bars", "Spring bar (orange): tip in the 1.0 mm hole", shape=win(M["bars"], *w), color="#B45309"),
        part("strap", "Strap end (blue), looped round the bar", shape=win(M["strap"], *w))],
        OUT / "joint-04.png", "Joint 4: spring bar and strap in the lug notch (cut through the bar)",
        subtitle="Seen square from the strap side. The 1.5 mm body sits between the horns; only the thin tip enters the horn",
        cut="+Y", elev=0, azim=-90, size=(8, 6)))
    # 05 cell pocket, lid off, from above
    ribs = win(M["base"], -p["cav_x"] / 2 + 0.01, p["cav_x"] / 2 - 0.01, -p["cav_y"] / 2 + 0.01, p["cav_y"] / 2 - 0.01,
               p["floor"] + 0.01, p["floor"] + p["collar_h"])
    out.append(bv.joint([
        part("base", "Base", shape=M["base"] - ribs),
        part("base", "Ribs and glue collar (green)", shape=ribs, color="#0F766E"),
        part("cell", "LiPo cell, 0.3 mm clear"),
        part("pogo", "Charging receptacle in its collar"),
        part("diode", "Schottky diode, glued to the floor")],
        OUT / "joint-05.png", "Joint 5: cell in its pocket (lid off, seen from above)",
        subtitle="Seen straight down. Three low ribs and the end wall hold the cell; the diode lies beside the collar; the wires run down the sides",
        elev=89, azim=-90, size=(8, 6)))
    return out


# ----------------------------------------------------------------- assembly steps
def steps():
    out = []

    def st(n, done, new, title, sub, **kw):
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    B = part("base")
    st(1, [B], [part("pogo", explode=(0, 0, -14))], "charging receptacle into the floor",
       "Leads soldered first; push it up through the opening, contacts flush underneath; epoxy in the collar. Seen from below",
       elev=-30, azim=-55, label_done=True)
    st(2, [B, part("pogo")], [part("cell", explode=(0, 0, 18))], "cell into its pocket",
       "Plug already cut off and leads insulated; leads out along the long sides. Drop it in; no glue",
       elev=30, azim=-55, label_done=False)
    st(4, [B, part("pogo"), part("cell")], [part("diode", explode=(0, 0, 8)), part("foam", explode=(0, 0, 10)), part("module", explode=(0, 0, 20))],
       "lower foam pad and module",
       "Diode glued beside the collar; pad on the cell; wired module on the pad, LED toward the light pipe end",
       elev=30, azim=-55, label_done=False)
    st(5, [B, part("pogo"), part("diode"), part("cell"), part("foam"), part("module")], [part("top_foam", explode=(0, 0, 14))],
       "upper foam pad", "Lay it on the module with its hole over the status LED",
       elev=30, azim=-55, label_done=False)
    st(6, [part("lid")], [part("pipe", explode=(0, 0, -12))], "light pipe into the lid",
       "Seen from below. Push the pipe in from underneath until its top is flush with the top face; clear epoxy; let it cure",
       elev=-35, azim=-55, label_done=True)
    inside = [B, part("pogo"), part("diode"), part("cell"), part("foam"), part("module"), part("top_foam")]
    st(7, inside, [part("gasket", explode=(0, 0, 12))], "gasket onto the rim",
       "Holes over the four screw holes; inside edge flush with the cavity wall",
       elev=30, azim=-55, label_done=False)
    closed = inside + [part("gasket")]
    st(8, closed, [part("lid", shape=M["lid"] + M["pipe"], name="Lid with light pipe", explode=(0, 0, 14)),
                   part("screws", explode=(0, 0, 26))], "lid and four screws",
       "Screws in a cross pattern, snug, until the heads sit flush; do not strip the plastic",
       elev=30, azim=-55, label_done=False)
    pod = closed + [part("lid"), part("pipe"), part("screws")]
    ends = win(M["strap"], -20, 20, -30, 30, -9, 10)
    st(9, pod, [part("bars", explode=(0, 0, -14)), part("strap", shape=ends, explode=(0, 0, -14))],
       "spring bars and strap halves",
       "Seen from below. Bar through each strap loop, then one tip into its hole, compress, let the other tip click in",
       elev=-20, azim=-55, label_done=False)
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    INK, MUT = "#111827", "#4B5563"
    RED, BLK, GRY = "#B91C1C", "#111827", "#6B7280"
    fig = plt.figure(figsize=(11, 6.6), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 110); ax.set_ylim(0, 66); ax.set_axis_off()
    ax.text(2, 64, "TremorTrace prototype: block-level wiring (step 3)", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 60.6, "Four wires and one small diode, 26 AWG stranded silicone. No circuit board; the module carries the charger, IMU, radio and LED.",
            fontsize=8.5, color=MUT, va="top")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.4, title, ha="center", va="top", fontsize=9.5, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.6, sub, ha="center", va="top", fontsize=7.6, color=MUT, linespacing=1.35)

    def wire(pts, color, lw=2.2):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, t, color, ha="left"):
        ax.text(x, y, t, fontsize=7.6, color=color, ha=ha, va="center", zorder=3, bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))

    blk(4, 30, 22, 17, "LiPo cell", "150 mAh, protected\n(protection board on the cell)\nplug cut off,\none lead at a time", "#C2410C")
    blk(42, 27, 30, 25, "Controller and IMU module", "XIAO nRF52840 Sense class\ncharger, IMU, radio, flash\n\nBAT+ and BAT- pads underneath\n5V and GND pins on the edge\nstatus LED on top", "#0F766E")
    blk(86, 30, 20, 17, "Charging receptacle", "magnetic, 2 contacts,\nin the base floor", "#D4A017")
    blk(42, 11, 30, 9, "Light pipe in the lid", "over the status LED (no wire)", "#93C5FD")
    # cell to BAT pads
    wire([(26, 42), (42, 42)], RED); lab(34, 44.2, "+ to BAT+, 26 AWG", RED, "center")
    wire([(26, 35), (42, 35)], BLK); lab(34, 32.8, "- to BAT-, 26 AWG", BLK, "center")
    # receptacle to 5V and GND
    wire([(86, 42), (72, 42)], RED); lab(79, 38.6, "+ to 5V pin", RED, "center")
    ax.add_patch(FancyBboxPatch((76, 40.6), 6, 2.8, boxstyle="round,pad=0.2", fc="#F3F4F6", ec="#374151", lw=1.4, zorder=4))
    ax.plot([77.2, 77.2], [40.9, 43.1], color="#374151", lw=1.6, zorder=5)
    lab(79, 45.4, "diode, band to module", "#374151", "center")
    wire([(86, 35), (72, 35)], BLK); lab(79, 32.8, "- to GND pin", BLK, "center")
    wire([(57, 27), (57, 20)], GRY, 1.2); lab(58, 23.5, "light only", GRY)
    ax.text(2, 6.2, "Safety: insulate every joint with heat shrink or polyimide tape before the module goes on the cell. Never short the cell leads; "
            "cut and solder one lead at a time.", fontsize=7.8, color="#B45309", fontweight="bold")
    ax.text(2, 3.7, "Charge at the 50 mA setting, never while worn. Load the over-the-air bootloader through the module's USB-C socket before step 8;", fontsize=7.6, color=MUT)
    ax.text(2, 1.4, "Later updates go over Bluetooth; opening the pod is for recovery only.", fontsize=7.6, color=MUT)
    ax.text(108, 64, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309", ha="right", va="top")
    ax.text(108, 61.4, "github.com/BoujeeEnjinia1701/tremortrace", fontsize=7, color="#0F766E", ha="right", va="top", family="monospace")
    OUT.mkdir(parents=True, exist_ok=True)
    o = OUT / "wiring.png"
    fig.savefig(o, facecolor="white"); plt.close(fig)
    return o


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "joints", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "joints": joints, "steps": steps, "wiring": wiring}
    for w_ in what:
        print(w_, "->", fns[w_]())
