# LSCherry — VFX

**Menu path:** `Add Shader > LSCherry > VFX`

> 2 node(s) in this category. Socket types, defaults and ranges below are extracted directly from the compiled node source — they are the ground truth.

Self-contained special-effect shaders: a sci-fi blueprint/wireframe look and a hologram look. Each is a complete surface shader rather than a modifier.

## When to use it

- Holographic UI props, projections, and ghost/spirit characters.
- Blueprint / schematic reveal effects.

## How to use it

1. Add the node and connect its `Shader`/`Combined` output straight to the Material Output.
2. Animate the exposed factors (scan lines, distortion, alpha) for motion.

## Node reference

### Blueprint Shader

Self-contained blueprint/schematic wireframe-reveal surface shader.

**Menu:** `Add Shader > LSCherry > VFX > Blueprint Shader`


Inputs are grouped into collapsible panels in the N-panel: **Outline**; **Grid**; **Triangular**.

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Outline/Grid` | Boolean | On | — | Toggle for this option. |
| `Outline Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color value for this slot. |
| `Grid Line Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color value for this slot. |
| `Triangular Detail Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color value for this slot. |
| `Emission Strength` | Float | 5 | 0 – 1000 | Multiplier for the emission color's brightness. |
| `Outline Opacity` | Float | 0.5 | 0–1 (factor) | Scalar value. |
| `Outline Thickness` | Float | 0.93 | 0.91 – 0.98 | Scalar value. |
| `Grid Opacity` | Float | 0.5 | 0–1 (factor) | Scalar value. |
| `Grid Density` | Float | 5 | 5 – 50 | Scalar value. |
| `Grid Line Thickness` | Float | 0.005 | 0.005 – 0.15 | Scalar value. |
| `Triangular Detail Opacity` | Float | 1 | 0–1 (factor) | Scalar value. |
| `Triangular Detail Scale` | Float | 0.3 | 0.01 – 1 | Scale of this feature. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shader` | Shader | Shader stream — connect the surface being processed (in) or pass it on (out). |

---

### Hologram Shader

Self-contained hologram surface shader (scan lines, transparency, glow).

**Menu:** `Add Shader > LSCherry > VFX > Hologram Shader`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Base Color` | Color (RGBA) | (0.09306, 0.5333, 1, 1) | — | The surface's lit (fully-illuminated) albedo color. |
| `Dispersion Hue` | Float | 0.5 | 0–1 (factor) | Scalar value. |
| `Flick Offset` | Float | 0 | 0 – ∞ | Positional offset applied to this term. |
| `Flick Intensity` | Float | 1 | 0–1 (factor) | Scalar value. |
| `Emission Strength` | Float | 12 | 0 – 1000000 | Multiplier for the emission color's brightness. |
| `Wireframe Sixe` | Float | 0.0007 | 0 – 100 | Scalar value. |
| `Wave Size` | Float | 2 | 0.1 – 100 | Size of this feature. |
| `Normal Map Strength` | Float | 1 | 0 – 10 | Ramp color stop — one color of the generated toon ramp. |
| `Normal Map` | Vector | (0, 0, 0) | -∞ – ∞ | Normal vector for this term. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shader` | Shader | Shader stream — connect the surface being processed (in) or pass it on (out). |
