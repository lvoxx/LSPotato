# LSCherry — GloTAni (External)

**Menu path:** `Add Shader > LSCherry > External`

> 1 node(s) in this category. Socket types, defaults and ranges below are extracted directly from the compiled node source — they are the ground truth.

GloTAni stylized glass shader. Appears under the **External** submenu.

## When to use it

- Stylised transparent glass/crystal surfaces that still read as toon.

## How to use it

1. Connect its output to the Material Output; tune transparency/tint inputs.

## Node reference

### GloTAni: Stylized Glass

Stylised toon-compatible glass/crystal surface shader.

**Menu:** `Add Shader > LSCherry > External > GloTAni: Stylized Glass`


Inputs are grouped into collapsible panels in the N-panel: **Gradient**; **Steaks**.

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Factor` | Float | 1 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color input/output for this operation. |
| `Emission Strength` | Float | 1.2 | 0 – 50 | Multiplier for the emission color's brightness. |
| `Fill` | Float | 0.4 | 0–1 (factor) | Scalar value. |
| `Sharpness` | Float | 0.02 | 0–1 (factor) | Scalar value. |
| `Refrection` | Float | 0 | 0–1 (factor) | Scalar value. |
| `Opacity` | Float | 0.5 | 0–1 (factor) | Scalar value. |
| `Rotation` | Float | 45 | -360–360 (factor) | Scalar value. |
| `Density` | Float | 6.5 | 0 – 25 | Scalar value. |
| `Seed` | Float | 0 | 0 – 200 | Random seed; change it to get a different variation of the procedural result. |
| `Opacity` | Float | 0.2 | 0–1 (factor) | Scalar value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shader` | Shader | Shader stream — connect the surface being processed (in) or pass it on (out). |
