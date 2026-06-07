# LSCherry — Starters / Strinova

**Menu path:** `Add Shader > LSCherry > Starters > Strinova`

> 17 node(s) in this category. Socket types, defaults and ranges below are extracted directly from the compiled node source — they are the ground truth.

Ready-made starting setups for *Strinova* character materials. `* Starter` nodes are complete per-part shaders (face, hair, body, skin, weapon); `* Resolver` nodes wire up the standard texture set for a part; `* Bundle` nodes pack groups of related ramp/shadow/SSS values into a single Bundle connection to keep the graph tidy.

## When to use it

- Shading a ripped Strinova character quickly with the intended look.
- A worked reference for how the LSCherry building blocks fit together for a real character.

## How to use it

1. Add the `* Starter` for the part you are shading and connect its output to the Material Output.
2. Feed the part's textures through the matching `* Textures Resolver`.
3. Tune ramps/shadows via the `* Bundle` inputs.

## Node reference

### Strinova: Body Starter

Complete starting shader for a Strinova character body.

**Menu:** `Add Shader > LSCherry > Starters > Strinova > Strinova: Body Starter`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Shadow Bundle` | Bundle | — | — | Bundle socket grouping several related values passed as one connection. |
| `SSS Bundle` | Bundle | — | — | Bundle socket grouping several related values passed as one connection. |
| `Mask_1 Range Bundle` | Bundle | — | — | Ramp range stop — position of a band edge in the generated color ramp. |
| `Mask_2 Range Bundle` | Bundle | — | — | Ramp range stop — position of a band edge in the generated color ramp. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shader` | Shader | Shader stream — connect the surface being processed (in) or pass it on (out). |
| `To AgrX` | Shader | Secondary shader stream routed to an AgX / view-transform path. |
| `Combined` | Color (RGBA) | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |
| `Diffuse Mask` | Color (RGBA) | Mask of the diffuse-lit region. |

---

### Strinova: Body Textures Resolver

Wires the standard body texture set into the body shader.

**Menu:** `Add Shader > LSCherry > Starters > Strinova > Strinova: Body Textures Resolver`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Shadow Bundle` | Bundle | — | — | Bundle socket grouping several related values passed as one connection. |
| `SSS Bundle` | Bundle | — | — | Bundle socket grouping several related values passed as one connection. |
| `Mask_1 Range Bundle` | Bundle | — | — | Ramp range stop — position of a band edge in the generated color ramp. |
| `Mask_2 Range Bundle` | Bundle | — | — | Ramp range stop — position of a band edge in the generated color ramp. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Base Color` | Color (RGBA) | The surface's lit (fully-illuminated) albedo color. |
| `Shadow Color` | Color (RGBA) | Color used in the shadow / shaded band of the toon step. |
| `SSS Color` | Color (RGBA) | Subsurface-scattering tint applied in the deepest shadow band. |
| `Normal` | Vector | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |
| `Enable Custom Ramp` | Boolean | When on, use the supplied Custom Ramp instead of the internal ramp. |
| `Custom Ramp` | Color (RGBA) | User-supplied ramp color that overrides the built-in toon ramp. |

---

### Strinova: Face Starter

Quick build Strinova face material

**Menu:** `Add Shader > LSCherry > Starters > Strinova > Strinova: Face Starter`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Shadow Color` | Color (RGBA) | (0.8469, 0.6939, 0.6105, 1) | — | Color used in the shadow / shaded band of the toon step. |
| `SSS Color` | Color (RGBA) | (0.4735, 0.0865, 0, 1) | — | Subsurface-scattering tint applied in the deepest shadow band. |
| `Alpha` | Float | 1 | 0–1 (factor) | Opacity (0 = fully transparent, 1 = fully opaque). |
| `Normal` | Vector | (0, 0, 0) | -∞ – ∞ | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shader` | Shader | Shader stream — connect the surface being processed (in) or pass it on (out). |
| `To AgrX` | Shader | Secondary shader stream routed to an AgX / view-transform path. |
| `Combined` | Color (RGBA) | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |
| `Diffuse Mask` | Color (RGBA) | Mask of the diffuse-lit region. |

---

### Strinova: Face Textures Resolver

Quick build Strinova face material

**Menu:** `Add Shader > LSCherry > Starters > Strinova > Strinova: Face Textures Resolver`

**Inputs**

_None._


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Base Color` | Color (RGBA) | The surface's lit (fully-illuminated) albedo color. |
| `Custom Ramp` | Color (RGBA) | User-supplied ramp color that overrides the built-in toon ramp. |

---

### Strinova: Hair Starter

Complete starting shader for Strinova hair.

**Menu:** `Add Shader > LSCherry > Starters > Strinova > Strinova: Hair Starter`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Shadow Bundle` | Bundle | — | — | Bundle socket grouping several related values passed as one connection. |
| `SSS Bundle` | Bundle | — | — | Bundle socket grouping several related values passed as one connection. |
| `Mask_1 Range Bundle` | Bundle | — | — | Ramp range stop — position of a band edge in the generated color ramp. |
| `Mask_2 Range Bundle` | Bundle | — | — | Ramp range stop — position of a band edge in the generated color ramp. |
| `Highlight Color` | Color (RGBA) | (1, 1, 1, 1) | — | Color value for this slot. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shader` | Shader | Shader stream — connect the surface being processed (in) or pass it on (out). |
| `To AgrX` | Shader | Secondary shader stream routed to an AgX / view-transform path. |
| `Combined` | Color (RGBA) | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |
| `Diffuse Mask` | Color (RGBA) | Mask of the diffuse-lit region. |

---

### Strinova: Hair Textures Resolver

Wires the standard hair texture set into the hair shader.

**Menu:** `Add Shader > LSCherry > Starters > Strinova > Strinova: Hair Textures Resolver`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Shadow Bundle` | Bundle | — | — | Bundle socket grouping several related values passed as one connection. |
| `SSS Bundle` | Bundle | — | — | Bundle socket grouping several related values passed as one connection. |
| `Mask_1 Range Bundle` | Bundle | — | — | Ramp range stop — position of a band edge in the generated color ramp. |
| `Mask_2 Range Bundle` | Bundle | — | — | Ramp range stop — position of a band edge in the generated color ramp. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Base Color` | Color (RGBA) | The surface's lit (fully-illuminated) albedo color. |
| `Shadow Color` | Color (RGBA) | Color used in the shadow / shaded band of the toon step. |
| `SSS Color` | Color (RGBA) | Subsurface-scattering tint applied in the deepest shadow band. |
| `Normal` | Vector | Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map. |
| `Enable Custom Ramp` | Boolean | When on, use the supplied Custom Ramp instead of the internal ramp. |
| `Custom Ramp` | Color (RGBA) | User-supplied ramp color that overrides the built-in toon ramp. |
| `Highlight Mask` | Float | Mask isolating a region (0–1). |

---

### Strinova: Mask_1 Range Body Bundle

Bundles the Mask 1 ramp ranges for the body into one connection.

**Menu:** `Add Shader > LSCherry > Starters > Strinova > Strinova: Mask_1 Range Body Bundle`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Range 1` | Float | 0.05 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 2` | Float | 0.2 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 3` | Float | 0.35 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 4` | Float | 0.55 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Mask_1 Range Bundle` | Bundle | Ramp range stop — position of a band edge in the generated color ramp. |

---

### Strinova: Mask_1 Range Hair Bundle

Bundles the Mask 1 ramp ranges for the hair into one connection.

**Menu:** `Add Shader > LSCherry > Starters > Strinova > Strinova: Mask_1 Range Hair Bundle`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Range 1` | Float | 0.01 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 2` | Float | 0.4 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 3` | Float | 1 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Mask_1 Range Bundle` | Bundle | Ramp range stop — position of a band edge in the generated color ramp. |

---

### Strinova: Mask_2 Range Body Bundle

Bundles the Mask 2 ramp ranges for the body into one connection.

**Menu:** `Add Shader > LSCherry > Starters > Strinova > Strinova: Mask_2 Range Body Bundle`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Range 1` | Float | 0.1 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 2` | Float | 0.4 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 3` | Float | 0.7 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 4` | Float | 1 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Mask_2 Range Bundle` | Bundle | Ramp range stop — position of a band edge in the generated color ramp. |

---

### Strinova: Mask_2 Range Hair Bundle

Bundles the Mask 2 ramp ranges for the hair into one connection.

**Menu:** `Add Shader > LSCherry > Starters > Strinova > Strinova: Mask_2 Range Hair Bundle`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Range 1` | Float | 0.01 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 2` | Float | 0.4 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 3` | Float | 0.9 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |
| `Range 4` | Float | 1 | 0–1 (factor) | Ramp range stop — position of a band edge in the generated color ramp. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Mask_2 Range Bundle` | Bundle | Ramp range stop — position of a band edge in the generated color ramp. |

---

### Strinova: MatCap Resolver

Resolves the matcap/sphere-map inputs for Strinova materials.

**Menu:** `Add Shader > LSCherry > Starters > Strinova > Strinova: MatCap Resolver`

**Inputs**

_None._


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Top-Left` | Color (RGBA) | Color value. |
| `Top-Right` | Color (RGBA) | Color value. |
| `Down-Left` | Color (RGBA) | Color value. |
| `Down-Right` | Color (RGBA) | Color value. |

---

### Strinova: Shadow Body Bundle

Bundles the body shadow settings into one connection.

**Menu:** `Add Shader > LSCherry > Starters > Strinova > Strinova: Shadow Body Bundle`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Map 1` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 2` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 3` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 4` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 5` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shadow Bundle` | Bundle | Bundle socket grouping several related values passed as one connection. |

---

### Strinova: Shadow Hair Bundle

Bundles the hair shadow settings into one connection.

**Menu:** `Add Shader > LSCherry > Starters > Strinova > Strinova: Shadow Hair Bundle`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Map 1` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 2` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 3` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shadow Bundle` | Bundle | Bundle socket grouping several related values passed as one connection. |

---

### Strinova: Skin Starter

Complete starting shader for Strinova skin.

**Menu:** `Add Shader > LSCherry > Starters > Strinova > Strinova: Skin Starter`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Shadow Color` | Color (RGBA) | (0.8469, 0.6939, 0.6105, 1) | — | Color used in the shadow / shaded band of the toon step. |
| `SSS Color` | Color (RGBA) | (0.4735, 0.0865, 0, 1) | — | Subsurface-scattering tint applied in the deepest shadow band. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shader` | Shader | Shader stream — connect the surface being processed (in) or pass it on (out). |
| `To AgrX` | Shader | Secondary shader stream routed to an AgX / view-transform path. |
| `Combined` | Color (RGBA) | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |
| `Diffuse Mask` | Color (RGBA) | Mask of the diffuse-lit region. |

---

### Strinova: SSS Body Bundle

Bundles the body subsurface (SSS) settings into one connection.

**Menu:** `Add Shader > LSCherry > Starters > Strinova > Strinova: SSS Body Bundle`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Map 1` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 2` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 3` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 4` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 5` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `SSS Bundle` | Bundle | Bundle socket grouping several related values passed as one connection. |

---

### Strinova: SSS Hair Bundle

Bundles the hair subsurface (SSS) settings into one connection.

**Menu:** `Add Shader > LSCherry > Starters > Strinova > Strinova: SSS Hair Bundle`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Map 1` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 2` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |
| `Map 3` | Color (RGBA) | (0, 0, 0, 1) | — | Ramp color stop — one color of the generated toon ramp. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `SSS Bundle` | Bundle | Bundle socket grouping several related values passed as one connection. |

---

### Strinova: Weapon Starter

Complete starting shader for Strinova weapons.

**Menu:** `Add Shader > LSCherry > Starters > Strinova > Strinova: Weapon Starter`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Shadow Color` | Color (RGBA) | (0.7874, 0.7874, 0.7874, 1) | — | Color used in the shadow / shaded band of the toon step. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Shader` | Shader | Shader stream — connect the surface being processed (in) or pass it on (out). |
| `To AgrX` | Shader | Secondary shader stream routed to an AgX / view-transform path. |
| `Combined` | Color (RGBA) | Flat combined color (all shading baked into RGB), ready for compositing or further color work. |
| `Diffuse Mask` | Color (RGBA) | Mask of the diffuse-lit region. |
