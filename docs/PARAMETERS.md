# Parameters

Defaults are written by `scripts/build_state.py`.

## Controls (sliders)

| Symbol | Desmos id | Default | Range | Controls |
|---|---|---|---|---|
| `T` | `time_T` | `1` | 0 to 18 | Master clock. Press play: one sweep takes 45 s (`animationPeriod`), in steps of 0.01. |
| `T_m` | `time_Tm` | `10` | 4 to 14 | Time at which the binary reaches contact (merger rate). |
| `R_0` | `rad_R0` | `5` | 2 to 7 | Starting separation in grid units (10 M). |
| `M_1`, `M_2` | `mass_m1`, `mass_m2` | `1`, `1` | 0.2 to 3 | Masses: well depths, barycentre, and `eta`, which sets the number of orbits. |
| `A` | `amp_A` | `1.2` | 0.2 to 4 | Well depth (visualization scale). |
| `S` | `scale_S` | `2.2` | 0 to 5 | Ripple amplification (visualization only). |
| `e_0` | `eps` | `1` | 0.3 to 2 | Well softening (larger: wider, shallower dips). |
| `v_w` | `wave_v` | `2.2` | 0.8 to 4 | Ripple propagation speed (display speed). |
| `Q_f` | `wave_Q` | `3.3` | 1 to 8 | Ringdown quality factor. Higher rings longer. |

## Physical constants (collapsed folder, editable)

| Symbol | Id | Value | Meaning |
|---|---|---|---|
| `q_c` | `phys_qc` | `0.6` | Contact radius over start radius, `6M/10M`. |
| `Delta_p` | `phys_dp` | `0.6` | Plunge duration (animation time). |
| `g_r` | `phys_gr` | `1.5` | Ringdown over contact GW frequency (real about 3.9; capped for grid resolution). |
| `A_p` | `phys_ap` | `0.85` | Merger peak wave amplitude, relative. |
| `a_i` | `phys_ai` | `0.22` | Inspiral wave amplitude at contact, relative. |
| `epsilon_r` | `phys_er` | `0.046` | Mass fraction radiated (GW150914: 3 of 65 solar masses). |

## Derived (do not edit)

`eta = M1 M2 / (M1+M2)^2` (`phys_eta`), `tau_p = T_m / (1 - q_c^4)` (`phys_tau`), `Phi_c = 7.127 / eta` (`phys_Phic`), and `Omega_c` (`phys_Omc`), the orbital angular frequency at contact.

Fixed in the equations: the plunge exponent 1.5, the frequency-ramp shape, the wave fade-in time 0.8, the radial decay 0.35, and the well exponent 1.4 (`WELL_EXP` in the build script).

Black-hole dots: `LIFT = 0.7` (height above the local fabric) and size `1 + 3 M` in `scripts/build_state.py`.

Grid density: `HALF = 6`, `STEP = 0.25` in `scripts/build_state.py` (49 lines per direction).
