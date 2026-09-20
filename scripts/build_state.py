"""Patch desmos_state.json in place by expression id (stable ids, idempotent).

Usage: python scripts/build_state.py

Physics (geometric units G = c = 1, lengths in M = m1 + m2, see docs/MODEL.md):
  * Peters (1964) circular inspiral:   R(t) = R0 (1 - t/tau)^(1/4)
  * Kepler + Peters orbital phase:     Phi(t) = Phi_c (1 - (1 - t/tau)^(5/8)) / (1 - q_c^(5/2))
  * contact at the Schwarzschild ISCO: R_c = 6M, start R0 = 10M  ->  q_c = R_c/R0 = 0.6
  * inspiral strain amplitude ~ f^(2/3) (chirp), ringdown = damped sinusoid with quality factor Q
"""
import json, math, pathlib

PATH = pathlib.Path(__file__).resolve().parent.parent / "desmos_state.json"
s = json.loads(PATH.read_text(encoding="utf-8"))
lst = s["expressions"]["list"]

# Expressions that belonged to the earlier ad-hoc wave model.
REMOVE = {"wave_k", "wave_sig", "func_zinsp"}
lst[:] = [e for e in lst if e["id"] not in REMOVE]
ex = {e["id"]: e for e in lst}

WELL_EXP = 1.4  # exponent of the softened potential wells (1.0 would be exactly Newtonian)


def upsert(i, latex, hidden=True, color="#6042a6", **extra):
    if i not in ex:
        e = {"type": "expression", "id": i}
        lst.append(e)
        ex[i] = e
    ex[i].update(latex=latex, color=ex[i].get("color", color), **extra)
    if hidden:
        ex[i]["hidden"] = True
    return ex[i]


def slider(i, lo, hi, step=None):
    ex[i]["slider"] = {"hardMin": True, "hardMax": True, "min": str(lo), "max": str(hi),
                       **({"step": str(step)} if step else {})}


# --- user-facing controls ----------------------------------------------------
upsert("time_T", "T=1", hidden=False)
ex["time_T"]["slider"].update(min="0", max="18", step="0.05")
for i, v, lo, hi in [
    ("time_Tm", "T_{m}=10", 4, 14), ("rad_R0", "R_{0}=5", 2, 7),
    ("mass_m1", "M_{1}=1", 0.2, 3), ("mass_m2", "M_{2}=1", 0.2, 3),
    ("amp_A", "A=1.2", 0.2, 4), ("scale_S", "S=2.2", 0, 5),
    ("eps", "e_{0}=1", 0.3, 2), ("wave_v", "v_{w}=2.2", 0.8, 4),
]:
    upsert(i, v, hidden=False)
    slider(i, lo, hi)
upsert("wave_Q", "Q_{f}=3.3", hidden=False)
slider("wave_Q", 1, 8)

# --- physical constants and derived scales -----------------------------------
upsert("phys_qc", r"q_{c}=0.6")                 # R_c / R_0 = 6M / 10M (ISCO contact)
upsert("phys_dp", r"\Delta_{p}=0.6")            # plunge duration (animation time)
upsert("phys_gr", r"g_{r}=1.5")                 # ringdown / contact frequency ratio (real ~3.9, capped: mesh resolution)
upsert("phys_ap", r"A_{p}=0.85")                 # peak merger amplitude (relative)
upsert("phys_ai", r"a_{i}=0.22")                # inspiral amplitude at contact (relative)
upsert("phys_er", r"\epsilon_{r}=0.046")        # fraction of mass radiated (GW150914: ~3 of 65 Msun)
upsert("phys_eta", r"\eta=\frac{M_{1}M_{2}}{\left(M_{1}+M_{2}\right)^{2}}")
upsert("phys_tau", r"\tau_{p}=\frac{T_{m}}{1-q_{c}^{4}}")            # Peters coalescence time, rescaled so R(T_m)=R_c
upsert("phys_Phic", r"\Phi_{c}=\frac{7.127}{\eta}")                   # orbital phase accumulated 10M -> 6M
upsert("phys_Omc", r"\Omega_{c}=\frac{5\Phi_{c}}{8\tau_{p}\left(1-q_{c}^{2.5}\right)q_{c}^{1.5}}")  # orbital ang. freq. at contact

# --- kinematics --------------------------------------------------------------
upsert("func_R",
       r"R\left(T\right)=\left\{T<T_{m}:R_{0}\left(1-\frac{T}{\tau_{p}}\right)^{0.25},"
       r"T<T_{m}+\Delta_{p}:R_{0}q_{c}\left(1-\frac{T-T_{m}}{\Delta_{p}}\right)^{1.5},0\right\}")
upsert("func_phi",
       r"\phi_{0}\left(T\right)=\left\{T<T_{m}:\frac{\Phi_{c}}{1-q_{c}^{2.5}}\left(1-\left(1-\frac{T}{\tau_{p}}\right)^{0.625}\right),"
       r"T<T_{m}+\Delta_{p}:\Phi_{c}+\Omega_{c}\left(\left(T-T_{m}\right)+\frac{\left(g_{r}-1\right)\left(T-T_{m}\right)^{2}}{2\Delta_{p}}\right),"
       r"\Phi_{c}+\Omega_{c}\Delta_{p}\frac{g_{r}+1}{2}+g_{r}\Omega_{c}\left(T-T_{m}-\Delta_{p}\right)\right\}")

# --- wells: two Newtonian-style potentials, total mass reduced by the radiated fraction
upsert("func_fm",
       r"f_{m}\left(T\right)=1-\epsilon_{r}\min\left(1,\max\left(0,\frac{T-T_{m}}{\Delta_{p}}\right)\right)")
upsert("func_zgrav",
       r"z_{g}\left(x,y,T\right)=-f_{m}\left(T\right)\left(\frac{A\cdot M_{1}}{r_{1}\left(x,y,T\right)^{" + str(WELL_EXP)
       + r"}}+\frac{A\cdot M_{2}}{r_{2}\left(x,y,T\right)^{" + str(WELL_EXP) + r"}}\right)")

# --- gravitational wave: ONE retarded-time field, chirp -> merger -> ringdown --
upsert("func_amp",
       r"A_{w}\left(u\right)=\left\{0<u<T_{m}:a_{i}q_{c}\left(1-\frac{u}{\tau_{p}}\right)^{-0.25}\min\left(1,\frac{u}{0.8}\right),"
       r"T_{m}\le u<T_{m}+\Delta_{p}:a_{i}+\left(A_{p}-a_{i}\right)\left(\frac{u-T_{m}}{\Delta_{p}}\right)^{2}\left(3-2\frac{u-T_{m}}{\Delta_{p}}\right),"
       r"u\ge T_{m}+\Delta_{p}:A_{p}e^{-\frac{g_{r}\Omega_{c}}{Q_{f}}\left(u-T_{m}-\Delta_{p}\right)},0\right\}")
upsert("func_ur", r"u_{r}\left(x,y,T\right)=T-\frac{r_{c}\left(x,y\right)}{v_{w}}")
upsert("func_zwave",
       r"z_{w}\left(x,y,T\right)=S\cdot A_{w}\left(u_{r}\left(x,y,T\right)\right)"
       r"\cdot\frac{\cos\left(2\arctan\left(y,x\right)-2\phi_{0}\left(u_{r}\left(x,y,T\right)\right)\right)}{1+0.35\cdot r_{c}\left(x,y\right)}")
upsert("func_ztotal", r"Z\left(x,y,T\right)=z_{g}\left(x,y,T\right)+z_{w}\left(x,y,T\right)")

# --- fabric grid: +-HALF, STEP spacing (line domain == grid extent) ----------
HALF, STEP = 6.0, 0.25
n = int(round(2 * HALF / STEP)) + 1
ex["grid_list"]["latex"] = r"L_{g}=\left[" + ",".join(f"{-HALF + STEP * i:g}" for i in range(n)) + r"\right]"
for i in ("grid_lines_x", "grid_lines_y"):
    # hairline light-grey lines: 0.3 renders as the thinnest line on a GPU-backed browser
    ex[i].update(domain={"min": str(-HALF), "max": str(HALF)},
                 parametricDomain={"min": str(-HALF), "max": str(HALF)}, color="#bdbdbd", lineWidth="0.3")

# --- slow, fluid playback: 45 s per sweep of T, fine step ---------------------
ex["time_T"]["slider"].update(animationPeriod=45000, step="0.01")

# --- black holes: small black dots that ride the fabric, then merge into one bigger dot
LIFT = 0.7  # dots float this far above the local fabric height Z, so they always sit on top of the mesh

def bh_point(px, py, cond):
    return (r"\left(" + px + "," + py + r",Z\left(" + px + "," + py + r",T\right)+" + str(LIFT) + r"\right)"
            r"\left\{" + cond + r"\right\}")

BEFORE, AFTER = r"T<T_{m}+\Delta_{p}", r"T\ge T_{m}+\Delta_{p}"
# size grows with mass (horizon radius ~ mass); the merged dot carries the radiated-mass deficit f_m
for i, (xf, yf), m in (("bh_point1", ("x_{1}\\left(T\\right)", "y_{1}\\left(T\\right)"), "M_{1}"),
                       ("bh_point2", ("x_{2}\\left(T\\right)", "y_{2}\\left(T\\right)"), "M_{2}")):
    ex[i].update(latex=bh_point(xf, yf, BEFORE), color="#000000", pointSize="1+3*" + m,
                 hidden=False)
    ex[i].pop("movablePointSize", None)
upsert("bh_merged", bh_point("0", "0", AFTER), hidden=False, color="#000000",
       pointSize=r"1+3\left(M_{1}+M_{2}\right)f_{m}\left(T\right)")
for i in ("ring_bh1", "ring_bh2"):
    ex[i]["hidden"] = True
for i, (xf, yf) in (("trail_obj1", ("x_{1}", "y_{1}")), ("trail_obj2", ("x_{2}", "y_{2}"))):
    px, py = xf + r"\left(t\cdot T\right)", yf + r"\left(t\cdot T\right)"
    ex[i].update(latex=r"\left(" + px + "," + py + r",z_{g}\left(" + px + "," + py + r",t\cdot T\right)+0.08\right)",
                 lineWidth="2", hidden=True)

# --- viewport and camera -----------------------------------------------------
def world_rotation(yaw, elev):
    """Horizon-level column-major 3x3 (Desmos discards non-horizon-level rotations)."""
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    ce, se = math.cos(math.radians(elev)), math.sin(math.radians(elev))
    r0, r1, r2 = (-ce * sy, ce * cy, -se), (-cy, -sy, 0.0), (-se * sy, se * cy, ce)
    return [round(v, 6) for v in (r0[0], r1[0], r2[0], r0[1], r1[1], r2[1], r0[2], r1[2], r2[2])]

vp = dict(xmin=-6.8, xmax=6.8, ymin=-6.8, ymax=6.8, zmin=-4.8, zmax=4.8)
s["graph"].update(viewport=vp, worldRotation3D=world_rotation(30, 34),
                  showBox3D=False, showPlane3D=False, showAxis3D=False,
                  axis3D=[False, False, False], showGrid=False)
s["graph"]["__v12ViewportLatexStash"] = {k: str(v) for k, v in vp.items()}

# --- organisation ------------------------------------------------------------
groups = [
    ("f_controls", "Controls", False,
     ["time_T", "time_Tm", "rad_R0", "mass_m1", "mass_m2", "amp_A", "scale_S", "wave_v", "wave_Q", "eps"]),
    ("f_phys", "Physical constants (see docs/MODEL.md)", True,
     ["phys_qc", "phys_dp", "phys_gr", "phys_ap", "phys_ai", "phys_er", "phys_eta", "phys_tau",
      "phys_Phic", "phys_Omc"]),
    ("f_model", "Model (kinematics and fields)", True,
     ["func_R", "func_phi", "coord_x1", "coord_y1", "coord_x2", "coord_y2", "dist_r1", "dist_r2",
      "dist_rc", "func_fm", "func_zgrav", "func_amp", "func_ur", "func_zwave", "func_ztotal"]),
    ("f_fabric", "Spacetime fabric", True, ["grid_list", "grid_lines_x", "grid_lines_y"]),
    ("f_bh", "Black holes", True, ["bh_point1", "bh_point2", "bh_merged"]),
    ("f_optional", "Optional markers (hidden)", True,
     ["trail_obj1", "trail_obj2", "rg1", "rg2", "ring_bh1", "ring_bh2"]),
]
title = {"type": "text", "id": "note_title",
         "text": ("Binary merger and spacetime ripple. A mathematical visualization inspired by general "
                  "relativity (not an exact simulation). Press play on T: inspiral (Peters decay, chirp), "
                  "merger at T_m, then a quasinormal ringdown. S only exaggerates the display height.")}
new_list, placed = [title], set()
for fid, ftitle, collapsed, ids in groups:
    new_list.append({"type": "folder", "id": fid, "title": ftitle, "collapsed": collapsed})
    for i in ids:
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
