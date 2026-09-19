# Model and Approximations

## Scientific framing

This project is an **interactive mathematical visualization inspired by general relativity**. It is a Desmos-based approximation of binary compact-object merger dynamics and spacetime perturbations.

It is **not** a numerical-relativity solution of the Einstein field equations. Every part of the model is one of four kinds:

| Kind | What it covers |
|---|---|
| **Conceptual visualization** | The fabric itself. A 2D "spacetime sheet" whose height stands for potential depth is an embedding metaphor, not the real 4D geometry. |
| **Newtonian-inspired approximation** | Two point masses orbiting their barycenter, with a shrinking separation `R(T)` and a chirping phase `phi0(T)`. |
| **Phenomenological wave model** | The merger-triggered wavepacket `z_w`: its envelope, its quadrupole factor and its radial decay are chosen to look right, not derived from the field equations. |
| **Visualization-only amplification** | The slider `S` and the well depth `A`. Displayed amplitudes are far larger than any physical strain. |

Displayed height: `A_display = A_model * S_visual`. Nothing on screen should be read as a physical magnitude.

## One master clock

Everything is a function of the single slider `T`. There are no independent clocks for the orbit and the wave.

```
                    Master time T
                          |
          +---------------+---------------+
          v                               v
   separation R(T)                 orbital phase phi0(T)
          |                               |
          +---------------+---------------+
                          v
              x1(T),y1(T)   x2(T),y2(T)
                          |
                          v
       binary curvature z_g   (two wells -> one at T = T_m)
                          |
      retarded time u_r = T - T_m - r/v_w   (0 at the merger)
                          |
                          v
       merger-generated quadrupolar wave z_w
                          |
                          v
   Z(x,y,T) = z_g + z_w  ->  deformable grid lines
```

## Regimes

1. **Inspiral** (`T < T_m`). Separation `R(T) = R0 * (1 - T/T_m)^0.38`, which falls faster and faster toward the merger. Phase `phi0(T) = 1.2 T + 7 (1 - (1 - T/T_m)^0.5)`, so the angular speed rises and the orbit visibly tightens. Positions are the barycentric split of `R(T)` by the masses.
2. **Curvature wells.** `z_g = -A M1 / r1^1.4 - A M2 / r2^1.4` with softened distances `r_i = sqrt(|r - r_i(T)|^2 + e0^2)`. The exponent 1.4 (steeper than the Newtonian 1) keeps the two wells visually separate until they are close. When `R -> 0` the two terms coincide and form one deeper remnant well.
3. **Merger** (`T = T_m`). There is no switch: the merger is simply `R(T) = 0`, so the two wells become one continuously.
4. **Merger-generated wave.** With `u_r = T - T_m - r_c/v_w`:
   - envelope: `exp(-u_r^2 / 0.5)` for `u_r < 0` (fast rise at the wavefront) and `exp(-u_r / sigma)` for `u_r >= 0` (slow ringdown behind it);
   - carrier: `sin(-k v_w u_r)`, an outward-travelling wave;
   - quadrupole: `1 + 0.6 cos(2 (atan2(y,x) - phi0(T_m)))`, four lobes as for a rotating binary;
   - radial decay: `1 / (1 + 0.35 r_c)`.

   The wave is essentially zero before `T_m` and starts at the centre at `T_m`.
5. **Ringdown.** The `exp(-u_r/sigma)` tail decays the disturbance at every radius after the front passes.

## Known limitations

- The wave envelope has a small non-zero tail before `T_m` at small radius. It is a deliberate precursor, not a physical effect.
- The two wells can look merged from some camera angles around `T = 7`, when the separation is about 3 and the well width about 1.6.
- Heights are exaggerated (see above). The wave speed `v_w` and wavelength are tuned to fit the grid and the time range, not to any physical system.
- The inspiral term `z_i` is a weak, phenomenological two-arm spiral, not a post-Newtonian waveform.
- The orbital plane is fixed to the fabric plane, and only the plus-like quadrupole pattern is drawn. There is no separate `h_x` component.
