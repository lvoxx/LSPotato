"""
Router
Xác định subfolder compiled và bl_label prefix cho từng node group
dựa trên tên collection/material trong Blender (ng.name).

Quy ước tên node group trong LSCherry:
    "lscherry.combiner.NodeName"
    "lscherry.core.NodeName"
    "lscherry.utils.bnodes.NodeName"
    "lscherry.external.michos.genshin_impact.NodeName"
    "lscherry.plugin.NodeName"
    v.v.

Router nhìn vào tiền tố của ng.name để quyết định:
    1. subpath  → subfolder trong compiled/  (vd: "lscherry/utils/bnodes")
    2. label_prefix → phần đầu của bl_label  (vd: "lscherry.utils.bnodes")

Nếu tên không khớp prefix nào → fallback về "lscherry" (root).
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Routing table
# Thứ tự: CỤ THỂ NHẤT trước — match prefix đầu tiên tìm được
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

# Fallback nếu không match gì
_DEFAULT_SUBPATH       = "lscherry"
_DEFAULT_LABEL_PREFIX  = "lscherry"


def resolve(ng_name: str) -> tuple[str, str]:
    """
    Nhận ng.name, trả về (subpath, label_prefix).

    Ví dụ:
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

    Ví dụ:
        ng_name="lscherry.utils.bnodes.TangentFix", label_prefix="lscherry.utils.bnodes"
            → "lscherry.utils.bnodes.TangentFix"   (giữ nguyên nếu đã đúng format)

        ng_name="TangentFix", label_prefix="lscherry"
            → "lscherry.TangentFix"
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

    compiled/lscherry/utils/bnodes/  →  depth=3  →  "....node"
    compiled/lscherry/               →  depth=1  →  "..node"

    Quy ước: mỗi level thêm 1 dấu chấm.
    Base: từ compiled/ lên nodes/ là 1 level (".."),
          mỗi subfolder thêm 1 level.
    """
    depth = len([p for p in subpath.split("/") if p])  # số folder
    dots  = "." * (depth + 1)   # +1 vì từ compiled/ lên nodes/
    return f"{dots}node"