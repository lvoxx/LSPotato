# LSCherry — MMD (External)

**Menu path:** `Add Shader > LSCherry > External`

> 1 node(s) in this category. Socket types, defaults and ranges below are extracted directly from the compiled node source — they are the ground truth.

MMD-style MatCap UV generator. Appears under the **External** submenu.

## When to use it

- Reproducing MMD/MME matcap (sphere-map) shading on imported models.

## How to use it

1. Use the output UVs to sample a matcap texture, then add it to your surface.

## Node reference

### MMD: MatCapUV

Generates MMD-style matcap (sphere-map) UVs.

**Menu:** `Add Shader > LSCherry > External > MMD: MatCapUV`

**Inputs**

_None._


**Outputs**

| Output | Type | Description |
|---|---|---|
| `ToonUV` | Vector | UV coordinates. |
| `SphereUV` | Vector | UV coordinates. |
