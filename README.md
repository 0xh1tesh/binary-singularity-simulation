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

### 1. Inspiral Separation & Frequency Chirp
- **Separation Decay**:
  $$R(T) = \begin{cases} R_0 \left(1 - \frac{T}{T_m}\right)^{0.38} & T < T_m \\ 0 & T \ge T_m \end{cases}$$
- **Chirping Phase Accumulation**:
  $$\phi_0(T) = \begin{cases} 1.2 T + 7\left(1 - \left(1 - \frac{T}{T_m}\right)^{0.5}\right) & T < T_m \\ 1.2 T_m + 7 & T \ge T_m \end{cases}$$

### 2. Spacetime Curvature Wells & Coalescence
- **Two-Well Regularized Potential**:
  $$z_g(x, y, T) = -\frac{A \cdot M_1}{r_1^{1.4}} - \frac{A \cdot M_2}{r_2^{1.4}}, \qquad r_i = \sqrt{|\mathbf{r} - \mathbf{r}_i(T)|^2 + e_0^2}$$
- At merger $T = T_m$, $R(T) \to 0$, so both wells smoothly become a single, deeper remnant funnel. The steeper-than-Newtonian exponent 1.4 keeps the two wells visibly separate until they are close.

### 3. Outward Propagating Merger Wavefront
- **Merger-generated, quadrupolar wave**, with retarded time $u_r = T - T_m - r_c/v_w$:
  $$z_w = S \cdot E(u_r) \cdot \big(1 + 0.6\cos(2(\theta - \phi_0(T_m)))\big) \cdot \frac{\sin(-k v_w u_r)}{1 + 0.35\, r_c}, \quad E(u_r) = \begin{cases} e^{-u_r^2/0.5} & u_r < 0 \\ e^{-u_r/\sigma} & u_r \ge 0 \end{cases}$$
- The fabric is calm during the orbit. At $T_m$ a strong ripple starts at the centre, travels outward at speed $v_w$ with four quadrupole lobes, and rings down behind the front.
- **Approximation notice:** this is a phenomenological, visualization-oriented model, not a solution of the Einstein equations, and the displayed amplitudes are exaggerated (`A_display = A_model * S`). See [`docs/MODEL.md`](./docs/MODEL.md).

### 4. Pure 3D Deformable Grid Representation
- Spacetime is rendered through intersecting parametric space curves over coordinate array $L_g$:
  $$\mathbf{r}_x(t) = \big(t,\; L_g,\; Z(t, L_g, T)\big), \quad \mathbf{r}_y(t) = \big(L_g,\; t,\; Z(L_g, t, T)\big)$$
- A dense 49 x 49 mesh (spacing 0.25, extent ±6) of thin blue lines, with the Desmos box, plane and axes switched off, so only the fabric is drawn and the lines themselves plunge into the wells and ripple with waves.

---

## 🎛️ Central Parameters

| Parameter | Desmos Symbol | Default Value | Description |
|---|---|---|---|
| `T` | $T$ | `1.0` | Master simulation time slider ($[0, 18]$) |
| `T_m` | $T_m$ | `10.0` | Coalescence/merger epoch |
| `R_0` | $R_0$ | `5.0` | Initial binary separation |
| `M_1, M_2` | $M_1, M_2$ | `1.0, 1.0` | Masses of singularity 1 and 2 |
| `A` | $A$ | `1.7` | Gravitational well depth scale |
| `S` | $S$ | `2.2` | Ripple amplification (visualization only) |
| `e_0` | $e_0$ | `0.8` | Softening constant (singularity regularization) |
| `v_w` | $v_w$ | `1.6` | Ripple propagation speed |
| `k` | $k$ | `2.2` | Spatial wavenumber |
| `\sigma` | $\sigma$ | `1.6` | Ringdown decay time behind the wavefront |

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
│   ├── EQUATIONS.md         # Expression-id registry
│   ├── PARAMETERS.md        # Slider reference
│   ├── VISUALIZATION.md     # Fabric rendering and stage guide
│   └── EXPERIMENTS.md       # Development log
├── scripts/
│   ├── load_graph.js        # Browser-console loader (validates and reports errors)
│   ├── build_state.py       # Patches desmos_state.json by expression id
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
- Parameter Exploration Table: [`docs/PARAMETERS.md`](./docs/PARAMETERS.md)
- Development & Experiment History: [`docs/EXPERIMENTS.md`](./docs/EXPERIMENTS.md)

---

##  Author

**0xh1tesh** ([GitHub Profile](https://github.com/0xh1tesh))
