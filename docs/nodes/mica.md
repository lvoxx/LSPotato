# LSCherry — MICA

**Menu path:** `Add Shader > LSCherry > MICA`

Shader nodes for MICA / Girls' Frontline 2: Exilium (GF2) character shading.

---

## `GF2_StandardBuiltIn`

The standard built-in shader for GF2 characters. Implements GF2's shading model: toon-stepped diffuse, lightmap-driven specular and outline, and the game's specific normal-map conventions.

**Inputs:**
- `Diffuse` — base color/albedo texture
- `Lightmap` — packed RGBA lightmap (R=shadow AO, G=specular, B=outline thickness, A=emission)
- `Normal Map` — tangent-space normal map
- `Detail Normal` — optional detail normal map for fine surface texture
- `Shadow Color` — toon shadow tint
- `Specular Color` — specular highlight tint
- `Outline Color` — outline tint color
- `Emission Strength` — emission intensity multiplier

**Outputs:** `Shader`

---

## Typical Setup

```
[Diffuse Texture]  ──┐
[Lightmap Texture] ──┤── GF2_StandardBuiltIn ──► Material Output
[Normal Map]       ──┘
```

The `GF2_StandardBuiltIn` node handles all major shading passes in a single node. Adjust `Shadow Color`, `Specular Color`, and `Outline Color` to match individual character variants.
