# LSPotato — Technical Reference

**Version 2.0.0 | Blender 5.0+ | MIT License**

---

## 1. Overview

LSPotato is a Blender 5.x add-on (Python, `bpy`) providing utility tools for the **LSCherry** toon-shader project. It handles the full lifecycle of working with LSCherry assets inside a Blender scene:

- Download and link LSCherry `.blend` releases from GitHub
- Manage a remote asset registry (LSRegistry) of linkable objects
- Replace and update shader node groups in-scene
- Sync lighting and world settings automatically
- Self-update from GitHub
- Provide a library of Python-encoded custom shader nodes accessible via the standard **Add Shader** menu (v2.0.0+)
- Compile Blender node groups into Python source files (dev tool)

**Location in Blender:** `3D View > Sidebar (N-panel) > LSPotato`

---

## 2. Installation

### Requirements

- Blender 5.0 or higher
- Internet access (for GitHub downloads and LSRegistry)
- Windows (primary target; Unix supported via `potato.sh`)

### Method A — Build Script (Recommended for development)

```bash
# Package and copy src/ into Blender's addons directory
potato install        # targets Blender 5.1 by default
potato install 5.2   # specify version if needed
```

Install target: `%APPDATA%\Blender Foundation\Blender\<version>\scripts\addons\LSPotato`

### Method B — Manual ZIP install

```bash
potato package       # produces dist/LSPotato_<branch>.zip
```

In Blender: **Edit > Preferences > Add-ons > Install** → select the `.zip` → enable **LSPotato**.

### After any install

Blender must be **restarted** — there is no live-reload.

### Uninstall

```bash
potato uninstall        # removes from Blender 5.1
potato uninstall 5.2    # specify version if needed
```

---

## 3. Features

| Feature | Description |
|---|---|
| **Find LSCherry** | Download, link, repair, or clean LSCherry releases from GitHub |
| **LSRegistry** | Download a remote asset registry; link listed objects into the scene |
| **Replace Nodes** | Swap outdated shader node groups for updated versions |
| **Make Local** | Convert linked node groups to local copies |
| **AutoSync** | Automatically sync LSCherry provider and global lighting/world configuration via Blender's `depsgraph_update_post` handler |
| **Check for Update** | Fetch the latest LSPotato release from GitHub; show a confirmation popup before applying |
| **Node Library** | Python-encoded custom `ShaderNodeCustomGroup` nodes accessible via **Add Shader → LSCherry/...** |
| **Node Compiler** | Dev-only operator: reads node groups from the open `.blend` and generates Python node source files |

---

## 4. Usage

### 4.1 Find & Link LSCherry

1. Open the **LSPotato** sidebar panel in the 3D View.
2. Under **Find LSCherry**, select the target LSCherry version from the dropdown (versions 1.0.0-beta.1 through 1.2.8.2 are supported).
3. Click **Download** — the release `.zip` is fetched from GitHub and extracted.
4. Click **Link** — the `LS Cherry.local.blend` file is linked into the current scene under the `LS Cherry` collection (colored red).
5. Use **Repair** to re-link a broken library path; use **Clean** to remove the local copy.

### 4.2 LSRegistry

1. (First time) Provide GitHub credentials under the **Credentials** section if the registry is private.
2. Click **Download Registry** — fetches `registry.yaml` from `lvoxx/LSRegistry` on the `main` branch.
3. Browse the registry list and click **Link** next to any asset — the object is linked into the scene under the `LSRegistry` collection (colored blue).

### 4.3 Replace Nodes

1. Select one or more objects with materials using outdated LSCherry node groups.
2. Click **Replace Nodes** — LSPotato scans materials and replaces matching node groups with the current versions.

### 4.4 Make Local

1. Select objects with linked node groups.
2. Click **Make Local** — converts linked node groups into local data, making the file self-contained.

### 4.5 AutoSync

AutoSync runs automatically in the background via `depsgraph_update_post`. No manual trigger needed. Two sub-systems:

- **Cherry Provider** (`Core.LSCherryProvider`) — keeps the LSCherry provider node group in sync.
- **Global Configuration** — syncs world/lighting properties from the LSCherry scene to the current scene.

### 4.6 Check for Update

1. Click **Check for Update** in the panel.
2. LSPotato queries `https://api.github.com/repos/lvoxx/LSPotato/releases/latest`.
3. If a newer version is found, a confirmation popup appears.
4. Confirm to download and replace the addon files. Restart Blender after update.

### 4.7 Using the Node Library (Add Shader menu)

Custom shader nodes are available after enabling the addon:

1. Open the **Shader Editor**.
2. Press `Shift+A` → **LSCherry** → navigate the submenu.
3. Select a node to add it to the material.

Nodes are organized by their `bl_label` prefix:

| Menu Path | Label Prefix |
|---|---|
| LSCherry/Combiner | `lscherry.combiner.*` |
| LSCherry/Utils/BNodes | `lscherry.utils.bnodes.*` |
| LSCherry/External/Michos/Genshin Impact | `lscherry.external.michos.genshin_impact.*` |
| LSCherry *(fallback)* | `lscherry.*` |

---

## 5. Node System Explanation

### Node Library (`src/nodes/`)

| File | Role |
|---|---|
| `node.py` | `ShaderNode` / `GeometryNode` mixin base classes |
| `node_impl.py` | `NodeLib` — scans `src/nodes/shader/**/*.py` via `importlib`, collects all `ShaderNodeCustomGroup` subclasses for registration |
| `node_info.py` | Builds and registers `bpy.types.Menu` classes for the Add Shader submenu tree; also registers a `load_post` handler to restore `NodeUndefined` nodes on file open |

**Node files are auto-generated by the Node Compiler — do not edit them manually.** Each file has a comment at the top stating this.

### Node Compiler (`src/features/node_compiler/`)

Developer-only pipeline. Run it inside Blender with the source `.blend` file open:

1. **Operator:** `lspotato.compile_node_groups` (panel button: **Compile Node Groups**)
2. **Pipeline stages:**
   - `sorter.py` — topological sort of node groups by dependency
   - `router.py` — maps node group name prefix → output subfolder + `bl_label`
   - `analyzer.py` — introspects sockets, nodes, links, and default values
   - `code_gen.py` — generates Python class source text
   - `exporter.py` / `geometry_exporter.py` — writes `.py` files and `__init__.py` files
3. **Output folder:** configured in `NodeCompilerProperties.compiled_folder` (default: `./compiled` relative to the `.blend` file).
4. After compiling, copy the output into `src/nodes/shader/` and run `potato reload`.

### Node Naming Convention

Node groups in Blender **must** use the dotted-path format:

```
lscherry.utils.bnodes.TangentFix
lscherry.combiner.HairCombiner
lscherry.external.michos.genshin_impact.Face
```

The router uses the prefix to determine the output subfolder and the `bl_label` assigned to the generated class. Non-conforming names fall back to the root `LSCherry` menu.

---

## 6. Limitations / Known Issues

- **Restart required** after every install, uninstall, or file copy — Blender has no live-reload for addons.
- **Node files must not be hand-edited** — they are regenerated by the Node Compiler and will be overwritten.
- **LSRegistry credentials** are stored in scene properties and are not encrypted.
- **No unit tests** — the only CI gate is `flake8` lint (`potato test`). There is no automated functional test suite.
- **AutoSync double-registration guard** is in place, but fully clearing handlers after disabling requires a Blender restart.
- `src/mock/` is dev-only and is excluded from packaged builds.

---

## 7. Version & Compatibility

| Property | Value |
|---|---|
| Add-on version | 2.0.0 |
| Minimum Blender | 5.0 |
| Tested Blender | 5.1 (install default) |
| LSCherry versions | 1.0.0-beta.1 → 1.2.8.2 |
| Python | Blender-bundled (3.11+) |
| License | MIT |
| Author | Lvoxx |
| Issue tracker | https://github.com/lvoxx/LSCherry/issues |
| Source / Docs | https://github.com/lvoxx/LSCherry |

### Changelog (v2.0.0)

- Added full node library system (`src/nodes/`) with `ShaderNodeCustomGroup` subclasses
- Added Node Compiler operator to generate node source files from a `.blend`
- Added `NodeCompilerProperties` scene property group
- Added geometry node export support
