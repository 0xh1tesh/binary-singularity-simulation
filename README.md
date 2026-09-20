## NOTE: THIS IS STILL UNDER HEAVY DEVELOPMENT

> **Scientific note:** this is an interactive mathematical visualization *inspired by* general relativity, not an exact simulation. See [`docs/MODEL.md`](./docs/MODEL.md) for what is approximated.
> 

##  How to Run in Desmos 3D

1. Open **[desmos.com/3d](https://www.desmos.com/3d)** in your browser.
2. Open Developer Tools Console (`F12` or `Ctrl+Shift+I` / `Cmd+Option+I`).
3. Paste the loader script from [`scripts/load_graph.js`](./scripts/load_graph.js) or paste the contents of [`desmos_state.json`](./desmos_state.json) directly into:
   ```javascript
   Calc.setState(/* paste JSON here */);
   ```
4. Press **Play** on the master time slider `T` to watch the complete evolution!
<img width="991" height="937" alt="image" src="https://github.com/user-attachments/assets/7971649f-34df-451b-aae4-247ea16f2c76" />

---

##  Mathematical Model & Dynamic Hierarchy

The entire simulation is unified under a single master simulation clock T:

```
                            Master Time T
                                  │
                ┌─────────────────┴─────────────────┐
                ▼                                   ▼
         Separation R(T)                     Orbital Phase φ₀(T)
                │                                   │
                └─────────────────┬─────────────────┘
                                  ▼
                        Singularity Trajectories
                      r₁(T) = (x₁, y₁), r₂(T) = (x₂, y₂)
                                  │
                ┌─────────────────┴─────────────────┐
                ▼                                   ▼
       Gravitational Wells                  Orbital Spiral Trails
          zg(x, y, T)                            trail(t·T)
                │                                   │
                └─────────────────┬─────────────────┘
                                  ▼
                         Merger Wavefront Blast
                            zw(x, y, T)
                                  │
                                  ▼
                   Total 3D Deformable Grid Lattice
                     Z(x, y, T) = zg + zw
```

### 1. Inspiral: Peters decay and Kepler phase
- **Separation** (Peters, circular orbit): R(T) = R0 · ⁴√(1 − T/τp), with τp = Tm / (1 − qc⁴), so that contact (Rc = 6GM/c², the Schwarzschild ISCO, qc = Rc/R0 = 0.6) happens at Tm.
- **Orbital phase** (Kepler + Peters, closed form): φ0(T) = Φc · (1 − ⁸√((1 − T/τp)⁵)) / (1 − qc²·√qc), so the frequency chirps as 1 / ⁸√((1 − T/τp)³). Φc = 7.127 / η rad is about 4.5 orbits for equal masses; GW150914 spent about 5 orbits in band.
- After contact the objects plunge (R falls to 0 within Δp) and the frequency ramps up toward the ringdown value.

### 2. Curvature wells and coalescence
- **Two softened potential wells**, with the total mass reduced by the radiated fraction fm (GW150914: about 3 of 65 solar masses):

  ```
  zg = − fm(T) · A · ( M1 / (d1² + e0²)  +  M2 / (d2² + e0²) )      di = distance from the point to object i
  ```
- Flamm's paraboloid (the Schwarzschild embedding diagram) is intentionally not used: it shows spatial curvature only and is not a gravity well.

### 3. One retarded-time gravitational-wave field
- Retarded time: ur = T − r / vw. Inspiral, merger and ringdown are a single field:

  ```
  zw = S · Aw(ur) · cos( 2θ − 2·φ0(ur) ) / (1 + 0.35·r)
  ```
- Aw: inspiral amplitude growing as the cube root of f² (chirp scaling) up to contact, a smooth rise to the merger peak, then a quasinormal ringdown that decays as exp(−γ·u) with γ = ω / 2Q, Q ≈ 3.3 (fundamental l = m = 2 mode, remnant spin near 0.69).
- cos(2θ − 2·φ0) is the m = 2 mode: a two-armed spiral wound by the orbit that tightens as the binary chirps.
- **Approximation notice:** this is a phenomenological visualization built on established formulas, not a solution of the Einstein equations; displayed heights are exaggerated (displayed height = model height · S). Which parts are established, approximate or visual is listed in [`docs/MODEL.md`](./docs/MODEL.md), with sources in [`docs/REFERENCES.md`](./docs/REFERENCES.md).

### 4. Pure 3D Deformable Grid Representation
- Spacetime is rendered through intersecting parametric space curves over the grid coordinates Lg:

  ```
  X family:  ( t, Lg, Z(t, Lg, T) )        Y family:  ( Lg, t, Z(Lg, t, T) )
  ```

- A dense 49 x 49 mesh (spacing 0.25, extent ±6) of hairline light-grey lines, with the Desmos box, plane and axes switched off, so only the fabric is drawn and the lines themselves dip into the wells and ripple with waves.
- Two small black dots (the black holes) float on top of the fabric in the wells, then merge into one larger dot that hovers over a deeper dip. Playback is slow (45 s per sweep) and smooth (step 0.01).
- **Performance:** the mesh is drawn as 10 serpentine curves instead of 98 separate lines, the same 49 x 49 mesh at about 40 fps (was about 8.5 on the reference machine). See [`docs/VISUALIZATION.md`](./docs/VISUALIZATION.md).

---

## 🎛️ Central Parameters

| Parameter | Desmos Symbol | Default | Description |
|---|---|---|---|
| `T` | T | `1` | Master clock (0 to 18) |
| `Tm` | Tm | `10` | Time of contact (merger) |
| `R0` | R0 | `5` | Starting separation (10 M) in grid units |
| `M1, M2` | M1, M2 | `1, 1` | Masses (well depth, barycentre, orbit count) |
| `A` | A | `1.2` | Well depth (visualization scale) |
| `S` | S | `2.2` | Ripple amplification (visualization only) |
| `e0` | e0 | `1` | Well softening |
| `vw` | vw | `2.2` | Ripple propagation speed (display speed) |
| `Qf` | Qf | `3.3` | Ringdown quality factor |

Physical constants (ISCO ratio, plunge time, radiated fraction, wave amplitudes) are in a collapsed folder in Desmos; see [`docs/PARAMETERS.md`](./docs/PARAMETERS.md).


---

## Repository Structure

```
binary-singularity-simulation/
├── README.md
├── desmos_state.json        # Canonical Desmos 3D graph state (stable expression ids)
├── package.json             # Dev tooling only (playwright-core)
├── .mcp.json                # Playwright MCP config for agent-driven testing
├── docs/
│   ├── MODEL.md             # What is modelled, approximated, or visualization-only
│   ├── EQUATIONS.md         # Expression-id registry with tags
│   ├── REFERENCES.md        # Sources for every formula and constant
│   ├── PARAMETERS.md        # Slider reference
│   ├── VISUALIZATION.md     # Fabric rendering and stage guide
│   └── EXPERIMENTS.md       # Development log
├── scripts/
│   ├── load_graph.js        # Browser-console loader (validates and reports errors)
│   ├── build_state.py       # Patches desmos_state.json by expression id
│   ├── make_mcp_loader.py   # Writes a Playwright-MCP snippet that loads the state
│   ├── bench_fps.js         # Playback frame-rate benchmark (GPU-backed Chromium)
│   └── render_checkpoints.js# Playwright screenshots at T checkpoints
└── assets/screenshots/
    ├── checkpoints/         # Current verified stages (T = 1, 7, 9.6, 10.4, 12, 15)
    └── *.png                # Earlier prototype captures
```

## Testing

```bash
npm install
npx playwright-core install chromium
node scripts/render_checkpoints.js   # screenshots at six checkpoints
node scripts/bench_fps.js            # measures real playback redraws per second
```

This loads the state into desmos.com/3d headlessly, reports expression errors, and writes screenshots to `assets/screenshots/checkpoints/`. No Desmos account is needed.

---

##  Documentation Links

- Detailed Mathematical Formulations: [`docs/MODEL.md`](./docs/MODEL.md)
- Complete Desmos LaTeX Registry: [`docs/EQUATIONS.md`](./docs/EQUATIONS.md)
- Sources and formula provenance: [`docs/REFERENCES.md`](./docs/REFERENCES.md)
- Parameter Exploration Table: [`docs/PARAMETERS.md`](./docs/PARAMETERS.md)
- Development & Experiment History: [`docs/EXPERIMENTS.md`](./docs/EXPERIMENTS.md)

---

##  Author

**0xh1tesh** ([GitHub Profile](https://github.com/0xh1tesh))
