"""
Code Generator
Assembles a complete Python class string from a NodeGroupInfo dict.
The import path for the base class (ShaderNode / GeometryNode) is
computed dynamically based on the compiled subfolder depth.
"""

from __future__ import annotations

_I1 = "    "    # 4 spaces — class body
_I2 = "        "  # 8 spaces — method body

_NG_TYPE_TO_TREE = {
    "SHADER":      "ShaderNodeTree",
    "GEOMETRY":    "GeometryNodeTree",
    "COMPOSITING": "CompositorNodeTree",
}

_NG_TYPE_TO_BASE = {
    "SHADER":      "ShaderNode",
    "GEOMETRY":    "GeometryNode",
    "COMPOSITING": "CompositorNode",
}


# ---------------------------------------------------------------------------
# Public
# ---------------------------------------------------------------------------

def generate_class(
    info: dict,
    class_name: str,
    import_prefix: str = "...node",
    compiled_nodes: "dict[str, tuple[str, str]]" = {},
) -> str:
    """
    Return the full Python source for one compiled node class.

    Parameters
    ----------
    info           : NodeGroupInfo dict from analyzer.analyze_node_group()
    class_name     : e.g. 'ShaderNodeCompiled_TangentFix'
    import_prefix  : relative import path to node.py, e.g. '...node'
    compiled_nodes : mapping  original_ng_name → (compiled_classname, stable_key)
                     used so GROUP-node references inside createNodetree call
                     create_node_group() on the nested compiled class instead of
                     looking up the original blend-file node group by name.
    """
    ng_type = info["type"]
    base    = _NG_TYPE_TO_BASE.get(ng_type, "ShaderNode")
    tree_t  = _NG_TYPE_TO_TREE.get(ng_type, "ShaderNodeTree")

    # Display name shown in the node header — last dot-separated segment
    full_label   = info["bl_label"]
    display_name = full_label.rsplit(".", 1)[-1].strip() if "." in full_label else full_label

    lines: list[str] = []

    # ── header ──────────────────────────────────────────────────────────────
    lines += [
        "import bpy  # type: ignore",
        f"from {import_prefix} import {base}",
        "",
        "",
        f"class {class_name}({base}):",
        f"{_I1}bl_idname = {_repr(class_name)}",
        f"{_I1}bl_label = {_repr(full_label)}",
        f'{_I1}bl_icon = "NONE"',
        f'{_I1}_PREFIX = "."',
        "",
    ]

    # draw_label returns just the user-facing name (no namespace prefix)
    lines += [
        f"{_I1}def draw_label(self):",
        f"{_I2}return {_repr(display_name)}",
        "",
    ]

    # ── custom props (Image / UV) ────────────────────────────────────────────
    prop_lines = _gen_props(info)
    if prop_lines:
        lines += prop_lines
        lines.append("")

    # ── init() ──────────────────────────────────────────────────────────────
    lines += _gen_init(info)
    lines.append("")

    # ── draw_buttons() ──────────────────────────────────────────────────────
    draw_lines = _gen_draw_buttons(info)
    if draw_lines:
        lines += draw_lines
        lines.append("")

    # ── createNodetree() ────────────────────────────────────────────────────
    lines += _gen_create_nodetree(info, tree_t, compiled_nodes)
    lines.append("")

    # ── valuesUpdate() ──────────────────────────────────────────────────────
    if info["has_image_nodes"] or info["has_uv_nodes"]:
        lines += _gen_values_update(info)
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Section generators
# ---------------------------------------------------------------------------

def _gen_props(info: dict) -> list[str]:
    lines: list[str] = []
    if info["has_image_nodes"]:
        lines += [
            f"{_I1}image_texture: bpy.props.PointerProperty(",
            f'{_I1}{_I1}name="Image Texture",',
            f"{_I1}{_I1}type=bpy.types.Image,",
            f'{_I1}{_I1}description="Image texture used by this node",',
            f"{_I1}{_I1}update=lambda self, ctx: self.valuesUpdate(ctx),",
            f"{_I1})  # type: ignore",
        ]
    if info["has_uv_nodes"]:
        lines += [
            f"{_I1}uv_map: bpy.props.StringProperty(",
            f'{_I1}{_I1}name="UV Map",',
            f'{_I1}{_I1}description="UV layer to use",',
            f'{_I1}{_I1}default="",',
            f"{_I1}{_I1}update=lambda self, ctx: self.valuesUpdate(ctx),",
            f"{_I1})  # type: ignore",
        ]
    return lines


def _gen_init(info: dict) -> list[str]:
    lines = [
        f"{_I1}def init(self, context):",
        f"{_I2}self.getNodetree(self.name + '_node_tree')",
    ]
    for sock in info["interface"]:
        if sock["in_out"] != "INPUT":
            continue
        dv = sock["default_value"]
        if dv is None:
            continue
        lines.append(
            f"{_I2}self.inputs[{_repr(sock['name'])}].default_value = {_repr_val(dv)}"
        )
    return lines


def _gen_draw_buttons(info: dict) -> list[str]:
    if not info["has_image_nodes"] and not info["has_uv_nodes"]:
        return []
    lines = [f"{_I1}def draw_buttons(self, context, layout):"]
    if info["has_image_nodes"]:
        lines.append(
            f'{_I2}layout.template_ID(self, "image_texture", open="image.open")'
        )
    if info["has_uv_nodes"]:
        lines += [
            f"{_I2}obj = context.active_object",
            f"{_I2}if obj and obj.data and hasattr(obj.data, 'uv_layers'):",
            f'{_I2}{_I1}layout.prop_search(self, "uv_map", obj.data, "uv_layers", text="UV Map")',
            f"{_I2}else:",
            f'{_I2}{_I1}layout.prop(self, "uv_map")',
        ]
    return lines


def _gen_create_nodetree(info: dict, tree_type: str, compiled_nodes: dict) -> list[str]:
    lines = [
        f"{_I1}def createNodetree(self, name):",
        f"{_I2}# Use bl_label as a stable, class-level key so all instances share",
        f"{_I2}# one node tree and nested references resolve correctly.",
        f"{_I2}nt = self.node_tree = bpy.data.node_groups.new(",
        f"{_I2}{_I1}self._PREFIX + self.bl_label, {_repr(tree_type)}",
        f"{_I2})",
        f"{_I2}nt.color_tag = {_repr(info['color_tag'])}",
    ]
    if info["description"]:
        lines.append(f"{_I2}nt.description = {_repr(info['description'])}")
    lines.append("")

    lines += _gen_interface(info["interface"])
    lines.append("")
    lines += _gen_nodes(info["nodes"], compiled_nodes)
    lines += _gen_zone_pairs(info)
    lines.append("")
    lines += _gen_links(info["links"])

    if info["has_image_nodes"] or info["has_uv_nodes"]:
        lines.append(f"{_I2}self.valuesUpdate(None)")

    return lines


def _gen_interface(sockets: list[dict]) -> list[str]:
    lines: list[str] = []
    for s in sockets:
        var = _sock_var(s["name"], s["in_out"])
        lines.append(
            f"{_I2}{var} = nt.interface.new_socket("
            f"name={_repr(s['name'])}, "
            f"in_out={_repr(s['in_out'])}, "
            f"socket_type={_repr(s['socket_type'])})"
        )
        if s["default_value"] is not None:
            try:
                lines.append(f"{_I2}{var}.default_value = {_repr_val(s['default_value'])}")
            except Exception:
                pass
        if s["min_value"] is not None:
            lines.append(f"{_I2}{var}.min_value = {_repr_val(s['min_value'])}")
        if s["max_value"] is not None:
            lines.append(f"{_I2}{var}.max_value = {_repr_val(s['max_value'])}")
        if s["subtype"] and s["subtype"] != "NONE":
            lines.append(f"{_I2}{var}.subtype = {_repr(s['subtype'])}")
        if s["hide_value"]:
            lines.append(f"{_I2}{var}.hide_value = True")
        if s["hide_in_modifier"]:
            lines.append(f"{_I2}{var}.hide_in_modifier = True")
        if s.get("dimensions") is not None:
            lines.append(f"{_I2}{var}.dimensions = {s['dimensions']}")
    return lines


def _gen_nodes(nodes: list[dict], compiled_nodes: dict = {}) -> list[str]:
    lines: list[str] = []
    for node in nodes:
        v = node["var_name"]
        lines.append(f"{_I2}{v} = nt.nodes.new({_repr(node['bl_idname'])})")
        lines.append(f"{_I2}{v}.location = {node['location']}")
        if node["width"] and node["width"] != 140.0:
            lines.append(f"{_I2}{v}.width = {node['width']}")
        if node["label"]:
            lines.append(f"{_I2}{v}.label = {_repr(node['label'])}")
        if node["hide"]:
            lines.append(f"{_I2}{v}.hide = True")
        if node["type"] == "GROUP" and node["node_tree_name"]:
            orig = node["node_tree_name"]
            entry = compiled_nodes.get(orig)
            if entry:
                cname, key = entry
                # Compiled node: ensure its class-level node tree exists first,
                # then assign it.  getattr on bpy.types is safe even if the
                # class was registered after this file was imported.
                lines.append(
                    f"{_I2}_cls_{v} = getattr(bpy.types, {_repr(cname)}, None)"
                )
                lines.append(f"{_I2}if _cls_{v}:")
                lines.append(f"{_I2}{_I1}{v}.node_tree = _cls_{v}.create_node_group()")
                lines.append(f"{_I2}else:")
                lines.append(f"{_I2}{_I1}{v}.node_tree = bpy.data.node_groups.get({_repr(key)})")
            else:
                # External / non-compiled group — look up by original blend name
                lines.append(
                    f"{_I2}{v}.node_tree = bpy.data.node_groups.get({_repr(orig)})"
                )
        for attr, val in node["attributes"].items():
            lines.append(f"{_I2}{v}.{attr} = {_repr(val)}")
        for idx, val in node["input_defaults"].items():
            lines.append(f"{_I2}{v}.inputs[{idx}].default_value = {_repr_val(val)}")
        lines.append("")
    return lines


def _gen_zone_pairs(info: dict) -> list[str]:
    lines: list[str] = []
    node_map = {n["var_name"]: n for n in info["nodes"]}
    for in_var, out_var in info["zone_pairs"]:
        lines.append(f"{_I2}{in_var}.pair_with_output({out_var})")
        out_node = node_map.get(out_var, {})
        for item in out_node.get("repeat_items", []):
            lines.append(
                f"{_I2}{out_var}.repeat_items.new("
                f"{_repr(item['socket_type'])}, {_repr(item['name'])})"
            )
    return lines


def _gen_links(links: list[dict]) -> list[str]:
    lines: list[str] = []
    for lnk in links:
        fv  = lnk["from_var"]
        tv  = lnk["to_var"]
        fsn = lnk["from_socket_name"]
        tsn = lnk["to_socket_name"]
        fsi = lnk["from_socket_index"]
        tsi = lnk["to_socket_index"]
        from_ref = f"{fv}.outputs[{_repr(fsn)}]" if fsn else f"{fv}.outputs[{fsi}]"
        to_ref   = f"{tv}.inputs[{_repr(tsn)}]"  if tsn else f"{tv}.inputs[{tsi}]"
        lines.append(f"{_I2}nt.links.new({from_ref}, {to_ref})")
    return lines


def _gen_values_update(info: dict) -> list[str]:
    lines = [
        f"{_I1}def valuesUpdate(self, context):",
        f"{_I2}if context is not None and self.node_tree.users > 1:",
        f"{_I2}{_I1}self.node_tree = self.node_tree.copy()",
        f"{_I2}for node in self.node_tree.nodes:",
    ]
    if info["has_image_nodes"]:
        lines += [
            f'{_I2}{_I1}if node.type == "TEX_IMAGE":',
            f"{_I2}{_I1}{_I1}node.image = self.image_texture",
        ]
    if info["has_uv_nodes"]:
        lines += [
            f'{_I2}{_I1}if hasattr(node, "uv_map") and self.uv_map:',
            f"{_I2}{_I1}{_I1}node.uv_map = self.uv_map",
        ]
    return lines


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _repr(v) -> str:
    return repr(v)


def _repr_val(v) -> str:
    if isinstance(v, tuple):
        return repr(tuple(float(x) for x in v))
    return repr(v)


def _sock_var(name: str, in_out: str) -> str:
    prefix = "out" if in_out == "OUTPUT" else "inp"
    clean  = "".join(c if c.isalnum() else "_" for c in name).strip("_")
    return f"_sock_{prefix}_{clean}" if clean else f"_sock_{prefix}"