# LSCherry — External / Michos / Honkai Impact 3

**Menu path:** `Add Shader > LSCherry > External > Michos > Honkai Impact 3`

Character shader nodes for Honkai Impact 3rd, contributed by the Michos pipeline. These nodes implement HI3's toon shading model with the game's specific lightmap conventions and character shading features.

---

## Texture Conventions

Honkai Impact 3rd uses a lightmap packing similar to Genshin but with slight differences per character type:

| Channel | Data |
|---|---|
| R | Shadow AO / ambient occlusion |
| G | Specular / ramp index |
| B | Outline thickness / material ID |
| A | Emission / glow mask |

---

## Package Builder

### `HI3_BuildBodyPackage`

The primary all-in-one node for an HI3 character body material. Wires up all standard HI3 shading passes from a set of texture inputs.

**Inputs:**
- `Diffuse` — base color texture
- `Lightmap` — packed RGBA lightmap
- `Normal Map` — tangent-space normal
- `Shadow Ramp` — color ramp for shadow graduation
- `Shadow Color` — toon shadow tint
- `Specular Color` — specular highlight tint
- `Outline Color` — outline tint

**Outputs:** `Shader`

---

## Component Nodes

HI3 provides a parallel set of individual component nodes for custom material assembly. 12 nodes total cover:

- Shadow from lightmap
- Outline from lightmap
- Specular layer
- Hair highlight
- Body color derivation
- Emission mask application
- Rim light
- Face-specific shading

Browse `Add Shader > LSCherry > External > Michos > Honkai Impact 3` for the complete list.

---

## Typical Setup

```
[Diffuse]   ──┐
[Lightmap]  ──┤── HI3_BuildBodyPackage ──► Material Output
[Normal]    ──┘
[Shadow Ramp]
```
