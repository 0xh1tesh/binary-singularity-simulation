# Experiment Logs & Benchmarks

## Experiment 001: Desmos 2D vs 3D Feasibility
- **Date**: 2026-09-18
- **Objective**: Determine whether Desmos Graphing Calculator (2D) or Desmos 3D (`desmos.com/3d`) is optimal for true 3D spacetime fabric rendering.
- **Finding**: Desmos 3D provides hardware-accelerated 3D surface rendering ($z = f(x,y)$), native 3D lighting, rotational viewport, and 3D point markers.
- **Outcome**: Adopted `desmos.com/3d` as the visualization environment.

## Experiment 002: 3D Spacetime Fabric & Static Wells Prototype
- **Date**: 2026-09-18
- **Expressions Deployed**: 20 expressions (Master time $t$, mass sliders $M_1, M_2$, curvature depth $A$, visualization amplification $S$, regularized distance functions $r_1, r_2, r_c$, gravitational well function $z_g$, ripple function $z_w$, surface equation $z$, and 3D singularity point markers).
- **Visual Result**: Clear dual-funnel gravitational well with distinct singularity centers and superposed outward propagating wave ripples.
- **Performance**: Desmos 3D maintained smooth 60fps rendering during slider manipulation and time progression.
- **Screenshot Artifact**: `desmos_3d_fabric_prototype.png`

## Experiment 003: Pure Deformable 3D Grid Fabric Implementation
- **Date**: 2026-09-18
- **Objective**: Replace solid surface rendering with pure 3D deformable grid curves that curl downward into singularities and undulate with ripples.
- **Result**: Implemented dual families of 3D parametric curves indexed across coordinate list $L_g$.
- **Visual Evaluation**: Extremely crisp and intuitive spacetime grid visualization. The fabric lines clearly plunge into the two singularity funnels and visibly undulate with the traveling wave.
- **Screenshot Artifact**: `desmos_3d_grid_refined.png`

## Experiment 004: Dynamic Inspiral, Coalescence, and Outward Propagating Wavefront
- **Date**: 2026-09-18
- **Objective**: Implement time-dependent orbital positions, chirping inspiral, smooth merger coalescence, and a localized traveling wavefront launched at merger time $T_m=10$.
- **Demonstrated States**:
  1. **Early Orbit ($T=1.0$)**: Wide separation ($R \approx 4.8$), steady orbit, calm outer fabric. Verified in `state_1_early_orbit.png`.
  2. **Inspiral ($T=7.0$)**: Tight separation ($R \approx 3.2$), accelerated chirping phase, two funnels rapidly closing in. Verified in `state_2_inspiral.png`.
  3. **Merger ($T=10.0$)**: Separation collapses to $R=0$, two funnels smoothly coalesce into a single central well, launching the primary burst. Verified in `state_3_merger.png`.
  4. **Post-Merger Ripple ($T=12.2$)**: Massive annular wavefront propagating outward at speed $v_w=1.3$, deforming grid lines into pronounced crests and troughs. Verified in `state_4_post_merger_ripple.png`.
  5. **Ringdown ($T=15.0$)**: Wavefront expands to the grid boundaries and decays, leaving a settled remnant well. Verified in `state_5_ringdown.png`.

## Experiment 005: Automated checkpoints and fabric realism pass
- **Date**: 2026-09-19
- **Findings on the committed state**: sliders had drifted from the documented defaults (`T_m=5.38`, `e_0=-3.9`, `sigma=-0.1`); the merged well was a needle about -10 deep; the wave was symmetric about `T_m`, so it also appeared before the merger; black markers and thick trails dominated the fabric.
- **Changes** (via `scripts/build_state.py`): defaults reset; wave gated by retarded time with a fast rise and slow ringdown plus a `cos(2(theta - phi_m))` quadrupole factor; well profile `r^-1.4`; 49 x 49 mesh over +-6 with the line domain equal to the grid extent; box, plane and axes hidden; markers hidden; trails hidden by default.
- **Tooling findings**: Playwright Chromium runs Desmos 3D headlessly (SwiftShader WebGL). Desmos 3D line width has a floor of 1; `colorLatex` is ignored on 3D curves; `showBox3D`, `showPlane3D`, `showAxis3D` and `axis3D` persist in the state, but `worldRotation3D` did not change the camera on load.
- **Verified stages**: T = 1, 7, 9.6, 10.4, 12, 15 in `assets/screenshots/checkpoints/`.
