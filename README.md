NOTE: THIS IS STILL UNDER HEAVY DEVELOPEMENT

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
  $$z_g(x, y, T) = -\frac{A \cdot M_1}{\sqrt{|\mathbf{r} - \mathbf{r}_1(T)|^2 + e_0^2}} - \frac{A \cdot M_2}{\sqrt{|\mathbf{r} - \mathbf{r}_2(T)|^2 + e_0^2}}$$
- At merger $T = T_m$, $R(T) \to 0$, causing both wells to smoothly merge into a single central remnant funnel of combined depth $-\frac{A(M_1 + M_2)}{\sqrt{x^2 + y^2 + e_0^2}}$.

### 3. Outward Propagating Merger Wavefront
- **Localized Wavepacket**:
  $$z_w(x, y, T) = S \cdot \exp\left(-\frac{(T - T_m - r_c(x,y)/v_w)^2}{2\sigma^2}\right) \cdot \frac{\sin\left(k(r_c(x,y) - v_w(T - T_m))\right)}{\sqrt{r_c(x,y) + 0.6}}$$
- Produces a calm fabric during early orbit, launching a strong undulating ripple at the moment of coalescence that expands outward at speed $v_w$.

### 4. Pure 3D Deformable Grid Representation
- Spacetime is rendered through intersecting parametric space curves over coordinate array $L_g$:
  $$\mathbf{r}_x(t) = \big(t,\; L_g,\; Z(t, L_g, T)\big), \quad \mathbf{r}_y(t) = \big(L_g,\; t,\; Z(L_g, t, T)\big)$$
- Rendered in thin 1.0 slate grey (`#606060`), eliminating solid polygonal surfaces so the grid lines themselves plunge into the wells and ripple with waves.

---

## 🎛️ Central Parameters

| Parameter | Desmos Symbol | Default Value | Description |
|---|---|---|---|
| `T` | $T$ | `1.0` | Master simulation time slider ($[0, 16]$) |
| `T_m` | $T_m$ | `10.0` | Coalescence/merger epoch |
| `R_0` | $R_0$ | `5.0` | Initial binary separation |
| `M_1, M_2` | $M_1, M_2$ | `1.0, 1.0` | Masses of singularity 1 and 2 |
| `A` | $A$ | `2.8` | Gravitational well depth scale |
| `S` | $S$ | `2.2` | Wavefront visualization amplification |
| `e_0` | $e_0$ | `0.55` | Softening constant (singularity regularization) |
| `v_w` | $v_w$ | `1.3` | Gravitational wavefront propagation velocity |
| `k` | $k$ | `2.8` | Spatial wavenumber |
| `\sigma` | $\sigma$ | `1.2` | Pulse width of the traveling wavepacket |

---

## Repository Structure

```
binary-singularity-simulation/
├── README.md                # Project documentation, visual gallery, and overview
├── desmos_state.json        # Serialized Desmos 3D calculator state
├── .gitignore
├── docs/
│   ├── MODEL.md             # Theoretical modeling & approximations
│   ├── EQUATIONS.md         # Active equation catalog and Desmos LaTeX syntax
│   ├── PARAMETERS.md        # Detailed parameter reference table
│   ├── VISUALIZATION.md     # 3D graphical architecture and styling
│   └── EXPERIMENTS.md       # Benchmarking and development logs
├── assets/
│   └── screenshots/         # Verified visual captures across all 5 simulation stages
└── scripts/
    └── load_graph.js        # Browser console injector script for Desmos 3D
```

---

##  Documentation Links

- Detailed Mathematical Formulations: [`docs/MODEL.md`](./docs/MODEL.md)
- Complete Desmos LaTeX Registry: [`docs/EQUATIONS.md`](./docs/EQUATIONS.md)
- Parameter Exploration Table: [`docs/PARAMETERS.md`](./docs/PARAMETERS.md)
- Development & Experiment History: [`docs/EXPERIMENTS.md`](./docs/EXPERIMENTS.md)

---

##  Author

**0xh1tesh** ([GitHub Profile](https://github.com/0xh1tesh))
