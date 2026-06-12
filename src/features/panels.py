import bpy  # type: ignore
from .lsregistry.ui import draw_lsregistry_panel
from .autosync.uni import draw_autosync_panel
from .node_compiler.ui import draw_compiler_panel


class LSPotatoPanel(bpy.types.Panel):
    bl_label = "LSPotato"
    bl_idname = "VIEW3D_PT_lspotato"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "LSPotato"

    def draw(self, context):
        layout = self.layout

        draw_autosync_panel(layout, context)
        draw_lsregistry_panel(layout, context)
        draw_compiler_panel(layout, context)
