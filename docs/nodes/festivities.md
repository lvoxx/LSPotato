# LSCherry — Festivities

**Menu path:** `Add Shader > LSCherry > Festivities`

Genshin Impact PBR nodes from the Festivities collection. These implement a physically-based rendering pipeline inspired by Genshin Impact's in-game shading, with scene interaction and SMBE (Specular, Metallic, Bump, Emission) texture conventions.

---

## `FesGI_GenshinPBR_SMBE`

Full Genshin Impact-style PBR shader using an SMBE-packed texture. Handles specular, metallic, bump, and emission from a single RGBA texture map.

**Inputs:**
- `Diffuse` — base color/albedo texture
- `SMBE` — packed RGBA texture (R=Specular, G=Metallic, B=Bump, A=Emission)
- `Normal Map` — tangent-space normal map
- `Roughness` — roughness override
- `Emission Strength` — emission intensity multiplier

**Outputs:** `Shader`

---

## `FesGI_CombineSMBEAndScene`

Merges the SMBE PBR data with scene lighting (world and sun). Used as an intermediate step between `FesGI_GenshinPBR_SMBE` and the final material output.

**Inputs:**
- `PBR Shader` — output of `FesGI_GenshinPBR_SMBE`
- `Scene Light` — scene light data

**Outputs:** `Shader`

---

## `FesGI_SceneInteraction`

Handles Genshin Impact's scene-interaction shading effects — rim lighting from the environment, light source color tinting, and dynamic scene response.

**Inputs:**
- `Shader` — base shader to apply interaction to
- `Scene Color` — world/light color driving the interaction
- `Interaction Strength` — how strongly the scene affects the material

**Outputs:** `Shader`

---

## Typical Setup

```
[Diffuse Texture] ──┐
[SMBE Texture]   ──┤── FesGI_GenshinPBR_SMBE ──► FesGI_CombineSMBEAndScene ──► FesGI_SceneInteraction ──► Material Output
[Normal Map]     ──┘
```
