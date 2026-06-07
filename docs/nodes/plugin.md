# LSCherry — Plugin

**Menu path:** `Add Shader > LSCherry > Plugin`

> 20 node(s) in this category. Socket types, defaults and ranges below are extracted directly from the compiled node source — they are the ground truth.

Procedural pattern and material generators: hatching styles (line, dot, checker, diagonal stripe), painted and watercolor textures, scratch, and stylised metals (brushed chrome, smooth metal, anisotropic). Each pattern outputs a color/mask you mix into a surface — most usefully into the `Pattern` input of `Make Toon` or `Simple Make Toon`.

## When to use it

- Comic-book / manga shading via hatching patterns driven by light.
- Painterly and watercolor stylisation of surfaces.
- Stylised metals for props, weapons, and accessories.

## How to use it

1. Add from `Add Shader > LSCherry > Plugin`.
2. Connect the pattern's color output to the `Pattern` socket of `Make Toon`/`Simple Make Toon`, or multiply it into your own base color.
3. Use `UV`/`Scale` to control tiling and `Seed` (where present) for variation.

## Node reference

### Plugin: Anisotropic Spherical

**Menu:** `Add Shader > LSCherry > Plugin > Plugin: Anisotropic Spherical`


Inputs are grouped into collapsible panels in the N-panel: **Transform**; **Noise**.

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Mix Various` | Float | 0.05 | 0–1 (factor) | Scalar value. |
| `Up Pattern Value` | Float | 1 | 0–1 (factor) | Scalar value. |
| `Strength` | Float | 0.05 | 0–1 (factor) | Overall intensity of the effect. |
| `Location` | Vector | (0, 0, 0) | -∞ – ∞ | Vector value. |
| `Rotation` | Vector | (0, 0, 0) | -∞ – ∞ | Vector value. |
| `Scale` | Vector | (1, 1, 1) | -∞ – ∞ | Scale of the pattern / texture — higher values tile it more densely. |
| `W` | Float | 1 | -1000 – 1000 | Scalar value. |
| `Scale` | Float | 50 | -1000 – 1000 | Scale of the pattern / texture — higher values tile it more densely. |
| `Detail` | Float | 15 | 0 – 15 | Procedural detail / number of noise octaves — higher adds finer structure. |
| `Roughness` | Float | 0.2 | 0–1 (factor) | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |
| `Lacunarity` | Float | 2 | 0 – 1000 | Frequency gap between procedural noise octaves. |
| `Distortion` | Float | 0 | -1000 – 1000 | Amount of procedural distortion / warping applied. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Pattern` | Float | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |
| `Normal` | Vector | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |

---

### Plugin: Brush Set

**Menu:** `Add Shader > LSCherry > Plugin > Plugin: Brush Set`


Inputs are grouped into collapsible panels in the N-panel: **Transformation**; **Noise**.

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Texture Normal` | Menu | Type 1 | — | Normal vector for this term. |
| `Brush Texture` | Menu | Object | — | Mode selector. |
| `Transformation Location` | Vector | (0, 0, 0) | -∞ – ∞ | Vector value. |
| `Transformation Rotation` | Vector | (0, 0, 0) | -∞ – ∞ | Vector value. |
| `Transformation Scale` | Vector | (1, 1, 1) | -∞ – ∞ | Scale of this feature. |
| `Noise Mixture` | Float | 0.275 | 0–1 (factor) | Scalar value. |
| `Noise Scale` | Float | 5 | -1000 – 1000 | Scale of this feature. |
| `Noise Detail` | Float | 2 | 0 – 15 | Scalar value. |
| `Noise Roughness` | Float | 0.5 | 0–1 (factor) | Surface roughness for this term. |
| `Noise Distortion` | Float | 0 | -1000 – 1000 | Scalar value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Brush` | Color (RGBA) | Color value. |

---

### Plugin: Brushed Chrome

**Menu:** `Add Shader > LSCherry > Plugin > Plugin: Brushed Chrome`


Inputs are grouped into collapsible panels in the N-panel: **Transform**; **Noise**.

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Scale` | Float | 1 | 0 – 10000 | Scale of the pattern / texture — higher values tile it more densely. |
| `Multiplier` | Float | 2 | 0 – 10000 | Scalar value. |
| `Up Pattern Value` | Float | 2 | 0 – 5 | Scalar value. |
| `Strength` | Float | 0.05 | 0–1 (factor) | Overall intensity of the effect. |
| `Location` | Vector | (0, 0, 0) | -∞ – ∞ | Vector value. |
| `Rotation` | Vector | (0, 0, 0) | -∞ – ∞ | Vector value. |
| `W` | Float | 1 | -1000 – 1000 | Scalar value. |
| `Scale` | Float | 5 | -1000 – 1000 | Scale of the pattern / texture — higher values tile it more densely. |
| `Detail` | Float | 15 | 0 – 15 | Procedural detail / number of noise octaves — higher adds finer structure. |
| `Roughness` | Float | 0.4 | 0–1 (factor) | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |
| `Lacunarity` | Float | 2 | 0 – 1000 | Frequency gap between procedural noise octaves. |
| `Distortion` | Float | 0.1 | -1000 – 1000 | Amount of procedural distortion / warping applied. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Pattern` | Float | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |
| `Normal` | Vector | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |

---

### Plugin: Checker Hatching Pattern

**Menu:** `Add Shader > LSCherry > Plugin > Plugin: Checker Hatching Pattern`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Size` | Float | 0.15 | 0–1 (factor) | Size of the feature (dot, cell, highlight, …); larger values enlarge it. |
| `Scale` | Float | 23.6 | 0 – 1000000015047466219876688855040 | Scale of the pattern / texture — higher values tile it more densely. |
| `Distortion` | Float | 0 | -1000 – 1000 | Amount of procedural distortion / warping applied. |
| `Detail` | Float | 2 | 0 – 15 | Procedural detail / number of noise octaves — higher adds finer structure. |
| `Detail Scale` | Float | 1 | -1000 – 1000 | Scale of this feature. |
| `Detail Roughness` | Float | 0.5 | 0–1 (factor) | Surface roughness for this term. |
| `Phase Offset` | Float | 0 | -1000 – 1000 | Positional offset applied to this term. |
| `Enable Light Blend` | Boolean | Off | — | When on, blends the effect with scene lighting. |
| `Toon Style` | Vector | (0, 0, 0) | -∞ – ∞ | Ramp-style vector selecting the toon band shaping (from a Ramp Style node). |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Pattern` | Float | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |

---

### Plugin: Diagonal Stripe Pattern

**Menu:** `Add Shader > LSCherry > Plugin > Plugin: Diagonal Stripe Pattern`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Size` | Float | 0.2 | 0–1 (factor) | Size of the feature (dot, cell, highlight, …); larger values enlarge it. |
| `Scale` | Float | 25 | 0 – 1000000015047466219876688855040 | Scale of the pattern / texture — higher values tile it more densely. |
| `Distortion` | Float | 0 | -1000 – 1000 | Amount of procedural distortion / warping applied. |
| `Detail` | Float | 2 | 0 – 15 | Procedural detail / number of noise octaves — higher adds finer structure. |
| `Detail Scale` | Float | 1 | -1000 – 1000 | Scale of this feature. |
| `Detail Roughness` | Float | 0.5 | 0–1 (factor) | Surface roughness for this term. |
| `Phase Offset` | Float | 0 | -1000 – 1000 | Positional offset applied to this term. |
| `Enable Light Blend` | Boolean | Off | — | When on, blends the effect with scene lighting. |
| `Toon Style` | Vector | (0, 0, 0) | -∞ – ∞ | Ramp-style vector selecting the toon band shaping (from a Ramp Style node). |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Pattern` | Float | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |

---

### Plugin: Dot Hatching Pattern

**Menu:** `Add Shader > LSCherry > Plugin > Plugin: Dot Hatching Pattern`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Scale` | Float | 15 | -1000 – 1000 | Scale of the pattern / texture — higher values tile it more densely. |
| `Dot Size` | Float | 0.4 | 0–1 (factor) | Size of this feature. |
| `Enable Light Dot Blend` | Boolean | Off | — | Toggle for this option. |
| `Toon Style` | Vector | (0, 0, 0) | -∞ – ∞ | Ramp-style vector selecting the toon band shaping (from a Ramp Style node). |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Pattern` | Float | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |

---

### Plugin: Half Checker Hatching Pattern

**Menu:** `Add Shader > LSCherry > Plugin > Plugin: Half Checker Hatching Pattern`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Scale` | Float | 25 | 0 – 1000000015047466219876688855040 | Scale of the pattern / texture — higher values tile it more densely. |
| `Distortion` | Float | 0 | -1000 – 1000 | Amount of procedural distortion / warping applied. |
| `Detail` | Float | 2 | 0 – 15 | Procedural detail / number of noise octaves — higher adds finer structure. |
| `Detail Scale` | Float | 1 | -1000 – 1000 | Scale of this feature. |
| `Detail Roughness` | Float | 0.5 | 0–1 (factor) | Surface roughness for this term. |
| `Phase Offset` | Float | 0 | -1000 – 1000 | Positional offset applied to this term. |
| `Enable Light Blend` | Boolean | Off | — | When on, blends the effect with scene lighting. |
| `Toon Style` | Vector | (0, 0, 0) | -∞ – ∞ | Ramp-style vector selecting the toon band shaping (from a Ramp Style node). |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Pattern` | Float | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |

---

### Plugin: Kristof Dedene Painted Pattern

**Menu:** `Add Shader > LSCherry > Plugin > Plugin: Kristof Dedene Painted Pattern`


Inputs are grouped into collapsible panels in the N-panel: **Small Brushes**; **Hard Lines**; **Edge**.

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Base Color` | Color (RGBA) | (0.4452, 1, 0.4735, 1) | — | The surface's lit (fully-illuminated) albedo color. |
| `Details Color` | Color (RGBA) | (0.3278, 0.5029, 0.6867, 1) | — | Color value for this slot. |
| `Seed` | Integer | 42 | 0 – 2147483647 | Random seed; change it to get a different variation of the procedural result. |
| `Scale` | Float | 5 | 0 – 1000 | Scale of the pattern / texture — higher values tile it more densely. |
| `Details` | Float | 0.4 | 0–1 (factor) | Scalar value. |
| `AO strength` | Float | 0.8 | 0–1 (factor) | Intensity of this contribution. |
| `Layer 1` | Float | 1 | 0–1 (factor) | Scalar value. |
| `Layer 1 Color` | Color (RGBA) | (0.1145, 0.2533, 1, 1) | — | Color value for this slot. |
| `Layer 2` | Float | 1 | 0–1 (factor) | Scalar value. |
| `Layer 2 Color` | Color (RGBA) | (0.1145, 0.2533, 1, 1) | — | Color value for this slot. |
| `Hard Lines Strength` | Float | 0.6 | 0–1 (factor) | Intensity of this contribution. |
| `Hard Lines Distortion` | Float | 0.05 | 0–1 (factor) | Scalar value. |
| `Hard Lines Scale` | Float | 30 | 0 – 1000 | Scale of this feature. |
| `Edge Wet Paint` | Float | 100 | 0 – 1000 | Scalar value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Base Color` | Color (RGBA) | The surface's lit (fully-illuminated) albedo color. |
| `Pattern` | Float | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |

---

### Plugin: Line Hatching Pattern

**Menu:** `Add Shader > LSCherry > Plugin > Plugin: Line Hatching Pattern`


Inputs are grouped into collapsible panels in the N-panel: **Voronoi** — Voronoi Various to the pattern.

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Size` | Float | 1 | 0 – 9.9 | Size of the feature (dot, cell, highlight, …); larger values enlarge it. |
| `Location` | Float | 10 | -1000 – 10000 | Scalar value. |
| `Rotation` | Float | 0.4363 | -180 – 180 | Scalar value. |
| `Scale` | Float | 10 | 0 – 10000 | Scale of the pattern / texture — higher values tile it more densely. |
| `Flip Side` | Boolean | Off | — | Toggle for this option. |
| `Enable Light Blend` | Boolean | Off | — | When on, blends the effect with scene lighting. |
| `Toon Style` | Vector | (0, 0, 0) | -∞ – ∞ | Ramp-style vector selecting the toon band shaping (from a Ramp Style node). |
| `Voronoi Enable` | Boolean | On | — | Toggle for this option. |
| `Voronoi Scale` | Float | 6.1 | -1000 – 1000 | Scale of this feature. |
| `Voronoi Detail` | Float | 0 | 0 – 15 | Scalar value. |
| `Voronoi Roughness` | Float | 0.5 | 0–1 (factor) | Surface roughness for this term. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Pattern` | Float | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |

---

### Plugin: Painted 001 Pattern

**Menu:** `Add Shader > LSCherry > Plugin > Plugin: Painted 001 Pattern`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Base Color` | Color (RGBA) | (1, 0.0007897, 0.02145, 1) | — | The surface's lit (fully-illuminated) albedo color. |
| `Scale` | Float | 10 | 0 – 10000 | Scale of the pattern / texture — higher values tile it more densely. |
| `Seed` | Integer | 42 | 0 – 2147483647 | Random seed; change it to get a different variation of the procedural result. |
| `Deep Strength` | Float | 0.5 | 0–1 (factor) | Intensity of the deepest (SSS / core) shadow band. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Base Color` | Color (RGBA) | The surface's lit (fully-illuminated) albedo color. |
| `Pattern` | Float | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |

---

### Plugin: Painted 002 Pattern

**Menu:** `Add Shader > LSCherry > Plugin > Plugin: Painted 002 Pattern`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Base Color` | Color (RGBA) | (1, 0.0007897, 0.02145, 1) | — | The surface's lit (fully-illuminated) albedo color. |
| `Scale` | Float | 10 | 0 – 10000 | Scale of the pattern / texture — higher values tile it more densely. |
| `Seed` | Integer | 42 | 0 – 2147483647 | Random seed; change it to get a different variation of the procedural result. |
| `Deep Strength` | Float | 1 | 0–1 (factor) | Intensity of the deepest (SSS / core) shadow band. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Base Color` | Color (RGBA) | The surface's lit (fully-illuminated) albedo color. |
| `Pattern` | Float | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |

---

### Plugin: Painted 003 Pattern

**Menu:** `Add Shader > LSCherry > Plugin > Plugin: Painted 003 Pattern`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Base Color` | Color (RGBA) | (1, 0.0007897, 0.02145, 1) | — | The surface's lit (fully-illuminated) albedo color. |
| `Scale` | Float | 10 | 0 – 10000 | Scale of the pattern / texture — higher values tile it more densely. |
| `Seed` | Integer | 42 | 0 – 2147483647 | Random seed; change it to get a different variation of the procedural result. |
| `Deep Strength` | Float | 1 | 0–1 (factor) | Intensity of the deepest (SSS / core) shadow band. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Base Color` | Color (RGBA) | The surface's lit (fully-illuminated) albedo color. |
| `Pattern` | Float | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |

---

### Plugin: Painted 004 Pattern

**Menu:** `Add Shader > LSCherry > Plugin > Plugin: Painted 004 Pattern`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Base Color` | Color (RGBA) | (1, 0.0007897, 0.02145, 1) | — | The surface's lit (fully-illuminated) albedo color. |
| `Scale` | Float | 10 | 0 – 10000 | Scale of the pattern / texture — higher values tile it more densely. |
| `Seed` | Integer | 42 | 0 – 2147483647 | Random seed; change it to get a different variation of the procedural result. |
| `Deep Strength` | Float | 1 | 0–1 (factor) | Intensity of the deepest (SSS / core) shadow band. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Base Color` | Color (RGBA) | The surface's lit (fully-illuminated) albedo color. |
| `Pattern` | Float | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |

---

### Plugin: Painted 005 Pattern

**Menu:** `Add Shader > LSCherry > Plugin > Plugin: Painted 005 Pattern`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Base Color` | Color (RGBA) | (1, 0.0007897, 0.02145, 1) | — | The surface's lit (fully-illuminated) albedo color. |
| `Scale` | Float | 10 | 0 – 10000 | Scale of the pattern / texture — higher values tile it more densely. |
| `Seed` | Integer | 42 | 0 – 2147483647 | Random seed; change it to get a different variation of the procedural result. |
| `Deep Strength` | Float | 1 | 0–1 (factor) | Intensity of the deepest (SSS / core) shadow band. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Base Color` | Color (RGBA) | The surface's lit (fully-illuminated) albedo color. |
| `Pattern` | Float | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |

---

### Plugin: Painted 006 Pattern

**Menu:** `Add Shader > LSCherry > Plugin > Plugin: Painted 006 Pattern`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Base Color` | Color (RGBA) | (1, 0.0007897, 0.02145, 1) | — | The surface's lit (fully-illuminated) albedo color. |
| `Scale` | Float | 10 | 0 – 10000 | Scale of the pattern / texture — higher values tile it more densely. |
| `Seed` | Integer | 42 | 0 – 2147483647 | Random seed; change it to get a different variation of the procedural result. |
| `Deep Strength` | Float | 1 | 0–1 (factor) | Intensity of the deepest (SSS / core) shadow band. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Base Color` | Color (RGBA) | The surface's lit (fully-illuminated) albedo color. |
| `Pattern` | Float | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |

---

### Plugin: Scratch Pattern

**Menu:** `Add Shader > LSCherry > Plugin > Plugin: Scratch Pattern`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Scale` | Float | 1 | 0 – 10000 | Scale of the pattern / texture — higher values tile it more densely. |
| `Seed` | Integer | 42 | 0 – 2147483647 | Random seed; change it to get a different variation of the procedural result. |
| `Enable Light Blend` | Boolean | Off | — | When on, blends the effect with scene lighting. |
| `Toon Style` | Vector | (0, 0, 0) | -∞ – ∞ | Ramp-style vector selecting the toon band shaping (from a Ramp Style node). |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Pattern` | Float | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |

---

### Plugin: Smooth Metal

**Menu:** `Add Shader > LSCherry > Plugin > Plugin: Smooth Metal`


Inputs are grouped into collapsible panels in the N-panel: **Voronoi L1**; **Noise L2**; **Noise L3**.

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Scale` | Float | 1 | 0 – ∞ | Scale of the pattern / texture — higher values tile it more densely. |
| `Mix Various` | Float | 0.1 | 0–1 (factor) | Scalar value. |
| `Strength` | Float | 0.05 | 0–1 (factor) | Overall intensity of the effect. |
| `Increase Pattern Value` | Float | 2 | 0 – 2 | Scalar value. |
| `Scale` | Float | 0.1 | -1000 – 1000 | Scale of the pattern / texture — higher values tile it more densely. |
| `Detail` | Float | 10 | 0 – 15 | Procedural detail / number of noise octaves — higher adds finer structure. |
| `Roughness` | Float | 0.2 | 0–1 (factor) | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |
| `Lacunarity` | Float | 2 | 0 – 1000 | Frequency gap between procedural noise octaves. |
| `Randomness` | Float | 1 | 0–1 (factor) | Scalar value. |
| `W` | Float | 1 | -1000 – 1000 | Scalar value. |
| `Scale` | Float | 0.1 | -1000 – 1000 | Scale of the pattern / texture — higher values tile it more densely. |
| `Detail` | Float | 10 | 0 – 15 | Procedural detail / number of noise octaves — higher adds finer structure. |
| `Roughness` | Float | 0.45 | 0–1 (factor) | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |
| `Lacunarity` | Float | 2 | 0 – 1000 | Frequency gap between procedural noise octaves. |
| `Distortion` | Float | 0 | -1000 – 1000 | Amount of procedural distortion / warping applied. |
| `W` | Float | 1 | -1000 – 1000 | Scalar value. |
| `Scale` | Float | 0.05 | -1000 – 1000 | Scale of the pattern / texture — higher values tile it more densely. |
| `Detail` | Float | 10 | 0 – 15 | Procedural detail / number of noise octaves — higher adds finer structure. |
| `Roughness` | Float | 1 | 0–1 (factor) | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |
| `Lacunarity` | Float | 2 | 0 – 1000 | Frequency gap between procedural noise octaves. |
| `Distortion` | Float | 0 | -1000 – 1000 | Amount of procedural distortion / warping applied. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Pattern` | Float | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |
| `Normal` | Vector | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |

---

### Plugin: Watercolor 001 Pattern

**Menu:** `Add Shader > LSCherry > Plugin > Plugin: Watercolor 001 Pattern`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Base Color` | Color (RGBA) | (1, 0.0007897, 0.02145, 1) | — | The surface's lit (fully-illuminated) albedo color. |
| `Scale` | Float | 10 | 0 – 10000 | Scale of the pattern / texture — higher values tile it more densely. |
| `Seed` | Integer | 42 | 0 – 2147483647 | Random seed; change it to get a different variation of the procedural result. |
| `Deep Strength` | Float | 1 | 0–1 (factor) | Intensity of the deepest (SSS / core) shadow band. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Base Color` | Color (RGBA) | The surface's lit (fully-illuminated) albedo color. |
| `Pattern` | Float | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |

---

### Plugin: Watercolor 002 Pattern

**Menu:** `Add Shader > LSCherry > Plugin > Plugin: Watercolor 002 Pattern`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Base Color` | Color (RGBA) | (1, 0.0007897, 0.02145, 1) | — | The surface's lit (fully-illuminated) albedo color. |
| `Scale` | Float | 10 | 0 – 10000 | Scale of the pattern / texture — higher values tile it more densely. |
| `Seed` | Integer | 42 | 0 – 2147483647 | Random seed; change it to get a different variation of the procedural result. |
| `Deep Strength` | Float | 1 | 0–1 (factor) | Intensity of the deepest (SSS / core) shadow band. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Base Color` | Color (RGBA) | The surface's lit (fully-illuminated) albedo color. |
| `Pattern` | Float | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |

---

### Plugin: Watercolor 003 Pattern

**Menu:** `Add Shader > LSCherry > Plugin > Plugin: Watercolor 003 Pattern`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Base Color` | Color (RGBA) | (1, 0.0007897, 0.02145, 1) | — | The surface's lit (fully-illuminated) albedo color. |
| `Scale` | Float | 10 | 0 – 10000 | Scale of the pattern / texture — higher values tile it more densely. |
| `Seed` | Integer | 42 | 0 – 2147483647 | Random seed; change it to get a different variation of the procedural result. |
| `Deep Strength` | Float | 1 | 0–1 (factor) | Intensity of the deepest (SSS / core) shadow band. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Base Color` | Color (RGBA) | The surface's lit (fully-illuminated) albedo color. |
| `Pattern` | Float | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |
