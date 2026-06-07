# LSCherry — Plugin

**Menu path:** `Add Shader > LSCherry > Plugin`

Procedural surface patterns and ready-made material presets. 21 nodes grouped into hatching patterns, painted styles, watercolor styles, and physical material surfaces.

---

## Hatching Patterns

### `DotHatching`

Dot-based cross-hatching pattern. Produces a halftone-dot grid usable as a toon shadow fill or overlay.

**Inputs:** `Scale`, `Density`, `Threshold`  
**Outputs:** `Pattern` (float mask)

### `LineHatching`

Parallel-line hatching pattern. Classic ink-hatching appearance.

**Inputs:** `Scale`, `Angle`, `Density`, `Threshold`  
**Outputs:** `Pattern`

### `DiagonalStripe`

45-degree diagonal stripe pattern. Useful for cross-hatching or stylized fabric weaves.

**Inputs:** `Scale`, `Width`, `Offset`  
**Outputs:** `Pattern`

### `CheckerHatching`

Checkerboard-based hatching — alternating cells filled with the hatching pattern.

**Inputs:** `Scale`, `Cell Size`, `Density`  
**Outputs:** `Pattern`

### `HalfCheckerHatching`

Half-checker variant — every other row of cells is filled, producing a brick-like hatching grid.

**Inputs:** `Scale`, `Cell Size`, `Density`  
**Outputs:** `Pattern`

---

## Painted Patterns

Six variations of a hand-painted brush stroke surface pattern, increasing in complexity:

| Node | Character |
|---|---|
| `Painted001` | Fine, tight brushwork |
| `Painted002` | Medium brushwork with slight variation |
| `Painted003` | Looser, more expressive strokes |
| `Painted004` | Heavy impasto-like texture |
| `Painted005` | Directional sweeping strokes |
| `Painted006` | Mixed direction, high variation |

All Painted nodes share the same interface:

**Inputs:** `Scale`, `Strength`, `Color`  
**Outputs:** `Pattern`, `Color`

### `KristofDedenePainted`

A painted pattern contributed by Kristof Dedene. Produces a distinctive gouache/acrylic-paint surface texture.

**Inputs:** `Scale`, `Strength`  
**Outputs:** `Pattern`

---

## Watercolor Patterns

Three watercolor wash patterns with increasing wash intensity:

| Node | Character |
|---|---|
| `Watercolor001` | Light, translucent wash |
| `Watercolor002` | Medium wash with visible paper texture |
| `Watercolor003` | Heavy wash, strong paper grain |

All Watercolor nodes:

**Inputs:** `Scale`, `Strength`, `Color`  
**Outputs:** `Pattern`, `Color`

---

## Special Patterns

### `ScratchPattern`

Procedural surface scratch/micro-detail pattern. Useful for worn metal, aged surfaces, or stylized grime.

**Inputs:** `Scale`, `Density`, `Strength`  
**Outputs:** `Pattern`

---

## Material Presets

### `SmoothMetal`

A complete smooth metallic surface. Outputs a `Shader` ready for Material Output.

**Inputs:** `Color`, `Roughness`, `Metallic`  
**Outputs:** `Shader`

### `BrushedChrome`

Brushed/directional chrome surface. Produces anisotropic-looking highlights along a defined brush direction.

**Inputs:** `Color`, `Brush Direction`, `Roughness`  
**Outputs:** `Shader`

### `AnisotropicSpherical`

Spherical anisotropic reflections — circular highlight rings typical of sphere-brushed or turned metal.

**Inputs:** `Color`, `Roughness`, `Anisotropy`  
**Outputs:** `Shader`

### `BrushSet`

A comprehensive brush-based texturing node. Combines multiple brush stroke layers into a unified surface shader with individual controls per layer.

**Inputs:** Multiple per-layer color, scale, and strength controls  
**Outputs:** `Shader`, `Pattern`
