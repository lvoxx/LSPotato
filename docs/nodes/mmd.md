# LSCherry — MMD

**Menu path:** `Add Shader > LSCherry > MMD`

Shader nodes for MikuMikuDance (MMD) compatible shading setups.

---

## `MMD_MatcapUV`

Generates UV coordinates mapped to a matcap (sphere map) texture using the view-space normal. Used to apply a matcap/sphere-map texture to a surface for quick, viewpoint-dependent shading — a common technique in MMD-style renders.

**Inputs:**
- `Normal` — surface normal (defaults to geometry normal; use a Normal Map node for texture-based normals)

**Outputs:** `Matcap UV` — UV coordinates to use as the Vector input of an Image Texture node

---

## Typical Setup

```
[Normal Map] ──► MMD_MatcapUV ──► [Image Texture (Matcap)] ──► [Shader]
```

Connect the `Matcap UV` output to the `Vector` socket of an Image Texture node that holds your matcap image. The resulting color can be mixed into your base shader for metallic, glossy, or stylized surface effects.
