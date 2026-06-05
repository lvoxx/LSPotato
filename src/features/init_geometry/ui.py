"""
Init Geometry Nodes UI.
Call draw_geometry_panel(layout, context) from panels.py.
"""


def draw_geometry_panel(layout, context):
    """Draw the Geometry Nodes section inside the LSPotato sidebar panel."""
    box = layout.box()
    box.label(text="Geometry Nodes", icon="MODIFIER")
    box.operator("lspotato.init_geometry_nodes", icon="IMPORT")
