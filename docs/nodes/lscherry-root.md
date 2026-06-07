# LSCherry — Root Nodes

**Menu path:** `Add Shader > LSCherry`

Top-level nodes: scene controllers, complete toon builders, and shared utility providers. They form the backbone of any LSCherry material.

---

## `LSCherryMainController`

The central controller for a full LSCherry material setup. Exposes 26 input sockets covering every major shading parameter and outputs six masks for downstream compositing.

**Inputs (grouped):**
- Base color, tint color, shadow color
- Shadow strength, highlight strength, AO strength
- Style selector (toon style index)
- Color ramp inputs (shadow ramp, highlight ramp)
- Pattern, emission toggles

**Outputs:**
- `Shader` — final toon shader
- Six mask outputs for custom compositing (specular mask, emission mask, etc.)

Use this as the spine of any complex LSCherry material. For simpler setups prefer `MakeToon` or `SimpleToon`.

---

## `MakeToon`

Builds a complete toon material in one node. Accepts pattern, emission, and style toggles.

**Outputs:** `Shader` — ready to connect to a Material Output node.

---

## `SimpleToon`

A lighter toon builder with individual toggles for AO, roughness, and diffuse blending. Good when you need predictable, controllable toon shading without the full feature set.

**Outputs:** `Shader`

---

## `SimpleMakeToon`

The fastest path to a toon result — minimal inputs, sane defaults. Good as a starting point before graduating to `MakeToon`.

**Outputs:** `Shader`

---

## `NamedProperties`

Reads five scene-level named attributes and exposes them as outputs so other nodes can consume them without duplicating the Attribute node setup.

**Outputs:**
- `Main Light Vector` — primary directional light vector
- `Back Light Vector` — secondary/back light vector
- `Fx` — horizontal light factor
- `Fy` — vertical light factor
- `Toon Normal` — custom toon normal override

Add once per material. All nodes that need these values should receive them from this single node rather than creating their own Attribute nodes.

---

## `GlobalConfigurationLoader`

Reads the scene-wide LSCherry configuration and exposes its flags as outputs.

**Outputs:**
- `Disable Environment` — whether environment lighting is suppressed
- `Value Enhance` — value enhancement multiplier
- `World Color` — world-tinted color value

Add once per material to respect scene-wide settings from the LSPotato panel.

---

## `MakeRay`

Performs ray-based shading calculations using the light vectors and surface normal. Outputs directional data consumed by highlight and specular nodes.

---

## `SeparateLightmap`

Splits a combined lightmap RGBA texture into its four individual shading channels.

**Inputs:** `Lightmap` — an RGBA image texture output

**Outputs:**
- `R` — shadow/AO channel
- `G` — highlight/specular channel
- `B` — specular intensity channel
- `A` — emission channel

Used as the first node after the lightmap image texture in any lightmap-driven material.

---

## `BuildFaceRamp`

Constructs the ramp structure needed for face shading. Outputs a preconfigured ramp that `MakeToon` and `ToonCore` can consume for face-specific shadow shaping.

---

## `BuildStackedToon`

Builds the node architecture for a stacked-toon setup — multiple toon layers composited on top of one another. Use when a character requires more than two distinct shading bands.

---

## `StackedToonBuilder`

A companion utility for `BuildStackedToon`. Sets up the layering structure and outputs the stacked toon result.

---

## `StackNextToon`

Chains an additional toon layer onto an existing stacked setup. Call once per extra layer needed beyond the initial `BuildStackedToon`.

---

## `SimplePantyhose`

A self-contained shader effect for semi-transparent, fabric-weave (pantyhose/stocking) materials.

**Outputs:** `Shader`

---

## `SimpleRandomize`

Applies per-object color randomization to a shader. Useful for crowd scenes where many instances of the same material need visible variation.

**Inputs:** `Shader` — source shader to vary  
**Outputs:** `Shader` — randomized result
