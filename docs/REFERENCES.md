# References

Formulas and numbers used by the model, and where each comes from. "Fetched" means the page was read while building this version; "recalled" means it is a standard result that was not re-checked against the source.

| Used for | Source | Status |
|---|---|---|
| Peters decay `dr/dt = -(64/5)(G^3/c^5) m1 m2 (m1+m2)/r^3`, time to coalescence `t = (5/256)(c^5/G^3) r^4/(m1 m2 (m1+m2))`, `r(t) = r0 (1 - t/t_c)^(1/4)`, and the GW150914 numbers (29 + 36 solar masses, about 5 orbits, 35 to 250 Hz, 3 solar masses radiated) | [Gravitational wave (Wikipedia)](https://en.wikipedia.org/wiki/Gravitational_wave) | Fetched |
| Schwarzschild ISCO `r = 6 GM/c^2 = 3 R_S` (contact radius) | [Innermost stable circular orbit (Wikipedia)](https://en.wikipedia.org/wiki/Innermost_stable_circular_orbit) | Fetched |
| Ringdown as a damped sinusoid `exp(-w'' t) cos(w' t)` after a merger | [Quasinormal mode (Wikipedia)](https://en.wikipedia.org/wiki/Quasinormal_mode) | Fetched (form only, no numbers on the page) |
| Flamm's paraboloid `w = 2 sqrt(r_s (r - r_s))` and the statement that it is not a gravity well (reason it is not used) | [Schwarzschild metric (Wikipedia)](https://en.wikipedia.org/wiki/Schwarzschild_metric) | Fetched |
| Fundamental `l = m = 2` quasinormal mode near `M w = 0.53`, `Q = 3.3` for remnant spin about 0.69 | Berti, Cardoso, Will, [Phys. Rev. D 73, 064030 (2006)](https://link.aps.org/doi/10.1103/PhysRevD.73.064030) | Recalled; the paper was located but the coefficients were not read |
| Kepler `Omega = sqrt(GM/a^3)`, GW frequency = 2 x orbital frequency, chirp-mass amplitude scaling `h ~ f^(2/3)` | Standard textbook results (e.g. Maggiore, *Gravitational Waves, Vol. 1*) | Recalled |
| Total inspiral phase `(1/(32 eta)) (R0/M)^(5/2)` | Follows from Kepler + Peters; derived in [MODEL.md](./MODEL.md) | Derived |
