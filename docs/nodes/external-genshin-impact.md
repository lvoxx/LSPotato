# LSCherry — External / Michos / Genshin Impact

**Menu path:** `Add Shader > LSCherry > External > Michos > Genshin Impact`

> 13 node(s) in this category. Socket types, defaults and ranges below are extracted directly from the compiled node source — they are the ground truth.

Michos's Genshin Impact (`GI:`) shader set. The `Build * Package` nodes are the one-click starting points per body part (head/body/hair); the `Seperate *` and `* From Lightmap/Colormap` nodes are the lower-level steps those packages are built from — exposed so you can wire a custom setup. Driven by Genshin's packed colormap + lightmap + ramp textures.

## When to use it

- Shading ripped Genshin Impact characters with game-accurate toon ramps.
- Customising one stage (e.g. just the ramp build) of a Genshin material.

## How to use it

1. Start with the `Build Head/Body/Hair Package` node for the part you are shading.
2. Feed the part's colormap, lightmap and ramp textures into the matching inputs.
3. Drop to the `Seperate *` / `* From Lightmap` nodes only when you need finer control.

## Node reference

### GI: Add Color From Colormap

Applies base colors from the Genshin Impact colormap.

**Menu:** `Add Shader > LSCherry > External > Michos > Genshin Impact > GI: Add Color From Colormap`

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

### GI: Add Outline From Lightmap

Adds an outline whose tint is driven by the Genshin Impact lightmap.

**Menu:** `Add Shader > LSCherry > External > Michos > Genshin Impact > GI: Add Outline From Lightmap`

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

### GI: Add Shadow From Lightmap

Adds shadow shading driven by the Genshin Impact lightmap.

**Menu:** `Add Shader > LSCherry > External > Michos > Genshin Impact > GI: Add Shadow From Lightmap`

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

### GI: Body Color From Lightmap

Derives body base color using the Genshin Impact lightmap.

**Menu:** `Add Shader > LSCherry > External > Michos > Genshin Impact > GI: Body Color From Lightmap`

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

### GI: Build Body Package

One-click body starting shader for a Genshin Impact character — wires the standard textures and ramps for that part.

**Menu:** `Add Shader > LSCherry > External > Michos > Genshin Impact > GI: Build Body Package`


Inputs are grouped into collapsible panels in the N-panel: **LightMap Range**; **Shadow**; **SSS**; **Specular**.

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Body Texture` | Color (RGBA) | (1, 1, 1, 1) | — | Color value. |
| `Body Alpha` | Float | 0 | -∞ – ∞ | Opacity of the body material region. |
| `Lightmap Texture` | Color (RGBA) | (1, 1, 1, 1) | — | Packed lightmap texture whose channels encode shadow, specular, AO, etc. |
| `Lighmap  Alpha Texture` | Float | 0 | 0 – 1 | Ramp color stop — one color of the generated toon ramp. |
| `Normal Map` | Vector | (0, 0, 0) | -∞ – ∞ | Normal vector for this term. |
| `Mix Core And Dot` | Float | 0 | 0–1 (factor) | Scalar value. |
| `Roughness` | Float | 0.2 | 0–1 (factor) | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |
| `Emission Strength` | Float | 1 | 0 – 10000 | Multiplier for the emission color's brightness. |
| `Range 1` | Float | 0.1 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 2` | Float | 0.3 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 3` | Float | 0.45 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 4` | Float | 0.62 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Map 1` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 2` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 3` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 4` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 5` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 1` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 2` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 3` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 4` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 5` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 1` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 2` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 3` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 4` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 5` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Base Color` | Color (RGBA) | The surface's lit (fully-illuminated) albedo color. |
| `Shadow Color` | Color (RGBA) | Color used in the shadow / shaded band of the toon step. |
| `SSS Color` | Color (RGBA) | Subsurface-scattering tint applied in the deepest shadow band. |
| `Normal` | Vector | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |
| `Body Alpha` | Float | Opacity of the body material region. |
| `Emission` | Color (RGBA) | Emission color added on top of the shading. |
| `Emission Strength` | Float | Multiplier for the emission color's brightness. |
| `Enable Metal Ramp` | Float | Scalar value. |
| `Metal Ramp` | Color (RGBA) | Color value. |
| `Metal Mask` | Float | Mask isolating a region (0–1). |
| `Shadow Mask` | Float | Mask isolating the shaded region (1 in shadow, 0 in light). |

---

### GI: Build Hair Package

One-click hair starting shader for a Genshin Impact character — wires the standard textures and ramps for that part.

**Menu:** `Add Shader > LSCherry > External > Michos > Genshin Impact > GI: Build Hair Package`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Hair Texture` | Color (RGBA) | (1, 1, 1, 1) | — | Color value. |
| `Hair Alpha` | Float | 0 | -∞ – ∞ | Opacity / alpha value. |
| `Lightmap Texture` | Color (RGBA) | (1, 1, 1, 1) | — | Packed lightmap texture whose channels encode shadow, specular, AO, etc. |
| `Lightmap Alpha` | Float | 0 | -∞ – ∞ | Alpha channel of the lightmap, commonly used as a shadow/AO factor. |
| `Shadow Factor` | Float | 0 | 0 – 1 | Scalar controlling how strongly the shadow band is applied. |
| `Shadow Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color used in the shadow / shaded band of the toon step. |
| `Emission Strength` | Float | 1 | 0 – 10000 | Multiplier for the emission color's brightness. |
| `Toon` | Float | 0 | 0 – 1 | Scalar value. |
| `Shadow Factor` | Float | 1 | 0–1 (factor) | Scalar controlling how strongly the shadow band is applied. |
| `Ramp Size` | Float | 0.95 | 0–1 (factor) | Width of the ramp transition region. |
| `Value Enhance` | Float | 0.1 | 0 – 1 | Boosts the value/contrast of the result. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Base Color` | Color (RGBA) | The surface's lit (fully-illuminated) albedo color. |
| `Emission` | Color (RGBA) | Emission color added on top of the shading. |
| `Emission Strength` | Float | Multiplier for the emission color's brightness. |
| `Shadow Mask` | Float | Mask isolating the shaded region (1 in shadow, 0 in light). |
| `Highlight Mask` | Float | Mask isolating a region (0–1). |
| `Metal Mask` | Float | Mask isolating a region (0–1). |
| `Hair Ramp UV` | Vector | UV coordinates. |

---

### GI: Build Head Package

One-click head starting shader for a Genshin Impact character — wires the standard textures and ramps for that part.

**Menu:** `Add Shader > LSCherry > External > Michos > Genshin Impact > GI: Build Head Package`

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

### GI: Build Ramps From Map

Builds the Genshin Impact toon color ramp(s) from a packed ramp/map texture.

**Menu:** `Add Shader > LSCherry > External > Michos > Genshin Impact > GI: Build Ramps From Map`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Toon` | Float | 0 | 0 – 1 | Scalar value. |
| `Shadow Factor` | Float | 1 | 0–1 (factor) | Scalar controlling how strongly the shadow band is applied. |
| `Shadow Mask` | Float | 0 | 0 – 1 | Mask isolating the shaded region (1 in shadow, 0 in light). |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Hot-UV1` | Vector | UV coordinates. |
| `Hot-UV2` | Vector | UV coordinates. |
| `Hot-UV3` | Vector | UV coordinates. |
| `Hot-UV4` | Vector | UV coordinates. |
| `Hot-UV5` | Vector | UV coordinates. |
| `Cold-UV1` | Vector | UV coordinates. |
| `Cold-UV2` | Vector | UV coordinates. |
| `Cold-UV3` | Vector | UV coordinates. |
| `Cold-UV4` | Vector | UV coordinates. |
| `Cold-UV5` | Vector | UV coordinates. |

---

### GI: From Map To Ramp

Converts a packed ramp map into a usable Genshin Impact toon ramp.

**Menu:** `Add Shader > LSCherry > External > Michos > Genshin Impact > GI: From Map To Ramp`


Inputs are grouped into collapsible panels in the N-panel: **Hot Ramp**; **Cool Ramp**; **Range**.

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Enable Cool Ramp` | Boolean | Off | — | Toggle for this option. |
| `Lighmap Alpha` | Float | 0 | 0 – 1 | Alpha channel of the lightmap, commonly used as a shadow/AO factor. |
| `Map 1` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 2` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 3` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 4` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 5` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
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
| `Ramp Map` | Color (RGBA) | Color value. |

---

### GI: Seperate Body Lightmap

Splits the Genshin Impact body lightmap into its individual channels.

**Menu:** `Add Shader > LSCherry > External > Michos > Genshin Impact > GI: Seperate Body Lightmap`

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

### GI: Seperate Hair Lightmap

Splits the Genshin Impact hair lightmap into its individual channels.

**Menu:** `Add Shader > LSCherry > External > Michos > Genshin Impact > GI: Seperate Hair Lightmap`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Lightmap` | Color (RGBA) | (1, 1, 1, 1) | — | Packed lightmap texture whose channels encode shadow, specular, AO, etc. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shadow` | Float | Shadow term/mask consumed or produced by this node. |
| `Highlight` | Float | Scalar value. |
| `Metal` | Float | Metalness factor — blends the surface toward a reflective metal look. |

---

### GI: Seperate Head Colormap

Splits the Genshin Impact head colormap into its individual channels.

**Menu:** `Add Shader > LSCherry > External > Michos > Genshin Impact > GI: Seperate Head Colormap`

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

### GI: Seperate Head Lightmap

Splits the Genshin Impact head lightmap into its individual channels.

**Menu:** `Add Shader > LSCherry > External > Michos > Genshin Impact > GI: Seperate Head Lightmap`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Lightmap` | Color (RGBA) | (1, 1, 1, 1) | — | Packed lightmap texture whose channels encode shadow, specular, AO, etc. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shadow` | Float | Shadow term/mask consumed or produced by this node. |
| `See-Through` | Float | Scalar value. |
