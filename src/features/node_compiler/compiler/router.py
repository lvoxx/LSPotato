"""
Router
Determines the compiled subfolder and bl_label prefix for each node group
based on the collection/material name in Blender (ng.name).

LSCherry node group naming convention:
    "lscherry.combiner.NodeName"
    "lscherry.core.NodeName"
    "lscherry.utils.bnodes.NodeName"
    "lscherry.external.michos.genshin_impact.NodeName"
    "lscherry.plugin.NodeName"
    etc.

Router inspects the prefix of ng.name to decide:
    1. subpath  → subfolder inside compiled/  (e.g. "lscherry/utils/bnodes")
    2. label_prefix → the leading part of bl_label  (e.g. "lscherry.utils.bnodes")

If the name matches no prefix → fall back to "lscherry" (root).
"""

from __future__ import annotations

import bpy  # type: ignore

# ---------------------------------------------------------------------------
# Routing table
# Order: MOST SPECIFIC first — match the first prefix found
# (subpath, label_prefix, ng_name_prefix)
# ---------------------------------------------------------------------------
_ROUTES: list[tuple[str, str, str]] = [
    # ── External / Michos ──────────────────────────────────────────────────
    ("lscherry/external/michos/honkai_impact_3",   "lscherry.external.michos.honkai_impact_3",   "lscherry.external.michos.honkai_impact_3."),
    ("lscherry/external/michos/genshin_impact",    "lscherry.external.michos.genshin_impact",    "lscherry.external.michos.genshin_impact."),
    ("lscherry/external/michos/honkai_star_rail",  "lscherry.external.michos.honkai_star_rail",  "lscherry.external.michos.honkai_star_rail."),
    ("lscherry/external/michos",                   "lscherry.external.michos",                   "lscherry.external.michos."),
    ("lscherry/external",                          "lscherry.external",                           "lscherry.external."),

    # ── Utils subgroups ────────────────────────────────────────────────────
    ("lscherry/utils/bnodes",    "lscherry.utils.bnodes",    "lscherry.utils.bnodes."),
    ("lscherry/utils/procedural","lscherry.utils.procedural","lscherry.utils.procedural."),
    ("lscherry/utils/ramp_style","lscherry.utils.ramp_style","lscherry.utils.ramp_style."),
    ("lscherry/utils/separator", "lscherry.utils.separator", "lscherry.utils.separator."),
    ("lscherry/utils/normal",    "lscherry.utils.normal",    "lscherry.utils.normal."),
    ("lscherry/utils",           "lscherry.utils",            "lscherry.utils."),

    # ── Standalone groups ──────────────────────────────────────────────────
    ("lscherry/combiner",        "lscherry.combiner",        "lscherry.combiner."),
    ("lscherry/core",            "lscherry.core",            "lscherry.core."),
    ("lscherry/festivities",     "lscherry.festivities",     "lscherry.festivities."),
    ("lscherry/glotani",         "lscherry.glotani",         "lscherry.glotani."),
    ("lscherry/avr",             "lscherry.avr",             "lscherry.avr."),
    ("lscherry/xtr",             "lscherry.xtr",             "lscherry.xtr."),
    ("lscherry/mmd",             "lscherry.mmd",             "lscherry.mmd."),
    ("lscherry/mica",            "lscherry.mica",            "lscherry.mica."),
    ("lscherry/post_production", "lscherry.post_production", "lscherry.post_production."),
    ("lscherry/global",          "lscherry.global",          "lscherry.global."),
    ("lscherry/dev",             "lscherry.dev",             "lscherry.dev."),
    ("lscherry/plugin",          "lscherry.plugin",          "lscherry.plugin."),
    ("lscherry/vfx",             "lscherry.vfx",             "lscherry.vfx."),

    # ── Root (fallback) ────────────────────────────────────────────────────
    ("lscherry",                 "lscherry",                  "lscherry."),
]

# Fallback if nothing matches
_DEFAULT_SUBPATH       = "lscherry"
_DEFAULT_LABEL_PREFIX  = "lscherry"


def resolve(ng_name: str) -> tuple[str, str]:
    """
    Takes ng.name and returns (subpath, label_prefix).

    Example:
        "lscherry.utils.bnodes.TangentFix"
            → ("lscherry/utils/bnodes", "lscherry.utils.bnodes")

        "lscherry.plugin.Pattern"
            → ("lscherry/plugin", "lscherry.plugin")

        "SomeRandomGroup"
            → ("lscherry", "lscherry")   ← fallback
    """
    name_lower = ng_name.lower()
    for subpath, label_prefix, ng_prefix in _ROUTES:
        if name_lower.startswith(ng_prefix.lower()):
            return subpath, label_prefix
    return _DEFAULT_SUBPATH, _DEFAULT_LABEL_PREFIX


def make_bl_label(ng_name: str, label_prefix: str) -> str:
    """
    Xây dựng bl_label theo quy ước "prefix.DisplayName".

    Nếu ng_name đã có label_prefix → dùng nguyên (e.g.
    "lscherry.utils.bnodes.TangentFix" + "lscherry.utils.bnodes"
        → "lscherry.utils.bnodes.TangentFix").

    Nếu ng_name dùng naming convention khác (e.g. "lscherry.Plugin: Brush Set"
    với label_prefix "lscherry.plugin"), ta strip "lscherry." nếu có
    và prepend label_prefix để tránh double-prefix:
        "lscherry.Plugin: Brush Set" + "lscherry.plugin"
            → "lscherry.plugin.Plugin: Brush Set"
    """
    name_lower = ng_name.lower()
    prefix_lower = (label_prefix + ".").lower()

    if name_lower.startswith(prefix_lower):
        return ng_name

    # Strip "lscherry." prefix if present to avoid double-prefixing
    base = ng_name
    if base.lower().startswith("lscherry."):
        base = base[len("lscherry."):]
    return f"{label_prefix}.{base}"


def make_import_prefix(subpath: str) -> str:
    """
    Computes the relative import prefix from compiled/<subpath>/ back to src/nodes/.

    compiled/lscherry/utils/bnodes/  →  depth=3  →  "....node"
    compiled/lscherry/               →  depth=1  →  "..node"

    Convention: each level adds 1 dot.
    Base: from compiled/ up to nodes/ is 1 level (".."),
          each subfolder adds 1 more level.
    """
    depth = len([p for p in subpath.split("/") if p])  # number of folders
    dots  = "." * (depth + 1)   # +1 because from compiled/ up to nodes/
    return f"{dots}node"


# ---------------------------------------------------------------------------
# Material-based routing helpers
# ---------------------------------------------------------------------------

def _build_ng_deps() -> dict[str, set[str]]:
    """
    Build a dependency graph: node_group_name → set of nested (child) node group names.

    Traverses every node group's node tree to find GROUP node references.
    """
    deps: dict[str, set[str]] = {}
    for ng in bpy.data.node_groups:
        children: set[str] = set()
        for node in ng.nodes:
            if node.type == 'GROUP' and node.node_tree:
                children.add(node.node_tree.name)
        deps[ng.name] = children
    return deps


def build_material_ng_map() -> dict[str, str]:
    """
    Build a mapping: node_group_name → material_name using transitive ownership.

    For each material, traces ALL node groups reachable from it through the
    node group dependency graph (direct + transitive/recursive usage).

    A node group is assigned to a material's folder if and only if it belongs
    to exactly one material's transitive closure. Node groups that are reachable
    from multiple materials are excluded (ambiguous/shared utilities), and they
    fall back to the router's default routing.
    """
    deps = _build_ng_deps()

    # For each material, collect its transitively-reachable node groups
    material_ngs: dict[str, set[str]] = {}
    for mat in bpy.data.materials:
        if not mat.node_tree:
            continue
        root: set[str] = set()
        for node in mat.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree:
                root.add(node.node_tree.name)
        if not root:
            continue

        visited = set(root)
        queue  = list(root)
        while queue:
            current = queue.pop(0)
            for child in deps.get(current, set()):
                if child not in visited:
                    visited.add(child)
                    queue.append(child)
        material_ngs[mat.name] = visited

    # Count how many materials own each node group
    ng_owners: dict[str, set[str]] = {}
    for mat_name, ng_set in material_ngs.items():
        for ng_name in ng_set:
            ng_owners.setdefault(ng_name, set()).add(mat_name)

    # Only unambiguous: owned by exactly one material
    return {
        ng_name: next(iter(owners))
        for ng_name, owners in ng_owners.items()
        if len(owners) == 1
    }


def sanitize_material_name(mat_name: str) -> str:
    """
    Convert a Blender material name into a valid folder name.

    Examples:
        'lscherry.LSCherry'  → 'LSCherry'
        'lscherry.Plugin'    → 'Plugin'
        'My Custom Material' → 'My_Custom_Material'
    """
    # Take the segment after the last dot (if any) — strips the vendor prefix
    if "." in mat_name:
        base = mat_name.rsplit(".", 1)[1]
    else:
        base = mat_name
    clean = "".join(c if c.isalnum() or c in "_-" else "_" for c in base)
    return clean.strip("_") or "Unnamed"