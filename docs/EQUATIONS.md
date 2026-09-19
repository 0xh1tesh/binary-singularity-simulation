# Equation Registry

`desmos_state.json` is the canonical graph state. Expression ids are stable. `scripts/build_state.py` patches the state by id, so this table is the map from id to model concept. "Model" tags say what each item is (see [MODEL.md](./MODEL.md)).

## Parameters (sliders)

| ID | Symbol | Default | Role |
|---|---|---|---|
| `time_T` | `T` | `1` | Master clock, 0 to 18 (visualization control) |
| `time_Tm` | `T_m` | `10` | Merger time |
| `rad_R0` | `R_0` | `5` | Initial separation |
| `mass_m1`, `mass_m2` | `M_1`, `M_2` | `1` | Masses |
| `amp_A` | `A` | `1.7` | Well depth (visualization scale) |
| `scale_S` | `S` | `2.2` | Ripple amplification (visualization only) |
| `eps` | `e_0` | `0.8` | Softening |
| `wave_v` | `v_w` | `1.6` | Ripple speed |
| `wave_k` | `k` | `2.2` | Wavenumber |
| `wave_sig` | `sigma` | `1.6` | Ringdown decay time |

## Kinematics (Newtonian-inspired approximation)

| ID | Expression | Role |
|---|---|---|
| `func_R` | `R(T) = {T<T_m : R_0 (1-T/T_m)^0.38, 0}` | Accelerating separation decay to zero at the merger |
| `func_phi` | `phi_0(T) = {T<T_m : 1.2 T + 7 (1-(1-T/T_m)^0.5), 1.2 T_m + 7}` | Chirping orbital phase |
| `coord_x1`, `coord_y1` | `x_1(T) = M_2/(M_1+M_2) R(T) cos phi_0(T)`, same with `sin` | Position of object 1 |
| `coord_x2`, `coord_y2` | `x_2(T) = -M_1/(M_1+M_2) R(T) cos phi_0(T)`, same with `sin` | Position of object 2 |

## Fields (conceptual and phenomenological)

| ID | Expression | Role |
|---|---|---|
| `dist_r1`, `dist_r2` | `r_i = sqrt((x-x_i(T))^2 + (y-y_i(T))^2 + e_0^2)` | Softened distance to each object |
| `dist_rc` | `r_c = sqrt(x^2 + y^2 + 0.05)` | Distance from the merger point (origin) |
| `func_zgrav` | `z_g = -A M_1 / r_1^1.4 - A M_2 / r_2^1.4` | Two wells that become one at `R = 0` |
| `func_ur` | `u_r = T - T_m - r_c / v_w` | **Retarded time**: zero on the wavefront, so the wave is tied to the merger |
| `func_zwave` | `z_w = S * env(u_r) * (1 + 0.6 cos(2(atan2(y,x) - phi_0(T_m)))) * sin(-k v_w u_r) / (1 + 0.35 r_c)` where `env = exp(-u_r^2/0.5)` for `u_r<0`, `exp(-u_r/sigma)` otherwise | Merger-generated, quadrupolar, ringing-down wave |
| `func_ztotal` | `Z = z_g + z_w` | Height field used by the grid |

## Fabric and markers

| ID | Expression | Role |
|---|---|---|
| `grid_list` | `L_g = [-6, -5.75, ..., 6]` (49 values) | Grid coordinates |
| `grid_lines_x` | `(t, L_g, Z(t, L_g, T))`, t in [-6, 6] | Fabric lines parallel to x |
| `grid_lines_y` | `(L_g, t, Z(L_g, t, T))`, t in [-6, 6] | Fabric lines parallel to y |
| `trail_obj1`, `trail_obj2` | `(x_i(tT), y_i(tT), z_g(x_i(tT), y_i(tT), tT) + 0.08)`, t in [0, 1] | Orbital tracks along the well floor (hidden by default) |
| `bh_point1`, `bh_point2`, `ring_bh1`, `ring_bh2` | Point and ring markers | Hidden: they drew attention away from the fabric |
