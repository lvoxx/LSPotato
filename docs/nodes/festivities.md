# LSCherry — Festivities (External)

**Menu path:** `Add Shader > LSCherry > External`

> 3 node(s) in this category. Socket types, defaults and ranges below are extracted directly from the compiled node source — they are the ground truth.

Genshin-inspired (FES_GI) PBR + scene-interaction nodes for festive/diorama scenes. Appear under the **External** submenu.

## When to use it

- Genshin-style PBR surfaces and scene/light interaction for environment shots.

## How to use it

1. Build the PBR term with `GenshinPBR - SMBE`, then combine with the scene via the scene nodes.

## Node reference

### FES_GI: Combine SMBE and Scene

Combines the SMBE PBR term with scene interaction.

**Menu:** `Add Shader > LSCherry > External > FES_GI: Combine SMBE and Scene`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `SMBE` | Shader | — | — | Shader stream. |
| `Scene` | Shader | — | — | Shader stream. |
| `Lightmap` | Color (RGBA) | (0.8, 0.8, 0.8, 1) | — | Packed lightmap texture whose channels encode shadow, specular, AO, etc. |
| `Emission Strength` | Float | 85 | 0 – 200 | Multiplier for the emission color's brightness. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shader` | Shader | Shader stream — connect the surface being processed (in) or pass it on (out). |

---

### FES_GI: GenshinPBR - SMBE

Genshin-style PBR (SMBE) surface term.

**Menu:** `Add Shader > LSCherry > External > FES_GI: GenshinPBR - SMBE`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Base` | Color (RGBA) | (1, 1, 1, 1) | — | Color value. |
| `Base Alpha` | Float | 1 | 0–1 (factor) | Opacity / alpha value. |
| `SMBE` | Color (RGBA) | (0, 0, 0, 1) | — | Color value. |
| `SMBE Alpha` | Float | 0 | 0–1 (factor) | Opacity / alpha value. |
| `Emission Strength` | Float | 1 | -∞–∞ (factor) | Multiplier for the emission color's brightness. |
| `Mix Diffuse with Emission` | Float | 0 | 0–1 (factor) | Scalar value. |
| `Emission Tint` | Color (RGBA) | (1, 1, 1, 1) | — | Color value. |
| `Normal` | Color (RGBA) | (0, 0, 0, 1) | — | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |
| `0 = OpenGL, 1 = DirectX` | Float | 1 | 0–1 (factor) | Scalar value. |
| `Normal Strength` | Float | 1 | 0–10 (factor) | Intensity of this contribution. |
| `Height` | Color (RGBA) | (0, 0, 0, 1) | — | Color value. |
| `Height Strength` | Float | 1 | 0–1 (factor) | Intensity of this contribution. |
| `Height Distance` | Float | 0.25 | 0 – 1000 | Scalar value. |
| `----------------` | Float | 0 | -∞–∞ (factor) | Scalar value. |
| `Principled BSDF = 0, Specular BSDF = 1` | Float | 0 | 0–1 (factor) | Scalar value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `BSDF` | Shader | Shader stream. |

---

### FES_GI: Scene Interaction

Adds scene/light interaction to the festive PBR surface.

**Menu:** `Add Shader > LSCherry > External > FES_GI: Scene Interaction`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Base Color` | Color (RGBA) | (0.5, 0.5, 0.5, 1) | — | The surface's lit (fully-illuminated) albedo color. |
| `NormalMap` | Color (RGBA) | (0.5, 0.5, 1, 1) | — | Normal vector for this term. |
| `Roughness` | Float | 0.5 | 0–1 (factor) | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |
| `Metallic` | Float | 0 | 0–1 (factor) | Scalar value. |
| `Specular` | Float | 0 | 0–1 (factor) | Scalar value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Color` | Color (RGBA) | Color input/output for this operation. |
| `Emission` | Shader | Emission color added on top of the shading. |
