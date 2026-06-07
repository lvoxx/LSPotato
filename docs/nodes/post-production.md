# LSCherry — Post Production

**Menu path:** `Add Shader > LSCherry > Post Production`

Nodes applied after the main toon shader is built. They add specular layers, hair highlights, tone mapping, body tints, and utility effects on top of a completed `Shader` input.

---

## Specular Layers

### `AddCoreSpecular`

Applies a core specular highlight on top of the base toon shader.

**Inputs:** `Shader`, `Specular Color`, `Roughness`, `Strength`  
**Outputs:** `Shader`

### `AddDotSpecular`

Adds a dot-shaped specular highlight.

**Inputs:** `Shader`, `Color`, `Dot Size`, `Strength`  
**Outputs:** `Shader`

### `AddSpecular`

General-purpose specular layer with selectable style.

**Inputs:** `Shader`, `Color`, `Roughness`, `Strength`  
**Outputs:** `Shader`

---

## Hair Highlights

### `AddHighlight`

Generic highlight addition — works on any surface, not just hair.

**Inputs:** `Shader`, `Color`, `Strength`  
**Outputs:** `Shader`

### `AddFrequentHairHighlight`

High-frequency hair specular — fine, repeated highlights for a silky or straight hair appearance.

**Inputs:** `Shader`, `Color`, `Frequency`, `Strength`  
**Outputs:** `Shader`

### `AddRandomToonHighlight`

Randomized toon highlight. Each object instance gets a slightly different highlight position, useful for stylized crowds or multiple hair clumps.

**Inputs:** `Shader`, `Color`, `Strength`  
**Outputs:** `Shader`

### `AddToonHighlight`

Standard toon-stylized hair highlight. Applies a hard-edged specular band along the hair normal direction.

**Inputs:** `Shader`, `Color`, `Band Position`, `Sharpness`, `Strength`  
**Outputs:** `Shader`

### `AddHighlightFromLightmap`

Drives highlight placement and intensity from a lightmap channel rather than a realtime calculation.

**Inputs:** `Shader`, `Lightmap`, `Color`, `Strength`  
**Outputs:** `Shader`

### `AddHighlightFromSpheremap`

Uses a sphere map (matcap) to add environment-based highlights. Produces realistic-looking light bands for metallic hair or polished surfaces.

**Inputs:** `Shader`, `Sphere Map`, `Strength`  
**Outputs:** `Shader`

---

## Body Tinting

### `AddTintVBody`

Tints the body shader based on a vertical (Y-axis) gradient. Useful for sky-to-ground ambient occlusion color shifts.

**Inputs:** `Shader`, `Tint Color`, `Gradient Start`, `Gradient End`, `Strength`  
**Outputs:** `Shader`

### `AddInvertTintVBody`

Inverted vertical body tint — strongest at the bottom of the gradient rather than the top.

**Inputs:** `Shader`, `Tint Color`, `Gradient Start`, `Gradient End`, `Strength`  
**Outputs:** `Shader`

---

## Tone Mapping

### `QuickToFilmic`

Fast conversion from linear to filmic tone mapping. Lower quality but cheaper to evaluate.

**Inputs:** `Shader`  
**Outputs:** `Shader`

### `StandardToFilmic`

Full-quality filmic tone mapping conversion with configurable exposure and contrast.

**Inputs:** `Shader`, `Exposure`, `Contrast`  
**Outputs:** `Shader`

---

## Utility

### `RandomColor`

Per-instance color randomization based on the object's random ID. Use in crowd/duplicate scenes.

**Inputs:** `Shader`, `Color Range`  
**Outputs:** `Shader`

### `DisableAllShader`

Replaces the shader with a transparent/black result. Useful for debugging which shader nodes contribute to the final result, or for masking entire sections during development.

**Inputs:** `Shader`  
**Outputs:** `Shader` (zeroed)
