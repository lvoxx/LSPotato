"""
NodeCompiler UI
Call draw_compiler_panel(layout, context) from panels.py.
The entire section is hidden unless Dev Mode is enabled in addon preferences.
"""

import bpy  # type: ignore
from ..addon_preferences import get_addon_prefs


def draw_compiler_panel(layout, context):
    prefs = get_addon_prefs(context)
    if prefs is None or not prefs.dev_mode:
        return

    if not hasattr(context.scene, "lspotato_compiler"):
        return

    props = context.scene.lspotato_compiler
    box = layout.box()

    col = box.column(align=False)
    col.label(text="Node Group Compiler", icon="NODETREE")

    col.prop(props, "compiled_folder", text="Output")

    row = col.row(align=True)
    row.prop(props, "include_nested", text="Nested Groups")
    row.prop(props, "copy_blend", text="Copy .blend")

    col.prop(props, "compile_geometry", text="Compile Geometry Nodes")

    col.separator(factor=0.5)
    col.operator(
        "lspotato.compile_node_groups",
        text="Compile All Node Groups",
        icon="EXPORT",
    )
