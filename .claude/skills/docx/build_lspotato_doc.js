const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat, TableOfContents, HeadingLevel,
  BorderStyle, WidthType, ShadingType, VerticalAlign, PageNumber, PageBreak,
  TabStopType,
} = require("docx");

// ---------- shared helpers ----------
const ACCENT = "B5341B";      // LSCherry-ish red
const ACCENT_DK = "7A2412";
const LIGHT = "F3E0DA";
const GREY = "555555";
const MONO = "1E1E1E";

const cellBorder = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const cellBorders = { top: cellBorder, left: cellBorder, bottom: cellBorder, right: cellBorder };

// allow inline **bold** and `code`
function textRuns(text) {
  if (Array.isArray(text)) return text;
  const runs = [];
  const re = /(\*\*[^*]+\*\*|`[^`]+`)/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) runs.push(new TextRun(text.slice(last, m.index)));
    const tok = m[0];
    if (tok.startsWith("**")) runs.push(new TextRun({ text: tok.slice(2, -2), bold: true }));
    else runs.push(new TextRun({ text: tok.slice(1, -1), font: "Consolas", size: 20, color: ACCENT_DK }));
    last = re.lastIndex;
  }
  if (last < text.length) runs.push(new TextRun(text.slice(last)));
  return runs.length ? runs : [new TextRun(text)];
}

function body(text, opts = {}) {
  return new Paragraph({ spacing: { after: 120, line: 276 }, children: textRuns(text), ...opts });
}
function h1(text) { return new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(text)] }); }
function h2(text) { return new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(text)] }); }

function bullet(text, level = 0) {
  return new Paragraph({ numbering: { reference: "bullets", level }, spacing: { after: 60 }, children: textRuns(text) });
}
function numbered(text) {
  return new Paragraph({ numbering: { reference: "steps", level: 0 }, spacing: { after: 80 }, children: textRuns(text) });
}

function codeBlock(lines) {
  return new Paragraph({
    spacing: { before: 60, after: 120 },
    shading: { type: ShadingType.CLEAR, fill: "F4F4F4" },
    border: { left: { style: BorderStyle.SINGLE, size: 18, color: ACCENT, space: 8 } },
    children: lines.map((l, i) =>
      i === 0
        ? new TextRun({ text: l, font: "Consolas", size: 18, color: MONO })
        : new TextRun({ break: 1, text: l, font: "Consolas", size: 18, color: MONO })),
  });
}

function note(label, text) {
  return new Paragraph({
    spacing: { before: 60, after: 140 },
    shading: { type: ShadingType.CLEAR, fill: LIGHT },
    border: { left: { style: BorderStyle.SINGLE, size: 18, color: ACCENT, space: 8 } },
    children: [new TextRun({ text: label + "  ", bold: true, color: ACCENT_DK }), ...textRuns(text)],
  });
}

function makeTable(headers, rows, colW) {
  const total = colW.reduce((a, b) => a + b, 0);
  const headRow = new TableRow({
    tableHeader: true,
    children: headers.map((hd, i) => new TableCell({
      borders: cellBorders,
      width: { size: colW[i], type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, fill: ACCENT },
      margins: { top: 60, bottom: 60, left: 120, right: 120 },
      verticalAlign: VerticalAlign.CENTER,
      children: [new Paragraph({ children: [new TextRun({ text: hd, bold: true, color: "FFFFFF", size: 20 })] })],
    })),
  });
  const bodyRows = rows.map((r, ri) => new TableRow({
    children: r.map((c, i) => new TableCell({
      borders: cellBorders,
      width: { size: colW[i], type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, fill: ri % 2 ? "FBF4F2" : "FFFFFF" },
      margins: { top: 60, bottom: 60, left: 120, right: 120 },
      verticalAlign: VerticalAlign.CENTER,
      children: [new Paragraph({ spacing: { after: 0 }, children: textRuns(String(c)) })],
    })),
  }));
  return new Table({ width: { size: total, type: WidthType.DXA }, columnWidths: colW, rows: [headRow, ...bodyRows] });
}

// ---------- document content ----------
const children = [];

// ===== COVER PAGE =====
children.push(
  new Paragraph({ spacing: { before: 2600 }, children: [] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
    children: [new TextRun({ text: "LSPotato", bold: true, size: 96, color: ACCENT })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 },
    children: [new TextRun({ text: "Technical Reference & User Guide", size: 36, color: GREY })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 600 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: ACCENT, space: 8 } },
    children: [new TextRun({ text: "Blender 5.x Add-on for the LSCherry Toon Shader", italics: true, size: 24, color: GREY })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
    children: [new TextRun({ text: "Architecture · Node Library · Node Compiler Pipeline", size: 24 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 1400, after: 40 },
    children: [new TextRun({ text: "Version 2.0.0", bold: true, size: 26 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 },
    children: [new TextRun({ text: "Requires Blender 5.0+   ·   Branch: V2.0.0", size: 20, color: GREY })] }),
  new Paragraph({ alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "Author: Lvoxx   ·   License: MIT   ·   June 2026", size: 20, color: GREY })] }),
  new Paragraph({ children: [new PageBreak()] }),
);

// ===== TOC =====
children.push(
  new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Table of Contents")] }),
  new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" }),
  new Paragraph({ children: [new PageBreak()] }),
);

// ===== 1. OVERVIEW =====
children.push(h1("1. Overview"));
children.push(body("**LSPotato** is a Blender 5.x add-on (Python / `bpy`) that bundles utility tooling for the companion **LSCherry** toon-shader project. It is distributed as a standard add-on ZIP and registered through a single entry point."));
children.push(body("The add-on serves two audiences at once. **Artists** get a sidebar panel that downloads LSCherry assets, links them into a scene, and keeps lighting and world settings in sync. **Technical artists and developers** get a library of Python-encoded shader nodes plus a Node Compiler that regenerates that library from a live `.blend` file."));

children.push(h2("1.1 At a glance"));
children.push(makeTable(["Attribute", "Value"], [
  ["Name", "LSPotato"],
  ["Version", "2.0.0"],
  ["Minimum Blender", "5.0.0"],
  ["Language", "Python (bpy)"],
  ["Category", "Tool (3D View > Sidebar > LSPotato)"],
  ["License", "MIT"],
  ["Companion project", "LSCherry (toon shader)"],
  ["Compiled shader nodes", "199 generated node files"],
], [2800, 6560]));

children.push(h2("1.2 What it does"));
children.push(bullet("Downloads and links LSCherry `.blend` releases into the current scene."));
children.push(bullet("Manages an **LSRegistry** of linkable assets, with GitHub credentials for private content."));
children.push(bullet("Synchronises lighting and world settings automatically (**AutoSync**)."));
children.push(bullet("Replaces shader node groups and makes linked data local."));
children.push(bullet("Ships a library of Python-encoded custom shader nodes that appear in Blender's **Add Shader → LSCherry/…** menu (v2.0.0 flagship feature)."));
children.push(bullet("Regenerates that node library from a live `.blend` file via the **Node Compiler** developer tool."));
children.push(new Paragraph({ children: [new PageBreak()] }));

// ===== 2. ARCHITECTURE =====
children.push(h1("2. Architecture"));
children.push(body("LSPotato is organised around a single registration spine, a consistent per-feature module layout, and a shared exception-handling pattern. Everything hangs off one entry point so registration order is explicit and deterministic."));

children.push(h2("2.1 The registration spine"));
children.push(body("`src/__init__.py` holds `bl_info` and is the single registration point. Every operator, panel, and `PropertyGroup` is imported here and listed in `rgt_classes`; `register()` / `unregister()` walk that list."));
children.push(note("Rule:", "Adding any new class always requires adding it to `rgt_classes`, and order matters — for example `LSRegistryCredentialItem` must precede `LSRegistryProperties` because the latter references the former."));
children.push(body("Beyond the class list, `register()` also:"));
children.push(bullet("Attaches scene-level `PointerProperty` state (see 2.2)."));
children.push(bullet("Dynamically attaches AutoSync properties onto `LSCherryProperties` (these live in `register()`, not the class body)."));
children.push(bullet("Appends AutoSync handlers to `bpy.app.handlers.depsgraph_update_post`, guarded against double-registration."));
children.push(bullet("Registers the node library and the **Add Shader** menu, gated by the user's enabled starter packs."));
children.push(bullet("Registers `load_post` handlers that restore custom nodes and append the geometry-node library when a file is opened."));

children.push(h2("2.2 Scene state"));
children.push(body("Per-scene state is exposed via `PointerProperty` on `bpy.types.Scene`:"));
children.push(makeTable(["Scene property", "Type", "Holds"], [
  ["context.scene.lscherry", "LSCherryProperties", "LSCherry version selector + all AutoSync props"],
  ["context.scene.lsregistry", "LSRegistryProperties", "Registry download + asset-linking + credentials"],
  ["context.scene.lspotato_compiler", "NodeCompilerProperties", "Node Compiler settings (output folder, etc.)"],
], [3100, 2900, 3360]));

children.push(h2("2.3 Feature module layout"));
children.push(body("Each feature is a package under `src/features/<name>/` with a consistent split:"));
children.push(makeTable(["File", "Responsibility"], [
  ["properties.py", "bpy.types.PropertyGroup subclasses"],
  ["operators.py", "bpy.types.Operator subclasses — logic lives in execute()"],
  ["ui.py", "draw_* functions (not Panel classes)"],
  ["__init__.py", "Package wiring"],
], [2600, 6760]));
children.push(body("The **single UI panel** is `LSPotatoPanel` in `src/features/panels.py` (3D View › Sidebar › LSPotato). It composes per-feature `draw_*` functions rather than defining many panels:"));
children.push(codeBlock([
  "def draw(self, context):",
  "    layout = self.layout",
  "    draw_autosync_panel(layout, context)",
  "    draw_lsregistry_panel(layout, context)",
  "    draw_compiler_panel(layout, context)",
]));
children.push(note("To add UI:", "Write a `draw_*` in the feature's `ui.py` and call it from `panels.py`."));

children.push(h2("2.4 Exception handling"));
children.push(body("`src/exception/base_handler.py` defines the project pattern — use it instead of bare `try/except` inside operators."));
children.push(bullet("Custom exceptions live in `exception/model/lspotato_exceptions.py` and `exception/model/node_compiler_exceptions.py`."));
children.push(bullet("Per-feature handlers in `exception/handler/` subclass `BaseExceptionHandler`."));
children.push(bullet("Operators mix in `OperatorExceptionMixin` and call `self.safe_execute(self._execute_impl, context)` — the mixin catches, logs, shows a Blender popup, and returns `{'CANCELLED'}`."));
children.push(bullet("Non-operator functions use the `@handle_errors(handler_class=...)` decorator."));

children.push(h2("2.5 Constants, logging & vendored deps"));
children.push(bullet("All hardcoded strings live in `src/constants/`. `app_const.py` is the source of truth for GitHub repo names, API/raw URLs, collection names, colours, and regexes."));
children.push(bullet("`lscherry_version.py` maps LSCherry version strings → release ZIP URLs — update here when a new LSCherry version ships."));
children.push(bullet("`src/utils/logger.py` exposes `get_logger(name)` (singleton). It logs to a temp file; only INFO reaches the Blender console."));
children.push(bullet("`src/vendor/yaml/` is PyYAML, vendored because Blender ships no pip. `__init__.py` appends the add-on root to `sys.path` — never remove the marked block."));
children.push(new Paragraph({ children: [new PageBreak()] }));

// ===== 3. FEATURE REFERENCE =====
children.push(h1("3. Feature Reference"));
children.push(body("The live V2.0.0 panel surfaces three feature groups — AutoSync, LSRegistry, and the Node Compiler — alongside the node library that registers into Blender's native Add Shader menu."));

children.push(h2("3.1 AutoSync"));
children.push(body("AutoSync keeps LSCherry lighting and world settings continuously matched to the scene. It is split into two sub-features unified through `autosync/uni.py`:"));
children.push(makeTable(["Sub-feature", "Purpose"], [
  ["cherry_provider", "Syncs a target collection/object (default _LS / MLight) as the light provider"],
  ["global_configuration", "Syncs global blend mode, value-enhance, world value-enhance, and world colour"],
], [3000, 6360]));
children.push(body("It works by appending handlers to `bpy.app.handlers.depsgraph_update_post` during `register()`. Toggling a sync property fires an `update=` callback that enables or disables the matching handler. Internal “last known” string properties track state so a handler only re-syncs when something actually changed."));

children.push(h2("3.2 LSRegistry"));
children.push(body("LSRegistry manages the catalogue of linkable LSCherry assets and the credentials needed to fetch private ones."));
children.push(bullet("Operators (`LSREGISTRY_OT_*`): create the registry text, `get` (download), `repair`, add/remove credential, and clear installed."));
children.push(bullet("`LSRegistryCredentialItem` is a collection item for stored GitHub credentials; `LSRegistryProperties` owns the list and registry state."));
children.push(bullet("Raw-content download URLs are built in `src/constants/registry_url.py`."));

children.push(h2("3.3 Node Compiler (developer tool)"));
children.push(body("A development-only operator (`lspotato.compile_node_groups`) that reads node groups from the currently open `.blend` and generates the Python node source files. Covered in detail in Section 5."));

children.push(h2("3.4 Node Library"));
children.push(body("The v2.0.0 flagship: a library of Python-encoded `ShaderNodeCustomGroup` subclasses that appear in Blender's **Add Shader → LSCherry/…** menu. Covered in Section 4 (usage) and Section 5 (generation)."));
children.push(new Paragraph({ children: [new PageBreak()] }));

// ===== 4. USER GUIDE =====
children.push(h1("4. User Guide"));

children.push(h2("4.1 Building and installing"));
children.push(body("Development and packaging are driven by `potato.bat` (Windows) / `potato.sh` (Unix). Call the platform script directly, or `potato` if it is on PATH."));
children.push(makeTable(["Command", "Effect"], [
  ["potato package", "Clean + zip src/ → dist/LSPotato_<git-branch>.zip"],
  ["potato install [5.1]", "Package + copy src/ into the Blender add-ons dir (default 5.1)"],
  ["potato uninstall [5.1]", "Remove the installed add-on"],
  ["potato reload", "Uninstall + install — the main dev loop after code changes"],
  ["potato clean", "Delete dist/ and *.pyc"],
  ["potato test", "flake8 src/ — the only test gate (lint only)"],
], [3000, 6360]));
children.push(note("Install target:", "`%APPDATA%\\Blender Foundation\\Blender\\<version>\\scripts\\addons\\LSPotato`. After installing you must **restart Blender** — there is no live reload. `src/mock/` is excluded from every package."));

children.push(h2("4.2 Opening the panel"));
children.push(numbered("Enable the add-on in Blender (Edit › Preferences › Add-ons › LSPotato)."));
children.push(numbered("In the 3D Viewport press **N** to open the Sidebar."));
children.push(numbered("Select the **LSPotato** tab. The AutoSync, LSRegistry, and Node Compiler sections appear stacked."));

children.push(h2("4.3 Enabling starter packs"));
children.push(body("Node starter packs are gated in the add-on preferences. Only the packs you enable are registered and shown in the Add Shader menu. Toggling a pack calls `refresh_node_library()`, which re-registers the node library so the change takes effect **without** a Blender restart."));

children.push(h2("4.4 Adding LSCherry shader nodes"));
children.push(numbered("In the Shader Editor, open **Add › Shader**."));
children.push(numbered("Navigate the **LSCherry** submenu tree (Combiner, Utils, External, …)."));
children.push(numbered("Pick a node; it is inserted as a custom group node, ready to wire up."));
children.push(body("If you open a `.blend` that references LSCherry nodes the add-on is missing, a `load_post` handler restores `NodeUndefined` placeholders so the file still loads cleanly."));

children.push(h2("4.5 Using AutoSync"));
children.push(numbered("In the AutoSync section choose the **Provider** or **Global** tab."));
children.push(numbered("For Provider: set the target collection and object (defaults `_LS` / `MLight`), then enable **AutoSync Provider**."));
children.push(numbered("For Global: enable **AutoSync Global**, then adjust blend mode, value-enhance, world value-enhance, and world colour — changes propagate live."));
children.push(new Paragraph({ children: [new PageBreak()] }));

// ===== 5. NODE LIBRARY & COMPILER =====
children.push(h1("5. Node Library & Compiler Pipeline"));

children.push(h2("5.1 Node library system (src/nodes/)"));
children.push(body("The node library is built from three key files:"));
children.push(makeTable(["File", "Role"], [
  ["node.py", "ShaderNode / GeometryNode mixin base classes; all compiled nodes subclass ShaderNode"],
  ["node_impl.py", "NodeLib — recursively scans shader/**/*.py via importlib and collects every ShaderNodeCustomGroup subclass"],
  ["node_info.py", "Builds and registers the Menu classes for Add Shader → LSCherry/…; registers the load_post restore handler"],
], [2400, 6960]));
children.push(body("**Node naming convention** — each class's `bl_label` drives its menu placement. The mapping lives in `_CATEGORY_MAP` (node_info.py) with a parallel `_ROUTES` table in the compiler's `router.py`:"));
children.push(makeTable(["bl_label prefix", "Blender menu path"], [
  ["lscherry.combiner.*", "LSCherry / Combiner"],
  ["lscherry.utils.bnodes.*", "LSCherry / Utils / BNodes"],
  ["lscherry.external.michos.genshin_impact.*", "LSCherry / External / Michos / Genshin Impact"],
  ["lscherry.* (fallback)", "LSCherry"],
], [4400, 4960]));
children.push(note("Important:", "Node files are auto-generated — do not edit them manually. They are produced by the Node Compiler and committed to the repo; the comment at the top of each compiled file says so."));

children.push(h2("5.2 The Node Compiler"));
children.push(body("`lspotato.compile_node_groups` reads node groups from the open `.blend` and emits Python node source. The pipeline lives in `src/features/node_compiler/compiler/` and runs in stages:"));
children.push(makeTable(["Stage", "Module", "Responsibility"], [
  ["1. Sort", "sorter.py", "Topologically sorts node groups by dependency"],
  ["2. Route", "router.py", "Maps ng.name prefix → output subfolder + bl_label prefix; material-based routing for unknown groups"],
  ["3. Analyze", "analyzer.py", "Introspects sockets, nodes, links, and default values"],
  ["4. Generate", "code_gen.py", "Emits the Python class source text"],
  ["5. Export", "exporter.py", "Writes .py files and __init__.py files"],
], [1700, 2200, 5460]));
children.push(body("Supporting modules round out the pipeline: `flattener.py` (inlines/flattens nested structures and handles placeholder images), `reroute_resolver.py` (resolves reroute nodes), `node_attrs.py` (attribute helpers), and `geometry_exporter.py` (geometry-node output)."));

children.push(h2("5.3 Compiler workflow"));
children.push(numbered("Name node groups in Blender using the dotted-path convention, e.g. `lscherry.utils.bnodes.TangentFix`, so the router can place them correctly."));
children.push(numbered("Run the **Compile Node Groups** operator. Output goes to `NodeCompilerProperties.compiled_folder` (default `./compiled`, relative to the .blend)."));
children.push(numbered("Move/copy the generated output into `src/nodes/shader/`."));
children.push(numbered("Run `potato reload` and restart Blender to pick up the new nodes."));

children.push(h2("5.4 Shader node categories"));
children.push(body("The committed library under `src/nodes/shader/lscherry/` is organised into these categories:"));
children.push(makeTable(["Category", "Contents (examples)"], [
  ["core", "toon_core, toon_dot, specular_core, reflective_toon, rim_core, toonmetal, toonray…"],
  ["combiner", "blend_color, add_transparent, add_fake_shadow_color, get_light_area…"],
  ["external", "Michos (Genshin Impact / Honkai-3 / Star-Rail), MICA, festivities, MMD matcap, parallax…"],
  ["plugin", "anisotropic_spherical, brush_set…"],
  ["general / utils / vfx / post_production / starters / dev", "World-color provider, utility nodes, VFX, post effects, starter packs, dev/experimental"],
], [2400, 6960]));
children.push(new Paragraph({ children: [new PageBreak()] }));

// ===== 6. CONVENTIONS & REFERENCE =====
children.push(h1("6. Conventions & Reference"));

children.push(h2("6.1 Coding conventions"));
children.push(bullet("`import bpy  # type: ignore` — standard for add-ons; `bpy` is not installed in the dev venv."));
children.push(bullet("Operator `bl_idname`s are namespaced by feature: `lscherry.*`, `lsregistry.*`, `lspotato.*`."));
children.push(bullet("Class-name prefixes: `LSCHERRY_OT_`, `LSREGISTRY_OT_`, `LSPOTATO_OT_`."));
children.push(bullet("Bump `bl_info['version']` in `src/__init__.py` for releases."));
children.push(bullet("Only `flake8` lint gates code (`potato test`) — no formatter config or type checker in CI."));

children.push(h2("6.2 Glossary"));
children.push(makeTable(["Term", "Meaning"], [
  ["LSCherry", "The companion toon-shader project LSPotato supports"],
  ["LSRegistry", "Catalogue of linkable LSCherry assets managed by the add-on"],
  ["AutoSync", "Handler-driven live syncing of lighting/world settings"],
  ["Node library", "Python-encoded ShaderNodeCustomGroup classes in src/nodes/shader/"],
  ["Node Compiler", "Dev operator that generates node source from a live .blend"],
  ["Starter pack", "A preference-gated group of nodes registered into the Add Shader menu"],
  ["rgt_classes", "The ordered list of classes register()/unregister() walk"],
], [2400, 6960]));

children.push(h2("6.3 Quick command card"));
children.push(makeTable(["Task", "Command"], [
  ["Package add-on", "potato package"],
  ["Install (Blender 5.1)", "potato install 5.1"],
  ["Dev reload loop", "potato reload"],
  ["Lint", "potato test"],
  ["Compile nodes", "Run lspotato.compile_node_groups in Blender"],
], [4000, 5360]));

children.push(new Paragraph({
  spacing: { before: 400 },
  border: { top: { style: BorderStyle.SINGLE, size: 6, color: ACCENT, space: 6 } },
  children: [new TextRun({ text: "End of document — LSPotato 2.0.0 Technical Reference & User Guide.", italics: true, color: GREY, size: 18 })],
}));

// ---------- assemble ----------
const doc = new Document({
  creator: "LSPotato Docs",
  title: "LSPotato 2.0.0 — Technical Reference & User Guide",
  description: "Architecture, user guide, and node compiler pipeline for the LSPotato Blender add-on.",
  styles: {
    default: { document: { run: { font: "Arial", size: 22, color: "222222" } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 34, bold: true, font: "Arial", color: ACCENT },
        paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 0,
          border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: LIGHT, space: 4 } } } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 27, bold: true, font: "Arial", color: ACCENT_DK },
        paragraph: { spacing: { before: 220, after: 120 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 23, bold: true, font: "Arial", color: "333333" },
        paragraph: { spacing: { before: 160, after: 80 }, outlineLevel: 2 } },
    ],
  },
  numbering: {
    config: [
      { reference: "bullets", levels: [
        { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 600, hanging: 280 } } } },
        { level: 1, format: LevelFormat.BULLET, text: "–", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 1080, hanging: 280 } } } },
      ] },
      { reference: "steps", levels: [
        { level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 600, hanging: 320 } } } },
      ] },
    ],
  },
  sections: [{
    properties: {
      page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } },
    },
    headers: {
      default: new Header({ children: [new Paragraph({
        spacing: { after: 0 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "DDDDDD", space: 4 } },
        tabStops: [{ type: TabStopType.RIGHT, position: 9360 }],
        children: [
          new TextRun({ text: "LSPotato", bold: true, color: ACCENT, size: 18 }),
          new TextRun({ text: "\tTechnical Reference & User Guide · v2.0.0", color: GREY, size: 16 }),
        ],
      })] }),
    },
    footers: {
      default: new Footer({ children: [new Paragraph({
        spacing: { before: 0 },
        border: { top: { style: BorderStyle.SINGLE, size: 4, color: "DDDDDD", space: 4 } },
        tabStops: [{ type: TabStopType.RIGHT, position: 9360 }],
        children: [
          new TextRun({ text: "© 2026 Lvoxx · MIT License", color: GREY, size: 16 }),
          new TextRun({ text: "\tPage ", color: GREY, size: 16 }),
          new TextRun({ children: [PageNumber.CURRENT], color: GREY, size: 16 }),
          new TextRun({ text: " of ", color: GREY, size: 16 }),
          new TextRun({ children: [PageNumber.TOTAL_PAGES], color: GREY, size: 16 }),
        ],
      })] }),
    },
    children,
  }],
});

const outDir = path.join(__dirname, "..", "..", "..", "docs");
const outPath = path.join(outDir, "LSPotato-Technical-Reference.docx");
fs.mkdirSync(outDir, { recursive: true });
Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(outPath, buf);
  console.log("WROTE", outPath, buf.length, "bytes");
});
