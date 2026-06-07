# -*- coding: utf-8 -*-
"""Authored prose for the node reference docs: per-category headers and
per-node one-line descriptions. Imported by _gen_node_docs.py.

Keys in NODE_DESC are the node's draw_label exactly as it appears in Blender.
"""

# ---------------------------------------------------------------------------
# Per-category header: title, overview, use_cases (list), usage (list of steps)
# ---------------------------------------------------------------------------
CATEGORY_META = {
"core.md": {
    "title": "LSCherry — Core",
    "menu": "Add Shader > LSCherry > Core",
    "overview": (
        "Core toon-shading primitives: the step/threshold calculation, halftone "
        "dot patterns, outlines, the specular family (core / dot / glossy / metal / "
        "reflective), rim light, and emission masking. These are the low-level "
        "building blocks that the higher-level builders (`Make Toon`, "
        "`LS Cherry Main Controller`) are assembled from. Most accept a shader "
        "stream and return a modified shader stream, so they can be chained."
    ),
    "use_cases": [
        "Hand-building a custom toon material instead of using the all-in-one `Make Toon`.",
        "Adding a single effect (outline, rim, a specific specular style) on top of an existing shader.",
        "Authoring stylised highlights — dot specular for a comic look, glossy/metal for shiny surfaces.",
    ],
    "usage": [
        "Drop the node into the Shader Editor from `Add Shader > LSCherry > Core`.",
        "Feed the upstream surface into the `Shader` input where present; nodes without a shader input (e.g. `Toon Core`, `Specular Core`) produce a color/mask you mix in yourself.",
        "Chain effects by routing each node's `Shader` output into the next node's `Shader` input.",
        "Leave `Normal` unconnected to use the geometry normal, or connect a normal map.",
    ],
},
"combiner.md": {
    "title": "LSCherry — Combiner",
    "menu": "Add Shader > LSCherry > Combiner",
    "overview": (
        "Color/shader blending helpers used to layer extra tints onto a toon result — "
        "fake bright and shadow colors, transparency mixing, generic color blending, "
        "and a light-area extractor. They are the glue between the Core shading terms "
        "and the final surface."
    ),
    "use_cases": [
        "Pushing extra warmth into lit areas or coolness into shadows without re-authoring the ramp.",
        "Mixing a transparent pass into an otherwise opaque toon surface.",
        "Deriving a light/shadow mask to drive other effects.",
    ],
    "usage": [
        "Insert between your shading nodes and the material output.",
        "Use `Get Light Area` to produce a mask, then feed it into the `Fac` of another blend.",
    ],
},
"post-production.md": {
    "title": "LSCherry — Post Production",
    "menu": "Add Shader > LSCherry > Post Production",
    "overview": (
        "Finishing-pass nodes that layer on top of a completed toon shader: specular and "
        "highlight variants (core, dot, sphere-map, lightmap-driven, hair, random), "
        "body tint adjustments, view-transform helpers (`Quick To Filmic`, "
        "`Standard To Filmic`), a shader kill-switch, and a random color generator. "
        "They are designed to stack in order."
    ),
    "use_cases": [
        "Adding anime hair highlights or specular glints after the base toon look is set.",
        "Converting a Standard-view result into a Filmic/AgX-friendly one for final render.",
        "Quickly tinting or muting a material during look-dev.",
    ],
    "usage": [
        "Apply after the main shader (e.g. after `Make Toon`).",
        "Layer in order: specular/core first, then highlights, then tone mapping.",
        "`Disable All Shader` is a debugging toggle — it flattens the surface so you can isolate geometry.",
    ],
},
"plugin.md": {
    "title": "LSCherry — Plugin",
    "menu": "Add Shader > LSCherry > Plugin",
    "overview": (
        "Procedural pattern and material generators: hatching styles (line, dot, checker, "
        "diagonal stripe), painted and watercolor textures, scratch, and stylised metals "
        "(brushed chrome, smooth metal, anisotropic). Each pattern outputs a color/mask "
        "you mix into a surface — most usefully into the `Pattern` input of `Make Toon` "
        "or `Simple Make Toon`."
    ),
    "use_cases": [
        "Comic-book / manga shading via hatching patterns driven by light.",
        "Painterly and watercolor stylisation of surfaces.",
        "Stylised metals for props, weapons, and accessories.",
    ],
    "usage": [
        "Add from `Add Shader > LSCherry > Plugin`.",
        "Connect the pattern's color output to the `Pattern` socket of `Make Toon`/`Simple Make Toon`, or multiply it into your own base color.",
        "Use `UV`/`Scale` to control tiling and `Seed` (where present) for variation.",
    ],
},
"vfx.md": {
    "title": "LSCherry — VFX",
    "menu": "Add Shader > LSCherry > VFX",
    "overview": (
        "Self-contained special-effect shaders: a sci-fi blueprint/wireframe look and a "
        "hologram look. Each is a complete surface shader rather than a modifier."
    ),
    "use_cases": [
        "Holographic UI props, projections, and ghost/spirit characters.",
        "Blueprint / schematic reveal effects.",
    ],
    "usage": [
        "Add the node and connect its `Shader`/`Combined` output straight to the Material Output.",
        "Animate the exposed factors (scan lines, distortion, alpha) for motion.",
    ],
},
"utils.md": {
    "title": "LSCherry — Utils",
    "menu": "Add Shader > LSCherry > Utils (and the Procedural / Ramp Style / BNodes subgroups)",
    "overview": (
        "The toolbox layer. Sub-groups: **BNodes** (boolean/logic + small math and attribute "
        "helpers), **Procedural** (face/nose ramps, skin detail `SST1:` set, pantyhose, "
        "fresnel, wave texture), **Ramp Style** (vectors that reshape toon/SSS/back ramps), "
        "**Separator** (lightmap channel splitting, number packing, PBR→toon conversion), and "
        "**Normal** helpers. These are wired *into* the bigger shaders rather than used "
        "stand-alone.\n\n"
        "> Note: the Separator group ships with the folder name `seperator` and the Ramp Style "
        "and Separator nodes appear directly under **LSCherry > Utils** in the menu (see each "
        "node's *Menu* line for the exact path)."
    ),
    "use_cases": [
        "Splitting a packed lightmap into its shadow / specular / AO channels.",
        "Driving anime face shadows from an SDF face map.",
        "Adding procedural skin detail (pores, freckles, moles, veins) via the `SST1:` nodes.",
        "Boolean/comparison logic to switch shader branches.",
    ],
    "usage": [
        "Pick the sub-group that matches your need (see each node's `Menu` line).",
        "Most Separator nodes take a texture/color and emit several derived channels.",
        "Ramp Style nodes output a style vector that plugs into the matching `* Style` input of `Make Toon` / `Toon3S`.",
    ],
},
"starters.md": {
    "title": "LSCherry — Starters / Strinova",
    "menu": "Add Shader > LSCherry > Starters > Strinova",
    "overview": (
        "Ready-made starting setups for *Strinova* character materials. `* Starter` nodes are "
        "complete per-part shaders (face, hair, body, skin, weapon); `* Resolver` nodes wire up "
        "the standard texture set for a part; `* Bundle` nodes pack groups of related ramp/shadow/"
        "SSS values into a single Bundle connection to keep the graph tidy."
    ),
    "use_cases": [
        "Shading a ripped Strinova character quickly with the intended look.",
        "A worked reference for how the LSCherry building blocks fit together for a real character.",
    ],
    "usage": [
        "Add the `* Starter` for the part you are shading and connect its output to the Material Output.",
        "Feed the part's textures through the matching `* Textures Resolver`.",
        "Tune ramps/shadows via the `* Bundle` inputs.",
    ],
},
"lscherry-root.md": {
    "title": "LSCherry — Root (Top-Level Builders & Controllers)",
    "menu": "Add Shader > LSCherry",
    "overview": (
        "The headline nodes that sit at the top of the `LSCherry` menu. These are the "
        "all-in-one builders and scene controllers most users start from: full character "
        "shaders (`Make Toon`, `LS Cherry Main Controller`), quick variants "
        "(`Simple Toon`, `Simple Make Toon`), the stacked-toon multi-layer system, the "
        "ray helper, and the shared `Named Properties` / `Global Configuration Loader` "
        "providers."
    ),
    "use_cases": [
        "Shading a character end-to-end from one node.",
        "Quick look-dev with `Simple Toon` before committing to the full controller.",
        "Sharing light vectors and global settings across many materials.",
    ],
    "usage": [
        "For most work start with `Make Toon` (full control) or `Simple Make Toon` (fast).",
        "Add `Named Properties` once per material to expose shared light/scene vectors without duplicating attribute nodes.",
        "Connect the builder's `Shader` output to the Material Output; use `To AgrX` if you are in an AgX view transform.",
    ],
},
"general.md": {
    "title": "LSCherry — General",
    "menu": "Add Shader > LSCherry > General",
    "overview": "General-purpose helpers that don't belong to a specific shading stage.",
    "use_cases": ["Feeding scene world/ambient color into a material."],
    "usage": ["Add the node and route its output where a world/ambient color is expected."],
},
"dev.md": {
    "title": "LSCherry — Dev (Experimental / Deprecated)",
    "menu": "Add Shader > LSCherry > Dev",
    "overview": (
        "Work-in-progress and retired nodes. **Not for production** — experimental nodes "
        "may change or break, and deprecated nodes are kept only for opening older files."
    ),
    "use_cases": ["Testing new ideas; loading legacy materials that still reference these groups."],
    "usage": ["Avoid in new materials. Migrate deprecated nodes to their current equivalents."],
},
"avr.md": {
    "title": "LSCherry — AVR (External)",
    "menu": "Add Shader > LSCherry > External",
    "overview": "AVR-contributed metal ramp effect. Appears under the **External** submenu.",
    "use_cases": ["Stylised metal banding on props and armour."],
    "usage": ["Add from `Add Shader > LSCherry > External` and mix its output into a metal surface."],
},
"xtr.md": {
    "title": "LSCherry — XTR (External)",
    "menu": "Add Shader > LSCherry > External",
    "overview": (
        "XTR parallax mapping pair: `Parallax UV` offsets UVs by view direction to fake depth, "
        "and `Parallax Combiner` layers the result. Appear under the **External** submenu."
    ),
    "use_cases": ["Fake interior/relief depth (eyes, panels, engravings) without extra geometry."],
    "usage": ["Generate offset UVs with `Parallax UV`, sample your textures with them, then combine."],
},
"mmd.md": {
    "title": "LSCherry — MMD (External)",
    "menu": "Add Shader > LSCherry > External",
    "overview": "MMD-style MatCap UV generator. Appears under the **External** submenu.",
    "use_cases": ["Reproducing MMD/MME matcap (sphere-map) shading on imported models."],
    "usage": ["Use the output UVs to sample a matcap texture, then add it to your surface."],
},
"mica.md": {
    "title": "LSCherry — MICA (External)",
    "menu": "Add Shader > LSCherry > External",
    "overview": "MICA-contributed GF2 standard built-in material. Appears under the **External** submenu.",
    "use_cases": ["A ready GF2-style material build for compatible characters."],
    "usage": ["Add it and wire the character's standard textures into its inputs."],
},
"glotani.md": {
    "title": "LSCherry — GloTAni (External)",
    "menu": "Add Shader > LSCherry > External",
    "overview": "GloTAni stylized glass shader. Appears under the **External** submenu.",
    "use_cases": ["Stylised transparent glass/crystal surfaces that still read as toon."],
    "usage": ["Connect its output to the Material Output; tune transparency/tint inputs."],
},
"festivities.md": {
    "title": "LSCherry — Festivities (External)",
    "menu": "Add Shader > LSCherry > External",
    "overview": (
        "Genshin-inspired (FES_GI) PBR + scene-interaction nodes for festive/diorama scenes. "
        "Appear under the **External** submenu."
    ),
    "use_cases": ["Genshin-style PBR surfaces and scene/light interaction for environment shots."],
    "usage": ["Build the PBR term with `GenshinPBR - SMBE`, then combine with the scene via the scene nodes."],
},
"external-genshin-impact.md": {
    "title": "LSCherry — External / Michos / Genshin Impact",
    "menu": "Add Shader > LSCherry > External > Michos > Genshin Impact",
    "overview": (
        "Michos's Genshin Impact (`GI:`) shader set. The `Build * Package` nodes are the "
        "one-click starting points per body part (head/body/hair); the `Seperate *` and "
        "`* From Lightmap/Colormap` nodes are the lower-level steps those packages are built "
        "from — exposed so you can wire a custom setup. Driven by Genshin's packed colormap + "
        "lightmap + ramp textures."
    ),
    "use_cases": [
        "Shading ripped Genshin Impact characters with game-accurate toon ramps.",
        "Customising one stage (e.g. just the ramp build) of a Genshin material.",
    ],
    "usage": [
        "Start with the `Build Head/Body/Hair Package` node for the part you are shading.",
        "Feed the part's colormap, lightmap and ramp textures into the matching inputs.",
        "Drop to the `Seperate *` / `* From Lightmap` nodes only when you need finer control.",
    ],
},
"external-honkai-impact-3.md": {
    "title": "LSCherry — External / Michos / Honkai Impact 3",
    "menu": "Add Shader > LSCherry > External > Michos > Honkai Impact 3",
    "overview": (
        "Michos's Honkai Impact 3 (`HI3:`) shader set. Same architecture as the Genshin set: "
        "`Build * Package` per-part entry points plus the lower-level `Seperate *` / "
        "`* From Lightmap/Colormap` building blocks."
    ),
    "use_cases": [
        "Shading ripped Honkai Impact 3 characters with game-accurate toon ramps.",
        "Hand-wiring a custom HI3 material from the per-stage nodes.",
    ],
    "usage": [
        "Start with `Build Head/Body/Hair Package` for the part.",
        "Feed the part's colormap / lightmap / ramp textures into the matching inputs.",
    ],
},
"external-honkai-star-rail.md": {
    "title": "LSCherry — External / Michos / Honkai Star Rail",
    "menu": "Add Shader > LSCherry > External > Michos > Honkai Star Rail",
    "overview": (
        "Michos's Honkai Star Rail (`HSR:`) shader set. Same architecture as the Genshin/HI3 "
        "sets: `Build * Package` per-part entry points plus the lower-level `Seperate *` / "
        "`* From Lightmap/Colormap` building blocks, including an outline-from-lightmap node."
    ),
    "use_cases": [
        "Shading ripped Honkai Star Rail characters with game-accurate toon ramps.",
        "Hand-wiring a custom HSR material from the per-stage nodes.",
    ],
    "usage": [
        "Start with `Build Head/Body/Hair Package` for the part.",
        "Feed the part's colormap / lightmap / ramp textures into the matching inputs.",
    ],
},
}


# ---------------------------------------------------------------------------
# Per-node one-line descriptions (keyed by draw_label).
# Only used when the node group has no embedded description of its own.
# ---------------------------------------------------------------------------
NODE_DESC = {
# ── core ──────────────────────────────────────────────────────────────────
"Add Outline": "Adds a flat colored outline shader you mix behind the surface (paired with inverted-hull or back-face geometry).",
"Add Outline From Lightmap": "Outline whose color is driven per-region by a lightmap + a 5-stop ramp, so different parts get different outline tints.",
"Emission Mask": "Turns a mask + color into an emission shader, for making specific areas glow (eyes, FX accents).",
"Inverted Toon Dot": "Halftone dot pattern placed in the lit areas instead of the shadows.",
"Reflective Toon": "Toon shading with environment reflection blended in — for eyes, gems, and shiny accents.",
"Rim Core": "Computes a view-angle rim-light term along the silhouette.",
"Simple Back Toon Dot": "Dot toon effect applied to back-facing geometry only (inner shadow / translucency look).",
"Simple Toon Dot": "Single-threshold halftone dot toon effect.",
"Specular Core": "Core specular highlight term, shaped for toon compositing.",
"Specular Dot": "Specular rendered as a discrete halftone dot rather than a smooth highlight.",
"Toon Core": "The fundamental toon step: takes diffuse lighting + AO and outputs a hard-edged toon color.",
"Toon Dot": "Full halftone dot effect with size, density and threshold control.",
"Toon Glossy": "Glossy toon reflection using a blurred environment sample plus a toon step.",
"Toon Metal": "Metallic toon shading — environment reflection combined with a stepped diffuse.",
"Toon Ray": "Ray-based toon shading driven by `Make Ray` for more directional, physical-feeling steps.",
"Toon Spec": "Toon-stylised specular: a hard step applied to the specular gradient.",
"Toon3S": "Three-band toon (shallow / mid / deep shadow) with per-band color, scale and weight, plus a specular panel.",
# ── combiner ──────────────────────────────────────────────────────────────
"Add Fake Bright Color": "Injects an artificial bright tint into lit areas to fake bounce/rim warmth.",
"Add Fake Shadow Color": "Injects an artificial tint into shadow areas for richer, art-directed shadows.",
"Add Transparent": "Mixes a transparent pass into the shader to fade or cut out regions.",
"Blend Color": "General two-color blend with a factor — the workhorse mixer.",
"Get Light Area": "Extracts a light/shadow mask from the shading, for driving other effects.",
# ── post production ───────────────────────────────────────────────────────
"Add Core Specular": "Layers a core-style specular highlight onto a finished shader.",
"Add Dot Specular": "Layers a halftone dot specular onto a finished shader.",
"Add Frequent Hair Highlight": "Anime hair highlight with multiple repeating bands.",
"Add Highlight": "Generic highlight pass added on top of the surface.",
"Add HightLight From LightMap": "Highlight whose placement/intensity is read from a lightmap channel.",
"Add HightLight From SphereMap": "Highlight sampled from a sphere/matcap map (view-locked specular).",
"Add Invert Tint V-Body": "Inverse vertical-gradient body tint (complements `Add Tint V-Body`).",
"Add Random Toon Highlight": "Randomised toon highlight for break-up/variation across a surface.",
"Add Specular": "Adds a standard specular highlight to the shader.",
"Add Tint V-Body": "Applies a vertical-gradient tint down the body (e.g. darker boots, lighter shoulders).",
"Add Toon Highlight": "Adds a hard, toon-stepped highlight.",
"Disable All Shader": "Debug switch that flattens the surface so geometry can be inspected.",
"Quick To Filmic": "Fast Standard→Filmic-style conversion of the result for final view.",
"Random Color": "Generates a random flat color (per object/material) for blocking and previews.",
"Standard To Filmic": "Converts a Standard-view color into a Filmic/AgX-friendly one.",
# ── vfx ───────────────────────────────────────────────────────────────────
"Blueprint Shader": "Self-contained blueprint/schematic wireframe-reveal surface shader.",
"Hologram Shader": "Self-contained hologram surface shader (scan lines, transparency, glow).",
# ── general ───────────────────────────────────────────────────────────────
"WorldColor Provider": "Exposes the scene world/ambient color as a shader input.",
# ── dev ───────────────────────────────────────────────────────────────────
"Deprecated": "Retired node retained only so older files keep opening. Do not use in new work.",
"Experimental": "Unstable work-in-progress node; behavior and sockets may change.",
# ── lscherry root ─────────────────────────────────────────────────────────
"Build Face Ramp": "Builds the anime face-shadow ramp used by the face shaders.",
"Build Stacked Toon": "Assembles a multi-layer (stacked) toon result from stacked toon layers.",
"Global Configuration Loader": "Loads shared global render/shading configuration into the material graph.",
"LS Cherry Main Controller": "The full LSCherry character controller — the most complete all-in-one shader.",
"Make Ray": "Produces directional ray data consumed by `Toon Ray` for physical-feeling steps.",
"Make Toon": "All-in-one toon character shader: base/shadow/SSS/rim/back colors, specular, pattern, emission and custom-ramp control, organised into N-panel sections.",
"Named Properties": "Central provider of shared, named light/scene vectors — add once per material to avoid duplicate attribute nodes.",
"Simple Make Toon": "Streamlined `Make Toon` with the most-used inputs for fast setups.",
"Simple Pantyhose": "Quick stylised pantyhose/stocking layer for legs.",
"Simple Randomize": "Adds quick per-object randomisation (color/value) for variation.",
"Simple Toon": "Minimal one-node toon shader — the fastest starting point.",
"Stack Next Toon": "Adds the next layer onto a stacked-toon chain.",
"Stacked Toon Builder": "Entry point for the stacked (multi-layer) toon system.",
# ── starters / strinova ───────────────────────────────────────────────────
"Strinova: Body Starter": "Complete starting shader for a Strinova character body.",
"Strinova: Body Textures Resolver": "Wires the standard body texture set into the body shader.",
"Strinova: Hair Starter": "Complete starting shader for Strinova hair.",
"Strinova: Hair Textures Resolver": "Wires the standard hair texture set into the hair shader.",
"Strinova: Mask_1 Range Body Bundle": "Bundles the Mask 1 ramp ranges for the body into one connection.",
"Strinova: Mask_1 Range Hair Bundle": "Bundles the Mask 1 ramp ranges for the hair into one connection.",
"Strinova: Mask_2 Range Body Bundle": "Bundles the Mask 2 ramp ranges for the body into one connection.",
"Strinova: Mask_2 Range Hair Bundle": "Bundles the Mask 2 ramp ranges for the hair into one connection.",
"Strinova: MatCap Resolver": "Resolves the matcap/sphere-map inputs for Strinova materials.",
"Strinova: Shadow Body Bundle": "Bundles the body shadow settings into one connection.",
"Strinova: Shadow Hair Bundle": "Bundles the hair shadow settings into one connection.",
"Strinova: Skin Starter": "Complete starting shader for Strinova skin.",
"Strinova: SSS Body Bundle": "Bundles the body subsurface (SSS) settings into one connection.",
"Strinova: SSS Hair Bundle": "Bundles the hair subsurface (SSS) settings into one connection.",
"Strinova: Weapon Starter": "Complete starting shader for Strinova weapons.",
# ── utils: bnodes (logic/math/attr) ───────────────────────────────────────
"? Use Override": "Chooses between a value and an override when the override is enabled.",
"A >= B": "Comparison: outputs 1 when A is greater than or equal to B, else 0.",
"AND": "Logical AND of two boolean/0-1 inputs.",
"NAND": "Logical NAND (NOT AND) of two inputs.",
"NOR": "Logical NOR (NOT OR) of two inputs.",
"NOT": "Logical NOT — inverts a boolean/0-1 input.",
"OR": "Logical OR of two inputs.",
"XNOR": "Logical XNOR (equality) of two inputs.",
"XOR": "Logical XOR (difference) of two inputs.",
"FROM A TO B": "Remaps a value from one range into another.",
"Background Color": "Provides a background/clear color.",
"Blend Dark": "Darken-style blend of two colors.",
"Blend It": "Generic blend helper.",
"Blend Light": "Lighten-style blend of two colors.",
"Default Attribute: Alpha": "Reads a named alpha attribute (with a fallback default).",
"Default Attribute: Color": "Reads a named color attribute (with a fallback default).",
"Default Attribute: Fac": "Reads a named factor attribute (with a fallback default).",
"Default Attribute: Vector": "Reads a named vector attribute (with a fallback default).",
"Limit Color Value": "Clamps a color's value/brightness within limits.",
"Value Enhance": "Boosts value/contrast of an input.",
"World Color": "Exposes the world/ambient color.",
"Use Default Normal": "Falls back to the geometry normal when no normal map is supplied.",
# ── utils: procedural ─────────────────────────────────────────────────────
"Build Face Normal": "Generates the corrected face normal for soft anime face shading.",
"Build Face Ramp": "Builds the face-shadow ramp from a face map.",
"Build Nose Ramp": "Builds the nose-shadow ramp.",
"Build Ramp From Map": "Generates a toon color ramp from a packed ramp/map texture.",
"Face Normal Builder": "Lower-level face-normal construction used by the face shaders.",
"Face Ramp Builder": "Lower-level face-ramp construction.",
"Faceramp Vector Provider": "Provides the vector that drives the face-shadow ramp lookup.",
"Metal Ramp": "Procedural metal banding ramp.",
"Mix Transparent VFX": "Mixes a transparent VFX layer into a surface.",
"Nose Ramp Builder": "Lower-level nose-ramp construction.",
"Rim Metal Ramp": "Metal ramp variant tuned for rim/edge response.",
"Simple Pantyhose Type 1": "Procedural pantyhose pattern, style 1.",
"Simple Pantyhose Type 2": "Procedural pantyhose pattern, style 2.",
"Simple Skin Type 1": "Procedural skin base, style 1 (foundation for the SST1 detail set).",
"SST1: Blemishes": "Skin detail: procedural blemishes.",
"SST1: Build": "Skin detail: assembles the selected SST1 detail layers.",
"SST1: Builder": "Skin detail: builder/entry point for the SST1 skin system.",
"SST1: Freckles": "Skin detail: procedural freckles.",
"SST1: Moles": "Skin detail: procedural moles.",
"SST1: Pores": "Skin detail: procedural pores.",
"SST1: Pores Dirt": "Skin detail: procedural pore dirt/grime.",
"SST1: Red Spots": "Skin detail: procedural red spots/irritation.",
"SST1: Skin Bump": "Skin detail: procedural skin bump/normal detail.",
"SST1: Veins": "Skin detail: procedural subdermal veins.",
"Stylized Fresnel": "Stylised fresnel/rim term for edge lighting.",
"XY Wave Texture": "Procedural XY wave texture for ripples/stripes.",
# ── utils: ramp style ─────────────────────────────────────────────────────
"Back Style": "Outputs a style vector that reshapes the back-face ramp (plug into a `Back Style` input).",
"SSS Harden": "Hardens (sharpens) the SSS band transition.",
"SSS Style": "Outputs a style vector that reshapes the SSS ramp.",
"Toon Harden": "Hardens (sharpens) the toon band transition.",
"Toon Style": "Outputs a style vector that reshapes the toon ramp.",
# ── utils: separator ──────────────────────────────────────────────────────
"Color Selector": "Selects/branches between colors.",
"Combined To Shader": "Converts a flat combined color back into a shader stream.",
"Convert [0, 255] to [0,1]": "Rescales 0–255 values into Blender's 0–1 range.",
"Number Compress": "Packs several numbers into one value.",
"Number Extract": "Extracts a packed number back out.",
"Number To Sequence": "Expands a number into a sequence of values.",
"Seperate Lightmap": "Splits a packed lightmap into its individual channels (shadow / spec / AO / …).",
"Set Color From LightMap": "Assigns colors based on lightmap channel values.",
"To Oxy": "Converts to the OXY channel layout used downstream.",
"Toonify PBR Colors": "Converts PBR base colors into toon-friendly stepped colors.",
# ── externals (per node) ──────────────────────────────────────────────────
"AVR: Metal Ramp": "AVR stylised metal banding ramp.",
"GloTAni: Stylized Glass": "Stylised toon-compatible glass/crystal surface shader.",
"MMD: MatCapUV": "Generates MMD-style matcap (sphere-map) UVs.",
"XTR: Parallax UV": "Offsets UVs along the view direction to fake surface depth.",
"XTR: Parallax Combiner": "Combines parallax-mapped layers produced from `Parallax UV`.",
"FES_GI: Combine SMBE and Scene": "Combines the SMBE PBR term with scene interaction.",
"FES_GI: GenshinPBR - SMBE": "Genshin-style PBR (SMBE) surface term.",
"FES_GI: Scene Interaction": "Adds scene/light interaction to the festive PBR surface.",
}


def _michos_desc(label, game):
    """Generate a description for a Michos GI/HI3/HSR node from its action."""
    L = label.split(":", 1)[1].strip() if ":" in label else label
    low = L.lower()
    if low.startswith("build") and "package" in low:
        part = low.replace("build", "").replace("package", "").strip()
        return ("One-click %s starting shader for a %s character — wires the standard "
                "textures and ramps for that part." % (part, game))
    if low.startswith("build ramp") or "ramp from map" in low or "ramps from map" in low:
        return "Builds the %s toon color ramp(s) from a packed ramp/map texture." % game
    if low == "from map to ramp":
        return "Converts a packed ramp map into a usable %s toon ramp." % game
    if low.startswith("seperate") or low.startswith("separate"):
        what = low.replace("seperate", "").replace("separate", "").strip()
        return "Splits the %s %s into its individual channels." % (game, what)
    if low.startswith("add color from colormap"):
        return "Applies base colors from the %s colormap." % game
    if low.startswith("body color from lightmap"):
        return "Derives body base color using the %s lightmap." % game
    if low.startswith("add shadow from lightmap"):
        return "Adds shadow shading driven by the %s lightmap." % game
    if low.startswith("add outline from lightmap"):
        return "Adds an outline whose tint is driven by the %s lightmap." % game
    return "%s shader stage for %s materials." % (L, game)


def node_description(doc, label, embedded):
    """Resolve the best description for a node section."""
    if embedded:
        return embedded.strip()
    if label in NODE_DESC:
        return NODE_DESC[label]
    if doc == "external-genshin-impact.md":
        return _michos_desc(label, "Genshin Impact")
    if doc == "external-honkai-impact-3.md":
        return _michos_desc(label, "Honkai Impact 3")
    if doc == "external-honkai-star-rail.md":
        return _michos_desc(label, "Honkai Star Rail")
    return ""
