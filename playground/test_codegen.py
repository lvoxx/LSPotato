"""
Standalone verification for the NodeCompiler code generator.

code_gen.py imports no `bpy`, so we can exercise generate_class() with hand-built
`info` dicts (the same shape analyzer.analyze_node_group produces) and assert the
generated source fixes the four reported compilation bugs:

  1. Duplicate-named sockets link by INDEX, not a collapsing name.
  2. ColorRamp stops are rebuilt.
  3. Constant-node OUTPUT defaults are emitted.
  4. Menu Switch enum items are rebuilt, with active_index applied AFTER them.

Run:  venv/Scripts/python.exe playground/test_codegen.py
"""

import importlib.util
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_CODE_GEN = os.path.normpath(os.path.join(
    _HERE, "..", "src", "features", "node_compiler", "compiler", "code_gen.py"
))


def _load_code_gen():
    # Load the module straight from its file so the bpy-importing package
    # __init__ chain is never touched.
    spec = importlib.util.spec_from_file_location("code_gen", _CODE_GEN)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def mk_node(**over):
    """A node dict with every key generate_class reads, overridable per test."""
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


def mk_info(nodes, links, interface=None):
    return {
        "name": "Test",
        "type": "SHADER",
        "bl_label": "lscherry.test.Test",
        "color_tag": "NONE",
        "description": "",
        "interface": interface or [],
        "nodes": nodes,
        "links": links,
        "zone_pairs": [],
        "has_image_nodes": [],
        "has_uv_nodes": [],
    }


def link(fv, fsn, fsi, tv, tsn, tsi):
    return {
        "from_var": fv, "from_socket_name": fsn, "from_socket_index": fsi,
        "to_var": tv, "to_socket_name": tsn, "to_socket_index": tsi,
    }


def main():
    cg = _load_code_gen()
    failures = []

    def check(label, cond):
        print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
        if not cond:
            failures.append(label)

    # ── Bug 1: duplicate-named sockets ───────────────────────────────────────
    print("Bug 1 — duplicate socket names link by index")
    nodes = [
        mk_node(var_name="Group_Input", type="GROUP_INPUT",
                bl_idname="NodeGroupInput",
                output_socket_names=["A", "B"]),
        mk_node(var_name="Vector_Math", type="CUSTOM",
                bl_idname="ShaderNodeVectorMath",
                attributes={"operation": "ADD"},
                input_socket_names=["Vector", "Vector", "Scale"],
                output_socket_names=["Vector", "Value"]),
        mk_node(var_name="Group_Output", type="GROUP_OUTPUT",
                bl_idname="NodeGroupOutput",
                input_socket_names=["Result"]),
    ]
    links = [
        link("Group_Input", "A", 0, "Vector_Math", "Vector", 0),
        link("Group_Input", "B", 1, "Vector_Math", "Vector", 1),
        link("Vector_Math", "Vector", 0, "Group_Output", "Result", 0),
    ]
    code = cg.generate_class(mk_info(nodes, links), "ShaderNodeCompiled_Test")
    check("second 'Vector' operand uses inputs[1]", "Vector_Math.inputs[1]" in code)
    check("no collapsing inputs['Vector']", "Vector_Math.inputs['Vector']" not in code)
    check("unique output name kept readable", "Vector_Math.outputs['Vector']" in code)
    check("unique group input name kept readable", "Group_Input.outputs['B']" in code)

    # ── Bug 2: ColorRamp stops ───────────────────────────────────────────────
    print("Bug 2 — ColorRamp stops rebuilt")
    cr = {
        "color_mode": "RGB", "interpolation": "EASE", "hue_interpolation": "NEAR",
        "elements": [
            {"position": 0.0, "color": (0.0, 0.0, 0.0, 1.0)},
            {"position": 0.5, "color": (1.0, 0.0, 0.0, 1.0)},
            {"position": 1.0, "color": (1.0, 1.0, 1.0, 1.0)},
        ],
    }
    nodes = [mk_node(var_name="Color_Ramp", bl_idname="ShaderNodeValToRGB", color_ramp=cr)]
    code = cg.generate_class(mk_info(nodes, []), "ShaderNodeCompiled_Test")
    check("first stop set in place", "_cr.elements[0].color = (0.0, 0.0, 0.0, 1.0)" in code)
    check("middle stop created", "_cr.elements.new(0.5)" in code)
    check("last stop created", "_cr.elements.new(1.0)" in code)
    check("interpolation captured", "_cr.interpolation = 'EASE'" in code)

    # ── Bug 3: constant-node output defaults ─────────────────────────────────
    print("Bug 3 — constant node output default emitted")
    nodes = [mk_node(var_name="RGB", bl_idname="ShaderNodeRGB",
                     output_socket_names=["Color"],
                     output_defaults={0: (0.1, 0.2, 0.3, 1.0)})]
    code = cg.generate_class(mk_info(nodes, []), "ShaderNodeCompiled_Test")
    check("output default emitted", "RGB.outputs[0].default_value = (0.1, 0.2, 0.3, 1.0)" in code)

    # ── Bug 4: Menu Switch enum items + active_index ordering ────────────────
    print("Bug 4 — Menu Switch items rebuilt, active_index after items")
    nodes = [mk_node(var_name="Menu_Switch", bl_idname="GeometryNodeMenuSwitch",
                     attributes={"data_type": "RGBA"},
                     enum_items=[{"name": "Type 1", "description": ""},
                                 {"name": "Type 2", "description": ""}],
                     active_index=1)]
    code = cg.generate_class(mk_info(nodes, []), "ShaderNodeCompiled_Test")
    check("enum item created", "_enum.enum_items.new('Type 1')" in code)
    check("active_index emitted", "Menu_Switch.active_index = 1" in code)
    i_dtype = code.find("data_type")
    i_items = code.find("enum_items.new")
    i_active = code.find("active_index")
    check("order: data_type < items < active_index",
          -1 < i_dtype < i_items < i_active)

    print()
    if failures:
        print(f"FAILED ({len(failures)}): " + "; ".join(failures))
        sys.exit(1)
    print("All code-gen checks passed.")


if __name__ == "__main__":
    main()
