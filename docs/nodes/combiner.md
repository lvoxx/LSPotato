# LSCherry — Combiner

**Menu path:** `Add Shader > LSCherry > Combiner`

Nodes that blend colors, masks, and shader layers together. Used to layer toon effects onto a base shader or combine lighting data.

---

## `AddFakeBrightColor`

Blends a stylized bright/highlight color into the base result using a mask and a blend factor.

**Inputs:** `Base`, `Bright Color`, `Mask`, `Factor`  
**Outputs:** `Color`

---

## `AddFakeShadowColor`

Adds a shadow-color variation for stylized self-shadowing on top of an existing shader.

**Inputs:** `Base`, `Shadow Color`, `Mask`, `Factor`  
**Outputs:** `Color`

---

## `AddTransparent`

Blends a transparency layer into the current shader using alpha and a mask.

**Inputs:** `Shader`, `Alpha`, `Mask`  
**Outputs:** `Shader`

---

## `BlendColor`

General-purpose color blend with selectable blend mode and factor control.

**Inputs:** `Color 1`, `Color 2`, `Mode`, `Factor`  
**Outputs:** `Color`

---

## `GetLightArea`

Extracts the lit-area mask from the current shading data using the main light vector and surface normal.

**Outputs:** `Light Area` — float mask (0 = shadow, 1 = lit)
