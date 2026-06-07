# LSCherry — MICA (External)

**Menu path:** `Add Shader > LSCherry > External`

> 1 node(s) in this category. Socket types, defaults and ranges below are extracted directly from the compiled node source — they are the ground truth.

MICA-contributed GF2 standard built-in material. Appears under the **External** submenu.

## When to use it

- A ready GF2-style material build for compatible characters.

## How to use it

1. Add it and wire the character's standard textures into its inputs.

## Node reference

### GF2: Standard Build-in

Standard GF2 materials build-in

**Menu:** `Add Shader > LSCherry > External > GF2: Standard Build-in`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Diffuse Texture` | Color (RGBA) | (0, 0, 0, 1) | — | Color value. |
| `Alpha` | Float | 1 | 0 – 1 | Opacity (0 = fully transparent, 1 = fully opaque). |
| `Spec Texture` | Color (RGBA) | (0, 0, 0, 1) | — | Color value. |
| `Normal Texture` | Vector | (0, 0, 0) | -∞ – ∞ | Normal vector for this term. |
| `Anisotropic` | Float | 0 | 0–1 (factor) | Scalar value. |
| `AO` | Float | 1 | 0–1 (factor) | Scalar value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Diffuse Texture` | Color (RGBA) | Color value. |
| `Alpha` | Float | Opacity (0 = fully transparent, 1 = fully opaque). |
| `Normal` | Vector | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |
| `Specular Color` | Color (RGBA) | Color of the specular highlight. |
| `Specular Tint` | Float | How much the specular highlight is tinted by the base color. |
| `Metal Ramp` | Color (RGBA) | Color value. |
| `Blend Metal Ramp` | Float | Scalar value. |
