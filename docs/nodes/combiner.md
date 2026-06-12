# LSCherry — Combiner

**Menu path:** `Add Shader > LSCherry > Combiner`

> 5 node(s) in this category. Socket types, defaults and ranges below are extracted directly from the compiled node source — they are the ground truth.

Color/shader blending helpers used to layer extra tints onto a toon result — fake bright and shadow colors, transparency mixing, generic color blending, and a light-area extractor. They are the glue between the Core shading terms and the final surface.

## When to use it

- Pushing extra warmth into lit areas or coolness into shadows without re-authoring the ramp.
- Mixing a transparent pass into an otherwise opaque toon surface.
- Deriving a light/shadow mask to drive other effects.

## How to use it

1. Insert between your shading nodes and the material output.
2. Use `Get Light Area` to produce a mask, then feed it into the `Fac` of another blend.

## Node reference

### Add Fake Bright Color

Injects an artificial bright tint into lit areas to fake bounce/rim warmth.

**Menu:** `Add Shader > LSCherry > Combiner > Add Fake Bright Color`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Original Color` | Color (RGBA) | (1, 1, 1, 1) | — | The unmodified input color, passed through for reference or re-mixing. |
| `Factor` | Float | 0 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Bright Mask` | Float | 0 | 0–1 (factor) | Mask isolating a region (0–1). |
| `Bright Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color injected into the brightest / lit area. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Color` | Color (RGBA) | Color input/output for this operation. |

---

### Add Fake Shadow Color

Injects an artificial tint into shadow areas for richer, art-directed shadows.

**Menu:** `Add Shader > LSCherry > Combiner > Add Fake Shadow Color`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Original Color` | Color (RGBA) | (1, 1, 1, 1) | — | The unmodified input color, passed through for reference or re-mixing. |
| `Factor` | Float | 0 | 0–1 (factor) | Blend factor (0 = first/original input, 1 = full effect). |
| `Shadow Mask` | Float | 0 | 0–1 (factor) | Mask isolating the shaded region (1 in shadow, 0 in light). |
| `Shadow Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color used in the shadow / shaded band of the toon step. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Color` | Color (RGBA) | Color input/output for this operation. |

---

### Add Transparent

Mixes a transparent pass into the shader to fade or cut out regions.

**Menu:** `Add Shader > LSCherry > Combiner > Add Transparent`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Fac` | Float | 0.5 | 0 – 1 | Blend factor (0 = first/original input, 1 = full effect). |
| `Combined` | Color (RGBA) | (0, 0, 0, 1) | — | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shader` | Shader | Shader stream — connect the surface being processed (in) or pass it on (out). |

---

### Blend Color

General two-color blend with a factor — the workhorse mixer.

**Menu:** `Add Shader > LSCherry > Combiner > Blend Color`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Mix` | Float | 1 | 0–1 (factor) | Scalar value. |
| `Base Color` | Color (RGBA) | (1, 1, 1, 1) | — | The surface's lit (fully-illuminated) albedo color. |
| `Outer Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color value for this slot. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Blend Color` | Color (RGBA) | Color value for this slot. |

---

### Get Light Area

Extracts a light/shadow mask from the shading, for driving other effects.

**Menu:** `Add Shader > LSCherry > Combiner > Get Light Area`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Mask` | Float | 0.5 | 0–1 (factor) | Mask isolating a region (0–1). |
| `Shading` | Float | 0 | -∞ – ∞ | Incoming shading/lighting term used by this node. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Fixed Shading` | Float | Scalar value. |
