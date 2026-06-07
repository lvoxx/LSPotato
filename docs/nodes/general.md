# LSCherry — General

**Menu path:** `Add Shader > LSCherry > General`

General-purpose utility nodes that don't belong to a specific shading category.

---

## `WorldColorProvider`

Reads the current world/sky color from the scene's world shader and exposes it as a usable color output. Allows material shaders to react to the world color without hardcoding a value.

**Outputs:** `World Color` — the scene's world background color as an RGB value

**Use case:** Use as a tint source in `AddTintVBody`, as an ambient fill in shadow areas, or anywhere you want the material to match the scene's sky tone automatically. Avoids the need to manually update color values across multiple materials when the world lighting changes.
