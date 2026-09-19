# Parameters

Defaults are written by `scripts/build_state.py`. Slider ranges are what the graph exposes.

| Symbol | Desmos id | Default | Slider range | Controls |
|---|---|---|---|---|
| `T` | `time_T` | `1` | 0 to 18, step 0.05 | Master simulation time. Press play to animate. |
| `T_m` | `time_Tm` | `10` | 4 to 14 | Merger time (also the merger rate: earlier means a faster inspiral). |
| `R_0` | `rad_R0` | `5` | 2 to 7 | Initial separation of the two objects. |
| `M_1`, `M_2` | `mass_m1`, `mass_m2` | `1`, `1` | 0.2 to 3 | Masses. They set the well depths and the barycentre position. |
| `A` | `amp_A` | `1.7` | 0.2 to 4 | Well depth (visualization scale). |
| `S` | `scale_S` | `2.2` | 0 to 5 | **Ripple amplification**, visualization only. |
| `e_0` | `eps` | `0.8` | 0.3 to 2 | Softening. Larger means wider, shallower wells. |
| `v_w` | `wave_v` | `1.6` | 0.5 to 3 | **Ripple propagation speed**. |
| `k` | `wave_k` | `2.2` | 0.5 to 5 | Wavenumber. The wavelength in space is `2 pi / k`. |
| `sigma` | `wave_sig` | `1.6` | 0.3 to 3 | Ringdown decay time behind the wavefront. |

Fixed inside the equations and not exposed as sliders: the inspiral exponent `0.38`, the phase coefficients `1.2` and `7`, the well exponent `1.4`, the quadrupole weight `0.6`, the radial decay `0.35`, and the wave rise width (the `0.5` in the pre-front Gaussian).

Grid density is set in `scripts/build_state.py` (`HALF = 6`, `STEP = 0.25`, so 49 lines in each direction).
