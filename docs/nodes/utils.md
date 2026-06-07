# LSCherry — Utils

**Menu path:** `Add Shader > LSCherry > Utils`

Utility nodes organized into five sub-categories. These are lower-level building blocks consumed by higher-level LSCherry nodes and useful as standalone utilities in any shader.

---

## BNodes

**Menu path:** `Add Shader > LSCherry > Utils > BNodes`

Basic node building blocks — color math, vector operations, and common shader primitives. 22 nodes.

| Group | Examples |
|---|---|
| Color utilities | Color blending, hue/saturation adjustment, color-to-value conversions |
| Math helpers | Remapping, clamping, smoothstep wrappers |
| Vector tools | Normal transformation, UV manipulation helpers |
| Background | Background color injection and environment blending |

Use BNodes as composable primitives when building custom shader setups from scratch.

---

## Procedural

**Menu path:** `Add Shader > LSCherry > Utils > Procedural`

Procedural texture generators — noise patterns, texture synthesis, and algorithmic surface generation. 27 nodes.

| Group | Examples |
|---|---|
| Noise | Layered Perlin, Voronoi variants, fractal noise |
| Patterns | Stripes, grids, radial patterns, checkerboards |
| Synthesis | Combining multiple procedurals with masks and blending |

Use these to generate surface detail without image textures, or as mask drivers for other effects.

---

## Ramp Style

**Menu path:** `Add Shader > LSCherry > Utils > Ramp Style`

Color ramp building and style application utilities. 6 nodes.

| Group | Purpose |
|---|---|
| Ramp builders | Construct color ramps from color pairs and stop positions |
| Style applicators | Apply a ramp to a gradient or shader output |
| Gradient tools | Convert a mask or shading value through a custom ramp |

---

## Separator

**Menu path:** `Add Shader > LSCherry > Utils > Separator`

Channel separation and component extraction utilities. 10 nodes.

| Group | Purpose |
|---|---|
| RGBA separators | Split a color or vector into individual R, G, B, A components |
| Channel routers | Route a specific channel to a scalar output |
| Lightmap splitters | Specialized separators for LSCherry lightmap RGBA conventions |

---

## Normal

**Menu path:** `Add Shader > LSCherry > Utils > Normal`

Normal map calculation and tangent space tools. 2 nodes.

| Node | Purpose |
|---|---|
| Normal calculation | Computes a normal vector from geometry or a normal map texture |
| Tangent space | Transforms normals between object, world, and tangent space |
