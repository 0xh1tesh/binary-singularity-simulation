"""Patch desmos_state.json in place by expression id (stable ids, minimal edits).

Usage: python scripts/build_state.py
"""
import json, pathlib

PATH = pathlib.Path(__file__).resolve().parent.parent / "desmos_state.json"
s = json.loads(PATH.read_text(encoding="utf-8"))
ex = {e["id"]: e for e in s["expressions"]["list"]}

def latex(i, v): ex[i]["latex"] = v

# --- parameters (defaults) -------------------------------------------------
latex("time_T", "T=1")
ex["time_T"]["slider"].update(min="0", max="18", step="0.05")
for i, v in {
    "time_Tm": "T_{m}=10", "rad_R0": "R_{0}=5", "amp_A": "A=1.7",
    "scale_S": "S=2.2", "eps": "e_{0}=0.8", "wave_v": "v_{w}=1.6",
    "wave_k": "k=2.2", "wave_sig": r"\sigma=1.6",
}.items():
    latex(i, v)
    ex[i].pop("slider", None)  # let Desmos derive sensible slider bounds
for i, (lo, hi) in {"time_Tm": (4, 14), "rad_R0": (2, 7), "amp_A": (0.2, 4),
                    "scale_S": (0, 5), "eps": (0.3, 2), "wave_v": (0.5, 3),
                    "wave_k": (0.5, 5), "wave_sig": (0.3, 3),
                    "mass_m1": (0.2, 3), "mass_m2": (0.2, 3)}.items():
    ex[i]["slider"] = {"hardMin": True, "hardMax": True, "min": str(lo), "max": str(hi)}

# --- merger-gated, quadrupolar wave -----------------------------------------
# u = retarded time (T - T_m - r/v_w). Fast rise, slow ringdown, cos(2(theta-phi_m)).
latex("func_zwave",
      r"z_{w}\left(x,y,T\right)=S\cdot\left\{u_{r}\left(x,y,T\right)<0:e^{-\frac{u_{r}\left(x,y,T\right)^{2}}{0.5}},e^{-\frac{u_{r}\left(x,y,T\right)}{\sigma}}\right\}"
      r"\cdot\left(1+0.6\cos\left(2\left(\arctan\left(y,x\right)-\phi_{0}\left(T_{m}\right)\right)\right)\right)"
      r"\cdot\frac{\sin\left(-k\cdot v_{w}\cdot u_{r}\left(x,y,T\right)\right)}{1+0.35\cdot r_{c}\left(x,y\right)}")
# insert retarded-time helper before z_w
lst = s["expressions"]["list"]
if "func_ur" not in ex:
    new = {"type": "expression", "id": "func_ur", "color": "#388c46", "hidden": True,
           "latex": r"u_{r}\left(x,y,T\right)=T-T_{m}-\frac{r_{c}\left(x,y\right)}{v_{w}}"}
    lst.insert(lst.index(ex["func_zwave"]), new)


# --- well profile: r^-1.4 (steeper than 1/r) keeps the two wells distinct during the inspiral
latex("func_zgrav",
      r"z_{g}\left(x,y,T\right)=-\frac{A\cdot M_{1}}{r_{1}\left(x,y,T\right)^{1.4}}"
      r"-\frac{A\cdot M_{2}}{r_{2}\left(x,y,T\right)^{1.4}}")

# --- fabric grid: +-HALF, STEP spacing (line domain == grid extent, no overhang)
HALF, STEP = 6.0, 0.25
n = int(round(2 * HALF / STEP)) + 1
latex("grid_list", r"L_{g}=\left[" + ",".join(f"{-HALF + STEP * i:g}" for i in range(n)) + r"\right]")
for i, col in (("grid_lines_x", "#1d4e89"), ("grid_lines_y", "#2f80c9")):
    ex[i]["domain"] = {"min": str(-HALF), "max": str(HALF)}
    ex[i]["parametricDomain"] = {"min": str(-HALF), "max": str(HALF)}
    ex[i]["color"] = col
    ex[i]["lineWidth"] = "1"

# --- markers: nothing that dominates the fabric -----------------------------
for i in ("bh_point1", "bh_point2", "ring_bh1", "ring_bh2"):
    ex[i]["hidden"] = True
# orbital trails ride the fabric: z follows the well depth at the trail's own time
for i, (xf, yf) in (("trail_obj1", ("x_{1}", "y_{1}")), ("trail_obj2", ("x_{2}", "y_{2}"))):
    px = xf + r"\left(t\cdot T\right)"
    py = yf + r"\left(t\cdot T\right)"
    latex(i, r"\left(" + px + "," + py + r",z_{g}\left(" + px + "," + py + r",t\cdot T\right)+0.08\right)")
    ex[i]["lineWidth"] = "2"
    ex[i]["hidden"] = True  # toggle on in Desmos to see the orbital tracks

# --- viewport: no box / plane / axes, so only the fabric is drawn ------------
vp = s["graph"]["viewport"]
vp.update(xmin=-7.5, xmax=7.5, ymin=-7.5, ymax=7.5, zmin=-5, zmax=5)
s["graph"]["__v12ViewportLatexStash"] = {k: str(v) for k, v in vp.items()}
s["graph"].update(showBox3D=False, showPlane3D=False, showAxis3D=False,
                  axis3D=[False, False, False], showGrid=False)

# --- inspiral radiation: a weak two-arm spiral that grows toward the merger ---
# Uses the retarded phase phi_0(T - r/v_w), so the arms are wound by the orbit itself.
if "func_zinsp" not in ex:
    zin = {"type": "expression", "id": "func_zinsp", "color": "#388c46", "hidden": True,
           "latex": (r"z_{i}\left(x,y,T\right)=\left\{0<T-\frac{r_{c}\left(x,y\right)}{v_{w}}<T_{m}:"
                     r"0.35\cdot S\cdot\left(\frac{T-\frac{r_{c}\left(x,y\right)}{v_{w}}}{T_{m}}\right)^{3}"
                     r"\cdot\frac{\cos\left(2\arctan\left(y,x\right)-2\phi_{0}\left(T-\frac{r_{c}\left(x,y\right)}{v_{w}}\right)\right)}"
                     r"{1+0.35\cdot r_{c}\left(x,y\right)},0\right\}")}
    lst.insert(lst.index(ex["func_ztotal"]), zin)
    ex["func_zinsp"] = zin
latex("func_ztotal", r"Z\left(x,y,T\right)=z_{g}\left(x,y,T\right)+z_{w}\left(x,y,T\right)+z_{i}\left(x,y,T\right)")

# --- camera: horizon-level world rotation (column-major 3x3), yaw/elevation in degrees
import math
def world_rotation(yaw, elev):
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    ce, se = math.cos(math.radians(elev)), math.sin(math.radians(elev))
    r0, r1, r2 = (-ce * sy, ce * cy, -se), (-cy, -sy, 0.0), (-se * sy, se * cy, ce)
    return [round(v, 6) for v in (r0[0], r1[0], r2[0], r0[1], r1[1], r2[1], r0[2], r1[2], r2[2])]

s["graph"]["worldRotation3D"] = world_rotation(yaw=30, elev=18)
vp.update(xmin=-6.8, xmax=6.8, ymin=-6.8, ymax=6.8, zmin=-4.8, zmax=4.8)
s["graph"]["viewport"] = vp
s["graph"]["__v12ViewportLatexStash"] = {k: str(v) for k, v in vp.items()}

# --- organisation: title note + folders (ids of model expressions unchanged) --
def folder(fid, title, collapsed):
    return {"type": "folder", "id": fid, "title": title, "collapsed": collapsed}

groups = [
    ("f_controls", "Controls", False,
     ["time_T", "time_Tm", "rad_R0", "mass_m1", "mass_m2", "amp_A", "scale_S", "wave_v", "wave_k",
      "wave_sig", "eps"]),
    ("f_model", "Model (kinematics and fields)", True,
     ["func_R", "func_phi", "coord_x1", "coord_y1", "coord_x2", "coord_y2", "dist_r1", "dist_r2",
      "dist_rc", "func_zgrav", "func_ur", "func_zwave", "func_zinsp", "func_ztotal"]),
    ("f_fabric", "Spacetime fabric", True, ["grid_list", "grid_lines_x", "grid_lines_y"]),
    ("f_optional", "Optional markers (hidden)", True,
     ["trail_obj1", "trail_obj2", "bh_point1", "bh_point2", "rg1", "rg2", "ring_bh1", "ring_bh2"]),
]
title = {"type": "text", "id": "note_title",
         "text": ("Binary merger and spacetime ripple. A mathematical visualization inspired by general "
                  "relativity (not an exact simulation). Press play on T: orbit, inspiral, merger at T_m, "
                  "then an outward gravitational-wave-like ripple. S only exaggerates the display height.")}
placed = set()
new_list = [title]
for fid, ftitle, collapsed, ids in groups:
    new_list.append(folder(fid, ftitle, collapsed))
    for i in ids:
        if i in ex:
            ex[i]["folderId"] = fid
            new_list.append(ex[i])
            placed.add(i)
for e in lst:
    if e["id"] not in placed and e.get("type") == "expression":
        new_list.append(e)
        print("unplaced (kept at end):", e["id"])
s["expressions"]["list"] = new_list

PATH.write_text(json.dumps(s, indent=2), encoding="utf-8")
print("wrote", PATH)
