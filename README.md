## NOTE: THIS IS STILL UNDER HEAVY DEVELOPMENT

> **Scientific note:** this is an interactive mathematical visualization *inspired by* general relativity, not an exact simulation. See [`docs/MODEL.md`](./docs/MODEL.md) for what is approximated.

##  How to Run in Desmos 3D

1. Open **[desmos.com/3d](https://www.desmos.com/3d)** in your browser.
2. Open Developer Tools Console (`F12` or `Ctrl+Shift+I` / `Cmd+Option+I`).
3. Paste the loader script from [`scripts/load_graph.js`](./scripts/load_graph.js) or paste the contents of [`desmos_state.json`](./desmos_state.json) directly into:
   ```javascript
   Calc.setState(/* paste JSON here */);
   ```
4. Press **Play** on the master time slider `T` to watch the complete evolution!

---

##  Mathematical Model & Dynamic Hierarchy

The entire simulation is unified under a single master simulation clock $T$:

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
        z_g(x, y, T)                             r_trail(t·T)
                │                                   │
                └─────────────────┬─────────────────┘
                                  ▼
                         Merger Wavefront Blast
                            z_w(x, y, T)
                                  │
                                  ▼
                   Total 3D Deformable Grid Lattice
                     Z(x, y, T) = z_g + z_w
```

### 1. Inspiral: Peters decay and Kepler phase
- **Separation** (Peters, circular orbit): $R(T) = R_0\left(1 - T/\tau_p\right)^{1/4}$, with $\tau_p = T_m/(1 - q_c^4)$ so that contact ($R_c = 6GM/c^2$, the Schwarzschild ISCO, $q_c = R_c/R_0 = 0.6$) happens at $T_m$.
- **Orbital phase** (Kepler + Peters, closed form): $\phi_0(T) = \dfrac{\Phi_c}{1 - q_c^{5/2}}\left(1 - (1 - T/\tau_p)^{5/8}\right)$, so the frequency chirps as $(1 - T/\tau_p)^{-3/8}$. $\Phi_c = 7.127/\eta$ rad is about 4.5 orbits for equal masses; GW150914 spent about 5 orbits in band.
- After contact the objects plunge (`R -> 0` in $\Delta_p$) and the frequency ramps up toward the ringdown value.

### 2. Curvature wells and coalescence
- **Two softened potential wells**, with the total mass reduced by the radiated fraction $f_m$ (GW150914: about 3 of 65 solar masses):
  $$z_g = -f_m(T)\left(\frac{A M_1}{r_1^{1.4}} + \frac{A M_2}{r_2^{1.4}}\right), \qquad r_i = \sqrt{|\mathbf{r} - \mathbf{r}_i(T)|^2 + e_0^2}$$
- Flamm's paraboloid (the Schwarzschild embedding diagram) is intentionally not used: it shows spatial curvature only and is not a gravity well.

### 3. One retarded-time gravitational-wave field
- $u_r = T - r/v_w$. Inspiral, merger and ringdown are a single field:
  $$z_w = S \cdot A_w(u_r) \cdot \frac{\cos\big(2\theta - 2\phi_0(u_r)\big)}{1 + 0.35\,r}$$
- $A_w$: inspiral amplitude $\propto f^{2/3}$ (chirp scaling) growing to contact, a smooth rise to the merger peak, then a quasinormal ringdown $e^{-\gamma u}\cos(\omega u)$ with $\gamma = \omega/2Q$, $Q \approx 3.3$ (fundamental $l = m = 2$ mode, remnant spin near 0.69).
- $\cos(2\theta - 2\phi_0)$ is the $m = 2$ mode: a two-armed spiral wound by the orbit that tightens as the binary chirps.
- **Approximation notice:** this is a phenomenological visualization built on established formulas, not a solution of the Einstein equations; displayed heights are exaggerated ($A_{display} = A_{model} \cdot S$). Which parts are established, approximate or visual is listed in [`docs/MODEL.md`](./docs/MODEL.md), with sources in [`docs/REFERENCES.md`](./docs/REFERENCES.md).

### 4. Pure 3D Deformable Grid Representation
- Spacetime is rendered through intersecting parametric space curves over coordinate array $L_g$:
  $$\mathbf{r}_x(t) = \big(t,\; L_g,\; Z(t, L_g, T)\big), \quad \mathbf{r}_y(t) = \big(L_g,\; t,\; Z(L_g, t, T)\big)$$
- A dense 49 x 49 mesh (spacing 0.25, extent ±6) of hairline light-grey lines, with the Desmos box, plane and axes switched off, so only the fabric is drawn and the lines themselves dip into the wells and ripple with waves.
- Two small black dots (the black holes) float on top of the fabric in the wells, then merge into one larger dot. Playback is slow (45 s per sweep) and smooth (step 0.01).

---

## 🎛️ Central Parameters

| Parameter | Desmos Symbol | Default | Description |
|---|---|---|---|
| `T` | $T$ | `1` | Master clock ($[0, 18]$) |
| `T_m` | $T_m$ | `10` | Time of contact (merger) |
| `R_0` | $R_0$ | `5` | Starting separation (10 M) in grid units |
| `M_1, M_2` | $M_1, M_2$ | `1, 1` | Masses (well depth, barycentre, orbit count) |
| `A` | $A$ | `1.2` | Well depth (visualization scale) |
| `S` | $S$ | `2.2` | Ripple amplification (visualization only) |
| `e_0` | $e_0$ | `1` | Well softening |
| `v_w` | $v_w$ | `2.2` | Ripple propagation speed (display speed) |
| `Q_f` | $Q_f$ | `3.3` | Ringdown quality factor |

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
│   └── render_checkpoints.js# Headless Playwright screenshots at T checkpoints
└── assets/screenshots/
    ├── checkpoints/         # Current verified stages (T = 1, 7, 9.6, 10.4, 12, 15)
    └── *.png                # Earlier prototype captures
```

## Testing

```bash
npm install
npx playwright-core install chromium
node scripts/render_checkpoints.js
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
