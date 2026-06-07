# LSCherry — Root (Top-Level Builders & Controllers)

**Menu path:** `Add Shader > LSCherry`

> 13 node(s) in this category. Socket types, defaults and ranges below are extracted directly from the compiled node source — they are the ground truth.

The headline nodes that sit at the top of the `LSCherry` menu. These are the all-in-one builders and scene controllers most users start from: full character shaders (`Make Toon`, `LS Cherry Main Controller`), quick variants (`Simple Toon`, `Simple Make Toon`), the stacked-toon multi-layer system, the ray helper, and the shared `Named Properties` / `Global Configuration Loader` providers.

## When to use it

- Shading a character end-to-end from one node.
- Quick look-dev with `Simple Toon` before committing to the full controller.
- Sharing light vectors and global settings across many materials.

## How to use it

1. For most work start with `Make Toon` (full control) or `Simple Make Toon` (fast).
2. Add `Named Properties` once per material to expose shared light/scene vectors without duplicating attribute nodes.
3. Connect the builder's `Shader` output to the Material Output; use `To AgrX` if you are in an AgX view transform.

## Node reference

### Build Face Ramp

Builds the face-shadow ramp from a face map.

**Menu:** `Add Shader > LSCherry > Build Face Ramp`

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

### Build Stacked Toon

Assembles a multi-layer (stacked) toon result from stacked toon layers.

**Menu:** `Add Shader > LSCherry > Build Stacked Toon`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Stack` | Color (RGBA) | (0, 0, 0, 1) | — | Color value. |
| `Alpha` | Float | 1 | 0–1 (factor) | Opacity (0 = fully transparent, 1 = fully opaque). |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shader` | Shader | Shader stream — connect the surface being processed (in) or pass it on (out). |
| `To AgX` | Shader | Shader stream. |

---

### Global Configuration Loader

Loads shared global render/shading configuration into the material graph.

**Menu:** `Add Shader > LSCherry > Global Configuration Loader`

**Inputs**

_None._


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Disable Enviroment` | Boolean | Toggle for this option. |
| `Value Enhance` | Float | Boosts the value/contrast of the result. |
| `World Color` | Color (RGBA) | Scene world/ambient color fed into the shading. |

---

### LS Cherry Main Controller

The full LSCherry character controller — the most complete all-in-one shader.

**Menu:** `Add Shader > LSCherry > LS Cherry Main Controller`


Inputs are grouped into collapsible panels in the N-panel: **Dot** — Panel of Dot product uses only; **Rim**; **Specular** — Specular Panel; **General** — Genereal Things that can be used from any purposes; **Stylized Ramp** — Custom Ramp; **Ramp** — Section of customize Ramps.

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Base Color` | Color (RGBA) | (1, 0, 0, 1) | — | The surface's lit (fully-illuminated) albedo color. |
| `Shadow Color` | Color (RGBA) | (0.7429, 0.6049, 0.6049, 1) | — | Color used in the shadow / shaded band of the toon step. |
| `SSS Color` | Color (RGBA) | (1, 0.0865, 0, 1) | — | Subsurface-scattering tint applied in the deepest shadow band. |
| `Rim Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color of the rim / fresnel light along the silhouette. |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |
| `Back Color` | Color (RGBA) | (0.04373, 0.0865, 0.4233, 1) | — | Color applied to back-facing geometry (inner shadow / translucency look). |
| `Rim Strength` | Float | 0.5 | 0–10 (factor) | Brightness of the rim light. |
| `Rim Size` | Float | 0.5 | 0 – 1 | Width of the rim light band. |
| `Rim Smooth` | Float | 0.5 | 0 – 1 | Softness of the rim light edge. |
| `Specular Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color of the specular highlight. |
| `Specular Tint` | Float | 0 | 0–1 (factor) | How much the specular highlight is tinted by the base color. |
| `Roughness` | Float | 0.1 | 0–1 (factor) | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |
| `Pattern` | Color (RGBA) | (1, 1, 1, 1) | — | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |
| `Emission` | Color (RGBA) | (0, 0, 0, 1) | — | Emission color added on top of the shading. |
| `Emission Strength` | Float | 1 | 0 – 100 | Multiplier for the emission color's brightness. |
| `Disable Toon Style` | Boolean | Off | — | Bypass the toon ramp styling. |
| `Toon Style` | Vector | (0, 0, 0) | -∞ – ∞ | Ramp-style vector selecting the toon band shaping (from a Ramp Style node). |
| `Disable SSS Style` | Boolean | Off | — | Bypass the SSS ramp styling. |
| `SSS Style` | Vector | (0, 0, 0) | -∞ – ∞ | Ramp-style vector selecting the SSS band shaping (from a Ramp Style node). |
| `Disable Back Style` | Boolean | Off | — | Bypass the back-face ramp styling. |
| `Back Style` | Vector | (0, 0, 0) | -∞ – ∞ | Ramp-style vector selecting the back-face band shaping (from a Ramp Style node). |
| `Enable Custom Ramp` | Boolean | Off | — | When on, use the supplied Custom Ramp instead of the internal ramp. |
| `Custom Ramp` | Color (RGBA) | (0, 0, 0, 1) | — | User-supplied ramp color that overrides the built-in toon ramp. |
| `Blend With Custom Ramp` | Float | 1 | 0–1 (factor) | How much the custom ramp is mixed over the default shading. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Combined` | Color (RGBA) | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |
| `Diffuse Mask` | Color (RGBA) | Mask of the diffuse-lit region. |
| `Post Diffuse Mask` | Color (RGBA) | Mask isolating a region (0–1). |
| `SSS Mask` | Color (RGBA) | Mask isolating a region (0–1). |
| `Rim Mask` | Color (RGBA) | Mask isolating a region (0–1). |
| `Back Mask` | Color (RGBA) | Mask isolating a region (0–1). |
| `Light Sources Mask` | Color (RGBA) | Mask isolating a region (0–1). |

---

### Make Ray

Produces directional ray data consumed by `Toon Ray` for physical-feeling steps.

**Menu:** `Add Shader > LSCherry > Make Ray`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `―【CORE】―` | Shader | — | — | Shader stream. |
| `Base Color` | Color (RGBA) | (1, 0, 0, 1) | — | The surface's lit (fully-illuminated) albedo color. |
| `Specular Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color of the specular highlight. |
| `Edge Tint` | Color (RGBA) | (1, 1, 1, 1) | — | Color value. |
| `―【GENERAL】―` | Shader | — | — | Shader stream. |
| `Size` | Float | 0.9 | 0–1 (factor) | Size of the feature (dot, cell, highlight, …); larger values enlarge it. |
| `Smooth` | Float | 0.1 | 0–1 (factor) | Softness of the transition edge — 0 is a hard toon step, higher feathers it. |
| `Roughness` | Float | 0 | 0–1 (factor) | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |
| `Metal` | Float | 0 | 0–1 (factor) | Metalness factor — blends the surface toward a reflective metal look. |
| `Alpha` | Float | 1 | 0 – 1 | Opacity (0 = fully transparent, 1 = fully opaque). |
| `Emission Color` | Color (RGBA) | (0.04971, 0.006049, 0, 1) | — | Color value for this slot. |
| `Emission Strength` | Float | 0 | 0 – 1000000 | Multiplier for the emission color's brightness. |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |
| `Tangent` | Vector | (0, 0, 0) | -∞ – ∞ | Vector value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shader` | Shader | Shader stream — connect the surface being processed (in) or pass it on (out). |

---

### Make Toon

All-in-one toon character shader: base/shadow/SSS/rim/back colors, specular, pattern, emission and custom-ramp control, organised into N-panel sections.

**Menu:** `Add Shader > LSCherry > Make Toon`


Inputs are grouped into collapsible panels in the N-panel: **Dot** — Panel of Dot product uses only; **Rim**; **Specular** — Specular Panel; **General** — Genereal Things that can be used from any purposes; **Stylized Ramp**; **Ramp** — Section of customize Ramps.

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Base Color` | Color (RGBA) | (1, 0, 0, 1) | — | The surface's lit (fully-illuminated) albedo color. |
| `Shadow Color` | Color (RGBA) | (0.1777, 0, 0, 1) | — | Color used in the shadow / shaded band of the toon step. |
| `SSS Color` | Color (RGBA) | (0.7484, 0.1325, 0, 1) | — | Subsurface-scattering tint applied in the deepest shadow band. |
| `Rim Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color of the rim / fresnel light along the silhouette. |
| `Alpha` | Float | 1 | 0–1 (factor) | Opacity (0 = fully transparent, 1 = fully opaque). |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |
| `Back Color` | Color (RGBA) | (0, 0.04392, 0.4233, 1) | — | Color applied to back-facing geometry (inner shadow / translucency look). |
| `Rim Strength` | Float | 0.5 | 0–10 (factor) | Brightness of the rim light. |
| `Rim Size` | Float | 0.3 | 0 – 1 | Width of the rim light band. |
| `Rim Smooth` | Float | 0.5 | 0 – 1 | Softness of the rim light edge. |
| `Specular Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color of the specular highlight. |
| `Specular Tint` | Float | 0 | 0–1 (factor) | How much the specular highlight is tinted by the base color. |
| `Roughness` | Float | 0.1 | 0–1 (factor) | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |
| `Pattern` | Color (RGBA) | (1, 1, 1, 1) | — | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |
| `Emission` | Color (RGBA) | (0, 0, 0, 1) | — | Emission color added on top of the shading. |
| `Emission Strength` | Float | 1 | 0 – 1000 | Multiplier for the emission color's brightness. |
| `Disable Toon Style` | Boolean | Off | — | Bypass the toon ramp styling. |
| `Toon Style` | Vector | (0, 0, 0) | -∞ – ∞ | Ramp-style vector selecting the toon band shaping (from a Ramp Style node). |
| `Disable SSS Style` | Boolean | Off | — | Bypass the SSS ramp styling. |
| `SSS Style` | Vector | (0, 0, 0) | -∞ – ∞ | Ramp-style vector selecting the SSS band shaping (from a Ramp Style node). |
| `Disable Back Style` | Boolean | Off | — | Bypass the back-face ramp styling. |
| `Back Style` | Vector | (0, 0, 0) | -∞ – ∞ | Ramp-style vector selecting the back-face band shaping (from a Ramp Style node). |
| `Enable Custom Ramp` | Boolean | Off | — | When on, use the supplied Custom Ramp instead of the internal ramp. |
| `Custom Ramp` | Color (RGBA) | (0, 0, 0, 1) | — | User-supplied ramp color that overrides the built-in toon ramp. |
| `Blend With Custom Ramp` | Float | 1 | 0–1 (factor) | How much the custom ramp is mixed over the default shading. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shader` | Shader | Shader stream — connect the surface being processed (in) or pass it on (out). |
| `To AgrX` | Shader | Secondary shader stream routed to an AgX / view-transform path. |
| `Combined` | Color (RGBA) | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |
| `Alpha` | Float | Opacity (0 = fully transparent, 1 = fully opaque). |
| `Diffuse Mask` | Color (RGBA) | Mask of the diffuse-lit region. |
| `Post Diffuse Mask` | Color (RGBA) | Mask isolating a region (0–1). |
| `SSS Mask` | Color (RGBA) | Mask isolating a region (0–1). |
| `Rim Mask` | Color (RGBA) | Mask isolating a region (0–1). |
| `Back Mask` | Color (RGBA) | Mask isolating a region (0–1). |
| `Light Sources Mask` | Color (RGBA) | Mask isolating a region (0–1). |

---

### Named Properties

Central provider of shared, named light/scene vectors — add once per material to avoid duplicate attribute nodes.

**Menu:** `Add Shader > LSCherry > Named Properties`

**Inputs**

_None._


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Main Light Vector` | Vector | Vector value. |
| `Back Light Vector` | Vector | Vector value. |
| `Fx` | Vector | Vector value. |
| `Fy` | Vector | Vector value. |
| `Toon Normal` | Vector | Normal vector for this term. |

---

### Simple Make Toon

Streamlined `Make Toon` with the most-used inputs for fast setups.

**Menu:** `Add Shader > LSCherry > Simple Make Toon`


Inputs are grouped into collapsible panels in the N-panel: **Rim**; **Configuration**.

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Base Color` | Color (RGBA) | (1, 0, 0, 1) | — | The surface's lit (fully-illuminated) albedo color. |
| `Shadow Color` | Color (RGBA) | (0.1779, 0, 0, 1) | — | Color used in the shadow / shaded band of the toon step. |
| `Rim Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color of the rim / fresnel light along the silhouette. |
| `Pattern` | Color (RGBA) | (1, 1, 1, 1) | — | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |
| `Disable Toon Style` | Boolean | Off | — | Bypass the toon ramp styling. |
| `Toon Style` | Vector | (0, 0, 0) | -∞ – ∞ | Ramp-style vector selecting the toon band shaping (from a Ramp Style node). |
| `Normal` | Vector | (0, 0, 0) | -10000 – 10000 | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |
| `Alpha` | Float | 1 | 0–1 (factor) | Opacity (0 = fully transparent, 1 = fully opaque). |
| `Rim Size` | Float | 0.3 | 0–10000 (factor) | Width of the rim light band. |
| `Rim Strength` | Float | 0.1 | 0–10 (factor) | Brightness of the rim light. |
| `Enable Dot` | Boolean | Off | — | Toggle for this option. |
| `World Color` | Color (RGBA) | (1, 1, 1, 1) | — | Scene world/ambient color fed into the shading. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shader` | Shader | Shader stream — connect the surface being processed (in) or pass it on (out). |
| `To AgX` | Shader | Shader stream. |
| `Combined` | Color (RGBA) | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |
| `Alpha` | Float | Opacity (0 = fully transparent, 1 = fully opaque). |
| `Toon Mask` | Color (RGBA) | Mask isolating a region (0–1). |
| `Post Toon Mask` | Color (RGBA) | Mask isolating a region (0–1). |

---

### Simple Pantyhose

Quick stylised pantyhose/stocking layer for legs.

**Menu:** `Add Shader > LSCherry > Simple Pantyhose`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `-- DEPRECATED --` | Shader | — | — | Shader stream. |
| `Enable Dot` | Boolean | Off | — | Toggle for this option. |
| `UV` | Vector | (0, 0, 0) | -∞ – ∞ | UV texture coordinates used to sample maps for this node. |
| `Base Color` | Color (RGBA) | (0.6858, 0.6858, 0.6858, 1) | — | The surface's lit (fully-illuminated) albedo color. |
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

### Simple Randomize

Adds quick per-object randomisation (color/value) for variation.

**Menu:** `Add Shader > LSCherry > Simple Randomize`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Seed` | Integer | 42 | 0 – 2147483647 | Random seed; change it to get a different variation of the procedural result. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Random` | Float | Scalar value. |

---

### Simple Toon

Minimal one-node toon shader — the fastest starting point.

**Menu:** `Add Shader > LSCherry > Simple Toon`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `AO Fac` | Float | 1 | 0–1 (factor) | Scalar value. |
| `Roughness` | Float | 0 | 0–1 (factor) | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |
| `Use Diffuse` | Boolean | On | — | Toggle for this option. |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Toon` | Color (RGBA) | Color value. |

---

### Stack Next Toon

Adds the next layer onto a stacked-toon chain.

**Menu:** `Add Shader > LSCherry > Stack Next Toon`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Shading` | Color (RGBA) | (0, 0, 0, 1) | — | Incoming shading/lighting term used by this node. |
| `Color` | Color (RGBA) | (1, 0, 0.002265, 1) | — | Color input/output for this operation. |
| `Stack` | Color (RGBA) | (0, 1, 0.01865, 1) | — | Color value. |
| `Size` | Float | 1 | 0.2–1 (factor) | Size of the feature (dot, cell, highlight, …); larger values enlarge it. |
| `Smooth` | Float | 0.05 | 0–1 (factor) | Softness of the transition edge — 0 is a hard toon step, higher feathers it. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shading` | Color (RGBA) | Incoming shading/lighting term used by this node. |
| `Stack` | Color (RGBA) | Color value. |

---

### Stacked Toon Builder

Entry point for the stacked (multi-layer) toon system.

**Menu:** `Add Shader > LSCherry > Stacked Toon Builder`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Pattern` | Color (RGBA) | (1, 1, 1, 1) | — | Pattern color/mask multiplied into the surface (connect a Plugin pattern node here). |
| `Enable Dot` | Boolean | Off | — | Toggle for this option. |
| `Normal` | Vector | (0, 0, 0) | -10000 – 10000 | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shading` | Color (RGBA) | Incoming shading/lighting term used by this node. |
