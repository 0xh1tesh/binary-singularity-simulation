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

PATH.write_text(json.dumps(s, indent=2), encoding="utf-8")
print("wrote", PATH)
