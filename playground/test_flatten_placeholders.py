"""
Standalone verification for the inline-subtree flattener's placeholder handling.

flattener.py imports no `bpy`, so we can drive flatten_info()/needs_flatten() with
hand-built `info` dicts (the same shape analyzer.analyze_node_group produces) and
assert the reported bug is fixed:

  A references nested group B; B holds an empty TEX_IMAGE placeholder but A exposes
  no texture input. After flattening, B's placeholder must land directly in A's own
  tree so the compiled A class exposes the texture input (via code_gen).

Run:  python playground/test_flatten_placeholders.py
"""

import importlib.util
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_COMPILER = os.path.normpath(os.path.join(
    _HERE, "..", "src", "features", "node_compiler", "compiler"
))


def _load(mod_name):
    path = os.path.join(_COMPILER, mod_name + ".py")
    spec = importlib.util.spec_from_file_location(mod_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def mk_node(**over):
    node = {
        "var_name": "Node",
        "name": "Node",
        "type": "CUSTOM",
        "bl_idname": "ShaderNodeValue",
        "location": (0.0, 0.0),
        "width": 140.0,
        "label": "",
        "hide": False,
        "attributes": {},
        "input_defaults": {},
        "output_defaults": {},
        "input_socket_names": [],
        "output_socket_names": [],
        "node_tree_name": None,
        "repeat_items": [],
        "color_ramp": None,
        "curve_mapping": None,
        "enum_items": [],
        "index_switch_count": None,
        "active_index": None,
    }
    node.update(over)
    return node


def sock(name, in_out, socket_type="NodeSocketColor"):
    return {
        "item_kind": "socket",
        "name": name,
        "in_out": in_out,
        "socket_type": socket_type,
        "description": "",
        "default_value": None,
        "min_value": None,
        "max_value": None,
        "subtype": "NONE",
        "hide_value": False,
        "hide_in_modifier": False,
        "dimensions": None,
        "identifier": name,
        "parent_id": None,
    }


def link(fv, fsn, fsi, tv, tsn, tsi):
    return {
        "from_var": fv, "from_socket_name": fsn, "from_socket_index": fsi,
        "to_var": tv, "to_socket_name": tsn, "to_socket_index": tsi,
    }


def mk_info(name, nodes, links, interface):
    return {
        "name": name,
        "type": "SHADER",
        "bl_label": "lscherry." + name,
        "color_tag": "NONE",
        "description": "",
        "interface": interface,
        "nodes": nodes,
        "links": links,
        "zone_pairs": [],
        "has_image_nodes": [],
        "has_uv_nodes": [],
        "nested_groups": [],
        "placeholder_image_node_names": [],
        "placeholder_images": [],
        "_predefined_images": [],
    }


def main():
    flat = _load("flattener")
    cg = _load("code_gen")
    failures = []

    def check(label, cond):
        print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
        if not cond:
            failures.append(label)

    # ── Child B: holds a placeholder TEX_IMAGE, no Attribute node ─────────────
    b_nodes = [
        mk_node(var_name="Group_Input", name="Group Input", type="GROUP_INPUT",
                bl_idname="NodeGroupInput"),
        mk_node(var_name="Image_Texture", name="Image Texture", type="TEX_IMAGE",
                bl_idname="ShaderNodeTexImage", label="Base Color",
                output_socket_names=["Color", "Alpha"]),
        mk_node(var_name="Group_Output", name="Group Output", type="GROUP_OUTPUT",
                bl_idname="NodeGroupOutput", input_socket_names=["Color"]),
    ]
    b_links = [link("Image_Texture", "Color", 0, "Group_Output", "Color", 0)]
    info_b = mk_info("b", b_nodes, b_links, [sock("Color", "OUTPUT")])

    # ── Parent A: references B, exposes NO texture input of its own ───────────
    a_nodes = [
        mk_node(var_name="Group", name="Group", type="GROUP",
                bl_idname="ShaderNodeGroup", node_tree_name="lscherry.b",
                output_socket_names=["Color"]),
        mk_node(var_name="Group_Output", name="Group Output", type="GROUP_OUTPUT",
                bl_idname="NodeGroupOutput", input_socket_names=["Surface"]),
    ]
    a_links = [link("Group", "Color", 0, "Group_Output", "Surface", 0)]
    info_a = mk_info("a", a_nodes, a_links, [sock("Surface", "OUTPUT")])

    infos = {"lscherry.b": info_b, "lscherry.a": info_a}

    # ── Detection: A must be flagged for flattening because B has a placeholder
    print("Detection — nested placeholder forces flatten")
    memo = {}
    check("group_needs_inline(B) is True",
          flat.group_needs_inline("lscherry.b", infos, memo) is True)
    check("needs_flatten(A) is True",
          flat.needs_flatten(info_a, infos, {}) is True)

    # ── Flatten: B's placeholder lands directly in A's tree ──────────────────
    print("Flatten — placeholder lifted into parent A")
    flat_a = flat.flatten_info(info_a, infos, {})
    ph_names = [p["node_name"] for p in flat_a["placeholder_images"]]
    check("placeholder_images carries the inlined TEX_IMAGE",
          "Image Texture" in ph_names)
    check("placeholder label preserved",
          any(p["label"] == "Base Color" for p in flat_a["placeholder_images"]))
    check("has_image_nodes populated",
          any(v.endswith("Image_Texture") for v in flat_a["has_image_nodes"]))
    check("nested group B no longer referenced",
          "lscherry.b" not in flat_a["nested_groups"])

    # ── Codegen: A now exposes a texture input ───────────────────────────────
    print("Codegen — A exposes the texture input")
    code = cg.generate_class(flat_a, "ShaderNodeCompiled_A", "...node", {})
    check("image PointerProperty emitted",
          "image_texture: bpy.props.PointerProperty" in code)
    check("draw_buttons exposes the texture slot",
          'template_ID(self,' in code)
    check("valuesUpdate assigns the placeholder image",
          "node.image = getattr(self, _placeholder_images[node.name])" in code)

    # ── Negative: an attribute-free, placeholder-free child stays referenced ─
    print("Negative — plain nested group is NOT flattened")
    plain_b = mk_info("plain", [
        mk_node(var_name="Group_Input", type="GROUP_INPUT", bl_idname="NodeGroupInput"),
        mk_node(var_name="Group_Output", type="GROUP_OUTPUT", bl_idname="NodeGroupOutput",
                input_socket_names=["Color"]),
    ], [], [sock("Color", "OUTPUT")])
    plain_infos = {"lscherry.plain": plain_b, "lscherry.a": info_a}
    a2 = mk_info("a", [
        mk_node(var_name="Group", type="GROUP", bl_idname="ShaderNodeGroup",
                node_tree_name="lscherry.plain", output_socket_names=["Color"]),
        mk_node(var_name="Group_Output", type="GROUP_OUTPUT", bl_idname="NodeGroupOutput",
                input_socket_names=["Surface"]),
    ], [link("Group", "Color", 0, "Group_Output", "Surface", 0)], [sock("Surface", "OUTPUT")])
    check("needs_flatten(A->plain) is False",
          flat.needs_flatten(a2, plain_infos, {}) is False)

    print()
    if failures:
        print(f"FAILED ({len(failures)}): " + "; ".join(failures))
        sys.exit(1)
    print("All flattener placeholder checks passed.")


if __name__ == "__main__":
    main()
