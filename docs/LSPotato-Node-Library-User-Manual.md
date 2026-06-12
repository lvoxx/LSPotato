# LSPotato — Node Library User Manual

**Version 2.0.0 | Blender 5.0+ | LSCherry Shader Nodes**

---

## 1. Overview

The LSPotato add-on ships a library of Python-encoded custom shader nodes accessible directly from Blender's **Add Shader** menu. These nodes are the same node groups used by the **LSCherry** toon-shader project, compiled from `.blend` source files into Python and embedded in the add-on.

You do not need to download a separate `.blend` file to access them — they are built programmatically the first time you add one to a material.

---

## 2. Accessing the Nodes

### In the Shader Editor

1. Open a material's node graph (**Shader Editor**).
2. Press **Shift + A** (or click **Add** in the header) to open the Add menu.
3. Navigate to **LSCherry** — this entry appears at the bottom of the standard shader categories.
4. Browse into subcategories (e.g., **Core**, **Utils/BNodes**, **External/Michos/Genshin Impact**) to find the node you need.
5. Click a node name to place it; it follows your cursor until you click again to confirm placement.

> **Note:** The `LSCherry` menu entry only appears when the active tree is a **Shader Node Tree**. It will not show up in Geometry Nodes or Compositor editors.

### First-time placement

The first time you add any LSCherry node in a Blender session, the add-on builds that node's entire internal node tree (including any nested sub-groups it depends on). This happens transparently — you may see a brief pause for complex nodes. Subsequent adds of the same node type reuse the already-built tree instantly.

---

## 3. Node Categories

The nodes are organized in a hierarchy under `Add Shader > LSCherry`. Each category has its own reference page:

| Menu Path | Description | Reference |
|---|---|---|
| `LSCherry` | Top-level nodes: main controllers, scene-wide builders | [lscherry-root.md](nodes/lscherry-root.md) |
| `LSCherry/Combiner` | Color and mask blending utilities | [combiner.md](nodes/combiner.md) |
| `LSCherry/Core` | Core toon shading: dots, outlines, specular, rim | [core.md](nodes/core.md) |
| `LSCherry/Post Production` | Highlights, hair specular, filmic mapping, body tinting | [post-production.md](nodes/post-production.md) |
| `LSCherry/Utils` | BNodes, Procedural, Ramp Style, Separator, Normal | [utils.md](nodes/utils.md) |
| `LSCherry/Plugin` | Pattern nodes: hatching, painted, watercolor, metals | [plugin.md](nodes/plugin.md) |
| `LSCherry/VFX` | Special effects: blueprint shader, hologram | [vfx.md](nodes/vfx.md) |
| `LSCherry/General` | General-purpose utilities (world color provider) | [general.md](nodes/general.md) |
| `LSCherry/Starters/Strinova` | Ready-to-use starter setups for Strinova characters | [starters.md](nodes/starters.md) |
| `LSCherry/External` | Festivities — Genshin-inspired PBR and scene interaction nodes | [festivities.md](nodes/festivities.md) |
| `LSCherry/External` | GloTAni stylized glass shader | [glotani.md](nodes/glotani.md) |
| `LSCherry/External` | AVR metal ramp effects | [avr.md](nodes/avr.md) |
| `LSCherry/External` | XTR parallax UV mapping | [xtr.md](nodes/xtr.md) |
| `LSCherry/External` | MMD matcap UV mapping | [mmd.md](nodes/mmd.md) |
| `LSCherry/External` | MICA/GF2 standard built-in shader | [mica.md](nodes/mica.md) |
| `LSCherry/External/Michos/Genshin Impact` | Genshin Impact-specific shader nodes | [external-genshin-impact.md](nodes/external-genshin-impact.md) |
| `LSCherry/External/Michos/Honkai Impact 3` | Honkai Impact 3-specific shader nodes | [external-honkai-impact-3.md](nodes/external-honkai-impact-3.md) |
| `LSCherry/External/Michos/Honkai Star Rail` | Honkai Star Rail-specific shader nodes | [external-honkai-star-rail.md](nodes/external-honkai-star-rail.md) |
| `LSCherry/Dev` | Experimental and deprecated nodes (not for production use) | [dev.md](nodes/dev.md) |

---

## 4. Geometry Nodes (Shipped as Library)

A separate set of **geometry node groups** is shipped as a binary `.blend` library (`src/nodes/geometry/library.blend`). These are not available in the Add menu — they are appended automatically to your file on open.

### Automatic management

When you open any `.blend` file with LSPotato active:

1. The add-on checks whether the required geometry node groups exist in `bpy.data.node_groups`.
2. Missing groups are appended from the shipped library.
3. If a group exists but its content hash differs from the shipped version, the shipped version overwrites it (preserving all modifier references via Blender's `user_remap`).
4. If the hash matches, the file's version is left untouched.

This means you always have the correct version of the shipped geometry nodes without manual management.

---

## 5. File Open Behavior — NodeUndefined Recovery

If you open a `.blend` file on a machine where LSPotato is not installed (or was uninstalled), LSCherry nodes saved in that file will appear as `NodeUndefined` blocks. When you re-open the file with LSPotato active, the add-on automatically:

1. Scans all materials and node groups for `NodeUndefined` nodes.
2. Identifies which ones correspond to known LSCherry node types.
3. Replaces each `NodeUndefined` with the correct LSCherry node, restoring socket connections and default values.

This recovery happens silently via a `load_post` handler.

---

## 6. Troubleshooting

### "LSCherry" does not appear in Add Shader menu

- Confirm the active node editor is a **Shader Node Tree** (not Geometry Nodes or Compositor).
- Ensure LSPotato is enabled in **Edit > Preferences > Add-ons**.
- Restart Blender after installing or updating the add-on.

### Node appears as "NodeUndefined" after opening a file

- The file was saved with LSCherry nodes but LSPotato was not installed or was disabled.
- Enable LSPotato and reopen the file — the recovery handler restores nodes automatically.

### Complex node shows "Missing Data Block" on first add

- Bypass the stock `node.add_node` operator and use the menu instead. The `LSCherry` menu routes through `lspotato.add_lscherry_node`, which pre-builds the entire node tree before placement.
- If calling Python directly, call `YourNodeClass.create_node_group()` before `bpy.ops.node.add_node(...)`.

### Geometry nodes revert after saving

- The add-on overwrites geometry node groups whose hash differs from the shipped version on every file open. This is by design — to ensure all files use the current library version.

---

## 7. Workflow Tips

- **Start with `SimpleToon` or `SimpleMakeToon`** for quick setups, then switch to `MakeToon` or `LSCherryMainController` when you need full control.
- **Use `NamedProperties`** once per material to access shared light vectors without duplicating the attribute nodes.
- **Chain Post Production nodes** — they are designed to layer: add core specular first, then highlights, then tone mapping.
- **For game-rip character shading**, use the appropriate External/Michos package node (`Build*Package`) as the starting point — it wires the standard textures in one step.
- **Pattern nodes** from the Plugin category can be mixed into any surface by connecting their output to the `Pattern` socket of `MakeToon` or `SimpleMakeToon`.
