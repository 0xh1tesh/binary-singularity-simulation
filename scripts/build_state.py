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

# --- performance: quantities that depend only on T are stored as variables, so Desmos
# --- evaluates them once per frame instead of once per curve sample.
upsert("func_fm",
       r"f_{m}\left(T\right)=1-\epsilon_{r}\min\left(1,\max\left(0,\frac{T-T_{m}}{\Delta_{p}}\right)\right)")
upsert("cur_x1", r"X_{1c}=x_{1}\left(T\right)")
upsert("cur_y1", r"Y_{1c}=y_{1}\left(T\right)")
upsert("cur_x2", r"X_{2c}=x_{2}\left(T\right)")
upsert("cur_y2", r"Y_{2c}=y_{2}\left(T\right)")
upsert("cur_fm", r"F_{mc}=f_{m}\left(T\right)")

# --- wells: two softened potentials 1/(d^2 + e0^2) (integer power: no sqrt or pow per sample),
# --- total mass reduced by the radiated fraction. r_i here is the softened distance SQUARED.
upsert("dist_r1", r"r_{1}\left(x,y,T\right)=\left(x-X_{1c}\right)^{2}+\left(y-Y_{1c}\right)^{2}+e_{0}^{2}")
upsert("dist_r2", r"r_{2}\left(x,y,T\right)=\left(x-X_{2c}\right)^{2}+\left(y-Y_{2c}\right)^{2}+e_{0}^{2}")
upsert("func_zgrav",
       r"z_{g}\left(x,y,T\right)=-F_{mc}\cdot A\left(\frac{M_{1}}{r_{1}\left(x,y,T\right)}+\frac{M_{2}}{r_{2}\left(x,y,T\right)}\right)")

# --- gravitational wave: ONE retarded-time field, chirp -> merger -> ringdown --
# A_w(u) is the amplitude envelope in retarded time u (piecewise ramp instead of min(), so it also works on lists).
upsert("func_amp",
       r"A_{w}\left(u\right)=\left\{0<u<T_{m}:a_{i}q_{c}\left(1-\frac{u}{\tau_{p}}\right)^{-0.25}\left\{u<0.8:\frac{u}{0.8},1\right\},"
       r"T_{m}\le u<T_{m}+\Delta_{p}:a_{i}+\left(A_{p}-a_{i}\right)\left(\frac{u-T_{m}}{\Delta_{p}}\right)^{2}\left(3-2\frac{u-T_{m}}{\Delta_{p}}\right),"
       r"u\ge T_{m}+\Delta_{p}:A_{p}e^{-\frac{g_{r}\Omega_{c}}{Q_{f}}\left(u-T_{m}-\Delta_{p}\right)},0\right\}")
# The wave depends on position only through r_c and the angle, so amplitude and phase are tabulated once
# per frame on a radial table R_t (step 0.02, u = T - r/v_w) and looked up by nearest entry per sample.
upsert("tab_r", r"R_{t}=\left[0,0.02...9.2\right]")
upsert("tab_a", r"W_{a}=\frac{S\cdot A_{w}\left(T-\frac{R_{t}}{v_{w}}\right)}{1+0.35R_{t}}")
upsert("tab_p", r"W_{p}=2\phi_{0}\left(T-\frac{R_{t}}{v_{w}}\right)")
upsert("tab_n", r"n_{r}\left(r\right)=\operatorname{round}\left(50r\right)+1")
upsert("func_zwave",
       r"z_{w}\left(x,y,T\right)=W_{a}\left[n_{r}\left(r_{c}\left(x,y\right)\right)\right]"
       r"\cos\left(2\arctan\left(y,x\right)-W_{p}\left[n_{r}\left(r_{c}\left(x,y\right)\right)\right]\right)")
upsert("func_ztotal", r"Z\left(x,y,T\right)=z_{g}\left(x,y,T\right)+z_{w}\left(x,y,T\right)")
REMOVE_LATE = {"func_ur"}   # u_r is now implicit in the tables
lst[:] = [e for e in lst if e["id"] not in REMOVE_LATE]
for i in REMOVE_LATE:
    ex.pop(i, None)

# --- fabric grid: +-HALF, STEP spacing (line domain == grid extent) ----------
HALF, STEP = 6.0, 0.25
n = int(round(2 * HALF / STEP)) + 1          # 49 grid lines in each direction
# Desmos takes a fixed number of samples per curve, so cost scales with the NUMBER of curves, not their
# length. Each mesh direction is therefore drawn as a few "serpentine" curves that each sweep ROWS grid
# lines in turn (boustrophedon). The short turn-around segments run along the mesh border, where the other
# direction's edge line already exists, so the picture is the same 49 x 49 mesh with far fewer curves.
ROWS = 10
CHUNKS = -(-n // ROWS)                       # ceil(49 / 10) = 5 curves per direction
def fmt(v): return f"{v:g}"
upsert("grid_xs", r"X_{s}\left(t\right)=" + fmt(-HALF) + r"+" + fmt(2 * HALF)
       + r"\left(\operatorname{mod}\left(t,1\right)+\operatorname{mod}\left(\operatorname{floor}\left(t\right),2\right)"
       r"\left(1-2\operatorname{mod}\left(t,1\right)\right)\right)")
upsert("grid_ys", r"Y_{s}\left(t,c\right)=\min\left(" + fmt(HALF) + r"," + fmt(-HALF) + r"+" + fmt(STEP)
       + r"\left(" + str(ROWS) + r"c+\operatorname{floor}\left(t\right)\right)\right)")   # surplus rows clamp onto the border line
ex["grid_list"]["latex"] = r"C_{k}=\left[" + ",".join(str(i) for i in range(CHUNKS)) + r"\right]"
dom = {"min": "0", "max": str(ROWS - 0.0001)}
for i, (a, b) in (("grid_lines_x", (r"X_{s}\left(t\right)", r"Y_{s}\left(t,C_{k}\right)")),
                  ("grid_lines_y", (r"Y_{s}\left(t,C_{k}\right)", r"X_{s}\left(t\right)"))):
    # hairline light-grey lines: 0.3 renders as the thinnest line on a GPU-backed browser
    ex[i].update(latex=r"\left(" + a + "," + b + r",Z\left(" + a + "," + b + r",T\right)\right)",
                 domain=dom, parametricDomain=dom, color="#bdbdbd", lineWidth="0.3")

# --- slow, fluid playback: 45 s per sweep of T, fine step ---------------------
ex["time_T"]["slider"].update(animationPeriod=45000, step="0.01")

# --- black holes: small black dots that ride the fabric, then merge into one bigger dot
LIFT = 0.7  # dots float this far above the well floor PLUS the local wave amplitude, so they always sit
            # on top of the mesh (they follow the smooth well, not the fast ripple, and never dip inside it)
ENV = r"S\cdot A_{w}\left(T-\frac{0.3}{v_{w}}\right)"   # wave amplitude envelope near the source

FOLLOW = 0.6  # the dot follows only this fraction of the well depth, so a deeper dip lifts it higher above
              # the sheet: the bigger merged hole hovers over a bigger bend instead of sinking into it

def bh_point(px, py, cond):
    zg = r"z_{g}\left(" + px + "," + py + r",T\right)"
    return (r"\left(" + px + "," + py + "," + str(FOLLOW) + zg + "+" + str(LIFT) + "+" + ENV + r"\right)"
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
    # the track is projected onto the current fabric height
    ex[i].update(latex=r"\left(" + px + "," + py + r",Z\left(" + px + "," + py + r",T\right)+0.08\right)",
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
     ["func_R", "func_phi", "coord_x1", "coord_y1", "coord_x2", "coord_y2",
      "func_fm", "cur_x1", "cur_y1", "cur_x2", "cur_y2", "cur_fm", "dist_r1", "dist_r2",
      "dist_rc", "func_zgrav", "func_amp", "tab_r", "tab_a", "tab_p", "tab_n", "func_zwave", "func_ztotal"]),
    ("f_fabric", "Spacetime fabric", True, ["grid_xs", "grid_ys", "grid_list", "grid_lines_x", "grid_lines_y"]),
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
