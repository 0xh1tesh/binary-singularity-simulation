# 3D Spacetime Fabric Visual Architecture

## Core Visual Paradigm: Pure Deformable 3D Grid Lines
Rather than rendering opaque or translucent continuous polygonal sheets with spherical markers, the spacetime fabric is represented entirely by an intersecting mesh of **3D parametric grid curves** that deform along the $Z$-axis in response to gravitational curvature and traveling wave perturbations.

### Mesh Structure
1. **X-Direction Parametric Family**:
   $$\mathbf{r}_x(t, y_i) = \big(t,\; y_i,\; Z(t, y_i, T)\big), \quad y_i \in L_g,\; t \in [-5.2, 5.2]$$
2. **Y-Direction Parametric Family**:
   $$\mathbf{r}_y(x_i, t) = \big(x_i,\; t,\; Z(x_i, t, T)\big), \quad x_i \in L_g,\; t \in [-5.2, 5.2]$$

### Visual Properties
- **Singularity Wells**: Grid lines converge and plunge downward into steep gravitational funnels around $(x_1, y_1)$ and $(x_2, y_2)$.
- **Gravitational Waves**: Wave crests and troughs undulate directly through the grid lines, causing them to physically rise and fall in 3D space.
- **Color & Weight**: Vibrant blue (`#2d70b3`), line width `2.5`, rendering high-contrast geometric lattice curves against the 3D coordinate frame.
