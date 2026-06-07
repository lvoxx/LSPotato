# LSCherry — Starters

**Menu path:** `Add Shader > LSCherry > Starters`

Ready-to-use starter material setups. Each starter is a complete, pre-wired shader for a specific character or asset type — designed as a starting point to customize rather than build from scratch.

---

## Strinova

**Menu path:** `Add Shader > LSCherry > Starters > Strinova`

A collection of 10+ starter setups for characters from the game **Strinova**. Each node is a complete material preconfigured with Strinova's shading conventions: lightmap channels, toon thresholds, and specular styles matching the game's visual style.

### Usage

1. Add the appropriate Strinova starter node for your character part (body, face, hair, etc.).
2. Connect your character's texture maps to the input sockets.
3. The node outputs a `Shader` ready for Material Output.
4. Adjust per-character parameters (color, threshold) to match the specific character's look.

### Available starters

The Strinova starters follow the naming pattern `Strinova_<CharacterPart>` or `Strinova_<Style>`. Browse `Add Shader > LSCherry > Starters > Strinova` for the full list.

> **Note:** Strinova starter nodes are opinionated presets. They hardcode several values specific to Strinova's art style. For a fully customizable setup, use the root-level `MakeToon` or `LSCherryMainController` instead.
