# LSCherry — XTR

**Menu path:** `Add Shader > LSCherry > XTR`

Shader nodes contributed by the XTR pipeline. These nodes provide parallax UV mapping for fake depth effects on flat surfaces.

---

## `XTR_ParallaxUV`

Generates a parallax-offset UV coordinate based on the view direction and a height map. Creates the illusion of surface depth on a flat polygon — useful for windows, panels, or layered decals.

**Inputs:**
- `Height Map` — grayscale texture encoding depth (brighter = raised)
- `Height Scale` — amount of parallax offset (higher = more exaggerated depth)
- `UV` — base UV coordinates to offset

**Outputs:** `Parallax UV` — modified UV coordinates to feed into subsequent texture nodes

---

## `XTR_ParallaxCombiner`

Combines multiple parallax layers into a single UV output. Use when stacking several height layers with different offsets (e.g., glass surface + interior detail + background).

**Inputs:**
- `Layer 1 UV`, `Layer 1 Depth`
- `Layer 2 UV`, `Layer 2 Depth`
- `Blend Factor` — how the layers are mixed

**Outputs:** `Combined UV`

---

## Typical Setup

```
[Height Map] ──► XTR_ParallaxUV ──► [Texture Node using Parallax UV] ──► Material
```

For a layered interior effect, chain `XTR_ParallaxCombiner` after two `XTR_ParallaxUV` nodes.
