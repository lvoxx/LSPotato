# LSCherry — Core

**Menu path:** `Add Shader > LSCherry > Core`

Core toon shading nodes: step thresholds, halftone dots, outlines, specular types, rim lights, and emission masks. These are the building blocks that more complex nodes like `MakeToon` are assembled from.

---

## Outline

### `AddOutline`

Adds a camera-space outline to the mesh using normal/depth edge detection.

**Inputs:** `Shader`, `Color`, `Thickness`  
**Outputs:** `Shader`

### `AddOutlineFromLightmap`

Drives outline thickness from a lightmap channel instead of a fixed value. Allows per-UV outline control baked into the lightmap.

**Inputs:** `Shader`, `Color`, `Lightmap Channel`  
**Outputs:** `Shader`

---

## Toon Dots (Halftone)

### `SimpleToonDot`

Simple halftone/dot toon effect. Single-threshold dot pattern.

**Inputs:** `Shader`, `Dot Size`, `Threshold`  
**Outputs:** `Shader`

### `ToonDot`

Full halftone dot effect with separate controls for dot size, density, and threshold.

**Inputs:** `Shader`, `Dot Size`, `Density`, `Threshold`  
**Outputs:** `Shader`

### `InvertedToonDot`

Inverted dot pattern — dots appear in lit areas instead of shadow areas.

**Inputs:** `Shader`, `Dot Size`, `Threshold`  
**Outputs:** `Shader`

### `SimpleBackToonDot`

Applies the dot toon effect to back-facing geometry only. Used for inner-outline or subsurface-style shading on back faces.

**Inputs:** `Shader`, `Dot Size`, `Threshold`  
**Outputs:** `Shader`

---

## Toon Shading

### `ToonCore`

Main toon step/threshold calculation. Converts a diffuse gradient into a hard-edged toon step.

**Inputs:** `Diffuse`, `Shadow Threshold`, `Shadow Softness`, `Shadow Color`, `Base Color`  
**Outputs:** `Color`, `Shadow Mask`

### `Toon3s`

Multi-stage toon with three distinct shading bands: lit, mid-shadow, and deep shadow. Each band has its own color and threshold.

**Inputs:** `Diffuse`, three `Threshold`/`Color` pairs  
**Outputs:** `Color`, `Shadow Mask`

---

## Specular

### `SpecularCore`

Core specular highlight calculation. Produces a toon-compatible specular mask.

**Inputs:** `View Vector`, `Normal`, `Roughness`, `Strength`  
**Outputs:** `Specular Mask`

### `SpecularDot`

Dot-shaped specular — produces a discrete dot in the specular position instead of a smooth highlight.

**Inputs:** `View Vector`, `Normal`, `Dot Size`, `Strength`  
**Outputs:** `Specular Mask`

### `ToonSpec`

Toon-stylized specular. Applies a hard step to the specular gradient for a cartoon look.

**Inputs:** `Shader`, `Specular Color`, `Roughness`, `Strength`  
**Outputs:** `Shader`

### `ToonMetal`

Metallic toon shading. Combines environment reflection with toon-stepped diffuse for a stylized metal surface.

**Inputs:** `Shader`, `Color`, `Roughness`, `Metal Strength`  
**Outputs:** `Shader`

### `ToonGlossy`

Glossy toon reflection. Uses a blurred environment sample combined with a toon step.

**Inputs:** `Shader`, `Color`, `Roughness`  
**Outputs:** `Shader`

### `ReflectiveToon`

Toon shader with environment reflection blended in. Useful for character eyes, shiny buttons, or any specular surface needing both toon shading and reflectivity.

**Inputs:** `Shader`, `Reflection Strength`, `Roughness`  
**Outputs:** `Shader`

### `ToonRay`

Ray-based toon shading using the output of `MakeRay`. Provides more physically accurate directional shading than `ToonCore`.

**Inputs:** `Ray Data` (from `MakeRay`), `Threshold`, `Color`  
**Outputs:** `Shader`

---

## Rim and Emission

### `RimCore`

Rim light calculation. Produces a rim-light mask based on view/normal angle.

**Inputs:** `Strength`, `Sharpness`, `Color`  
**Outputs:** `Rim Mask`, `Shader`

### `EmissionMask`

Generates a selective emission mask from a lightmap channel or a manually driven input. Use to make specific areas of a character glow (eyes, FX accents, etc.).

**Inputs:** `Emission Source`, `Strength`, `Color`  
**Outputs:** `Emission Shader`
