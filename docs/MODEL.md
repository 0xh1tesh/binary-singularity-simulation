# Theoretical Model & Mathematical Framework

## Scientific Framing & Disclaimer

This project is an **interactive mathematical visualization inspired by General Relativity**. It models the phenomenological behavior of binary compact objects undergoing inspiral, merger, and gravitational wave emission.

It is **not** a direct numerical relativity solution to the non-linear Einstein Field Equations $G_{\mu
u} = rac{8\pi G}{c^4} T_{\mu
u}$. Approximations and visualization-specific amplifications are intentionally applied to render the geometric dynamics legible and interactive inside Desmos 3D.

---

## Dynamical Hierarchy

The simulation is unified under a single master simulation clock $t$:

```
                             Master Time t
                                   │
                 ┌─────────────────┴─────────────────┐
                 ▼                                   ▼
          Separation R(t)                     Orbital Phase θ(t)
                 │                                   │
                 └─────────────────┬─────────────────┘
                                   ▼
                         Singularity Positions
                        (x₁(t), y₁(t)), (x₂(t), y₂(t))
                                   │
                 ┌─────────────────┴─────────────────┐
                 ▼                                   ▼
        Curvature Well 1                    Curvature Well 2
                 │                                   │
                 └─────────────────┬─────────────────┘
                                   ▼
                         Static/Moving Binary Fabric
                                   │
                                   ▼
                            Merger Envelope
                                   │
                                   ▼
                     Gravitational Wave Disturbance
                                   │
                                   ▼
                      Combined 3D Spacetime Surface
```

---

## Phenomenological Regimes

1. **Early & Late Inspiral ($t < t_{	ext{merger}}$)**:
   - Decreasing orbital separation: $R(t) = R_0 (1 - t / t_m)^{1/4}$ or smooth polynomial decay.
   - Frequency chirp: $\omega(t) \propto R(t)^{-3/2}$ (Keplerian-inspired angular velocity scaling).
   - Dynamic trajectory tracking:
     $$\mathbf{r}_1(t) = \left(rac{M_2}{M_1+M_2} R(t) \cos	heta(t),\, rac{M_2}{M_1+M_2} R(t) \sin	heta(t)ight)$$
     $$\mathbf{r}_2(t) = \left(-rac{M_1}{M_1+M_2} R(t) \cos	heta(t),\, -rac{M_1}{M_1+M_2} R(t) \sin	heta(t)ight)$$

2. **Gravitational Potential Curvature Wells**:
   - Regularized Newtonian/Schwarzschild embedding diagrams:
     $$z_{	ext{grav}}(x,y,t) = -rac{A \cdot M_1}{\sqrt{|\mathbf{r}-\mathbf{r}_1(t)|^2 + \epsilon_0^2}} - rac{A \cdot M_2}{\sqrt{|\mathbf{r}-\mathbf{r}_2(t)|^2 + \epsilon_0^2}}$$
   - Regularization constant $\epsilon_0 > 0$ prevents infinite coordinate singularities while retaining steep funnels.

3. **Merger & Coalescence ($t pprox t_{	ext{merger}}$)**:
   - Smooth logistic or tanh transition merging the two independent wells into a central Kerr/Schwarzschild well of effective mass $M_{	ext{remnant}} pprox (M_1 + M_2) - E_{	ext{rad}}$.

4. **Gravitational Wave Perturbation ($z_{	ext{wave}}$)**:
   - Outward-propagating wavefront with speed $v$:
     $$z_{	ext{wave}}(x,y,t) = S \cdot \mathcal{A}(t, r) \sin(k(r - v t)) \cdot \cos(2	heta - 2\omega t)$$
   - Geometric attenuation factor $\propto (1 + lpha r)^{-1/2}$.
   - Quadrupolar pattern $\cos(2	heta)$ reflecting the quadrupole radiation moment of binary systems.

5. **Post-Merger Ringdown**:
   - Damped quasi-normal mode oscillations: $\mathcal{A}_{	ext{ring}}(t) \propto e^{-\gamma (t - t_m)} \cos(\omega_{	ext{qnm}} (t - t_m))$.
