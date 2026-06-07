# LSCherry — GloTAni

**Menu path:** `Add Shader > LSCherry > GloTAni`

Shader nodes contributed by the GloTAni pipeline.

---

## `StylizedGlass`

A stylized glass shader that produces a toon-compatible transparent surface with refraction approximation, rim glow, and internal color tinting. Unlike a physically-accurate glass shader, this version produces clean, flat-shaded transparency suitable for anime/toon-style renders.

**Inputs:**
- `Color` — glass tint color
- `Opacity` — overall transparency (0 = fully transparent, 1 = opaque)
- `Refraction Strength` — intensity of the simulated refraction distortion
- `Rim Color` — color of the fresnel rim glow
- `Rim Strength` — intensity of the rim glow
- `Roughness` — surface roughness (affects highlight sharpness)

**Outputs:** `Shader`

**Use case:** Toon-style windows, bottles, glasses, shields, magical barriers, or any transparent surface in a stylized render.
