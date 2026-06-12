# LSCherry — AVR (External)

**Menu path:** `Add Shader > LSCherry > External`

> 1 node(s) in this category. Socket types, defaults and ranges below are extracted directly from the compiled node source — they are the ground truth.

AVR-contributed metal ramp effect. Appears under the **External** submenu.

## When to use it

- Stylised metal banding on props and armour.

## How to use it

1. Add from `Add Shader > LSCherry > External` and mix its output into a metal surface.

## Node reference

### AVR: Metal Ramp

AVR stylised metal banding ramp.

**Menu:** `Add Shader > LSCherry > External > AVR: Metal Ramp`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Use Dot` | Boolean | Off | — | Toggle for this option. |
| `Roughness` | Float | 0.392 | 0–1 (factor) | Microsurface roughness — lower is sharper/glossier, higher is more diffuse. |
| `Scale` | Float | 4.01 | 0 – 100 | Scale of the pattern / texture — higher values tile it more densely. |
| `Distortion` | Float | 1 | 0 – 100 | Amount of procedural distortion / warping applied. |
| `Value Enhance` | Float | 0.1 | 0–1 (factor) | Boosts the value/contrast of the result. |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shader` | Shader | Shader stream — connect the surface being processed (in) or pass it on (out). |
| `Ramp` | Color (RGBA) | Color value. |
