# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

**LSPotato** is a Blender 5.x add-on (Python, `bpy`) — a collection of utility tools for the companion **LSCherry** toon-shader project. It: downloads/links LSCherry `.blend` releases, manages an LSRegistry of linkable assets, replaces shader node groups, syncs lighting/world settings, self-updates from GitHub, and (v2.0.0) ships a library of Python-encoded shader nodes that can be added via the standard Blender "Add Shader" menu.

## Build & dev commands

Driven by `potato.bat` (Windows) / `potato.sh` (Unix). Call the platform script directly or via `potato` if it's on PATH.

```bash
potato package            # clean + zip src/ → dist/LSPotato_<git-branch>.zip
potato install [5.1]      # package + copy src/ into Blender addons dir (default version: 5.1)
potato uninstall [5.1]    # remove installed addon
potato reload             # uninstall + install — main dev loop after code changes
potato clean              # delete dist/ and *.pyc
potato test               # flake8 src/  (only "test" gate — lint only, no unit tests)
```

- Install target: `%APPDATA%\Blender Foundation\Blender\<version>\scripts\addons\LSPotato`
- After installing, **restart Blender** — there is no live-reload.
- `src/mock/` is excluded from all packages (it's a dev-only fixture).

## Architecture

### Registration (the spine)

`src/__init__.py` holds `bl_info` (version 2.0.0, requires Blender 5.0) and is the single registration point. Every operator, panel, and PropertyGroup is imported here and listed in `rgt_classes`; `register()`/`unregister()` walk that list. **Adding a new class always requires adding it to `rgt_classes`** — order matters (e.g., `LSRegistryCredentialItem` must precede `LSRegistryProperties`).

Scene state is exposed via `PointerProperty`:
- `context.scene.lspotato` → `LSPotatoProperties` (replace-nodes settings + nested `github_updater`)
- `context.scene.lscherry` → `LSCherryProperties` (LSCherry version selector + all autosync props — note these are attached dynamically in `register()`, not in the class body)
- `context.scene.lsregistry` → `LSRegistryProperties`
- `context.scene.lspotato_compiler` → `NodeCompilerProperties`

AutoSync works by appending handlers to `bpy.app.handlers.depsgraph_update_post` in `register()`, guarded against double-registration.

### Feature module layout

Each feature is a package under `src/features/<name>/` with a consistent split:
- `properties.py` — `bpy.types.PropertyGroup` subclasses
- `operators.py` — `bpy.types.Operator` subclasses (actual logic in `execute()`)
- `ui.py` — `draw_*` functions (not Panel classes)
- `__init__.py`

The **single UI panel** is `LSPotatoPanel` in [src/features/panels.py](src/features/panels.py) (3D View > Sidebar > "LSPotato"). It composes per-feature `draw_*` functions. To add UI, write a `draw_*` in the feature's `ui.py` and call it from `panels.py`.

Features: `find_lscherry` (download/link/repair/clean LSCherry releases), `lsregistry` (registry download, asset linking, GitHub credentials), `replace_nodes`, `make_local`, `autosync` (`cherry_provider` + `global_configuration` sub-features, unified via `autosync/uni.py`), `checkfor_update` (GitHub self-update with confirmation popups), `node_compiler` (dev tool — see below).

### Node library system (`src/nodes/`)

v2.0.0's major feature: a library of Python-encoded custom shader nodes (`ShaderNodeCustomGroup` subclasses) that appear in Blender's "Add Shader → LSCherry/..." menu.

**Three key files:**

- [src/nodes/node.py](src/nodes/node.py) — `ShaderNode` / `GeometryNode` mixin base classes. All compiled nodes subclass `ShaderNode`.
- [src/nodes/node_impl.py](src/nodes/node_impl.py) — `NodeLib`: recursively scans `src/nodes/shader/**/*.py` via `importlib`, finds every subclass of `ShaderNodeCustomGroup`, and returns them as a list ready to register.
- [src/nodes/node_info.py](src/nodes/node_info.py) — menu registration: `ng_register()` / `ng_unregister()` build and register `bpy.types.Menu` classes that populate the "Add Shader → LSCherry/..." submenu tree, based on each class's `bl_label`. Also registers a `load_post` handler that restores `NodeUndefined` nodes when opening a file.

**Node naming convention** (`bl_label` drives menu placement):

| `bl_label` prefix | Blender menu path |
|---|---|
| `lscherry.combiner.*` | LSCherry/Combiner |
| `lscherry.utils.bnodes.*` | LSCherry/Utils/BNodes |
| `lscherry.external.michos.genshin_impact.*` | LSCherry/External/Michos/Genshin Impact |
| `lscherry.*` (fallback) | LSCherry |

The mapping is defined in `_CATEGORY_MAP` in `node_info.py` and the parallel `_ROUTES` table in `node_compiler/compiler/router.py`.

**Node files are auto-generated — do not edit manually.** They are produced by the NodeCompiler (see below) and committed to the repo. The comment at the top of every compiled file says so.

### Node Compiler (`src/features/node_compiler/`)

A development-only Blender operator (`lspotato.compile_node_groups`) that reads node groups from the currently open `.blend` file and generates the Python node source files:

1. `compiler/sorter.py` — topologically sorts node groups by dependency
2. `compiler/router.py` — maps `ng.name` prefix → output subfolder + `bl_label` prefix; also does material-based routing for unrecognized groups
3. `compiler/analyzer.py` — introspects node group sockets, nodes, links, and default values
4. `compiler/code_gen.py` — generates the Python class source text
5. `compiler/exporter.py` — writes `.py` files and `__init__.py` files

Output goes to the folder configured in `NodeCompilerProperties.compiled_folder` (default: `./compiled` relative to the .blend file). After compiling, move/copy the output into `src/nodes/shader/` and re-run `potato reload`.

Node group names in Blender must follow the dotted-path convention (`lscherry.utils.bnodes.TangentFix`) so the router can place them in the correct subfolder.

### Exception handling

`src/exception/base_handler.py` defines the pattern — use it, not bare `try/except` in operators:
- Custom exceptions live in `exception/model/lspotato_exceptions.py` and `exception/model/node_compiler_exceptions.py`.
- Per-feature handlers in `exception/handler/` subclass `BaseExceptionHandler`.
- Operators mix in `OperatorExceptionMixin` and call `self.safe_execute(self._execute_impl, context)` — the mixin catches, logs, shows a Blender popup, and returns `{'CANCELLED'}`.
- Non-operator functions use the `@handle_errors(handler_class=...)` decorator.

### Constants & URLs

All hardcoded strings live in `src/constants/`. `app_const.py` is the source of truth for GitHub repo names, API/raw URLs, collection names, colors, and regexes. `lscherry_version.py` maps LSCherry version strings → release zip URLs — **update here when a new LSCherry version ships**. `registry_url.py` builds raw-content download URLs. Import from constants rather than inlining URLs or names in feature code.

### Logging & vendored deps

- `src/utils/logger.py` — `get_logger(name)` singleton; logs to a temp file; only INFO goes to the Blender console.
- `src/vendor/yaml/` — PyYAML vendored because Blender has no pip. `src/__init__.py` appends the addon root to `sys.path`; **never remove** the marked block.

## Conventions

- `import bpy  # type: ignore` — standard for add-ons; `bpy` isn't installed in the dev venv.
- Operator `bl_idname`s are namespaced by feature: `lscherry.*`, `lsregistry.*`, `lspotato.*` (class name prefixes: `LSCHERRY_OT_`, `LSREGISTRY_OT_`, `LSPOTATO_OT_`).
- Bump `bl_info["version"]` in `src/__init__.py` for releases.
- Only `flake8` lint gates code (`potato test`); no formatter config or type checker in CI.

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **LSPotato** (7019 symbols, 10214 relationships, 203 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `gitnexus_impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `gitnexus_detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `gitnexus_query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `gitnexus_context({name: "symbolName"})`.

## Never Do

- NEVER edit a function, class, or method without first running `gitnexus_impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `gitnexus_rename` which understands the call graph.
- NEVER commit changes without running `gitnexus_detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/LSPotato/context` | Codebase overview, check index freshness |
| `gitnexus://repo/LSPotato/clusters` | All functional areas |
| `gitnexus://repo/LSPotato/processes` | All execution flows |
| `gitnexus://repo/LSPotato/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
