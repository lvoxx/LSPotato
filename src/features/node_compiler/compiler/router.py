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
    ("lscherry/external/michos/honkai-impact-3",   "lscherry.external.michos.honkai_impact_3",   "lscherry.external.michos.honkai_impact_3."),
    ("lscherry/external/michos/genshin-impact",    "lscherry.external.michos.genshin_impact",    "lscherry.external.michos.genshin_impact."),
    ("lscherry/external/michos/honkai-star-rail",  "lscherry.external.michos.honkai_star_rail",  "lscherry.external.michos.honkai_star_rail."),
    
    # ── External / Others ───────────────────────────────────────────────────
    ("lscherry/external/festivities",              "lscherry.external.festivities",              "lscherry.external.festivities."),
    ("lscherry/external/GloTAni",                  "lscherry.external.GloTAni",                  "lscherry.external.GloTAni."),
    ("lscherry/external/AVR",                      "lscherry.external.AVR",                      "lscherry.external.AVR."),
    ("lscherry/external/XTR",                      "lscherry.external.XTR",                      "lscherry.external.XTR."),
    ("lscherry/external/MMD",                      "lscherry.external.MMD",                      "lscherry.external.MMD."),
    ("lscherry/external/MICA",                     "lscherry.external.MICA",                     "lscherry.external.MICA."),
    
    # ── External / Fallback ───────────────────────────────────────────────────
    ("lscherry/external",                          "lscherry.external",                          "lscherry.external."),


    # ── Utils subgroups ────────────────────────────────────────────────────
    ("lscherry/utils/bnodes",                      "lscherry.utils.bnodes",                      "lscherry.utils.bnodes."),
    ("lscherry/utils/procedural",                  "lscherry.utils.procedural",                  "lscherry.utils.procedural."),
    ("lscherry/utils/ramp-style",                  "lscherry.utils.ramp_style",                  "lscherry.utils.ramp_style."),
    ("lscherry/utils/seperator",                   "lscherry.utils.seperator",                   "lscherry.utils.seperator."),
    ("lscherry/utils/normal",                      "lscherry.utils.normal",                      "lscherry.utils.normal."),
    ("lscherry/utils",                             "lscherry.utils",                             "lscherry.utils."),


    # ── Standalone groups ──────────────────────────────────────────────────
    ("lscherry/combiner",                          "lscherry.combiner",                          "lscherry.combiner."),
    ("lscherry/core",                              "lscherry.core",                              "lscherry.core."),
    ("lscherry/global",                            "lscherry.global",                            "lscherry.global."),
    ("lscherry/post-production",                   "lscherry.post_production",                   "lscherry.post_production."),
    ("lscherry/dev",                               "lscherry.dev",                               "lscherry.dev."),
    ("lscherry/plugin",                            "lscherry.plugin",                            "lscherry.plugin."),
    ("lscherry/vfx",                               "lscherry.vfx",                               "lscherry.vfx."),


    # ── Root (fallback) ────────────────────────────────────────────────────
    ("lscherry",                                   "lscherry",                                   "lscherry."),

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
    Computes the relative import prefix from src/nodes/shader/<subpath>/ back to src/nodes/.

    A file at src/nodes/shader/lscherry/x.py has package src.nodes.shader.lscherry.
    To reach src.nodes from there requires 2 levels up (shader→nodes), plus 1 per
    subfolder component inside lscherry/.

    src/nodes/shader/lscherry/          → depth=1 → "...node"   (3 dots)
    src/nodes/shader/lscherry/core/     → depth=2 → "....node"  (4 dots)
    src/nodes/shader/lscherry/u/bnodes/ → depth=3 → ".....node" (5 dots)
    """
    depth = len([p for p in subpath.split("/") if p])  # number of path components
    dots  = "." * (depth + 2)   # +2: one for shader/, one for lscherry root
    return f"{dots}node"


# ---------------------------------------------------------------------------
# Material-based routing helpers
# ---------------------------------------------------------------------------

def build_direct_material_ng_map() -> dict[str, str]:
    """
    Build a mapping: node_group_name → material_name using DIRECT ownership only.

    Only inspects node groups referenced directly in each material's node tree —
    nested (transitive) references are excluded so that sub-materials with more
    specific namespaces always win over root materials.

    When multiple materials directly reference the same node group, the most
    specific one wins (most dots in the material name = deepest namespace).
    """
    ng_owners: dict[str, dict[str, int]] = {}
    for mat in bpy.data.materials:
        if not mat.node_tree:
            continue
        depth = mat.name.count(".")
        for node in mat.node_tree.nodes:
            if node.type == 'GROUP' and node.node_tree:
                name = node.node_tree.name
                ng_owners.setdefault(name, {})[mat.name] = depth
    return {
        ng: max(owners, key=lambda m: owners[m])
        for ng, owners in ng_owners.items()
    }


def material_name_to_route(mat_name: str) -> tuple[str, str] | None:
    """
    Convert a Blender material name to (subpath, label_prefix).

    Convention: materials are named "lscherry.<subcategory>.<DisplayName>".
    The subcategory path (everything between "lscherry." and the last segment)
    becomes the subfolder under compiled/lscherry/.

    Examples:
        'lscherry.LSCherry'            → ('lscherry', 'lscherry')
        'lscherry.core.ToonDiffuse'    → ('lscherry/core', 'lscherry.core')
        'lscherry.utils.ramp-style.X'  → ('lscherry/utils/ramp-style',
                                          'lscherry.utils.ramp_style')

    Returns None if the name does not start with 'lscherry.'.
    """
    if not mat_name.lower().startswith("lscherry."):
        return None
    remainder = mat_name[len("lscherry."):]   # e.g. "LSCherry" or "core.ToonDiffuse"
    parts = remainder.split(".")
    if len(parts) <= 1:
        # Root material like "lscherry.LSCherry" — no subfolder
        return "lscherry", "lscherry"
    subfolder = parts[:-1]      # all segments except the material display name
    subpath      = "lscherry/" + "/".join(subfolder)
    label_prefix = "lscherry." + ".".join(p.replace("-", "_") for p in subfolder)
    return subpath, label_prefix