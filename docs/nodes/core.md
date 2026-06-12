# LSCherry — Core

**Menu path:** `Add Shader > LSCherry > Core`

> 17 node(s) in this category. Socket types, defaults and ranges below are extracted directly from the compiled node source — they are the ground truth.

Core toon-shading primitives: the step/threshold calculation, halftone dot patterns, outlines, the specular family (core / dot / glossy / metal / reflective), rim light, and emission masking. These are the low-level building blocks that the higher-level builders (`Make Toon`, `LS Cherry Main Controller`) are assembled from. Most accept a shader stream and return a modified shader stream, so they can be chained.

## When to use it

- Hand-building a custom toon material instead of using the all-in-one `Make Toon`.
- Adding a single effect (outline, rim, a specific specular style) on top of an existing shader.
- Authoring stylised highlights — dot specular for a comic look, glossy/metal for shiny surfaces.

## How to use it

1. Drop the node into the Shader Editor from `Add Shader > LSCherry > Core`.
2. Feed the upstream surface into the `Shader` input where present; nodes without a shader input (e.g. `Toon Core`, `Specular Core`) produce a color/mask you mix in yourself.
3. Chain effects by routing each node's `Shader` output into the next node's `Shader` input.
4. Leave `Normal` unconnected to use the geometry normal, or connect a normal map.

## Node reference

### Add Outline

Adds a flat colored outline shader you mix behind the surface (paired with inverted-hull or back-face geometry).

**Menu:** `Add Shader > LSCherry > Core > Add Outline`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Outline Color` | Color (RGBA) | (0.01277, 0.01277, 0.01277, 1) | — | Color value for this slot. |
| `Alpha` | Float | 1 | 0–1 (factor) | Opacity (0 = fully transparent, 1 = fully opaque). |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Outline` | Shader | Shader stream. |

---

### Add Outline From Lightmap

Outline whose color is driven per-region by a lightmap + a 5-stop ramp, so different parts get different outline tints.

**Menu:** `Add Shader > LSCherry > Core > Add Outline From Lightmap`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Lighmap Alpha` | Float | 0 | 0 – 1 | Alpha channel of the lightmap, commonly used as a shadow/AO factor. |
| `Alpha` | Float | 1 | 0–1 (factor) | Opacity (0 = fully transparent, 1 = fully opaque). |
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
| `Outline` | Shader | Shader stream. |

---

### Emission Mask

Turns a mask + color into an emission shader, for making specific areas glow (eyes, FX accents).

**Menu:** `Add Shader > LSCherry > Core > Emission Mask`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Mask` | Float | 0.5 | 0–1 (factor) | Mask isolating a region (0–1). |
| `Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color input/output for this operation. |
| `Scale` | Float | 1 | 1 – 1000 | Scale of the pattern / texture — higher values tile it more densely. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shader` | Shader | Shader stream — connect the surface being processed (in) or pass it on (out). |

---

### Inverted Toon Dot

Halftone dot pattern placed in the lit areas instead of the shadows.

**Menu:** `Add Shader > LSCherry > Core > Inverted Toon Dot`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Light Dir` | Vector | (0, 0, 0) | -∞ – ∞ | Vector value. |
| `Mix Light and View` | Float | 0 | 0–1 (factor) | Scalar value. |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `NdotV` | Float | Scalar value. |
| `NdotInvL` | Float | Scalar value. |
| `Mix InvL and V` | Float | Scalar value. |
| `Main Inv Light Vector` | Vector | Vector value. |
| `Face To X` | Float | Scalar value. |
| `Face To Y` | Float | Scalar value. |

---

### Reflective Toon

Toon shading with environment reflection blended in — for eyes, gems, and shiny accents.

**Menu:** `Add Shader > LSCherry > Core > Reflective Toon`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Color` | Color (RGBA) | (0.8, 0.8, 0.8, 1) | — | Color input/output for this operation. |
| `Roughness` | Float | 0 | 0–1 (factor) | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |
| `Emission Strength` | Float | 1 | 0 – 1000000 | Multiplier for the emission color's brightness. |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shader` | Shader | Shader stream — connect the surface being processed (in) or pass it on (out). |

---

### Rim Core

Computes a view-angle rim-light term along the silhouette.

**Menu:** `Add Shader > LSCherry > Core > Rim Core`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Rim Strength` | Float | 0 | 0 – 10 | Brightness of the rim light. |
| `Roughness` | Float | 0 | 0 – 1 | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Rim` | Color (RGBA) | Color value. |

---

### Simple Back Toon Dot

Dot toon effect applied to back-facing geometry only (inner shadow / translucency look).

**Menu:** `Add Shader > LSCherry > Core > Simple Back Toon Dot`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `NdotL` | Float | Scalar value. |

---

### Simple Toon Dot

Single-threshold halftone dot toon effect.

**Menu:** `Add Shader > LSCherry > Core > Simple Toon Dot`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `NdotL` | Float | Scalar value. |

---

### Specular Core

Core specular highlight term, shaped for toon compositing.

**Menu:** `Add Shader > LSCherry > Core > Specular Core`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Roughness` | Float | 0 | 0–1 (factor) | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Specular` | Float | Scalar value. |

---

### Specular Dot

Specular rendered as a discrete halftone dot rather than a smooth highlight.

**Menu:** `Add Shader > LSCherry > Core > Specular Dot`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Light Dir` | Vector | (0, 0, 0) | -10000 – 10000 | Vector value. |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Specular` | Float | Scalar value. |

---

### Toon Core

The fundamental toon step: takes diffuse lighting + AO and outputs a hard-edged toon color.

**Menu:** `Add Shader > LSCherry > Core > Toon Core`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `AO Fac` | Float | 1 | 0–1 (factor) | Scalar value. |
| `Roughness` | Float | 0 | 0–1 (factor) | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Toon` | Color (RGBA) | Color value. |

---

### Toon Dot

Full halftone dot effect with size, density and threshold control.

**Menu:** `Add Shader > LSCherry > Core > Toon Dot`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Invert MLight` | Boolean | Off | — | Toggle for this option. |
| `Light Dir` | Vector | (0, 0, 0) | -∞ – ∞ | Vector value. |
| `Mix Light and View` | Float | 0 | 0–1 (factor) | Scalar value. |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `NdotV` | Float | Scalar value. |
| `NdotL` | Float | Scalar value. |
| `VcrsNcrsL` | Float | Scalar value. |
| `Mix L and V` | Float | Scalar value. |
| `Main Light Vector` | Vector | Vector value. |
| `Face To X` | Boolean | Toggle for this option. |
| `Face To Y` | Boolean | Toggle for this option. |

---

### Toon Glossy

Glossy toon reflection using a blurred environment sample plus a toon step.

**Menu:** `Add Shader > LSCherry > Core > Toon Glossy`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color input/output for this operation. |
| `Size` | Float | 0.9 | 0–1 (factor) | Size of the feature (dot, cell, highlight, …); larger values enlarge it. |
| `Smooth` | Float | 0.1 | 0–1 (factor) | Softness of the transition edge — 0 is a hard toon step, higher feathers it. |
| `Roughness` | Float | 0.5 | 0–1 (factor) | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shader` | Shader | Shader stream — connect the surface being processed (in) or pass it on (out). |

---

### Toon Metal

Metallic toon shading — environment reflection combined with a stepped diffuse.

**Menu:** `Add Shader > LSCherry > Core > Toon Metal`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color input/output for this operation. |
| `Edge Tint` | Color (RGBA) | (0.77, 0.77, 0.77, 1) | — | Color value. |
| `Size` | Float | 0.9 | 0–1 (factor) | Size of the feature (dot, cell, highlight, …); larger values enlarge it. |
| `Smooth` | Float | 0.1 | 0–1 (factor) | Softness of the transition edge — 0 is a hard toon step, higher feathers it. |
| `Roughness` | Float | 0 | 0–1 (factor) | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |
| `Tangent` | Vector | (0, 0, 0) | -∞ – ∞ | Vector value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shader` | Shader | Shader stream — connect the surface being processed (in) or pass it on (out). |

---

### Toon Ray

Ray-based toon shading driven by `Make Ray` for more directional, physical-feeling steps.

**Menu:** `Add Shader > LSCherry > Core > Toon Ray`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color input/output for this operation. |
| `Size` | Float | 0.9 | 0–1 (factor) | Size of the feature (dot, cell, highlight, …); larger values enlarge it. |
| `Smooth` | Float | 0.1 | 0–1 (factor) | Softness of the transition edge — 0 is a hard toon step, higher feathers it. |
| `Roughness` | Float | 0 | 0–1 (factor) | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shader` | Shader | Shader stream — connect the surface being processed (in) or pass it on (out). |

---

### Toon Spec

Toon-stylised specular: a hard step applied to the specular gradient.

**Menu:** `Add Shader > LSCherry > Core > Toon Spec`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color input/output for this operation. |
| `Size` | Float | 0.9 | 0–1 (factor) | Size of the feature (dot, cell, highlight, …); larger values enlarge it. |
| `Smooth` | Float | 0.1 | 0–1 (factor) | Softness of the transition edge — 0 is a hard toon step, higher feathers it. |
| `Roughness` | Float | 0 | 0–1 (factor) | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |
| `Tangent` | Vector | (0, 0, 0) | -∞ – ∞ | Vector value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shader` | Shader | Shader stream — connect the surface being processed (in) or pass it on (out). |

---

### Toon3S

Three-band toon (shallow / mid / deep shadow) with per-band color, scale and weight, plus a specular panel.

**Menu:** `Add Shader > LSCherry > Core > Toon3S`


Inputs are grouped into collapsible panels in the N-panel: **Shallow**; **Mid**; **Deep**; **Spec**.

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Base Color` | Color (RGBA) | (0.8, 0.8, 0.8, 1) | — | The surface's lit (fully-illuminated) albedo color. |
| `Spec Color` | Color (RGBA) | (0.8, 0.8, 0.8, 1) | — | Color of the specular highlight. |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |
| `Shallow Color` | Color (RGBA) | (0, 0, 0, 1) | — | Color value for this slot. |
| `Shallow Scale` | Float | 0.05 | 0 – 1 | Scale of this feature. |
| `Mid Color` | Color (RGBA) | (0, 0, 0, 1) | — | Color value for this slot. |
| `Mid Scale` | Float | 0.05 | 0 – 1 | Scale of this feature. |
| `Mid Weight` | Float | 0.6 | 0–1 (factor) | Relative weight of this contribution. |
| `Deep Color` | Color (RGBA) | (0, 0, 0, 1) | — | Color value for this slot. |
| `Deep Scale` | Float | 0.05 | 0 – 1 | Scale of this feature. |
| `Deep Weight` | Float | 0.4 | 0–1 (factor) | Relative weight of this contribution. |
| `Spec Tint` | Float | 0.1 | 0–1 (factor) | Scalar value. |
| `Spec Roughness` | Float | 0.5 | 0–1 (factor) | Surface roughness for this term. |
| `Oil Spec` | Float | 0.5 | 0–1 (factor) | Scalar value. |
| `Oil Roughness` | Float | 0.5 | 0–1 (factor) | Surface roughness for this term. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shader` | Shader | Shader stream — connect the surface being processed (in) or pass it on (out). |
