# LSCherry — External / Michos / Honkai Star Rail

**Menu path:** `Add Shader > LSCherry > External > Michos > Honkai Star Rail`

Character shader nodes for Honkai Star Rail, contributed by the Michos pipeline. These implement HSR's distinct shading model, which uses a ramp-texture approach for shadow graduation rather than a hard step threshold.

---

## Texture Conventions

Honkai Star Rail's lightmap packing:

| Channel | Data |
|---|---|
| R | Shadow AO |
| G | Specular mask |
| B | Ramp row index (selects shadow ramp row) |
| A | Emission |

The B channel ramp-row index is unique to HSR — it selects a specific horizontal row from a 2D ramp texture, allowing per-surface shadow color variation from a single texture.

---

## Package Builder

### `HSR_BuildBodyPackage`

All-in-one node for an HSR character body material.

**Inputs:**
- `Diffuse` — base color texture
- `Lightmap` — packed RGBA lightmap
- `Normal Map` — tangent-space normal
- `Shadow Ramp` — 2D ramp texture (rows = material type, columns = shadow gradient)
- `Warm Shadow Color` — warm-toned shadow tint
- `Cool Shadow Color` — cool-toned shadow tint
- `Specular Color` — specular highlight tint
- `Outline Color` — outline tint

**Outputs:** `Shader`

---

## Component Nodes

13 nodes total, covering:

- Shadow from lightmap with ramp-row selection
- Outline from lightmap
- Specular with HSR-style soft edge
- Hair highlight (two variants)
- Face shadow with SDF (signed distance field) technique
- Emission mask
- Rim light with scene color influence
- Body color derivation

Browse `Add Shader > LSCherry > External > Michos > Honkai Star Rail` for the complete list.

---

## Typical Setup

```
[Diffuse]     ──┐
[Lightmap]    ──┤── HSR_BuildBodyPackage ──► Material Output
[Normal]      ──┤
[Shadow Ramp] ──┘
```

The 2D `Shadow Ramp` texture is critical for HSR's look — the B channel of the lightmap indexes into it to produce the characteristic warm/cool shadow graduation per material zone.
