# LSCherry — AVR

**Menu path:** `Add Shader > LSCherry > AVR`

Shader nodes contributed by the AVR pipeline.

---

## `AVR_MetalRamp`

A metal ramp shader that produces stylized metallic shading using a color ramp driven by the view/normal relationship. Outputs a toon-compatible metallic appearance without relying on environment reflections.

**Inputs:**
- `Color Ramp` — the ramp driving the metallic gradient (dark to bright)
- `Normal` — surface normal (defaults to geometry normal)
- `Strength` — blend strength between the ramp result and the base color

**Outputs:** `Shader`

**Use case:** Stylized armor, weapons, or any metallic surface in an anime-style render where environment reflections are undesirable or unavailable.
