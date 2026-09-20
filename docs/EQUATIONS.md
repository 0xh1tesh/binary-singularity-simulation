# Equation Registry

`desmos_state.json` is the canonical graph state. `scripts/build_state.py` patches it by expression id, so this table is the map from id to model concept. Tags (Established, Approximation, Phenomenological, Visualization only) are explained in [MODEL.md](./MODEL.md); sources are in [REFERENCES.md](./REFERENCES.md). In Desmos the expressions sit in folders: Controls, Physical constants, Model, Spacetime fabric, Optional markers.

## Controls

`time_T` (`T`), `time_Tm` (`T_m`), `rad_R0` (`R_0`), `mass_m1`, `mass_m2` (`M_1`, `M_2`), `amp_A` (`A`), `scale_S` (`S`), `eps` (`e_0`), `wave_v` (`v_w`), `wave_Q` (`Q_f`). Defaults and ranges: [PARAMETERS.md](./PARAMETERS.md).

## Physical constants and derived scales

| ID | Expression | Tag |
|---|---|---|
| `phys_qc` | `q_c = 0.6` (`R_c/R_0 = 6M/10M`) | Established (ISCO) |
| `phys_dp` | `Delta_p = 0.6` plunge duration | Visualization only |
| `phys_gr` | `g_r = 1.5` ringdown/contact frequency ratio | Approximation (real about 3.9) |
| `phys_ap`, `phys_ai` | `A_p = 0.85`, `a_i = 0.22` relative wave amplitudes | Phenomenological |
| `phys_er` | `epsilon_r = 0.046` radiated mass fraction | Established (GW150914) |
| `phys_eta` | `eta = M1 M2 / (M1+M2)^2` | Established |
| `phys_tau` | `tau_p = T_m / (1 - q_c^4)` | Established (Peters, rescaled) |
| `phys_Phic` | `Phi_c = 7.127 / eta` | Derived (Kepler + Peters) |
| `phys_Omc` | `Omega_c = 5 Phi_c / (8 tau_p (1 - q_c^2.5) q_c^1.5)` | Derived |

## Kinematics

| ID | Expression | Tag |
|---|---|---|
| `func_R` | `R(T) = {T<T_m: R_0 (1 - T/tau_p)^0.25, T<T_m+Delta_p: R_0 q_c (1 - (T-T_m)/Delta_p)^1.5, 0}` | Established inspiral, phenomenological plunge |
| `func_phi` | `phi_0(T)`: inspiral `Phi_c (1 - (1 - T/tau_p)^0.625)/(1 - q_c^2.5)`; plunge `Phi_c + Omega_c((T-T_m) + (g_r-1)(T-T_m)^2/(2 Delta_p))`; ringdown `Phi_c + Omega_c Delta_p (g_r+1)/2 + g_r Omega_c (T - T_m - Delta_p)` | Established inspiral, approximate afterwards |
| `coord_x1`, `coord_y1` | `M_2/(M_1+M_2) R(T) cos / sin phi_0(T)` | Established |
| `coord_x2`, `coord_y2` | `-M_1/(M_1+M_2) R(T) cos / sin phi_0(T)` | Established |

## Fields

| ID | Expression | Tag |
|---|---|---|
| `dist_r1`, `dist_r2` | `r_i = sqrt((x - x_i(T))^2 + (y - y_i(T))^2 + e_0^2)` | Visualization only (softening) |
| `dist_rc` | `r_c = sqrt(x^2 + y^2 + 0.05)` | Visualization only |
| `func_fm` | `f_m(T) = 1 - epsilon_r min(1, max(0, (T-T_m)/Delta_p))` | Established magnitude, phenomenological shape |
| `func_zgrav` | `z_g = -f_m (A M_1 / r_1^1.4 + A M_2 / r_2^1.4)` | Approximation (Newtonian-style wells) |
| `func_amp` | `A_w(u)`: `0<u<T_m: a_i q_c (1 - u/tau_p)^-0.25 min(1, u/0.8)`; plunge smoothstep to `A_p`; `u >= T_m+Delta_p: A_p exp(-g_r Omega_c (u - T_m - Delta_p)/Q_f)`; else 0 | Chirp scaling `f^(2/3)` established; ringdown form established |
| `func_ur` | `u_r = T - r_c / v_w` (retarded time) | Visualization only (`v_w` is a display speed) |
| `func_zwave` | `z_w = S A_w(u_r) cos(2 atan2(y,x) - 2 phi_0(u_r)) / (1 + 0.35 r_c)` | Phenomenological |
| `func_ztotal` | `Z = z_g + z_w` | |

## Fabric and markers

| ID | Expression | Role |
|---|---|---|
| `grid_list` | `L_g = [-6, -5.75, ..., 6]` (49 values) | Grid coordinates |
| `grid_lines_x`, `grid_lines_y` | `(t, L_g, Z(t, L_g, T))`, `(L_g, t, Z(L_g, t, T))`, t in [-6, 6] | Fabric lines |
| `trail_obj1`, `trail_obj2` | Orbital tracks along the well floor | Hidden by default |
| `bh_point1`, `bh_point2` | `(x_i(T), y_i(T), Z(x_i, y_i, T) + 0.7)` for `T < T_m + Delta_p`, size `1 + 3 M_i` | Black holes: small dots floating on top of the fabric |
| `bh_merged` | `(0, 0, Z(0, 0, T) + 0.7)` for `T >= T_m + Delta_p`, size `1 + 3 (M_1 + M_2) f_m` | The merged, larger black hole |
| `ring_bh1`, `ring_bh2`, `rg1`, `rg2` | Horizon rings and radii | Hidden |

Removed in this version: `wave_k`, `wave_sig` (replaced by the ringdown quality factor `wave_Q`) and `func_zinsp` (its role is now inside `func_zwave`).
