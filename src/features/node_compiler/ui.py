"""
NodeCompiler UI
Call draw_compiler_panel(layout, context) from panels.py.
The entire section is hidden unless Dev Mode is enabled.
"""

import bpy  # type: ignore


def draw_compiler_panel(layout, context):
    """
    Draw the NodeCompiler section inside the LSPotato sidebar panel.
    Only the toggle row is always visible; the rest appears when Dev Mode is on.
    """
    if not hasattr(context.scene, "lspotato_compiler"):
        return

    props = context.scene.lspotato_compiler
    box   = layout.box()

    # ── Dev Mode toggle ──────────────────────────────────────────────────────
    row = box.row(align=True)
    icon = "HIDE_OFF" if props.dev_mode else "HIDE_ON"
    row.prop(props, "dev_mode", text="Dev Mode", icon=icon, toggle=True)

    if not props.dev_mode:
        return

    # ── Compiler settings ────────────────────────────────────────────────────
    col = box.column(align=False)
    col.separator(factor=0.5)
    col.label(text="Node Group Compiler", icon="NODETREE")

    col.prop(props, "compiled_folder", text="Output")

    row2 = col.row(align=True)
    row2.prop(props, "include_nested", text="Nested Groups")
    row2.prop(props, "copy_blend",     text="Copy .blend")

    col.separator(factor=0.5)
    col.operator(
        "lspotato.compile_node_groups",
        text="Compile All Node Groups",
        icon="EXPORT",
    )
