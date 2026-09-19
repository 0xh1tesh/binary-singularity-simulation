# Visual Architecture

## The fabric is the grid

There is no filled surface and no solid marker. The spacetime fabric is two families of 3D parametric curves that share one height field `Z(x, y, T)`:

```
X family:  (t, L_g, Z(t, L_g, T))     Y family:  (L_g, t, Z(L_g, t, T))
```

with `t` in [-6, 6] and `L_g` a list of 49 grid coordinates (spacing 0.25). Every line deforms in z as wells and waves pass, so the grid itself curls into the funnels and ripples.

## Look

- Two blue tones for the two line families (`#1d4e89`, `#2f80c9`) at the minimum line width (Desmos does not go thinner than 1). Density, not line weight, gives the fabric feel.
- The Desmos box, plane grid and axes are switched off in the state (`showBox3D`, `showPlane3D`, `showAxis3D`, `axis3D`), so only the fabric is drawn.
- The black object markers and rings are hidden. The orbital trails are hidden by default and ride the fabric (`z = z_g` along the path) when switched on.
- The viewport is x, y in [-7.5, 7.5] and z in [-5, 5].

## Stage guide

| T | What to look for |
|---|---|
| 1 | Two separate wells, the fabric otherwise calm. |
| 7 | Tight, fast orbit, the wells close together. |
| 9.6 | Almost one well, deepening. |
| 10.4 | Single deep remnant funnel, a ring of crests opening around it. |
| 12 | The wavefront has moved outward and the fabric is visibly rippled. |
| 15 | The front has reached the edge with four quadrupole lobes, the centre settling. |

Checkpoints are in `assets/screenshots/checkpoints/`.

## Automated checking

`node scripts/render_checkpoints.js` loads `desmos_state.json` into desmos.com/3d in headless Chromium (Playwright), sets `T`, reports any expression errors and saves a screenshot per checkpoint. It uses no account or credentials.

## Limitations of the Desmos camera

The camera angle is not part of the exported state in the way we can set it, so the default view is Desmos's own. Rotate with the mouse. A lower angle shows the ripple heights best.
