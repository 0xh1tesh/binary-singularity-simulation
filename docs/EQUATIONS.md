# Equation Registry

`desmos_state.json` is the canonical graph state. `scripts/build_state.py` patches it by expression id, so this table is the map from id to model concept. Tags (Established, Approximation, Phenomenological, Visualization only) are explained in [MODEL.md](./MODEL.md); sources are in [REFERENCES.md](./REFERENCES.md). In Desmos the expressions sit in folders: Controls, Physical constants, Model, Spacetime fabric, Optional markers.

**Notation.** Formulas are written in plain text. A name such as `Tm`, `qc` or `zg` is one symbol (a base letter plus a label), so a product is always written with a dot: `A · Tm`. Squares and cubes use ², ³, ⁴; roots use √, ∛, ⁴√, ⁸√; a power is written as a root or a fraction rather than with a caret. `x1(T)` means the function x1 of T. Expression ids (`time_Tm`, `phys_qc`, ...) are code identifiers and keep their underscores.

## Controls

`time_T` (T), `time_Tm` (Tm), `rad_R0` (R0), `mass_m1`, `mass_m2` (M1, M2), `amp_A` (A), `scale_S` (S), `eps` (e0), `wave_v` (vw), `wave_Q` (Qf). Defaults and ranges: [PARAMETERS.md](./PARAMETERS.md).

## Physical constants and derived scales

| ID | Expression | Tag |
|---|---|---|
| `phys_qc` | `qc = 0.6` (Rc / R0 = 6M / 10M) | Established (ISCO) |
| `phys_dp` | `Δp = 0.6`, the plunge duration | Visualization only |
| `phys_gr` | `gr = 1.5`, ringdown-to-contact frequency ratio | Approximation (real value about 3.9) |
| `phys_ap`, `phys_ai` | `Ap = 0.85`, `ai = 0.22`, relative wave amplitudes | Phenomenological |
| `phys_er` | `εr = 0.046`, radiated mass fraction | Established (GW150914) |
| `phys_eta` | `η = M1 · M2 / (M1 + M2)²` | Established |
| `phys_tau` | `τp = Tm / (1 − qc⁴)` | Established (Peters, rescaled) |
| `phys_Phic` | `Φc = 7.127 / η` | Derived (Kepler + Peters) |
| `phys_Omc` | `Ωc = 5 · Φc / ( 8 · τp · (1 − qc² · √qc) · qc · √qc )` | Derived |

## Kinematics

| ID | Expression | Tag |
|---|---|---|
| `func_R` | `R(T)` = `R0 · ⁴√(1 − T/τp)` for T < Tm; `R0 · qc · (1 − (T−Tm)/Δp) · √(1 − (T−Tm)/Δp)` for Tm ≤ T < Tm + Δp; 0 afterwards | Established inspiral, phenomenological plunge |
| `func_phi` | `φ0(T)`: inspiral `Φc · (1 − ⁸√((1 − T/τp)⁵)) / (1 − qc² · √qc)`; plunge `Φc + Ωc · ( (T−Tm) + (gr−1) · (T−Tm)² / (2·Δp) )`; ringdown `Φc + Ωc · Δp · (gr+1)/2 + gr · Ωc · (T − Tm − Δp)` | Established inspiral, approximate afterwards |
| `coord_x1`, `coord_y1` | `x1 = M2/(M1+M2) · R(T) · cos φ0(T)`, `y1 = M2/(M1+M2) · R(T) · sin φ0(T)` | Established |
| `coord_x2`, `coord_y2` | `x2 = −M1/(M1+M2) · R(T) · cos φ0(T)`, `y2 = −M1/(M1+M2) · R(T) · sin φ0(T)` | Established |

## Fields

| ID | Expression | Tag |
|---|---|---|
| `cur_x1`, `cur_y1`, `cur_x2`, `cur_y2`, `cur_fm` | `X1c = x1(T)` and so on, and `Fmc = fm(T)`: T-only values stored as variables | Performance (evaluated once per frame, not per sample) |
| `dist_r1`, `dist_r2` | `ri = (x − Xic)² + (y − Yic)² + e0²`, the softened distance **squared** | Visualization only (softening) |
| `dist_rc` | `rc = √(x² + y² + 0.05)` | Visualization only |
| `func_fm` | `fm(T) = 1 − εr · clamp((T − Tm) / Δp, 0, 1)` | Established magnitude, phenomenological shape |
| `func_zgrav` | `zg = − Fmc · A · ( M1 / r1 + M2 / r2 )` | Approximation (softened potential wells) |
| `func_amp` | `Aw(u)`: for 0 < u < Tm, `ai · qc / ⁴√(1 − u/τp)`, ramped in over u < 0.8; over the plunge a smoothstep from `ai` to `Ap`; for u ≥ Tm + Δp, `Ap · exp( −gr · Ωc · (u − Tm − Δp) / Qf )`; otherwise 0 | Chirp scaling (cube root of f²) established; ringdown form established |
| `tab_r`, `tab_a`, `tab_p`, `tab_n` | Radial table `Rt = [0, 0.02 ... 9.2]`; `Wa = S · Aw(T − Rt/vw) / (1 + 0.35 · Rt)`; `Wp = 2 · φ0(T − Rt/vw)`; index `nr(r) = round(50 · r) + 1` | Radial wave table (retarded time u = T − r/vw; vw is a display speed) |
| `func_zwave` | `zw = Wa[nr(rc)] · cos( 2 · atan2(y, x) − Wp[nr(rc)] )`, equal to `S · Aw(ur) · cos(2θ − 2·φ0(ur)) / (1 + 0.35 · rc)` up to the table step | Phenomenological |
| `func_ztotal` | `Z = zg + zw` | |

## Fabric and markers

| ID | Expression | Role |
|---|---|---|
| `grid_xs`, `grid_ys` | `Xs(t) = −6 + 12 · ( mod(t,1) + mod(floor(t),2) · (1 − 2·mod(t,1)) )`; `Ys(t,c) = min(6, −6 + 0.25 · (10·c + floor(t)))` | Serpentine path: sweeps one grid line per unit of t, alternating direction |
| `grid_list` | `Ck = [0, 1, 2, 3, 4]` | Chunk index: 5 curves per direction, 10 grid lines each |
| `grid_lines_x`, `grid_lines_y` | `(Xs(t), Ys(t,Ck), Z(...))` and `(Ys(t,Ck), Xs(t), Z(...))`, t from 0 to 10 | The 49 × 49 fabric mesh (surplus rows clamp onto the border line) |
| `trail_obj1`, `trail_obj2` | Orbital tracks along the well floor | Hidden by default |
| `bh_point1`, `bh_point2` | `( xi(T), yi(T), 0.6·zg + 0.7 + S·Aw(min(T, Tm) − 0.3/vw) )` for T < Tm + Δp, size `1 + 3·Mi` | Black holes: small dots floating on top of the fabric |
| `bh_merged` | `( 0, 0, 0.6·zg + 0.7 + S·Aw(min(T, Tm) − 0.3/vw) )` for T ≥ Tm + Δp, size `1 + 3·(M1 + M2)·fm` | The merged, larger black hole, hovering over a deeper dip |
| `ring_bh1`, `ring_bh2`, `rg1`, `rg2` | Horizon rings and radii | Hidden |

Removed in this version: `func_ur` (retarded time is now implicit in the wave table); `wave_k`, `wave_sig` (replaced by the ringdown quality factor `wave_Q`) and `func_zinsp` (its role is now inside `func_zwave`).
