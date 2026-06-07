# -*- coding: utf-8 -*-
"""Dev-only: regenerate per-category node reference docs under docs/nodes/.

Reads ground-truth socket data from _nodes_data.json (produced by
_extract_nodes.py) and emits accurate Markdown with:
  * real Blender menu path per node (derived from bl_label),
  * node description (from the node group's own description when present),
  * Inputs / Outputs tables with type, default, range and a description.

Run with system Python 3.14:  py -3.14 src/mock/_gen_node_docs.py
"""
import json
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
from _doc_content import CATEGORY_META, node_description  # noqa: E402

DATA = os.path.join(HERE, "_nodes_data.json")
DOCS = os.path.abspath(os.path.join(HERE, "..", "..", "docs", "nodes"))

# ---------------------------------------------------------------------------
# Real menu routing (mirrors src/nodes/node_info.py)
# ---------------------------------------------------------------------------
_CATEGORY_MAP = [
    ("lscherry.external.michos.honkai_impact_3.",  "LSCherry/External/Michos/Honkai Impact 3"),
    ("lscherry.external.michos.genshin_impact.",   "LSCherry/External/Michos/Genshin Impact"),
    ("lscherry.external.michos.honkai_star_rail.", "LSCherry/External/Michos/Honkai Star Rail"),
    ("lscherry.external.michos.",                  "LSCherry/External/Michos"),
    ("lscherry.external.",                         "LSCherry/External"),
    ("lscherry.utils.bnodes.",     "LSCherry/Utils/BNodes"),
    ("lscherry.utils.procedural.", "LSCherry/Utils/Procedural"),
    ("lscherry.utils.ramp_style.", "LSCherry/Utils/Ramp Style"),
    ("lscherry.utils.separator.",  "LSCherry/Utils/Separator"),
    ("lscherry.utils.normal.",     "LSCherry/Utils/Normal"),
    ("lscherry.utils.",            "LSCherry/Utils"),
    ("lscherry.starters.strinova.", "LSCherry/Starters/Strinova"),
    ("lscherry.starters.",         "LSCherry/Starters"),
    ("lscherry.combiner.",        "LSCherry/Combiner"),
    ("lscherry.core.",            "LSCherry/Core"),
    ("lscherry.festivities.",     "LSCherry/Festivities"),
    ("lscherry.glotani.",         "LSCherry/GloTAni"),
    ("lscherry.avr.",             "LSCherry/AVR"),
    ("lscherry.xtr.",             "LSCherry/XTR"),
    ("lscherry.mmd.",             "LSCherry/MMD"),
    ("lscherry.mica.",            "LSCherry/MICA"),
    ("lscherry.post_production.", "LSCherry/Post Production"),
    ("lscherry.general.",          "LSCherry/General"),
    ("lscherry.dev.",             "LSCherry/Dev"),
    ("lscherry.plugin.",          "LSCherry/Plugin"),
    ("lscherry.vfx.",             "LSCherry/VFX"),
    ("lscherry.",                 "LSCherry"),
]


def real_category(bl_label):
    low = (bl_label or "").lower()
    for prefix, cat in _CATEGORY_MAP:
        if low.startswith(prefix):
            return cat
    return "LSCherry"


def display_name(bl_label):
    parts = (bl_label or "").split(".")
    return parts[-1].strip() if parts else bl_label


def menu_path(bl_label):
    cat = real_category(bl_label).replace("/", " > ")
    return "Add Shader > {} > {}".format(cat, display_name(bl_label))


# ---------------------------------------------------------------------------
# Folder -> doc file routing (keeps the existing reference-page layout)
# ---------------------------------------------------------------------------
def doc_for(relpath):
    p = relpath
    if p.startswith("lscherry/combiner/"):
        return "combiner.md"
    if p.startswith("lscherry/core/"):
        return "core.md"
    if p.startswith("lscherry/dev/"):
        return "dev.md"
    if p.startswith("lscherry/external/michos/genshin-impact/"):
        return "external-genshin-impact.md"
    if p.startswith("lscherry/external/michos/honkai-impact-3/"):
        return "external-honkai-impact-3.md"
    if p.startswith("lscherry/external/michos/honkai-star-rail/"):
        return "external-honkai-star-rail.md"
    if p.startswith("lscherry/external/festivities/"):
        return "festivities.md"
    if p.startswith("lscherry/external/MICA/"):
        return "mica.md"
    if p.startswith("lscherry/external/glotani"):
        return "glotani.md"
    if p.startswith("lscherry/external/avr"):
        return "avr.md"
    if p.startswith("lscherry/external/xtr"):
        return "xtr.md"
    if p.startswith("lscherry/external/mmd"):
        return "mmd.md"
    if p.startswith("lscherry/general/"):
        return "general.md"
    if p.startswith("lscherry/plugin/"):
        return "plugin.md"
    if p.startswith("lscherry/post_production/"):
        return "post-production.md"
    if p.startswith("lscherry/starters/"):
        return "starters.md"
    if p.startswith("lscherry/utils/"):
        return "utils.md"
    if p.startswith("lscherry/vfx/"):
        return "vfx.md"
    # top-level lscherry/*.py
    if p.startswith("lscherry/") and p.count("/") == 1:
        return "lscherry-root.md"
    return None


# ---------------------------------------------------------------------------
# Type + value formatting
# ---------------------------------------------------------------------------
TYPE_LABEL = {
    "NodeSocketFloat": "Float",
    "NodeSocketColor": "Color (RGBA)",
    "NodeSocketVector": "Vector",
    "NodeSocketShader": "Shader",
    "NodeSocketBool": "Boolean",
    "NodeSocketInt": "Integer",
    "NodeSocketBundle": "Bundle",
    "NodeSocketMenu": "Menu",
}

_INF = 3.4e38


def fnum(x):
    if isinstance(x, float):
        if x == int(x):
            return str(int(x))
        return "{:.4g}".format(x)
    return str(x)


def fmt_default(s):
    v = s.get("default")
    t = s.get("type")
    if v is None:
        return "—"
    if t == "NodeSocketBool":
        return "On" if v else "Off"
    if isinstance(v, (list, tuple)):
        return "(" + ", ".join(fnum(c) for c in v) + ")"
    if isinstance(v, float):
        return fnum(v)
    return str(v)


def fmt_range(s):
    lo, hi = s.get("min"), s.get("max")
    if lo is None and hi is None:
        return "—"
    def f(x):
        if x is None:
            return "?"
        if isinstance(x, (int, float)) and abs(x) >= _INF:
            return "∞" if x > 0 else "-∞"
        return fnum(x)
    if s.get("subtype") == "FACTOR":
        return "{}–{} (factor)".format(f(lo), f(hi))
    return "{} – {}".format(f(lo), f(hi))


# ---------------------------------------------------------------------------
# Socket description heuristics
# ---------------------------------------------------------------------------
# Curated descriptions for common / important socket names (case-insensitive).
SOCKET_DESC = {
    "shader": "Shader stream — connect the surface being processed (in) or pass it on (out).",
    "to agrx": "Secondary shader stream routed to an AgX / view-transform path.",
    "combined": "Flat combined color (all shading baked into RGB), ready for compositing or further color work.",
    "base color": "The surface's lit (fully-illuminated) albedo color.",
    "shadow color": "Color used in the shadow / shaded band of the toon step.",
    "sss color": "Subsurface-scattering tint applied in the deepest shadow band.",
    "rim color": "Color of the rim / fresnel light along the silhouette.",
    "back color": "Color applied to back-facing geometry (inner shadow / translucency look).",
    "spec color": "Color of the specular highlight.",
    "specular color": "Color of the specular highlight.",
    "bright color": "Color injected into the brightest / lit area.",
    "red color": "Tint for the red lightmap/mask channel.",
    "original color": "The unmodified input color, passed through for reference or re-mixing.",
    "color": "Color input/output for this operation.",
    "alpha": "Opacity (0 = fully transparent, 1 = fully opaque).",
    "body alpha": "Opacity of the body material region.",
    "lighmap alpha": "Alpha channel of the lightmap, commonly used as a shadow/AO factor.",
    "lightmap alpha": "Alpha channel of the lightmap, commonly used as a shadow/AO factor.",
    "normal": "Surface normal vector. Leave unconnected to use the geometry normal, or feed a normal map.",
    "roughness": "Microsurface roughness — lower is sharper/glossier, higher is more diffuse.",
    "uv": "UV texture coordinates used to sample maps for this node.",
    "scale": "Scale of the pattern / texture — higher values tile it more densely.",
    "size": "Size of the feature (dot, cell, highlight, …); larger values enlarge it.",
    "seed": "Random seed; change it to get a different variation of the procedural result.",
    "fac": "Blend factor (0 = first/original input, 1 = full effect).",
    "factor": "Blend factor (0 = first/original input, 1 = full effect).",
    "strength": "Overall intensity of the effect.",
    "smooth": "Softness of the transition edge — 0 is a hard toon step, higher feathers it.",
    "threshold": "Cutoff position of the toon step; shifts where light turns to shadow.",
    "distortion": "Amount of procedural distortion / warping applied.",
    "detail": "Procedural detail / number of noise octaves — higher adds finer structure.",
    "lacunarity": "Frequency gap between procedural noise octaves.",
    "pattern": "Pattern color/mask multiplied into the surface (connect a Plugin pattern node here).",
    "emission": "Emission color added on top of the shading.",
    "emission strength": "Multiplier for the emission color's brightness.",
    "metal": "Metalness factor — blends the surface toward a reflective metal look.",
    "shading": "Incoming shading/lighting term used by this node.",
    "shadow": "Shadow term/mask consumed or produced by this node.",
    "shadow mask": "Mask isolating the shaded region (1 in shadow, 0 in light).",
    "diffuse mask": "Mask of the diffuse-lit region.",
    "shadow factor": "Scalar controlling how strongly the shadow band is applied.",
    "deep strength": "Intensity of the deepest (SSS / core) shadow band.",
    "face value": "Face-shadow ramp coordinate, typically driven by the light direction vs. the face.",
    "face map": "Face SDF / ramp map used to drive soft anime face shadows.",
    "lightmap": "Packed lightmap texture whose channels encode shadow, specular, AO, etc.",
    "lightmap texture": "Packed lightmap texture whose channels encode shadow, specular, AO, etc.",
    "custom ramp": "User-supplied ramp color that overrides the built-in toon ramp.",
    "enable custom ramp": "When on, use the supplied Custom Ramp instead of the internal ramp.",
    "blend with custom ramp": "How much the custom ramp is mixed over the default shading.",
    "toon style": "Ramp-style vector selecting the toon band shaping (from a Ramp Style node).",
    "sss style": "Ramp-style vector selecting the SSS band shaping (from a Ramp Style node).",
    "back style": "Ramp-style vector selecting the back-face band shaping (from a Ramp Style node).",
    "disable toon style": "Bypass the toon ramp styling.",
    "disable sss style": "Bypass the SSS ramp styling.",
    "disable back style": "Bypass the back-face ramp styling.",
    "value enhance": "Boosts the value/contrast of the result.",
    "ramp size": "Width of the ramp transition region.",
    "rim strength": "Brightness of the rim light.",
    "rim size": "Width of the rim light band.",
    "rim smooth": "Softness of the rim light edge.",
    "specular tint": "How much the specular highlight is tinted by the base color.",
    "result": "Computed result of this node.",
    "builder": "Aggregated build bundle passed between starter/builder nodes.",
    "o": "Output value of the logic / math operation.",
    "a": "First operand.",
    "b": "Second operand.",
    "enable light blend": "When on, blends the effect with scene lighting.",
    "world color": "Scene world/ambient color fed into the shading.",
}

# Token-based fallback fragments (checked as substrings, longest first).
TOKEN_DESC = [
    ("range ", "Ramp range stop — position of a band edge in the generated color ramp."),
    ("map ", "Ramp color stop — one color of the generated toon ramp."),
    ("bundle", "Bundle socket grouping several related values passed as one connection."),
    ("color", "Color value for this slot."),
    ("alpha", "Opacity / alpha value."),
    ("strength", "Intensity of this contribution."),
    ("roughness", "Surface roughness for this term."),
    ("normal", "Normal vector for this term."),
    ("threshold", "Step / cutoff position."),
    ("scale", "Scale of this feature."),
    ("size", "Size of this feature."),
    ("smooth", "Edge softness."),
    ("mask", "Mask isolating a region (0–1)."),
    ("factor", "Blend factor (0–1)."),
    ("weight", "Relative weight of this contribution."),
    ("offset", "Positional offset applied to this term."),
    ("uv", "UV coordinates."),
    ("seed", "Random seed."),
    ("shader", "Shader stream."),
]

TYPE_FALLBACK = {
    "NodeSocketShader": "Shader stream.",
    "NodeSocketColor": "Color value.",
    "NodeSocketFloat": "Scalar value.",
    "NodeSocketVector": "Vector value.",
    "NodeSocketBool": "Toggle for this option.",
    "NodeSocketInt": "Integer count.",
    "NodeSocketBundle": "Bundle of grouped values.",
    "NodeSocketMenu": "Mode selector.",
}


def describe_socket(s):
    name = (s.get("name") or "").strip()
    key = name.lower()
    if s.get("description"):
        return s["description"]
    if key in SOCKET_DESC:
        return SOCKET_DESC[key]
    for tok, desc in TOKEN_DESC:
        if tok in key:
            return desc
    return TYPE_FALLBACK.get(s.get("type"), "Value for this slot.")


def humanize(name):
    """Turn a draw_label / class name into a readable node description stub."""
    return name


# ---------------------------------------------------------------------------
# Markdown emission
# ---------------------------------------------------------------------------
def socket_table(socks, is_input):
    if not socks:
        return "_None._\n"
    if is_input:
        head = "| Input | Type | Default | Range | Description |\n"
        head += "|---|---|---|---|---|\n"
        rows = []
        for s in socks:
            rows.append("| `{}` | {} | {} | {} | {} |".format(
                s.get("name") or "—",
                TYPE_LABEL.get(s.get("type"), s.get("type") or "—"),
                fmt_default(s),
                fmt_range(s),
                describe_socket(s),
            ))
        return head + "\n".join(rows) + "\n"
    else:
        head = "| Output | Type | Description |\n|---|---|---|\n"
        rows = []
        for s in socks:
            rows.append("| `{}` | {} | {} |".format(
                s.get("name") or "—",
                TYPE_LABEL.get(s.get("type"), s.get("type") or "—"),
                describe_socket(s),
            ))
        return head + "\n".join(rows) + "\n"


def panel_note(node):
    panels = node.get("panels") or {}
    if not panels:
        return ""
    items = []
    for var in node.get("panel_order", []):
        p = panels.get(var, {})
        nm = p.get("name")
        desc = p.get("description")
        if nm:
            items.append("**{}**{}".format(nm, " — " + desc if desc else ""))
    if not items:
        return ""
    return ("\nInputs are grouped into collapsible panels in the N-panel: "
            + "; ".join(items) + ".\n")


def node_section(node, doc):
    label = node.get("draw_label") or display_name(node.get("bl_label"))
    out = []
    out.append("### {}\n".format(label))
    desc = node_description(doc, label, node.get("description"))
    if desc:
        out.append(desc.strip() + "\n")
    out.append("**Menu:** `{}`\n".format(menu_path(node.get("bl_label"))))
    pn = panel_note(node)
    if pn:
        out.append(pn)
    out.append("**Inputs**\n")
    out.append(socket_table(node.get("inputs", []), True))
    out.append("\n**Outputs**\n")
    out.append(socket_table(node.get("outputs", []), False))
    return "\n".join(out)


def build_header(doc, count):
    meta = CATEGORY_META.get(doc)
    if not meta:
        return "# {}\n\n_{} node(s)._\n".format(doc.replace(".md", ""), count)
    h = ["# {}\n".format(meta["title"])]
    if meta.get("menu"):
        h.append("**Menu path:** `{}`\n".format(meta["menu"]))
    h.append("> {} node(s) in this category. Socket types, defaults and ranges below "
             "are extracted directly from the compiled node source — they are the "
             "ground truth.\n".format(count))
    h.append(meta["overview"] + "\n")
    if meta.get("use_cases"):
        h.append("## When to use it\n")
        h.append("\n".join("- " + u for u in meta["use_cases"]) + "\n")
    if meta.get("usage"):
        h.append("## How to use it\n")
        h.append("\n".join("{}. {}".format(i + 1, s)
                           for i, s in enumerate(meta["usage"])) + "\n")
    h.append("## Node reference\n")
    return "\n".join(h)


def main():
    with open(DATA, encoding="utf-8") as f:
        data = json.load(f)

    buckets = {}
    for rel, node in data.items():
        doc = doc_for(rel)
        if doc is None:
            print("UNROUTED:", rel)
            continue
        buckets.setdefault(doc, []).append((rel, node))

    for doc, items in sorted(buckets.items()):
        items.sort(key=lambda kv: (kv[1].get("draw_label") or kv[0]).lower())
        node_parts = [node_section(node, doc) for rel, node in items]
        body = build_header(doc, len(items)) + "\n" + "\n---\n\n".join(node_parts)
        with open(os.path.join(DOCS, doc), "w", encoding="utf-8") as f:
            f.write(body.rstrip() + "\n")
        print("{:40s} {:3d} nodes".format(doc, len(items)))


if __name__ == "__main__":
    main()
