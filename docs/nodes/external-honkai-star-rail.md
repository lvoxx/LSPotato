# LSCherry — External / Michos / Honkai Star Rail

**Menu path:** `Add Shader > LSCherry > External > Michos > Honkai Star Rail`

> 12 node(s) in this category. Socket types, defaults and ranges below are extracted directly from the compiled node source — they are the ground truth.

Michos's Honkai Star Rail (`HSR:`) shader set. Same architecture as the Genshin/HI3 sets: `Build * Package` per-part entry points plus the lower-level `Seperate *` / `* From Lightmap/Colormap` building blocks, including an outline-from-lightmap node.

## When to use it

- Shading ripped Honkai Star Rail characters with game-accurate toon ramps.
- Hand-wiring a custom HSR material from the per-stage nodes.

## How to use it

1. Start with `Build Head/Body/Hair Package` for the part.
2. Feed the part's colormap / lightmap / ramp textures into the matching inputs.

## Node reference

### HSR: Add Color From Colormap

Applies base colors from the Honkai Star Rail colormap.

**Menu:** `Add Shader > LSCherry > External > Michos > Honkai Star Rail > HSR: Add Color From Colormap`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Original Color` | Color (RGBA) | (1, 1, 1, 1) | — | The unmodified input color, passed through for reference or re-mixing. |
| `Factor` | Float | 0 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Bright Mask` | Float | 0 | 0–1 (factor) | Mask isolating a region (0–1). |
| `Bright Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color injected into the brightest / lit area. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Color` | Color (RGBA) | Color input/output for this operation. |

---

### HSR: Add Outline From Lightmap

Adds an outline whose tint is driven by the Honkai Star Rail lightmap.

**Menu:** `Add Shader > LSCherry > External > Michos > Honkai Star Rail > HSR: Add Outline From Lightmap`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Lighmap Alpha` | Float | 0 | 0 – 1 | Alpha channel of the lightmap, commonly used as a shadow/AO factor. |
| `Map 1` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 2` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 3` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 4` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Range 1` | Float | 0.1 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 2` | Float | 0.3 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 3` | Float | 0.45 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Outline` | Shader | Shader stream. |

---

### HSR: Add Shadow From Lightmap

Adds shadow shading driven by the Honkai Star Rail lightmap.

**Menu:** `Add Shader > LSCherry > External > Michos > Honkai Star Rail > HSR: Add Shadow From Lightmap`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Original Color` | Color (RGBA) | (1, 1, 1, 1) | — | The unmodified input color, passed through for reference or re-mixing. |
| `Factor` | Float | 0 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Shadow` | Float | 0 | 0–1 (factor) | Shadow term/mask consumed or produced by this node. |
| `Shadow Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color used in the shadow / shaded band of the toon step. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Color` | Color (RGBA) | Color input/output for this operation. |

---

### HSR: Body Color From Lightmap

Derives body base color using the Honkai Star Rail lightmap.

**Menu:** `Add Shader > LSCherry > External > Michos > Honkai Star Rail > HSR: Body Color From Lightmap`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Lighmap Alpha` | Float | 0 | 0 – 1 | Alpha channel of the lightmap, commonly used as a shadow/AO factor. |
| `Map 0` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 1` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 2` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 3` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 4` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 5` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Range 1` | Float | 0.1 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 2` | Float | 0.3 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 3` | Float | 0.45 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 4` | Float | 0.62 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Color Map` | Color (RGBA) | Color value for this slot. |

---

### HSR: Build Body Package

One-click body starting shader for a Honkai Star Rail character — wires the standard textures and ramps for that part.

**Menu:** `Add Shader > LSCherry > External > Michos > Honkai Star Rail > HSR: Build Body Package`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Body Texture` | Color (RGBA) | (1, 1, 1, 1) | — | Color value. |
| `Body Alpha` | Float | 0 | -∞ – ∞ | Opacity of the body material region. |
| `Lightmap Texture` | Color (RGBA) | (1, 1, 1, 1) | — | Packed lightmap texture whose channels encode shadow, specular, AO, etc. |
| `Lighmap  Alpha Texture` | Float | 0 | 0 – 1 | Ramp color stop — one color of the generated toon ramp. |
| `-- Fake Shadow --` | Shader | — | — | Shader stream. |
| `Fac` | Float | 0 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Map 1` | Color (RGBA) | (0.8518, 0.8518, 0.8518, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 2` | Color (RGBA) | (0.855, 0.855, 0.855, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 3` | Color (RGBA) | (0.855, 0.855, 0.855, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 4` | Color (RGBA) | (0.855, 0.855, 0.855, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 5` | Color (RGBA) | (0.855, 0.855, 0.855, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Range 1` | Float | 0.1 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 2` | Float | 0.3 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 3` | Float | 0.45 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 4` | Float | 0.62 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `--- Shadow ---` | Shader | — | — | Shader stream. |
| `Map 1` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 2` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 3` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 4` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 5` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Range 1` | Float | 0.1 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 2` | Float | 0.3 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 3` | Float | 0.45 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 4` | Float | 0.62 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `--- SSS ---` | Shader | — | — | Shader stream. |
| `Map 1` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 2` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 3` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 4` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 5` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Range 1` | Float | 0.1 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 2` | Float | 0.3 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 3` | Float | 0.45 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 4` | Float | 0.62 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Base Color` | Color (RGBA) | The surface's lit (fully-illuminated) albedo color. |
| `Shadow Color` | Color (RGBA) | Color used in the shadow / shaded band of the toon step. |
| `SSS Color` | Color (RGBA) | Subsurface-scattering tint applied in the deepest shadow band. |
| `Body Alpha` | Float | Opacity of the body material region. |
| `Enable Custom Ramp` | Float | When on, use the supplied Custom Ramp instead of the internal ramp. |
| `Custom Ramp` | Color (RGBA) | User-supplied ramp color that overrides the built-in toon ramp. |
| `Metal Mask` | Float | Mask isolating a region (0–1). |
| `Shadow Mask` | Float | Mask isolating the shaded region (1 in shadow, 0 in light). |

---

### HSR: Build Hair Package

One-click hair starting shader for a Honkai Star Rail character — wires the standard textures and ramps for that part.

**Menu:** `Add Shader > LSCherry > External > Michos > Honkai Star Rail > HSR: Build Hair Package`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Hair Texture` | Color (RGBA) | (1, 1, 1, 1) | — | Color value. |
| `Lightmap Texture` | Color (RGBA) | (1, 1, 1, 1) | — | Packed lightmap texture whose channels encode shadow, specular, AO, etc. |
| `Shadow Factor` | Float | 0 | 0 – 1 | Scalar controlling how strongly the shadow band is applied. |
| `Shadow Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color used in the shadow / shaded band of the toon step. |
| `Toon` | Float | 0 | 0 – 1 | Scalar value. |
| `Shadow Factor` | Float | 1 | 0–1 (factor) | Scalar controlling how strongly the shadow band is applied. |
| `Ramp Size` | Float | 0.95 | 0–1 (factor) | Width of the ramp transition region. |
| `Value Enhance` | Float | 0.1 | 0 – 1 | Boosts the value/contrast of the result. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Base Color` | Color (RGBA) | The surface's lit (fully-illuminated) albedo color. |
| `Shadow Mask` | Float | Mask isolating the shaded region (1 in shadow, 0 in light). |
| `Highlight Mask` | Float | Mask isolating a region (0–1). |
| `Hair Ramp UV` | Vector | UV coordinates. |

---

### HSR: Build Head Package

One-click head starting shader for a Honkai Star Rail character — wires the standard textures and ramps for that part.

**Menu:** `Add Shader > LSCherry > External > Michos > Honkai Star Rail > HSR: Build Head Package`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Head Base Texture` | Color (RGBA) | (1, 1, 1, 1) | — | Color value. |
| `Head Lightmap Texture` | Color (RGBA) | (1, 1, 1, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Head Colormap Texture` | Color (RGBA) | (1, 1, 1, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Fake Shadow Factor` | Float | 0 | 0 – 1 | Blend factor (0–1). |
| `Fake Shadow Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color value for this slot. |
| `Blush Factor` | Float | 0 | 0–1 (factor) | Blend factor (0–1). |
| `Bright Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color injected into the brightest / lit area. |
| `Mood Down Factor` | Float | 0 | 0–1 (factor) | Blend factor (0–1). |
| `Mood Down Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color value for this slot. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Base Color` | Color (RGBA) | The surface's lit (fully-illuminated) albedo color. |

---

### HSR: Build Ramp From Map

Builds the Honkai Star Rail toon color ramp(s) from a packed ramp/map texture.

**Menu:** `Add Shader > LSCherry > External > Michos > Honkai Star Rail > HSR: Build Ramp From Map`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Shadow Factor` | Float | 1 | 0–1 (factor) | Scalar controlling how strongly the shadow band is applied. |
| `Toon` | Float | 0 | 0 – 1 | Scalar value. |
| `Shadow Mask` | Float | 0 | 0 – 1 | Mask isolating the shaded region (1 in shadow, 0 in light). |
| `Ramp Size` | Float | 0.8 | 0–1 (factor) | Width of the ramp transition region. |
| `Value Enhance` | Float | 0.1 | 0–1 (factor) | Boosts the value/contrast of the result. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `UV` | Vector | UV texture coordinates used to sample maps for this node. |

---

### HSR: Seperate Body Lightmap

Splits the Honkai Star Rail body lightmap into its individual channels.

**Menu:** `Add Shader > LSCherry > External > Michos > Honkai Star Rail > HSR: Seperate Body Lightmap`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Lightmap` | Color (RGBA) | (1, 1, 1, 1) | — | Packed lightmap texture whose channels encode shadow, specular, AO, etc. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shadow` | Float | Shadow term/mask consumed or produced by this node. |
| `Metal` | Float | Metalness factor — blends the surface toward a reflective metal look. |

---

### HSR: Seperate Hair Lightmap

Splits the Honkai Star Rail hair lightmap into its individual channels.

**Menu:** `Add Shader > LSCherry > External > Michos > Honkai Star Rail > HSR: Seperate Hair Lightmap`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Lightmap` | Color (RGBA) | (1, 1, 1, 1) | — | Packed lightmap texture whose channels encode shadow, specular, AO, etc. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shadow` | Float | Shadow term/mask consumed or produced by this node. |
| `Highlight` | Float | Scalar value. |

---

### HSR: Seperate Head Colormap

Splits the Honkai Star Rail head colormap into its individual channels.

**Menu:** `Add Shader > LSCherry > External > Michos > Honkai Star Rail > HSR: Seperate Head Colormap`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Lightmap` | Color (RGBA) | (1, 1, 1, 1) | — | Packed lightmap texture whose channels encode shadow, specular, AO, etc. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Blush` | Float | Scalar value. |
| `Mood Down` | Float | Scalar value. |

---

### HSR: Seperate Head Lightmap

Splits the Honkai Star Rail head lightmap into its individual channels.

**Menu:** `Add Shader > LSCherry > External > Michos > Honkai Star Rail > HSR: Seperate Head Lightmap`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Lightmap` | Color (RGBA) | (1, 1, 1, 1) | — | Packed lightmap texture whose channels encode shadow, specular, AO, etc. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shadow` | Float | Shadow term/mask consumed or produced by this node. |
| `See-Through` | Float | Scalar value. |
