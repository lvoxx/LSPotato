# LSCherry — External / Michos / Genshin Impact

**Menu path:** `Add Shader > LSCherry > External > Michos > Genshin Impact`

Character shader nodes for Genshin Impact, contributed by the Michos pipeline. These nodes implement GI's lightmap-driven toon shading model with game-accurate channel conventions.

---

## Texture Conventions

Genshin Impact uses a specific lightmap packing convention across all character textures:

| Channel | Data |
|---|---|
| R | Shadow AO / ambient occlusion |
| G | Specular intensity |
| B | Outline/edge softness (ramp-index in some cases) |
| A | Emission mask |

---

## Package Builder

### `GI_BuildBodyPackage`

The all-in-one entry point for a Genshin Impact character body material. Accepts the four standard GI textures and outputs a complete shader.

**Inputs:**
- `Diffuse` — base color texture
- `Lightmap` — packed RGBA lightmap
- `Normal Map` — tangent-space normal
- `Shadow Ramp` — 1D ramp texture for shadow color graduation
- `Shadow Color` — toon shadow tint
- `Specular Color` — specular highlight tint
- `Outline Color` — outline tint

**Outputs:** `Shader`

**Start here** for most GI body materials.

---

## Component Nodes

Use these individually when you need to override specific shading steps or compose a custom GI material.

### `GI_AddColorFromColormap`

Blends a colormap-driven color onto the base material. Used for character-specific color variation driven by a secondary texture.

**Inputs:** `Shader`, `Colormap`, `Blend Factor`  
**Outputs:** `Shader`

### `GI_AddOutlineFromLightmap`

Adds a lightmap-controlled outline. Outline thickness per-vertex is encoded in the lightmap's B channel.

**Inputs:** `Shader`, `Lightmap`, `Outline Color`, `Thickness Scale`  
**Outputs:** `Shader`

### `GI_AddShadowFromLightmap`

Applies toon shadow using the lightmap's R channel as the AO/shadow mask.

**Inputs:** `Shader`, `Lightmap`, `Shadow Ramp`, `Shadow Color`  
**Outputs:** `Shader`

### `GI_BodyColorFromLightmap`

Derives the body base color from the lightmap's channels. Used when the diffuse color is partially driven by lightmap data rather than a flat texture.

**Inputs:** `Diffuse`, `Lightmap`, `Shadow Color`  
**Outputs:** `Color`

---

## Supporting Nodes

Additional per-feature nodes (specular, face ramp, hair highlight, etc.) are available in the same menu. Browse `Add Shader > LSCherry > External > Michos > Genshin Impact` for the full list of 14 nodes.

---

## Typical Setup

```
[Diffuse]   ──┐
[Lightmap]  ──┤── GI_BuildBodyPackage ──► Material Output
[Normal]    ──┘
[Shadow Ramp]
```

For custom setups, replace `GI_BuildBodyPackage` with individual component nodes chained in order: color → shadow → outline → specular.
