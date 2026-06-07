# LSCherry — Utils

**Menu path:** `Add Shader > LSCherry > Utils (and the Procedural / Ramp Style / BNodes subgroups)`

> 63 node(s) in this category. Socket types, defaults and ranges below are extracted directly from the compiled node source — they are the ground truth.

The toolbox layer. Sub-groups: **BNodes** (boolean/logic + small math and attribute helpers), **Procedural** (face/nose ramps, skin detail `SST1:` set, pantyhose, fresnel, wave texture), **Ramp Style** (vectors that reshape toon/SSS/back ramps), **Separator** (lightmap channel splitting, number packing, PBR→toon conversion), and **Normal** helpers. These are wired *into* the bigger shaders rather than used stand-alone.

> Note: the Separator group ships with the folder name `seperator` and the Ramp Style and Separator nodes appear directly under **LSCherry > Utils** in the menu (see each node's *Menu* line for the exact path).

## When to use it

- Splitting a packed lightmap into its shadow / specular / AO channels.
- Driving anime face shadows from an SDF face map.
- Adding procedural skin detail (pores, freckles, moles, veins) via the `SST1:` nodes.
- Boolean/comparison logic to switch shader branches.

## How to use it

1. Pick the sub-group that matches your need (see each node's `Menu` line).
2. Most Separator nodes take a texture/color and emit several derived channels.
3. Ramp Style nodes output a style vector that plugs into the matching `* Style` input of `Make Toon` / `Toon3S`.

## Node reference

### ? Use Override

Chooses between a value and an override when the override is enabled.

**Menu:** `Add Shader > LSCherry > Utils > BNodes > ? Use Override`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Condition ` | Float | 0 | 0 – 1 | Scalar value. |
| `Color` | Color (RGBA) | (0.5, 0.5, 0.5, 1) | — | Color input/output for this operation. |
| `Override Color` | Color (RGBA) | (0, 0, 0, 1) | — | Color value for this slot. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Color` | Color (RGBA) | Color input/output for this operation. |

---

### A >= B

Comparison: outputs 1 when A is greater than or equal to B, else 0.

**Menu:** `Add Shader > LSCherry > Utils > BNodes > A >= B`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `A` | Float | 0.5 | -10000 – 10000 | First operand. |
| `B` | Float | 0.5 | -10000 – 10000 | Second operand. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Boolean` | Float | Scalar value. |

---

### AND

Logical AND of two boolean/0-1 inputs.

**Menu:** `Add Shader > LSCherry > Utils > BNodes > AND`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `A` | Float | 0 | 0 – 1 | First operand. |
| `B` | Float | 0 | 0 – 1 | Second operand. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `O` | Float | Output value of the logic / math operation. |

---

### Back Style

Outputs a style vector that reshapes the back-face ramp (plug into a `Back Style` input).

**Menu:** `Add Shader > LSCherry > Utils > Ramp Style > Back Style`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Disable Back Style` | Boolean | Off | — | Bypass the back-face ramp styling. |
| `Shading` | Float | 1 | -1 – 1 | Incoming shading/lighting term used by this node. |
| `Fresnel (Required)` | Float | 0 | -1 – 1 | Scalar value. |
| `Back Style` | Vector | (0, 0, 0) | -∞ – ∞ | Ramp-style vector selecting the back-face band shaping (from a Ramp Style node). |
| `Size` | Float | 0.9 | 0–1 (factor) | Size of the feature (dot, cell, highlight, …); larger values enlarge it. |
| `Smooth` | Float | 1 | 0–1 (factor) | Softness of the transition edge — 0 is a hard toon step, higher feathers it. |
| `Soft Shading Fac` | Float | 0.75 | 0–1 (factor) | Scalar value. |
| `Mix With Fresnel` | Float | 0.8 | 0–1 (factor) | Scalar value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shading` | Float | Incoming shading/lighting term used by this node. |
| `Back Style` | Vector | Ramp-style vector selecting the back-face band shaping (from a Ramp Style node). |

---

### Background Color

Provides a background/clear color.

**Menu:** `Add Shader > LSCherry > Utils > BNodes > Background Color`

**Inputs**

_None._


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Base` | Color (RGBA) | Color value. |
| `Stylized` | Color (RGBA) | Color value. |

---

### Blend Dark

Darken-style blend of two colors.

**Menu:** `Add Shader > LSCherry > Utils > BNodes > Blend Dark`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Factor` | Float | 1 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Mix Multiply And Blend` | Float | 1 | 0–1 (factor) | Scalar value. |
| `Base Color` | Color (RGBA) | (1, 1, 1, 1) | — | The surface's lit (fully-illuminated) albedo color. |
| `Blend Color` | Color (RGBA) | (0, 0, 0, 1) | — | Color value for this slot. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Blended Color` | Color (RGBA) | Color value for this slot. |

---

### Blend It

Generic blend helper.

**Menu:** `Add Shader > LSCherry > Utils > BNodes > Blend It`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Fac` | Float | 1 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Color A` | Color (RGBA) | (1, 1, 1, 1) | — | Color value for this slot. |
| `Color B` | Color (RGBA) | (1, 1, 1, 1) | — | Color value for this slot. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Color` | Color (RGBA) | Color input/output for this operation. |

---

### Blend Light

Lighten-style blend of two colors.

**Menu:** `Add Shader > LSCherry > Utils > BNodes > Blend Light`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Factor` | Float | 1 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Mix Add And Blend` | Float | 0 | 0–1 (factor) | Scalar value. |
| `Base Color` | Color (RGBA) | (1, 1, 1, 1) | — | The surface's lit (fully-illuminated) albedo color. |
| `Blend Color` | Color (RGBA) | (0, 0, 0, 1) | — | Color value for this slot. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Blended Color` | Color (RGBA) | Color value for this slot. |

---

### Build Face Normal

Generates the corrected face normal for soft anime face shading.

**Menu:** `Add Shader > LSCherry > Utils > Procedural > Build Face Normal`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Face Value` | Float | 0.5 | -10000 – 10000 | Face-shadow ramp coordinate, typically driven by the light direction vs. the face. |
| `Face Map` | Float | 0.5 | -10000 – 10000 | Face SDF / ramp map used to drive soft anime face shadows. |
| `Face To X` | Boolean | Off | — | Toggle for this option. |
| `Face To Y` | Boolean | Off | — | Toggle for this option. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Normal` | Vector | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |

---

### Build Face Ramp

Builds the face-shadow ramp from a face map.

**Menu:** `Add Shader > LSCherry > Utils > Procedural > Build Face Ramp`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Face Value` | Float | 0.5 | -10000 – 10000 | Face-shadow ramp coordinate, typically driven by the light direction vs. the face. |
| `Face Map` | Float | 0.5 | -10000 – 10000 | Face SDF / ramp map used to drive soft anime face shadows. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Custom Ramp` | Color (RGBA) | User-supplied ramp color that overrides the built-in toon ramp. |

---

### Build Nose Ramp

Builds the nose-shadow ramp.

**Menu:** `Add Shader > LSCherry > Utils > Procedural > Build Nose Ramp`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Face Ramp (Required)` | Color (RGBA) | (0, 0, 0, 1) | — | Color value. |
| `Face Value` | Float | 0.5 | -10000 – 10000 | Face-shadow ramp coordinate, typically driven by the light direction vs. the face. |
| `Face Map` | Float | 0.5 | -10000 – 10000 | Face SDF / ramp map used to drive soft anime face shadows. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shading` | Float | Incoming shading/lighting term used by this node. |

---

### Build Ramp From Map

Generates a toon color ramp from a packed ramp/map texture.

**Menu:** `Add Shader > LSCherry > Utils > Procedural > Build Ramp From Map`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Toon` | Float | 0 | -∞ – ∞ | Scalar value. |
| `Ramp Size` | Float | 0.5 | -10000 – 10000 | Width of the ramp transition region. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `UV` | Vector | UV texture coordinates used to sample maps for this node. |

---

### Color Selector

Selects/branches between colors.

**Menu:** `Add Shader > LSCherry > Utils > Color Selector`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Case Number` | Integer | 1 | 1 – 10 | Integer count. |
| `Color 1` | Color (RGBA) | (0, 0, 0, 1) | — | Color value for this slot. |
| `Color 2` | Color (RGBA) | (0, 0, 0, 1) | — | Color value for this slot. |
| `Color 3` | Color (RGBA) | (0, 0, 0, 1) | — | Color value for this slot. |
| `Color 4` | Color (RGBA) | (0, 0, 0, 1) | — | Color value for this slot. |
| `Color 5` | Color (RGBA) | (0, 0, 0, 1) | — | Color value for this slot. |
| `Color 6` | Color (RGBA) | (0, 0, 0, 1) | — | Color value for this slot. |
| `Color 7` | Color (RGBA) | (0, 0, 0, 1) | — | Color value for this slot. |
| `Color 8` | Color (RGBA) | (0, 0, 0, 1) | — | Color value for this slot. |
| `Color 9` | Color (RGBA) | (0, 0, 0, 1) | — | Color value for this slot. |
| `Color 10` | Color (RGBA) | (0, 0, 0, 1) | — | Color value for this slot. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Selected Color` | Color (RGBA) | Color value for this slot. |

---

### Combined To Shader

Converts a flat combined color back into a shader stream.

**Menu:** `Add Shader > LSCherry > Utils > Combined To Shader`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Combined` | Color (RGBA) | (0, 0, 0, 1) | — | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |
| `Alpha` | Float | 1 | 0–1 (factor) | Opacity (0 = fully transparent, 1 = fully opaque). |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shader` | Shader | Shader stream — connect the surface being processed (in) or pass it on (out). |
| `To AgX` | Shader | Shader stream. |

---

### Convert [0, 255] to [0,1]

Rescales 0–255 values into Blender's 0–1 range.

**Menu:** `Add Shader > LSCherry > Utils > Convert [0, 255] to [0,1]`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `[0, 255]` | Float | 0 | -10000 – 10000 | Scalar value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `[0, 1]` | Float | Scalar value. |

---

### Default Attribute: Alpha

Reads a named alpha attribute (with a fallback default).

**Menu:** `Add Shader > LSCherry > Utils > BNodes > Default Attribute: Alpha`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Alpha` | Float | 0 | -10000 – 10000 | Opacity (0 = fully transparent, 1 = fully opaque). |
| `Default` | Float | 0 | -10000 – 10000 | Scalar value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Result` | Float | Computed result of this node. |
| `Compare` | Float | Scalar value. |

---

### Default Attribute: Color

Reads a named color attribute (with a fallback default).

**Menu:** `Add Shader > LSCherry > Utils > BNodes > Default Attribute: Color`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Color` | Color (RGBA) | (0, 0, 0, 1) | — | Color input/output for this operation. |
| `Default` | Color (RGBA) | (1, 1, 1, 1) | — | Color value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Result` | Color (RGBA) | Computed result of this node. |
| `Compare` | Float | Scalar value. |

---

### Default Attribute: Fac

Reads a named factor attribute (with a fallback default).

**Menu:** `Add Shader > LSCherry > Utils > BNodes > Default Attribute: Fac`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Fac` | Float | 0 | -10000 – 10000 | Blend factor (0 = first/original input, 1 = full effect). |
| `Default` | Float | 0 | -10000 – 10000 | Scalar value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Result` | Float | Computed result of this node. |
| `Compare` | Float | Scalar value. |

---

### Default Attribute: Vector

Reads a named vector attribute (with a fallback default).

**Menu:** `Add Shader > LSCherry > Utils > BNodes > Default Attribute: Vector`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Vector` | Vector | (0, 0, 0) | -∞ – ∞ | Vector value. |
| `Default` | Vector | (0, 0, 0) | -∞ – ∞ | Vector value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Result` | Vector | Computed result of this node. |
| `Compare` | Float | Scalar value. |

---

### Face Normal Builder

Lower-level face-normal construction used by the face shaders.

**Menu:** `Add Shader > LSCherry > Utils > Procedural > Face Normal Builder`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `UV` | Vector | (0, 0, 0) | -∞ – ∞ | UV texture coordinates used to sample maps for this node. |
| `Min Dot Value` | Float | -0.5 | -1 – 1 | Scalar value. |
| `Max  Dot Value` | Float | 0.5 | -1 – 1 | Scalar value. |
| `Default UV` | Float | -1 | -1 – 1 | UV coordinates. |
| `Flip UV` | Float | 1 | -1 – 1 | UV coordinates. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Face Value` | Float | Face-shadow ramp coordinate, typically driven by the light direction vs. the face. |
| `Face OS-Vector` | Vector | Vector value. |
| `Face To X` | Boolean | Toggle for this option. |
| `Face To Y` | Boolean | Toggle for this option. |

---

### Face Ramp Builder

Lower-level face-ramp construction.

**Menu:** `Add Shader > LSCherry > Utils > Procedural > Face Ramp Builder`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `UV` | Vector | (0, 0, 0) | -∞ – ∞ | UV texture coordinates used to sample maps for this node. |
| `Min Dot Value` | Float | -0.5 | -1 – 1 | Scalar value. |
| `Max  Dot Value` | Float | 0.5 | -1 – 1 | Scalar value. |
| `Default UV` | Float | -1 | -1 – 1 | UV coordinates. |
| `Flip UV` | Float | 1 | -1 – 1 | UV coordinates. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Face Value` | Float | Face-shadow ramp coordinate, typically driven by the light direction vs. the face. |
| `Face GS-Vector` | Vector | Vector value. |

---

### Faceramp Vector Provider

Provides the vector that drives the face-shadow ramp lookup.

**Menu:** `Add Shader > LSCherry > Utils > Procedural > Faceramp Vector Provider`

**Inputs**

_None._


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Fx` | Vector | Vector value. |
| `Fy` | Vector | Vector value. |
| `X(-1, 0, 0)` | Vector | Vector value. |
| `X(1, 0, 0)` | Vector | Vector value. |

---

### FROM A TO B

Remaps a value from one range into another.

**Menu:** `Add Shader > LSCherry > Utils > BNodes > FROM A TO B`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `A` | Float | 0.5 | -10000 – 10000 | First operand. |
| `B` | Float | 0.5 | -10000 – 10000 | Second operand. |
| `Input` | Float | 0.5 | -10000 – 10000 | Scalar value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Boolean` | Float | Scalar value. |

---

### Limit Color Value

Clamps a color's value/brightness within limits.

**Menu:** `Add Shader > LSCherry > Utils > BNodes > Limit Color Value`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Target Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color value for this slot. |
| `Limit Color` | Color (RGBA) | (0, 0, 0, 1) | — | Color value for this slot. |
| `Limit Value` | Float | 0.89 | 0 – 1 | Scalar value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Limited Color` | Color (RGBA) | Color value for this slot. |

---

### Metal Ramp

Procedural metal banding ramp.

**Menu:** `Add Shader > LSCherry > Utils > Procedural > Metal Ramp`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Mix 1` | Float | 0.7 | 0 – 1 | Scalar value. |
| `Mix 2` | Float | 0.85 | 0 – 1 | Scalar value. |
| `Mix 3` | Float | 0.95 | 0 – 1 | Scalar value. |
| `Lv 1` | Color (RGBA) | (0, 0, 0, 1) | — | Color value. |
| `Lv 2` | Color (RGBA) | (0.02479, 0.02479, 0.02479, 1) | — | Color value. |
| `Lv 3` | Color (RGBA) | (0.1235, 0.1235, 0.1235, 1) | — | Color value. |
| `Lv 4` | Color (RGBA) | (1, 1, 1, 1) | — | Color value. |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Custom Ramp` | Color (RGBA) | User-supplied ramp color that overrides the built-in toon ramp. |

---

### Mix Transparent VFX

Mixes a transparent VFX layer into a surface.

**Menu:** `Add Shader > LSCherry > Utils > Procedural > Mix Transparent VFX`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Fac` | Float | 2.98e-08 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Shader` | Shader | — | — | Shader stream — connect the surface being processed (in) or pass it on (out). |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Mask` | Shader | Mask isolating a region (0–1). |

---

### NAND

Logical NAND (NOT AND) of two inputs.

**Menu:** `Add Shader > LSCherry > Utils > BNodes > NAND`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `A` | Float | 0 | 0 – 1 | First operand. |
| `B` | Float | 0 | 0 – 1 | Second operand. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `O` | Float | Output value of the logic / math operation. |

---

### NOR

Logical NOR (NOT OR) of two inputs.

**Menu:** `Add Shader > LSCherry > Utils > BNodes > NOR`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `A` | Float | 0 | 0–1 (factor) | First operand. |
| `B` | Float | 0 | 0–1 (factor) | Second operand. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `NOR` | Float | Scalar value. |

---

### Nose Ramp Builder

Lower-level nose-ramp construction.

**Menu:** `Add Shader > LSCherry > Utils > Procedural > Nose Ramp Builder`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `UV` | Vector | (0, 0, 0) | -∞ – ∞ | UV texture coordinates used to sample maps for this node. |
| `Min Dot Value` | Float | 0 | -1 – 1 | Scalar value. |
| `Max  Dot Value` | Float | 1 | -1 – 1 | Scalar value. |
| `Default UV` | Float | -1 | -1 – 1 | UV coordinates. |
| `Flip UV` | Float | 1 | -1 – 1 | UV coordinates. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Face Value` | Float | Face-shadow ramp coordinate, typically driven by the light direction vs. the face. |
| `Face Vector` | Vector | Vector value. |

---

### NOT

Logical NOT — inverts a boolean/0-1 input.

**Menu:** `Add Shader > LSCherry > Utils > BNodes > NOT`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `A` | Float | 0 | 0 – 1 | First operand. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `O` | Float | Output value of the logic / math operation. |

---

### Number Compress

Packs several numbers into one value.

**Menu:** `Add Shader > LSCherry > Utils > Number Compress`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `MAX 2 SEQUENCES` | Shader | — | — | Shader stream. |
| `Sequence 1` | Float | 0.5 | -10000 – 10000 | Scalar value. |
| `Sequence 2` | Float | 1000 | -10000 – 10000 | Scalar value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Compressed` | Float | Scalar value. |

---

### Number Extract

Extracts a packed number back out.

**Menu:** `Add Shader > LSCherry > Utils > Number Extract`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Compressed` | Float | 0.5 | -10000 – 10000 | Scalar value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Compressed` | Float | Scalar value. |
| `Extracted` | Float | Scalar value. |

---

### Number To Sequence

Expands a number into a sequence of values.

**Menu:** `Add Shader > LSCherry > Utils > Number To Sequence`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Number` | Float | 0.5 | -10000 – 10000 | Scalar value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Sequence` | Float | Scalar value. |

---

### OR

Logical OR of two inputs.

**Menu:** `Add Shader > LSCherry > Utils > BNodes > OR`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `A` | Float | 0 | 0–1 (factor) | First operand. |
| `B` | Float | 0 | 0–1 (factor) | Second operand. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `O` | Float | Output value of the logic / math operation. |

---

### Rim Metal Ramp

Metal ramp variant tuned for rim/edge response.

**Menu:** `Add Shader > LSCherry > Utils > Procedural > Rim Metal Ramp`


Inputs are grouped into collapsible panels in the N-panel: **Metal**.

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Roughness` | Float | 0.1 | -100 – 100 | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |
| `Mix 1` | Float | 0.7 | 0 – 1 | Scalar value. |
| `Mix 2` | Float | 0.85 | 0 – 1 | Scalar value. |
| `Mix 3` | Float | 0.95 | 0 – 1 | Scalar value. |
| `Lv 1` | Color (RGBA) | (0, 0, 0, 1) | — | Color value. |
| `Lv 2` | Color (RGBA) | (0.02479, 0.02479, 0.02479, 1) | — | Color value. |
| `Lv 3` | Color (RGBA) | (0.1235, 0.1235, 0.1235, 1) | — | Color value. |
| `Lv 4` | Color (RGBA) | (1, 1, 1, 1) | — | Color value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Metal Ramp` | Color (RGBA) | Color value. |

---

### Seperate Lightmap

Splits a packed lightmap into its individual channels (shadow / spec / AO / …).

**Menu:** `Add Shader > LSCherry > Utils > Seperate Lightmap`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Lightmap` | Color (RGBA) | (1, 1, 1, 1) | — | Packed lightmap texture whose channels encode shadow, specular, AO, etc. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Metal` | Float | Metalness factor — blends the surface toward a reflective metal look. |
| `Diffuse` | Float | Scalar value. |
| `Highlight` | Float | Scalar value. |

---

### Set Color From LightMap

Assigns colors based on lightmap channel values.

**Menu:** `Add Shader > LSCherry > Utils > Set Color From LightMap`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Lighmap Alpha` | Float | 0 | 0 – 1 | Alpha channel of the lightmap, commonly used as a shadow/AO factor. |
| `Map 0` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 1` | Color (RGBA) | (0.5, 0.5, 0.5, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 2` | Color (RGBA) | (0.5, 0.5, 0.5, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 3` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 4` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 5` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Range 1` | Float | 0.125 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 2` | Float | 0.25 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 3` | Float | 0.375 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 4` | Float | 0.62 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Color Map` | Color (RGBA) | Color value for this slot. |

---

### Simple Pantyhose Type 1

Procedural pantyhose pattern, style 1.

**Menu:** `Add Shader > LSCherry > Utils > Procedural > Simple Pantyhose Type 1`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `UV` | Vector | (0, 0, 0) | -∞ – ∞ | UV texture coordinates used to sample maps for this node. |
| `Combined` | Color (RGBA) | (1, 1, 1, 1) | — | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |
| `Color` | Color (RGBA) | (0.5, 0.5, 0.5, 1) | — | Color input/output for this operation. |
| `Factor` | Float | 1 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Scale` | Float | 50 | 0 – 1000 | Scale of the pattern / texture — higher values tile it more densely. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Combined` | Color (RGBA) | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |
| `Pattern` | Float | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |

---

### Simple Pantyhose Type 2

Procedural pantyhose pattern, style 2.

**Menu:** `Add Shader > LSCherry > Utils > Procedural > Simple Pantyhose Type 2`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Enable Dot` | Boolean | Off | — | Toggle for this option. |
| `UV` | Vector | (0, 0, 0) | -∞ – ∞ | UV texture coordinates used to sample maps for this node. |
| `Color` | Color (RGBA) | (0.6858, 0.6858, 0.6858, 1) | — | Color input/output for this operation. |
| `Highlight Color` | Color (RGBA) | (1, 0.6242, 0.5514, 1) | — | Color value for this slot. |
| `Size` | Float | 8 | 1 – 100 | Size of the feature (dot, cell, highlight, …); larger values enlarge it. |
| `Roughness` | Float | 0.2 | 0–1 (factor) | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Color` | Color (RGBA) | Color input/output for this operation. |
| `Pattern` | Float | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |
| `Normal` | Vector | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |

---

### Simple Skin Type 1

Procedural skin base, style 1 (foundation for the SST1 detail set).

**Menu:** `Add Shader > LSCherry > Utils > Procedural > Simple Skin Type 1`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Skin Color` | Color (RGBA) | (0.95, 0.6191, 0.5205, 1) | — | Color value for this slot. |
| `UV` | Vector | (0, 0, 0) | -∞ – ∞ | UV texture coordinates used to sample maps for this node. |
| `-- Blemishes --` | Shader | — | — | Shader stream. |
| `Red Color` | Color (RGBA) | (0.9, 0.1926, 0.1357, 1) | — | Tint for the red lightmap/mask channel. |
| `Blue Color` | Color (RGBA) | (0.3673, 0.248, 0.9, 1) | — | Color value for this slot. |
| `Size` | Float | 1.1 | 0 – 100 | Size of the feature (dot, cell, highlight, …); larger values enlarge it. |
| `Strength` | Float | 1 | 0 – 100 | Overall intensity of the effect. |
| `-- Red Spots --` | Shader | — | — | Shader stream. |
| `Red Spots Red Color` | Color (RGBA) | (0.8, 0.1712, 0.1206, 1) | — | Color value for this slot. |
| `Scale` | Float | 1 | 0 – 100 | Scale of the pattern / texture — higher values tile it more densely. |
| `Strength` | Float | 1 | 0 – 100 | Overall intensity of the effect. |
| `-- Veins --` | Shader | — | — | Shader stream. |
| `Blue Color` | Color (RGBA) | (0.3557, 0.08279, 0.8, 1) | — | Color value for this slot. |
| `Scale` | Float | 1 | 0 – 100 | Scale of the pattern / texture — higher values tile it more densely. |
| `Mask Scale` | Float | 7 | 0 – 100 | Scale of this feature. |
| `Strength` | Float | 1 | 0 – 100 | Overall intensity of the effect. |
| `-- Moles --` | Shader | — | — | Shader stream. |
| `Red Color` | Color (RGBA) | (0.8, 0.3501, 0.2015, 1) | — | Tint for the red lightmap/mask channel. |
| `Scale` | Float | 75 | 0 – 1000 | Scale of the pattern / texture — higher values tile it more densely. |
| `Threadhold` | Integer | 0 | 0 – 1000 | Integer count. |
| `-- Freckles --` | Shader | — | — | Shader stream. |
| `Factor` | Float | 0 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Red Color` | Color (RGBA) | (0.8, 0.3501, 0.2015, 1) | — | Tint for the red lightmap/mask channel. |
| `Intensity` | Float | 0.5 | 0–1 (factor) | Scalar value. |
| `Scale` | Float | 1 | 0 – 1000 | Scale of the pattern / texture — higher values tile it more densely. |
| `Scale Small` | Float | 2000 | 0 – 1000 | Scale of this feature. |
| `Scale Big` | Float | 1100 | 0 – 1000 | Scale of this feature. |
| `-- Pores --` | Shader | — | — | Shader stream. |
| `Factor` | Float | 0 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Scale` | Float | 1.5 | 0 – 1000 | Scale of the pattern / texture — higher values tile it more densely. |
| `Dirt Color` | Color (RGBA) | (0.05, 0.01832, 0.005012, 1) | — | Color value for this slot. |
| `Dirt Strength` | Float | 0.25 | 0 – 1 | Intensity of this contribution. |
| `-- Skin Bump --` | Shader | — | — | Shader stream. |
| `Goose Bumps` | Float | 0 | 0–1 (factor) | Scalar value. |
| `Details` | Float | 0.3 | 0–1 (factor) | Scalar value. |
| `Skin Scale` | Float | 9 | 0 – 1000 | Scale of this feature. |
| `Noise Scale` | Float | 50 | 0 – 1000 | Scale of this feature. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Color` | Color (RGBA) | Color input/output for this operation. |
| `Normal` | Vector | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |

---

### SSS Harden

Hardens (sharpens) the SSS band transition.

**Menu:** `Add Shader > LSCherry > Utils > Ramp Style > SSS Harden`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Shading` | Float | 0 | -∞ – ∞ | Incoming shading/lighting term used by this node. |
| `Size` | Float | 0.9 | 0 – 1 | Size of the feature (dot, cell, highlight, …); larger values enlarge it. |
| `Smooth` | Float | 0.15 | 0 – 1 | Softness of the transition edge — 0 is a hard toon step, higher feathers it. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shading` | Float | Incoming shading/lighting term used by this node. |

---

### SSS Style

Outputs a style vector that reshapes the SSS ramp.

**Menu:** `Add Shader > LSCherry > Utils > Ramp Style > SSS Style`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Disable SSS Style` | Boolean | Off | — | Bypass the SSS ramp styling. |
| `Shading` | Float | 1 | -1 – 1 | Incoming shading/lighting term used by this node. |
| `Toon Style (If only using Toon Style)` | Vector | (0, 0, 0) | -∞ – ∞ | Vector value. |
| `SSS Style` | Vector | (0, 0, 0) | -∞ – ∞ | Ramp-style vector selecting the SSS band shaping (from a Ramp Style node). |
| `Smooth` | Float | 0.15 | 0–1 (factor) | Softness of the transition edge — 0 is a hard toon step, higher feathers it. |
| `SSS Intensity` | Float | 5 | 0–15 (factor) | Scalar value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shading` | Float | Incoming shading/lighting term used by this node. |
| `SSS Style` | Vector | Ramp-style vector selecting the SSS band shaping (from a Ramp Style node). |

---

### SST1: Blemishes

Skin detail: procedural blemishes.

**Menu:** `Add Shader > LSCherry > Utils > Procedural > SST1: Blemishes`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Builder` | Color (RGBA) | (1, 1, 1, 1) | — | Aggregated build bundle passed between starter/builder nodes. |
| `Red Color` | Color (RGBA) | (0.9, 0.1926, 0.1357, 1) | — | Tint for the red lightmap/mask channel. |
| `Blue Color` | Color (RGBA) | (0.3673, 0.248, 0.9, 1) | — | Color value for this slot. |
| `Size` | Float | 1.1 | 0 – 100 | Size of the feature (dot, cell, highlight, …); larger values enlarge it. |
| `Strength` | Float | 1 | 0 – 100 | Overall intensity of the effect. |
| `UV` | Vector | (0, 0, 0) | -∞ – ∞ | UV texture coordinates used to sample maps for this node. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Builder` | Color (RGBA) | Aggregated build bundle passed between starter/builder nodes. |
| `UV` | Vector | UV texture coordinates used to sample maps for this node. |

---

### SST1: Build

Skin detail: assembles the selected SST1 detail layers.

**Menu:** `Add Shader > LSCherry > Utils > Procedural > SST1: Build`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Color` | Color (RGBA) | (0.8, 0.8, 0.8, 1) | — | Color input/output for this operation. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Color` | Color (RGBA) | Color input/output for this operation. |

---

### SST1: Builder

Skin detail: builder/entry point for the SST1 skin system.

**Menu:** `Add Shader > LSCherry > Utils > Procedural > SST1: Builder`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Skin Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color value for this slot. |
| `UV` | Vector | (0, 0, 0) | -∞ – ∞ | UV texture coordinates used to sample maps for this node. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Builder` | Color (RGBA) | Aggregated build bundle passed between starter/builder nodes. |
| `UV` | Vector | UV texture coordinates used to sample maps for this node. |

---

### SST1: Freckles

Skin detail: procedural freckles.

**Menu:** `Add Shader > LSCherry > Utils > Procedural > SST1: Freckles`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Builder` | Color (RGBA) | (1, 1, 1, 1) | — | Aggregated build bundle passed between starter/builder nodes. |
| `Factor` | Float | 1 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Red Color` | Color (RGBA) | (0.8, 0.3501, 0.2015, 1) | — | Tint for the red lightmap/mask channel. |
| `Intensity` | Float | 0.5 | 0–1 (factor) | Scalar value. |
| `Scale` | Float | 1 | 0 – 1000 | Scale of the pattern / texture — higher values tile it more densely. |
| `Scale Small` | Float | 2000 | 0 – 1000 | Scale of this feature. |
| `Scale Big` | Float | 1100 | 0 – 1000 | Scale of this feature. |
| `UV` | Vector | (0, 0, 0) | -∞ – ∞ | UV texture coordinates used to sample maps for this node. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Builder` | Color (RGBA) | Aggregated build bundle passed between starter/builder nodes. |
| `UV` | Vector | UV texture coordinates used to sample maps for this node. |

---

### SST1: Moles

Skin detail: procedural moles.

**Menu:** `Add Shader > LSCherry > Utils > Procedural > SST1: Moles`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Builder` | Color (RGBA) | (1, 1, 1, 1) | — | Aggregated build bundle passed between starter/builder nodes. |
| `Red Color` | Color (RGBA) | (0.8, 0.3501, 0.2015, 1) | — | Tint for the red lightmap/mask channel. |
| `Scale` | Float | 75 | 0 – 1000 | Scale of the pattern / texture — higher values tile it more densely. |
| `Threadhold` | Integer | 0 | 0 – 1000 | Integer count. |
| `UV` | Vector | (0, 0, 0) | -∞ – ∞ | UV texture coordinates used to sample maps for this node. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Builder` | Color (RGBA) | Aggregated build bundle passed between starter/builder nodes. |
| `UV` | Vector | UV texture coordinates used to sample maps for this node. |

---

### SST1: Pores

Skin detail: procedural pores.

**Menu:** `Add Shader > LSCherry > Utils > Procedural > SST1: Pores`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Factor` | Float | 0 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Scale` | Float | 1.5 | 0 – 1000 | Scale of the pattern / texture — higher values tile it more densely. |
| `UV` | Vector | (0, 0, 0) | -∞ – ∞ | UV texture coordinates used to sample maps for this node. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Pores` | Color (RGBA) | Color value. |
| `UV` | Vector | UV texture coordinates used to sample maps for this node. |

---

### SST1: Pores Dirt

Skin detail: procedural pore dirt/grime.

**Menu:** `Add Shader > LSCherry > Utils > Procedural > SST1: Pores Dirt`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Builder` | Color (RGBA) | (1, 1, 1, 1) | — | Aggregated build bundle passed between starter/builder nodes. |
| `Pores (require)` | Color (RGBA) | (1, 1, 1, 1) | — | Color value. |
| `Dirt Color` | Color (RGBA) | (0.05, 0.01832, 0.005012, 1) | — | Color value for this slot. |
| `Dirt Strength` | Float | 0.25 | 0 – 1 | Intensity of this contribution. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Builder` | Color (RGBA) | Aggregated build bundle passed between starter/builder nodes. |

---

### SST1: Red Spots

Skin detail: procedural red spots/irritation.

**Menu:** `Add Shader > LSCherry > Utils > Procedural > SST1: Red Spots`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Builder` | Color (RGBA) | (1, 1, 1, 1) | — | Aggregated build bundle passed between starter/builder nodes. |
| `Red Color` | Color (RGBA) | (0.8, 0.1712, 0.1206, 1) | — | Tint for the red lightmap/mask channel. |
| `Scale` | Float | 1 | 0 – 100 | Scale of the pattern / texture — higher values tile it more densely. |
| `Strength` | Float | 1 | 0 – 100 | Overall intensity of the effect. |
| `UV` | Vector | (0, 0, 0) | -∞ – ∞ | UV texture coordinates used to sample maps for this node. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Builder` | Color (RGBA) | Aggregated build bundle passed between starter/builder nodes. |
| `UV` | Vector | UV texture coordinates used to sample maps for this node. |

---

### SST1: Skin Bump

Skin detail: procedural skin bump/normal detail.

**Menu:** `Add Shader > LSCherry > Utils > Procedural > SST1: Skin Bump`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Pores (require)` | Color (RGBA) | (0, 0, 0, 1) | — | Color value. |
| `Goose Bumps` | Float | 0 | 0–1 (factor) | Scalar value. |
| `Details` | Float | 0.3 | 0–1 (factor) | Scalar value. |
| `Skin Scale` | Float | 9 | 0 – 1000 | Scale of this feature. |
| `Noise Scale` | Float | 50 | 0 – 1000 | Scale of this feature. |
| `UV` | Vector | (0, 0, 0) | -∞ – ∞ | UV texture coordinates used to sample maps for this node. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Normal` | Vector | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |

---

### SST1: Veins

Skin detail: procedural subdermal veins.

**Menu:** `Add Shader > LSCherry > Utils > Procedural > SST1: Veins`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Builder` | Color (RGBA) | (1, 1, 1, 1) | — | Aggregated build bundle passed between starter/builder nodes. |
| `Blue Color` | Color (RGBA) | (0.3557, 0.08279, 0.8, 1) | — | Color value for this slot. |
| `Scale` | Float | 1 | 0 – 100 | Scale of the pattern / texture — higher values tile it more densely. |
| `Mask Scale` | Float | 7 | 0 – 100 | Scale of this feature. |
| `Strength` | Float | 1 | 0 – 100 | Overall intensity of the effect. |
| `UV` | Vector | (0, 0, 0) | -∞ – ∞ | UV texture coordinates used to sample maps for this node. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Builder` | Color (RGBA) | Aggregated build bundle passed between starter/builder nodes. |
| `UV` | Vector | UV texture coordinates used to sample maps for this node. |

---

### Stylized Fresnel

Stylised fresnel/rim term for edge lighting.

**Menu:** `Add Shader > LSCherry > Utils > Procedural > Stylized Fresnel`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Roughness` | Float | 0 | 0 – 1 | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Fresnel` | Float | Scalar value. |

---

### To Oxy

Converts to the OXY channel layout used downstream.

**Menu:** `Add Shader > LSCherry > Utils > To Oxy`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Oxyz` | Vector | (0, 0, 0) | -10000 – 10000 | Vector value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Oxy` | Vector | Vector value. |

---

### Toon Harden

Hardens (sharpens) the toon band transition.

**Menu:** `Add Shader > LSCherry > Utils > Ramp Style > Toon Harden`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Shading` | Float | 0 | -∞ – ∞ | Incoming shading/lighting term used by this node. |
| `Size` | Float | 0.9 | 0 – 0.999 | Size of the feature (dot, cell, highlight, …); larger values enlarge it. |
| `Smooth` | Float | 0.15 | 0 – 1 | Softness of the transition edge — 0 is a hard toon step, higher feathers it. |
| `White Level` | Float | 1 | 0 – 1 | Scalar value. |
| `Soft Shading Fac` | Float | 1 | 0–1 (factor) | Scalar value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shading` | Float | Incoming shading/lighting term used by this node. |

---

### Toon Style

Outputs a style vector that reshapes the toon ramp.

**Menu:** `Add Shader > LSCherry > Utils > Ramp Style > Toon Style`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Disable Toon Style` | Boolean | Off | — | Bypass the toon ramp styling. |
| `Shading` | Float | 1 | -1 – 1 | Incoming shading/lighting term used by this node. |
| `Fresnel (Required)` | Float | 0 | -1 – 1 | Scalar value. |
| `Toon Style` | Vector | (0, 0, 0) | -∞ – ∞ | Ramp-style vector selecting the toon band shaping (from a Ramp Style node). |
| `Size` | Float | 1 | 0–1 (factor) | Size of the feature (dot, cell, highlight, …); larger values enlarge it. |
| `Smooth` | Float | 0.1 | 0–1 (factor) | Softness of the transition edge — 0 is a hard toon step, higher feathers it. |
| `Soft Shading Fac` | Float | 0 | 0–1 (factor) | Scalar value. |
| `Mix With Fresnel` | Float | 0 | 0–1 (factor) | Scalar value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shading` | Float | Incoming shading/lighting term used by this node. |
| `Toon Style` | Vector | Ramp-style vector selecting the toon band shaping (from a Ramp Style node). |

---

### Toonify PBR Colors

Converts PBR base colors into toon-friendly stepped colors.

**Menu:** `Add Shader > LSCherry > Utils > Toonify PBR Colors`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Color` | Color (RGBA) | (0.8, 0.8, 0.8, 1) | — | Color input/output for this operation. |
| `Saturation` | Float | 0.85 | 0 – 2 | Scalar value. |
| `Gamma` | Float | 0.75 | 0.001 – 10 | Scalar value. |
| `Bright` | Float | 0.1 | -100 – 100 | Scalar value. |
| `Contrast` | Float | 0.15 | -100 – 100 | Scalar value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Color` | Color (RGBA) | Color input/output for this operation. |

---

### Use Default Normal

Falls back to the geometry normal when no normal map is supplied.

**Menu:** `Add Shader > LSCherry > Utils > Normal > Use Default Normal`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Normal` | Vector | (0, 0, 0) | -10000 – 10000 | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Normal` | Vector | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |

---

### Value Enhance

Boosts value/contrast of an input.

**Menu:** `Add Shader > LSCherry > Utils > BNodes > Value Enhance`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Shading` | Float | 1 | -10000 – 10000 | Incoming shading/lighting term used by this node. |
| `Value Enhance` | Float | 0.1 | 0–1 (factor) | Boosts the value/contrast of the result. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Enhanced Shading` | Float | Scalar value. |

---

### World Color

Exposes the world/ambient color.

**Menu:** `Add Shader > LSCherry > Utils > BNodes > World Color`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color input/output for this operation. |
| `Strength` | Float | 0 | 0 – ∞ | Overall intensity of the effect. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `WorldColor` | Color (RGBA) | Color value for this slot. |

---

### XNOR

Logical XNOR (equality) of two inputs.

**Menu:** `Add Shader > LSCherry > Utils > BNodes > XNOR`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `A` | Float | 0 | 0 – 1 | First operand. |
| `B` | Float | 0 | 0 – 1 | Second operand. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `O` | Float | Output value of the logic / math operation. |

---

### XOR

Logical XOR (difference) of two inputs.

**Menu:** `Add Shader > LSCherry > Utils > BNodes > XOR`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `A` | Float | 0 | 0 – 1 | First operand. |
| `B` | Float | 0 | 0 – 1 | Second operand. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `O` | Float | Output value of the logic / math operation. |

---

### XY Wave Texture

Procedural XY wave texture for ripples/stripes.

**Menu:** `Add Shader > LSCherry > Utils > Procedural > XY Wave Texture`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Scale` | Float | 25 | 0 – 1000000015047466219876688855040 | Scale of the pattern / texture — higher values tile it more densely. |
| `Distortion` | Float | 0 | -1000 – 1000 | Amount of procedural distortion / warping applied. |
| `Detail` | Float | 2 | 0 – 15 | Procedural detail / number of noise octaves — higher adds finer structure. |
| `Detail Scale` | Float | 1 | -1000 – 1000 | Scale of this feature. |
| `Detail Roughness` | Float | 0.5 | 0–1 (factor) | Surface roughness for this term. |
| `Phase Offset` | Float | 0 | -1000 – 1000 | Positional offset applied to this term. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Factor X` | Float | Blend factor (0–1). |
| `Factor Y` | Float | Blend factor (0–1). |
