# Desmos Equation Catalog & Registry — Dynamic Binary Merger

## Complete 3D Spacetime Fabric Equation Set

| ID | Variable / Symbol | Desmos LaTeX Expression | Description / Purpose |
|---|---|---|---|
| `time_T` | $T$ | `T=1.0` | Master simulation time slider ($[0, 16]$, step $0.05$) |
| `time_Tm` | $T_m$ | `T_{m}=10` | Coalescence/merger epoch |
| `rad_R0` | $R_0$ | `R_{0}=5` | Initial binary separation |
| `mass_m1` | $M_1$ | `M_{1}=1` | Mass parameter for object 1 |
| `mass_m2` | $M_2$ | `M_{2}=1` | Mass parameter for object 2 |
| `amp_A` | $A$ | `A=3.0` | Gravitational well depth scale |
| `scale_S` | $S$ | `S=2.8` | Merger wavefront amplitude amplification |
| `eps` | $e_0$ | `e_{0}=0.55` | Softening constant preventing singularities |
| `wave_v` | $v_w$ | `v_{w}=1.3` | Gravitational wavefront propagation velocity |
| `wave_k` | $k$ | `k=2.8` | Spatial wavenumber ($2\pi/\lambda$) |
| `wave_sig` | $\sigma$ | `\sigma=1.2` | Gaussian wavepacket spatial-temporal pulse width |
| `func_R` | $R(T)$ | `R(T)=\{T<T_{m}:R_{0}\cdot(1-T/T_{m})^{0.38},0\}` | Monotonic accelerating separation decay |
| `func_phi` | $\phi_0(T)$ | `\phi_{0}(T)=\{T<T_{m}:1.2\cdot T+7\cdot(1-(1-T/T_{m})^{0.5}),1.2\cdot T_{m}+7\}` | Chirping orbital phase accumulation |
| `coord_x1` | $x_1(T)$ | `x_{1}(T)=\frac{M_{2}}{M_{1}+M_{2}}R(T)\cos(\phi_{0}(T))` | Dynamic X coordinate of singularity 1 |
| `coord_y1` | $y_1(T)$ | `y_{1}(T)=\frac{M_{2}}{M_{1}+M_{2}}R(T)\sin(\phi_{0}(T))` | Dynamic Y coordinate of singularity 1 |
| `coord_x2` | $x_2(T)$ | `x_{2}(T)=-\frac{M_{1}}{M_{1}+M_{2}}R(T)\cos(\phi_{0}(T))` | Dynamic X coordinate of singularity 2 |
| `coord_y2` | $y_2(T)$ | `y_{2}(T)=-\frac{M_{1}}{M_{1}+M_{2}}R(T)\sin(\phi_{0}(T))` | Dynamic Y coordinate of singularity 2 |
| `dist_r1` | $r_1(x,y,T)$ | `r_{1}(x,y,T)=\sqrt{(x-x_{1}(T))^{2}+(y-y_{1}(T))^{2}+e_{0}^{2}}` | Distance to dynamic singularity 1 (hidden) |
| `dist_r2` | $r_2(x,y,T)$ | `r_{2}(x,y,T)=\sqrt{(x-x_{2}(T))^{2}+(y-y_{2}(T))^{2}+e_{0}^{2}}` | Distance to dynamic singularity 2 (hidden) |
| `dist_rc` | $r_c(x,y)$ | `r_{c}(x,y)=\sqrt{x^{2}+y^{2}+0.05}` | Radial distance to merger barycenter (hidden) |
| `func_zgrav` | $z_g(x,y,T)$ | `z_{g}(x,y,T)=-\frac{A\cdot M_{1}}{r_{1}(x,y,T)}-\frac{A\cdot M_{2}}{r_{2}(x,y,T)}` | Dynamic two-well to merged single-well potential (hidden) |
| `func_zwave` | $z_w(x,y,T)$ | `z_{w}(x,y,T)=S\cdot e^{-\frac{(T-T_{m}-r_{c}(x,y)/v_{w})^{2}}{2\sigma^{2}}}\cdot\frac{\sin(k\cdot(r_{c}(x,y)-v_{w}\cdot(T-T_{m})))}{\sqrt{r_{c}(x,y)+0.6}}` | Outward propagating merger wavefront ripple (hidden) |
| `func_ztotal` | $Z(x,y,T)$ | `Z(x,y,T)=z_{g}(x,y,T)+z_{w}(x,y,T)` | Total 3D vertical displacement field (hidden) |
| `grid_list` | $L_g$ | `L_{g}=[-5,-4.6,-4.2,...,5]` | Discrete coordinate array for grid lattice |
| `grid_lines_x` | $\mathbf{r}_x(t)$ | `(t, L_{g}, Z(t, L_{g}, T))` | 3D Grid lines parallel to X-axis |
| `grid_lines_y` | $\mathbf{r}_y(t)$ | `(L_{g}, t, Z(L_{g}, t, T))` | 3D Grid lines parallel to Y-axis |

## Visual Refinements: Slate Grey Grid, Orbital Trails & Compact Horizons

| ID | Variable / Symbol | Desmos LaTeX Syntax | Description |
|---|---|---|---|
| `grid_lines_x` | $\mathbf{r}_x(t)$ | `(t, L_g, Z(t, L_g, T))` | Thin 1.0 slate grey (`#606060`) X grid lines |
| `grid_lines_y` | $\mathbf{r}_y(t)$ | `(L_g, t, Z(L_g, t, T))` | Thin 1.0 slate grey (`#606060`) Y grid lines |
| `trail_obj1` | $\mathbf{r}_{\text{trail}, 1}(t)$ | `(x_1(t\cdot T), y_1(t\cdot T), 0.05)` | Blue spiral orbital trail for Singularity 1 ($t \in [0, 1]$) |
| `trail_obj2` | $\mathbf{r}_{\text{trail}, 2}(t)$ | `(x_2(t\cdot T), y_2(t\cdot T), 0.05)` | Red spiral orbital trail for Singularity 2 ($t \in [0, 1]$) |
| `bh_point1` | $P_1$ | `(x_1(T), y_1(T), z_g(x_1(T), y_1(T), T))` | Compact black object 1 at throat tip (size 9) |
| `bh_point2` | $P_2$ | `(x_2(T), y_2(T), z_g(x_2(T), y_2(T), T))` | Compact black object 2 at throat tip (size 9) |
| `ring_bh1` | $H_1(t)$ | `(x_1(T)+0.3\cos(t), y_1(T)+0.3\sin(t), 0.05)` | Cyan horizon ring around Singularity 1 |
| `ring_bh2` | $H_2(t)$ | `(x_2(T)+0.3\cos(t), y_2(T)+0.3\sin(t), 0.05)` | Coral horizon ring around Singularity 2 |
