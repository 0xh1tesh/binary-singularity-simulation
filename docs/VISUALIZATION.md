# Visual Architecture

## The fabric is the grid

There is no filled surface and no solid marker. The spacetime fabric is two families of 3D parametric curves that share one height field `Z(x, y, T)`:

```
X family:  ( t, Lg, Z(t, Lg, T) )        Y family:  ( Lg, t, Z(Lg, t, T) )
```

for 49 grid coordinates in each direction (spacing 0.25, extent ±6). Every line deforms in z as wells and waves pass, so the grid itself curls into the funnels and ripples.

### How the mesh is drawn (performance)

Desmos samples every curve a fixed number of times regardless of its length, so drawing cost is proportional to the *number of curves*. Drawing 49 + 49 separate lines cost about 118 ms per frame. Instead, each direction is drawn as 5 *serpentine* curves that each sweep 10 grid lines in turn, alternating direction. The short turn-around segments run along the mesh border, where the other direction's border line already exists, so the picture is the same 49 × 49 mesh with 10 curves instead of 98. The T-only quantities (orbit positions, radiated-mass factor) are stored as variables and the wave is read from a per-frame radial table, so per-sample work is small.

## Look

- Light-grey (`#bdbdbd`) hairline lines: `lineWidth` 0.3, which a GPU-backed browser draws as the thinnest line (software renderers clamp to 1 and look heavier). The mesh is subtle and reads as fabric.
- The Desmos box, plane grid and axes are switched off in the state (`showBox3D`, `showPlane3D`, `showAxis3D`, `axis3D`), so only the fabric is drawn.
- **Black holes**: two small black dots (size grows with mass) ride the wells and float above the fabric. At `Tm + Δp` they are replaced by one larger dot for the merged hole. The dot follows only 60% of the local well depth, so the deeper merged dip lifts the bigger hole higher above the sheet: it hovers over a bigger bend and never sinks into it. The horizon rings stay hidden. The orbital trails are hidden by default and ride the fabric (`z = zg` along the path) when switched on.
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

## Camera

The default view is stored in the state as `graph.worldRotation3D`: a column-major 3 × 3 rotation that must be horizon-level (Desmos discards it otherwise). `scripts/build_state.py` builds it from a yaw and elevation (`world_rotation(30, 34)`). A low elevation shows funnel depth and ripple heights; about 50 degrees shows the ring and quadrupole pattern from above. The viewport is x, y in [-6.8, 6.8] and z in [-4.8, 4.8].
