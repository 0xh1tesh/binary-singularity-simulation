# Model and Approximations

## Scientific framing

This project is an **interactive mathematical visualization inspired by general relativity**. It is not a numerical-relativity solution of the Einstein field equations. Each part below is tagged with what kind of statement it is:

| Tag | Meaning |
|---|---|
| **Established** | A standard published result, used as written (references in [REFERENCES.md](./REFERENCES.md)). |
| **Approximation** | A simplification of a real result (Newtonian limit, capped ratio, etc.). |
| **Phenomenological** | Chosen to look right, with the physical shape but not derived here. |
| **Visualization only** | Exaggeration or layout with no physical meaning. |

Formulas use plain text: a name like `Tm` or `zg` is one symbol, a product is written with a dot, and powers are written with ², ³, ⁴, roots or fractions (see the notation note in [EQUATIONS.md](./EQUATIONS.md)).

Displayed height = model height · S. Nothing on screen is a physical magnitude.

## One master clock

Everything is a function of the slider `T`. The orbit and the wave share it, and the wave is emitted from the orbit at the retarded time `ur = T − r / vw`.

```
                       Master time T
                             |
       Peters decay R(T) ----+---- Kepler+Peters phase φ0(T)
                             |
                x1(T),y1(T)  x2(T),y2(T)
                             |
   zg: two potential wells --+-- zw: wave field, retarded time ur = T − r/vw
   (mass reduced by radiation)        chirp -> merger peak -> ringdown
                             |
                   Z = zg + zw  ->  deformable grid
```

## Units

Geometric units G = c = 1, lengths in units of the total mass M = m1 + m2 (so GM/c² = 1). The binary starts at R0 = 10 M and the merger begins at the Schwarzschild innermost stable circular orbit Rc = 6 M, so qc = Rc / R0 = 0.6. The `R0` slider rescales this to screen units; `T` is animation time, not seconds.

## Inspiral (Established, Newtonian limit)

- **Separation decay** (Peters): dR/dt = −(64/5) · m1 · m2 · (m1 + m2) / R³, whose solution is R(t) = R0 · ⁴√(1 − t/τ) with τ = (5/256) · R0⁴ / (m1 · m2 · (m1 + m2)). Here τp = Tm / (1 − qc⁴), so that R(Tm) = Rc.
- **Orbital frequency** (Kepler): Ω = √(M / R³). Integrating with the Peters decay gives the closed form
  Φ(T) = Φc · (1 − ⁸√((1 − T/τp)⁵)) / (1 − qc² · √qc), and Ω grows as 1 / ⁸√((1 − T/τp)³): the chirp.
- **Total phase**: Φc = ( (R0/M)² · √(R0/M) − (Rc/M)² · √(Rc/M) ) / (32 · η) = 7.127 / η rad, about 4.5 orbits for equal masses, with η = m1 · m2 / M². GW150914 spent about 5 orbits in the detector band, so the visible inspiral length is realistic.
- **GW frequency** is twice the orbital frequency, so the wave phase is 2 · φ0.
- **Positions**: barycentric split of R by the masses, at angle φ0.

## Merger (Approximation)

- **Plunge**: for Tm ≤ T < Tm + Δp, R = Rc · (1 − x) · √(1 − x) with x = (T − Tm) / Δp, reaching 0. This is a phenomenological plunge, not a geodesic.
- **Frequency ramp**: the GW frequency rises from the contact value to gr times it. The real ratio is about 3.9 (ringdown M·ω = 0.53 against 2·Ωisco = 2 / (6·√6) = 0.136); it is capped at gr = 1.5 so the shortest wavelength stays resolvable by the 0.25 grid.
- **Radiated mass**: the well mass is scaled by fm = 1 − 0.046 · clamp((T − Tm) / Δp, 0, 1). GW150914 radiated about 3 of 65 solar masses.

## Wells (Approximation, Visualization only)

`zg = − fm · A · ( M1 / (d1² + e0²) + M2 / (d2² + e0²) )`, where `di` is the distance to object i. This is a softened, potential-style well chosen to look like the familiar gravity-well picture. A true 1/r potential would merge the two visual wells much earlier; the form `1 / (d² + e0²)` keeps them distinct until contact and needs no square roots or fractional powers, which makes it cheap to evaluate. Depth scales with mass, so the merged well (mass M1 + M2, minus the radiated fraction) is about twice as deep as either single well: a visibly bigger bend.

The Schwarzschild embedding diagram (Flamm's paraboloid) is deliberately **not** used: the Wikipedia article states it must not be confused with a gravity well, because it shows only the spatial slice geometry.

## Gravitational wave (Phenomenological, shaped by Established results)

One retarded-time field, not separate pieces:

`zw = S · Aw(ur) · cos( 2θ − 2·φ0(ur) ) / (1 + 0.35 · r)`, with `ur = T − r / vw`.

- **Angular pattern**: cos(2θ − 2·φ0) is the m = 2 mode: a two-armed spiral wound by the orbit, four lobes, rotating with the binary. It is a scalar stand-in for the plus polarization seen face-on, not a tensor field.
- **Inspiral amplitude**: Aw grows as the cube root of f² (chirp-mass scaling), which with f growing as 1 / ⁸√((1 − t/τ)³) gives Aw = ai · qc / ⁴√(1 − u/τp), equal to ai at contact. It is faded in over the first 0.8 time units.
- **Merger**: a smoothstep from ai to the peak Ap over the plunge.
- **Ringdown** (Established form, approximate numbers): a damped sinusoid that decays as exp(−γ·u) and oscillates as cos(ω·u), with γ = ω / (2·Q). The quality factor Qf = 3.3 is the fundamental l = m = 2 mode for a remnant spin near 0.69 (Berti, Cardoso and Will 2006); the exact coefficients were recalled, not re-verified, so treat Q as approximate.
- **Radial decay**: 1 / (1 + 0.35·r) regularizes the far-field 1/r at the source.
- **Evaluation**: amplitude and phase depend on position only through the radius, so they are tabulated once per frame on a radial table (step 0.02, nearest entry). The look-up phase error is below 0.07 rad.
- **Speed** `vw` is a display speed, not c.

## Black-hole dots (Visualization only)

Two small dots (size `1 + 3·Mi`) follow the wells, then one larger dot (size `1 + 3·(M1 + M2)·fm`) replaces them at `Tm + Δp`. Their height is `0.6·zg + 0.7 + S·Aw(min(T, Tm) − 0.3/vw)`: they follow only 60% of the well depth, so a deeper dip lifts the dot higher above the sheet, and they add the wave amplitude frozen at the merger (`min(T, Tm)`), so ripples never swallow them and the merged dot keeps a steady height instead of bouncing with the ringdown amplitude. The dots float on top of the fabric and are not part of the physics.

## Known limitations

- Amplitude ratios (`ai`, `Ap`) and the plunge shape are visual choices.
- The scalar cos(2θ) field is not the tensor GW field; there is no cross polarization and no inclination.
- The orbit is circular and planar, and there is no spin.
- The two wells can read as one from some camera angles shortly before contact.
- Heights are exaggerated, and `T` is animation time.
