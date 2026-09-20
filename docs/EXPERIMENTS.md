# Experiment Logs & Benchmarks

## Experiment 001: Desmos 2D vs 3D Feasibility
- **Date**: 2026-09-18
- **Objective**: Determine whether Desmos Graphing Calculator (2D) or Desmos 3D (`desmos.com/3d`) is optimal for true 3D spacetime fabric rendering.
- **Finding**: Desmos 3D provides hardware-accelerated 3D surface rendering (z = f(x,y)), native 3D lighting, rotational viewport, and 3D point markers.
- **Outcome**: Adopted `desmos.com/3d` as the visualization environment.

## Experiment 002: 3D Spacetime Fabric & Static Wells Prototype
- **Date**: 2026-09-18
- **Expressions Deployed**: 20 expressions (Master time t, mass sliders M1, M2, curvature depth A, visualization amplification S, regularized distance functions r1, r2, rc, gravitational well function zg, ripple function zw, surface equation z, and 3D singularity point markers).
- **Visual Result**: Clear dual-funnel gravitational well with distinct singularity centers and superposed outward propagating wave ripples.
- **Performance**: Desmos 3D maintained smooth 60fps rendering during slider manipulation and time progression.
- **Screenshot Artifact**: `desmos_3d_fabric_prototype.png`

## Experiment 003: Pure Deformable 3D Grid Fabric Implementation
- **Date**: 2026-09-18
- **Objective**: Replace solid surface rendering with pure 3D deformable grid curves that curl downward into singularities and undulate with ripples.
- **Result**: Implemented dual families of 3D parametric curves indexed across coordinate list Lg.
- **Visual Evaluation**: Extremely crisp and intuitive spacetime grid visualization. The fabric lines clearly plunge into the two singularity funnels and visibly undulate with the traveling wave.
- **Screenshot Artifact**: `desmos_3d_grid_refined.png`

## Experiment 004: Dynamic Inspiral, Coalescence, and Outward Propagating Wavefront
- **Date**: 2026-09-18
- **Objective**: Implement time-dependent orbital positions, chirping inspiral, smooth merger coalescence, and a localized traveling wavefront launched at merger time Tm=10.
- **Demonstrated States**:
  1. **Early Orbit (T=1.0)**: Wide separation (R ≈ 4.8), steady orbit, calm outer fabric. Verified in `state_1_early_orbit.png`.
  2. **Inspiral (T=7.0)**: Tight separation (R ≈ 3.2), accelerated chirping phase, two funnels rapidly closing in. Verified in `state_2_inspiral.png`.
  3. **Merger (T=10.0)**: Separation collapses to R=0, two funnels smoothly coalesce into a single central well, launching the primary burst. Verified in `state_3_merger.png`.
  4. **Post-Merger Ripple (T=12.2)**: Massive annular wavefront propagating outward at speed vw=1.3, deforming grid lines into pronounced crests and troughs. Verified in `state_4_post_merger_ripple.png`.
  5. **Ringdown (T=15.0)**: Wavefront expands to the grid boundaries and decays, leaving a settled remnant well. Verified in `state_5_ringdown.png`.

## Experiment 005: Automated checkpoints and fabric realism pass
- **Date**: 2026-09-19
- **Findings on the committed state**: sliders had drifted from the documented defaults (`Tm=5.38`, `e0=-3.9`, `sigma=-0.1`); the merged well was a needle about -10 deep; the wave was symmetric about `T_m`, so it also appeared before the merger; black markers and thick trails dominated the fabric.
- **Changes** (via `scripts/build_state.py`): defaults reset; wave gated by retarded time with a fast rise and slow ringdown plus a `cos(2·(θ − φm))` quadrupole factor; well profile 1 / r to the power 1.4; 49 × 49 mesh over ±6 with the line domain equal to the grid extent; box, plane and axes hidden; markers hidden; trails hidden by default.
- **Tooling findings**: Playwright Chromium runs Desmos 3D headlessly (SwiftShader WebGL). Desmos 3D line width has a floor of 1; `colorLatex` is ignored on 3D curves; `showBox3D`, `showPlane3D`, `showAxis3D` and `axis3D` persist in the state, but `worldRotation3D` did not change the camera on load.
- **Verified stages**: T = 1, 7, 9.6, 10.4, 12, 15 in `assets/screenshots/checkpoints/`.

## Experiment 006: Physics engine v2 (Peters, chirp, ringdown)
- **Date**: 2026-09-19
- **Sources**: Wikipedia articles on gravitational waves (Peters decay, GW150914 numbers), the ISCO, quasinormal modes and the Schwarzschild metric (Flamm's paraboloid); Berti, Cardoso and Will (2006) for ringdown numbers (see `docs/REFERENCES.md`).
- **Changes**: `R(T) = R0 · ⁴√(1 − T/τ)` with ISCO contact and a plunge; closed-form Kepler+Peters phase (exponent 5/8), giving a real chirp; one retarded-time wave field with inspiral amplitude growing as ∛(f²), a merger peak and a quasinormal ringdown (`Q = 3.3`); 4.6% of the mass radiated; ad-hoc `k`, `sigma` and the separate inspiral term removed.
- **Verification with Playwright MCP** on a real GPU (AMD Radeon 860M): 52 expressions, 0 errors; redraw while stepping `T` had a median of 11 ms and p90 of 17 ms. Live tuning dropped the inspiral amplitude `a_i` from 0.35 to 0.22 so the two wells stay visible before contact.
- **Findings**: at `T = 10.4` a single deep remnant funnel with an outgoing wave train; by `T = 15` the ringdown has decayed and the remnant is settled. The real ringdown/contact frequency ratio (about 3.9) is capped at 1.8 so the wavelength stays resolvable by the 0.25 mesh.
- **Tooling note**: the Playwright MCP sandbox has no `require`, so `scripts/make_mcp_loader.py` embeds the state in a snippet loaded via `browser_run_code_unsafe`'s `filename` argument (inside the MCP's allowed root).

## Experiment 007: Subtle fabric, black-hole dots, slow playback
- **Date**: 2026-09-20
- **Fabric**: hairline light-grey lines (`lineWidth` 0.3, `#bdbdbd`). On a real-GPU browser this renders as the thinnest line; the headless software renderer clamps widths below 1, so checkpoints are now captured with Playwright MCP in a GPU-backed browser, not `render_checkpoints.js`.
- **Black holes**: `bh_point1`, `bh_point2` (size `1 + 3 M_i`) and `bh_merged` (size `1 + 3 (M1+M2) f_m`, so the merged dot is visibly larger and reflects the radiated mass). Desmos accepted expression-valued `pointSize` and domain-restricted points (`{T < T_m + Delta_p}`).
- **Dots on top of the fabric**: dots exactly on the surface looked sunk into the deep, narrow wells and were veiled by the mesh. Fixes: dots lifted 0.7 above `Z`; wells widened and made shallower (`A` 1.7 to 1.2, `e_0` 0.8 to 1); camera elevation 18 to 34 degrees; merger peak `A_p` 1.6 to 0.85 and `g_r` 1.8 to 1.5 so the ringdown wall no longer hides the merged hole.
- **Playback**: slider `animationPeriod` 45000 ms with step 0.01. Measured by pressing the play button: 0.404 T per second, 44.6 s per sweep.
- **Tooling note**: the `isPlaying` API flag did not start playback; clicking the "Play T Animation" button did.

## Experiment 008: Playback performance (8.5 to 40 fps)
- **Date**: 2026-09-20
- **Method**: `scripts/bench_fps.js` presses the real Play button in a GPU-backed Chromium (background throttling disabled) and counts completed 3D redraws per second. Measurements in a normal browser window are unreliable: the window gets throttled and readings collapse to about 1 fps regardless of content.
- **Baseline**: 8.5 fps on an AMD Radeon 860M (about 118 ms per frame).
- **Decomposition** (redraws/s): trivial height function 40, wells only 21, wave only 10.8, everything 8.5. Wave parameters (amplitude, speed, frequency) made no difference, so the cost is per-sample evaluation and per-curve overhead, not curve steepness.
- **Key finding**: Desmos takes a fixed number of samples per curve regardless of its length (halving line length changed nothing; halving the line count nearly doubled speed). Cost is proportional to the number of curves.
- **Fixes and effect**: serpentine curves (98 curves to 10): 8.6 to 25.6 fps; T-only values as variables plus integer-power wells: 29.9; radial wave table with nearest entry: 34.9; 5 curves per direction instead of 7: 40 (the same ceiling as the trivial-height test).
- **Tried and rejected**: lists of points drawn as polylines (Desmos draws each point as a 3D object: about 2 s per frame and a cap of about 1000 points per list); an atan-free trig table (slower than the atan version); a single-power rewrite of `A_w` and `phi_0` (no gain).
- **Unchanged**: the 49 × 49 mesh density and the look. Wells changed from 1 / r to the power 1.4 to `1 / (d² + e0²)`, which needs no sqrt or pow and looks essentially the same.
- **Black holes**: the merged dot now follows only 60% of the well depth plus the local wave amplitude, so it hovers above the deeper merged dip instead of sinking into it.
