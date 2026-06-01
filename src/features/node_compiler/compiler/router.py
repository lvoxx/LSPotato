"""
Router
Xác định subfolder compiled và bl_label prefix cho từng node group
dựa trên tên collection/material trong Blender (ng.name).

Quy ước tên node group trong LSCherry:
    "cherry.combiner.NodeName"
    "cherry.core.NodeName"
    "cherry.utils.bnodes.NodeName"
    "cherry.external.michos.genshin_impact.NodeName"
    "cherry.plugin.NodeName"
    v.v.

Router nhìn vào tiền tố của ng.name để quyết định:
    1. subpath  → subfolder trong compiled/  (vd: "cherry/utils/bnodes")
    2. label_prefix → phần đầu của bl_label  (vd: "cherry.utils.bnodes")

Nếu tên không khớp prefix nào → fallback về "cherry" (root).
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Routing table
# Thứ tự: CỤ THỂ NHẤT trước — match prefix đầu tiên tìm được
# (subpath, label_prefix, ng_name_prefix)
# ---------------------------------------------------------------------------
_ROUTES: list[tuple[str, str, str]] = [
    # ── External / Michos ──────────────────────────────────────────────────
    ("cherry/external/michos/honkai_impact_3",   "cherry.external.michos.honkai_impact_3",   "cherry.external.michos.honkai_impact_3."),
    ("cherry/external/michos/genshin_impact",    "cherry.external.michos.genshin_impact",    "cherry.external.michos.genshin_impact."),
    ("cherry/external/michos/honkai_star_rail",  "cherry.external.michos.honkai_star_rail",  "cherry.external.michos.honkai_star_rail."),
    ("cherry/external/michos",                   "cherry.external.michos",                   "cherry.external.michos."),
    ("cherry/external",                          "cherry.external",                           "cherry.external."),

    # ── Utils subgroups ────────────────────────────────────────────────────
    ("cherry/utils/bnodes",    "cherry.utils.bnodes",    "cherry.utils.bnodes."),
    ("cherry/utils/procedural","cherry.utils.procedural","cherry.utils.procedural."),
    ("cherry/utils/ramp_style","cherry.utils.ramp_style","cherry.utils.ramp_style."),
    ("cherry/utils/separator", "cherry.utils.separator", "cherry.utils.separator."),
    ("cherry/utils/normal",    "cherry.utils.normal",    "cherry.utils.normal."),
    ("cherry/utils",           "cherry.utils",            "cherry.utils."),

    # ── Standalone groups ──────────────────────────────────────────────────
    ("cherry/combiner",        "cherry.combiner",        "cherry.combiner."),
    ("cherry/core",            "cherry.core",            "cherry.core."),
    ("cherry/festivities",     "cherry.festivities",     "cherry.festivities."),
    ("cherry/glotani",         "cherry.glotani",         "cherry.glotani."),
    ("cherry/avr",             "cherry.avr",             "cherry.avr."),
    ("cherry/xtr",             "cherry.xtr",             "cherry.xtr."),
    ("cherry/mmd",             "cherry.mmd",             "cherry.mmd."),
    ("cherry/mica",            "cherry.mica",            "cherry.mica."),
    ("cherry/post_production", "cherry.post_production", "cherry.post_production."),
    ("cherry/global",          "cherry.global",          "cherry.global."),
    ("cherry/dev",             "cherry.dev",             "cherry.dev."),
    ("cherry/plugin",          "cherry.plugin",          "cherry.plugin."),
    ("cherry/vfx",             "cherry.vfx",             "cherry.vfx."),

    # ── Root (fallback) ────────────────────────────────────────────────────
    ("cherry",                 "cherry",                  "cherry."),
]

# Fallback nếu không match gì
_DEFAULT_SUBPATH       = "cherry"
_DEFAULT_LABEL_PREFIX  = "cherry"


def resolve(ng_name: str) -> tuple[str, str]:
    """
    Nhận ng.name, trả về (subpath, label_prefix).

    Ví dụ:
        "cherry.utils.bnodes.TangentFix"
            → ("cherry/utils/bnodes", "cherry.utils.bnodes")

        "cherry.plugin.Pattern"
            → ("cherry/plugin", "cherry.plugin")

        "SomeRandomGroup"
            → ("cherry", "cherry")   ← fallback
    """
    name_lower = ng_name.lower()
    for subpath, label_prefix, ng_prefix in _ROUTES:
        if name_lower.startswith(ng_prefix.lower()):
            return subpath, label_prefix
    return _DEFAULT_SUBPATH, _DEFAULT_LABEL_PREFIX


def make_bl_label(ng_name: str, label_prefix: str) -> str:
    """
    Xây dựng bl_label theo quy ước "prefix.DisplayName".

    Ví dụ:
        ng_name="cherry.utils.bnodes.TangentFix", label_prefix="cherry.utils.bnodes"
            → "cherry.utils.bnodes.TangentFix"   (giữ nguyên nếu đã đúng format)

        ng_name="TangentFix", label_prefix="cherry"
            → "cherry.TangentFix"
    """
    name_lower = ng_name.lower()
    prefix_lower = (label_prefix + ".").lower()

    if name_lower.startswith(prefix_lower):
        # ng_name đã có prefix đúng → dùng nguyên
        return ng_name
    else:
        # Ghép prefix vào
        return f"{label_prefix}.{ng_name}"


def make_import_prefix(subpath: str) -> str:
    """
    Tính import prefix tương đối từ compiled/<subpath>/ về src/nodes/.

    compiled/cherry/utils/bnodes/  →  depth=3  →  "....node"
    compiled/cherry/               →  depth=1  →  "..node"

    Quy ước: mỗi level thêm 1 dấu chấm.
    Base: từ compiled/ lên nodes/ là 1 level (".."),
          mỗi subfolder thêm 1 level.
    """
    depth = len([p for p in subpath.split("/") if p])  # số folder
    dots  = "." * (depth + 1)   # +1 vì từ compiled/ lên nodes/
    return f"{dots}node"