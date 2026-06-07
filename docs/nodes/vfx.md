# LSCherry — VFX

**Menu path:** `Add Shader > LSCherry > VFX`

Special-effect shaders for dramatic visual styles. These are complete, standalone materials — connect their `Shader` output directly to a Material Output node.

---

## `BlueprintShader`

Renders the mesh as a technical blueprint drawing. Produces a dark background with glowing edge lines, grid overlay, and annotation-style highlights — similar to CAD wireframe visualizations.

**Inputs:**
- `Line Color` — color of the blueprint edge lines
- `Background Color` — dark background color (default: deep blue)
- `Grid Scale` — size of the background grid
- `Grid Opacity` — how visible the grid lines are
- `Line Thickness` — edge line width
- `Glow Strength` — intensity of the edge glow effect

**Outputs:** `Shader`

**Use case:** Mech, robot, or sci-fi prop reveals; architectural visualization; holographic UI panels.

---

## `HologramShader`

Simulates a holographic or energy-field appearance. Produces semi-transparent, scan-line-animated shading with rim glow and flickering.

**Inputs:**
- `Color` — primary hologram color (default: cyan)
- `Scan Line Speed` — animation speed of the horizontal scan lines
- `Scan Line Density` — number of scan lines per unit
- `Opacity` — overall transparency level
- `Rim Strength` — intensity of the fresnel rim glow
- `Flicker Amount` — magnitude of the random brightness flickering

**Outputs:** `Shader`

**Use case:** Projections, AI constructs, sci-fi characters, ghost/spirit effects, energy barriers.

> **Note:** `HologramShader` uses time-driven animation. Scan lines animate automatically when the timeline is playing.
