# Model and Approximations

## Scientific framing

This project is an **interactive mathematical visualization inspired by general relativity**. It is not a numerical-relativity solution of the Einstein field equations. Each part below is tagged with what kind of statement it is:

| Tag | Meaning |
|---|---|
| **Established** | A standard published result, used as written (references in [REFERENCES.md](./REFERENCES.md)). |
| **Approximation** | A simplification of a real result (Newtonian limit, capped ratio, etc.). |
| **Phenomenological** | Chosen to look right, with the physical shape but not derived here. |
| **Visualization only** | Exaggeration or layout with no physical meaning. |

Displayed height is `A_display = A_model * S`. Nothing on screen is a physical magnitude.

## One master clock

Everything is a function of the slider `T`. The orbit and the wave share it, and the wave is emitted from the orbit at the retarded time `u_r = T - r/v_w`.

```
                       Master time T
                             |
       Peters decay R(T) ----+---- Kepler+Peters phase phi0(T)
                             |
                x1(T),y1(T)  x2(T),y2(T)
                             |
   z_g: two potential wells --+-- z_w: wave field h(u_r), u_r = T - r/v_w
   (mass reduced by radiation)        chirp -> merger peak -> ringdown
                             |
                   Z = z_g + z_w  ->  deformable grid
```

## Units

Geometric units `G = c = 1`, lengths in units of the total mass `M = m1 + m2` (so `GM/c^2 = 1`). The binary starts at `R0 = 10 M` and the merger begins at the Schwarzschild innermost stable circular orbit `R_c = 6 M`, so `q_c = R_c/R0 = 0.6`. The `R_0` slider rescales this to screen units; `T` is animation time, not seconds.

## Inspiral (Established, Newtonian limit)

- **Separation decay** (Peters): `dR/dt = -(64/5) m1 m2 (m1+m2) / R^3`, whose solution is `R(t) = R0 (1 - t/tau)^(1/4)` with `tau = (5/256) R0^4 / (m1 m2 (m1+m2))`. Here `tau_p = T_m / (1 - q_c^4)`, so that `R(T_m) = R_c`.
- **Orbital frequency** (Kepler): `Omega = sqrt(M / R^3)`. Integrating with the Peters decay gives the closed form
  `Phi(T) = Phi_c (1 - (1 - T/tau_p)^(5/8)) / (1 - q_c^(5/2))`, and `Omega ~ (1 - T/tau_p)^(-3/8)`: the chirp.
- **Total phase**: `Phi_c = (1/(32 eta)) ((R0/M)^(5/2) - (R_c/M)^(5/2)) = 7.127 / eta` rad, about 4.5 orbits for equal masses, with `eta = m1 m2 / M^2`. GW150914 spent about 5 orbits in the detector band, so the visible inspiral length is realistic.
- **GW frequency** is twice the orbital frequency, so the wave phase is `2 phi0`.
- **Positions**: barycentric split of `R` by the masses, at angle `phi0`.

## Merger (Approximation)

- **Plunge**: for `T_m <= T < T_m + Delta_p`, `R = R_c (1 - x)^1.5` with `x = (T - T_m)/Delta_p`, reaching 0. This is a phenomenological plunge, not a geodesic.
- **Frequency ramp**: the GW frequency rises from the contact value to `g_r` times it. The real ratio is about 3.9 (ringdown `M w = 0.53` against `2 Omega_isco = 2 * 6^(-3/2) = 0.136`); it is capped at `g_r = 1.8` so the shortest wavelength stays resolvable by the 0.25 grid.
- **Radiated mass**: the well mass is scaled by `f_m = 1 - 0.046 * clamp((T - T_m)/Delta_p)`. GW150914 radiated about 3 of 65 solar masses.

## Wells (Approximation, Visualization only)

`z_g = -f_m (A M1 / r1^1.4 + A M2 / r2^1.4)`, with softened distances `r_i = sqrt(|r - r_i|^2 + e0^2)`. This is a Newtonian-potential-style well, chosen to look like the familiar gravity-well picture. A true `1/r` potential would merge the two visual wells earlier; the exponent 1.4 keeps them distinct.

The Schwarzschild embedding diagram (Flamm's paraboloid) is deliberately **not** used: the Wikipedia article states it must not be confused with a gravity well, because it shows only the spatial slice geometry.

## Gravitational wave (Phenomenological, shaped by Established results)

One retarded-time field, not separate pieces:

`z_w = S * A_w(u_r) * cos(2 theta - 2 phi0(u_r)) / (1 + 0.35 r)`, with `u_r = T - r/v_w`.

- **Angular pattern**: `cos(2 theta - 2 phi0)` is the `m = 2` mode: a two-armed spiral wound by the orbit, four lobes, rotating with the binary. It is a scalar stand-in for the plus polarization seen face-on, not a tensor field.
- **Inspiral amplitude**: `A_w ~ f^(2/3)` (chirp-mass scaling), which with `f ~ (1 - t/tau)^(-3/8)` gives `A_w = a_i q_c (1 - u/tau_p)^(-1/4)`, equal to `a_i` at contact. It is faded in over the first 0.8 time units.
- **Merger**: a smoothstep from `a_i` to the peak `A_p` over the plunge.
- **Ringdown** (Established form, approximate numbers): a damped sinusoid `exp(-gamma u) cos(w u)` with `gamma = w / (2 Q)`. The quality factor `Q_f = 3.3` is the fundamental `l = m = 2` mode for a remnant spin near 0.69 (Berti, Cardoso and Will 2006); the exact coefficients were recalled, not re-verified, so treat `Q` as approximate.
- **Radial decay**: `1/(1 + 0.35 r)` regularizes the far-field `1/r` at the source.
- **Speed** `v_w` is a display speed, not `c`.

## Known limitations

- Amplitude ratios (`a_i`, `A_p`) and the plunge shape are visual choices.
- The scalar `cos(2 theta)` field is not the tensor GW field; there is no `h_x` and no inclination.
- The orbit is circular and planar, and there is no spin.
- The two wells can read as one from some camera angles shortly before contact.
- Heights are exaggerated, and `T` is animation time.
