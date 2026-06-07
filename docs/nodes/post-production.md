# LSCherry — Post Production

**Menu path:** `Add Shader > LSCherry > Post Production`

> 15 node(s) in this category. Socket types, defaults and ranges below are extracted directly from the compiled node source — they are the ground truth.

Finishing-pass nodes that layer on top of a completed toon shader: specular and highlight variants (core, dot, sphere-map, lightmap-driven, hair, random), body tint adjustments, view-transform helpers (`Quick To Filmic`, `Standard To Filmic`), a shader kill-switch, and a random color generator. They are designed to stack in order.

## When to use it

- Adding anime hair highlights or specular glints after the base toon look is set.
- Converting a Standard-view result into a Filmic/AgX-friendly one for final render.
- Quickly tinting or muting a material during look-dev.

## How to use it

1. Apply after the main shader (e.g. after `Make Toon`).
2. Layer in order: specular/core first, then highlights, then tone mapping.
3. `Disable All Shader` is a debugging toggle — it flattens the surface so you can isolate geometry.

## Node reference

### Add Core Specular

Layers a core-style specular highlight onto a finished shader.

**Menu:** `Add Shader > LSCherry > Post Production > Add Core Specular`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Factor` | Float | 1 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Combined` | Color (RGBA) | (0, 0, 0, 1) | — | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |
| `Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color input/output for this operation. |
| `Roughness` | Float | 0.1 | 0–1 (factor) | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Combined` | Color (RGBA) | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |

---

### Add Dot Specular

Layers a halftone dot specular onto a finished shader.

**Menu:** `Add Shader > LSCherry > Post Production > Add Dot Specular`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Factor` | Float | 1 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Combined` | Color (RGBA) | (0, 0, 0, 1) | — | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |
| `Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color input/output for this operation. |
| `Roughness` | Float | 0.1 | 0–1 (factor) | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Combined` | Color (RGBA) | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |

---

### Add Frequent Hair Highlight

Anime hair highlight with multiple repeating bands.

**Menu:** `Add Shader > LSCherry > Post Production > Add Frequent Hair Highlight`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Fac` | Float | 1 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Combined` | Color (RGBA) | (0, 0, 0, 1) | — | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |
| `Toon` | Color (RGBA) | (0, 0, 0, 1) | — | Color value. |
| `Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color input/output for this operation. |
| `Mix High And Low Frequent` | Float | 0.5 | -10–10 (factor) | Scalar value. |
| `Size` | Float | 0 | -10–10 (factor) | Size of the feature (dot, cell, highlight, …); larger values enlarge it. |
| `Frequency` | Float | 1 | -10 – 10 | Scalar value. |
| `Fill Gap` | Float | 0 | -1–1 (factor) | Scalar value. |
| `Offset-Z` | Float | 0 | -10–10 (factor) | Positional offset applied to this term. |
| `Z-View Instensity` | Float | 0 | 0–1 (factor) | Scalar value. |
| `Z-limit - top` | Float | 0.4 | 0–1 (factor) | Scalar value. |
| `Z-limit- bot` | Float | 0.6 | 0–1 (factor) | Scalar value. |
| `Planar UV` | Vector | (0, 0, 0) | -∞ – ∞ | UV coordinates. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Combined` | Color (RGBA) | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |

---

### Add Highlight

Generic highlight pass added on top of the surface.

**Menu:** `Add Shader > LSCherry > Post Production > Add Highlight`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Fac` | Float | 1 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Combined` | Color (RGBA) | (0.5, 0.5, 0.5, 1) | — | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |
| `Shading` | Float | 1 | 0 – 1 | Incoming shading/lighting term used by this node. |
| `Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color input/output for this operation. |
| `Pattern` | Color (RGBA) | (1, 1, 1, 1) | — | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Combined` | Color (RGBA) | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |

---

### Add HightLight From LightMap

Highlight whose placement/intensity is read from a lightmap channel.

**Menu:** `Add Shader > LSCherry > Post Production > Add HightLight From LightMap`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Fac` | Float | 1 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Combined` | Color (RGBA) | (0, 0, 0, 1) | — | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |
| `Toon` | Color (RGBA) | (0, 0, 0, 1) | — | Color value. |
| `Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color input/output for this operation. |
| `LightMap` | Float | 1 | 0 – 1 | Packed lightmap texture whose channels encode shadow, specular, AO, etc. |
| `Pattern` | Color (RGBA) | (1, 1, 1, 1) | — | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Combined` | Color (RGBA) | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |

---

### Add HightLight From SphereMap

Highlight sampled from a sphere/matcap map (view-locked specular).

**Menu:** `Add Shader > LSCherry > Post Production > Add HightLight From SphereMap`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Fac` | Float | 1 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Combined` | Color (RGBA) | (0.5, 0.5, 0.5, 1) | — | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |
| `SphereMap` | Float | 0 | -∞ – ∞ | Scalar value. |
| `Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color input/output for this operation. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Combined` | Color (RGBA) | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |
| `Result` | Color (RGBA) | Computed result of this node. |

---

### Add Invert Tint V-Body

Inverse vertical-gradient body tint (complements `Add Tint V-Body`).

**Menu:** `Add Shader > LSCherry > Post Production > Add Invert Tint V-Body`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Fac` | Float | 0 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Combine` | Color (RGBA) | (0, 0, 0, 1) | — | Color value. |
| `Shading` | Float | 1 | 0 – 1 | Incoming shading/lighting term used by this node. |
| `Pattern` | Color (RGBA) | (1, 1, 1, 1) | — | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |
| `Low Color` | Color (RGBA) | (1, 0.7686, 0.7463, 1) | — | Color value for this slot. |
| `Mid Color` | Color (RGBA) | (0.678, 0.2375, 0.1805, 1) | — | Color value for this slot. |
| `High Color` | Color (RGBA) | (0.734, 0.1929, 0.1444, 1) | — | Color value for this slot. |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Combined` | Color (RGBA) | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |

---

### Add Random Toon Highlight

Randomised toon highlight for break-up/variation across a surface.

**Menu:** `Add Shader > LSCherry > Post Production > Add Random Toon Highlight`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Fac` | Float | 1 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Combined` | Color (RGBA) | (0, 0, 0, 1) | — | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |
| `Shading` | Float | 1 | 0–1 (factor) | Incoming shading/lighting term used by this node. |
| `Pattern` | Color (RGBA) | (1, 1, 1, 1) | — | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |
| `Size` | Float | 0.7 | 0 – 1 | Size of the feature (dot, cell, highlight, …); larger values enlarge it. |
| `Seed` | Integer | 0 | 0 – 100 | Random seed; change it to get a different variation of the procedural result. |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Combined` | Color (RGBA) | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |

---

### Add Specular

Adds a standard specular highlight to the shader.

**Menu:** `Add Shader > LSCherry > Post Production > Add Specular`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Factor` | Float | 1 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Combined` | Color (RGBA) | (0, 0, 0, 1) | — | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |
| `Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color input/output for this operation. |
| `Use Dot` | Boolean | Off | — | Toggle for this option. |
| `Roughness` | Float | 0.1 | 0–1 (factor) | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Combined` | Color (RGBA) | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |

---

### Add Tint V-Body

Applies a vertical-gradient tint down the body (e.g. darker boots, lighter shoulders).

**Menu:** `Add Shader > LSCherry > Post Production > Add Tint V-Body`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Fac` | Float | 0 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Combine` | Color (RGBA) | (0, 0, 0, 1) | — | Color value. |
| `Shading` | Float | 1 | 0 – 1 | Incoming shading/lighting term used by this node. |
| `Pattern` | Float | 1 | 0 – 1 | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |
| `Low Color` | Color (RGBA) | (1, 0.7686, 0.7463, 1) | — | Color value for this slot. |
| `Mid Color` | Color (RGBA) | (0.678, 0.2375, 0.1805, 1) | — | Color value for this slot. |
| `High Color` | Color (RGBA) | (0.734, 0.1929, 0.1444, 1) | — | Color value for this slot. |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Combined` | Color (RGBA) | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |

---

### Add Toon Highlight

Adds a hard, toon-stepped highlight.

**Menu:** `Add Shader > LSCherry > Post Production > Add Toon Highlight`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Fac` | Float | 1 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Combined` | Color (RGBA) | (0, 0, 0, 1) | — | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |
| `Shading` | Float | 1 | 0–1 (factor) | Incoming shading/lighting term used by this node. |
| `Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color input/output for this operation. |
| `Pattern` | Color (RGBA) | (1, 1, 1, 1) | — | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Combined` | Color (RGBA) | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |

---

### Disable All Shader

Debug switch that flattens the surface so geometry can be inspected.

**Menu:** `Add Shader > LSCherry > Post Production > Disable All Shader`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Fac` | Float | 0 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Shader` | Shader | — | — | Shader stream — connect the surface being processed (in) or pass it on (out). |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shader` | Shader | Shader stream — connect the surface being processed (in) or pass it on (out). |

---

### Quick To Filmic

Fast Standard→Filmic-style conversion of the result for final view.

**Menu:** `Add Shader > LSCherry > Post Production > Quick To Filmic`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Combined` | Color (RGBA) | (1, 1, 1, 1) | — | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Combined` | Color (RGBA) | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |

---

### Random Color

Generates a random flat color (per object/material) for blocking and previews.

**Menu:** `Add Shader > LSCherry > Post Production > Random Color`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Seed` | Integer | 0 | 0 – 10000000 | Random seed; change it to get a different variation of the procedural result. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Color` | Color (RGBA) | Color input/output for this operation. |

---

### Standard To Filmic

Converts a Standard-view color into a Filmic/AgX-friendly one.

**Menu:** `Add Shader > LSCherry > Post Production > Standard To Filmic`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Combined` | Color (RGBA) | (1, 1, 1, 1) | — | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Combined` | Color (RGBA) | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |
