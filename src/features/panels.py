import bpy  # type: ignore
from .checkfor_update.ui import draw_update_notification
from .autosync.uni import draw_autosync_panel


class LSPotatoPanel(bpy.types.Panel):
    bl_label = "LSPotato"
    bl_idname = "VIEW3D_PT_lspotato"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "LSPotato"

    def draw(self, context):
        layout = self.layout
        bp_props = context.scene.lspotato
        ls_props = context.scene.lscherry

        # --------------------------------------------------
        # Update notification (at the top)
        draw_update_notification(layout, context)

        # --------------------------------------------------
        # Find and download LSCherry
        box = layout.box()
        box.label(text="LSCherry Version Manager")

        # Populate versions from version_urls
        box.prop(ls_props, "selected_version", text="Version")
        box.operator("lscherry.download_and_link_cherry")

        # Add Repair and Clean Disk buttons in a row
        row = box.row()
        # Repair button with yellow/orange color
        row.operator("lscherry.repair", text="Repair", icon="TOOL_SETTINGS")
        # Clean Disk button with red color (alert=True)
        clean_row = row.row()
        clean_row.alert = True  # Makes the button red
        clean_row.operator("lscherry.clean_disk", text="Clean Disk", icon="TRASH")

        # --------------------------------------------------
        draw_autosync_panel(layout, context)

        # --------------------------------------------------
        # Replace Node Groups
        box = layout.box()
        box.label(text="Replace Node Groups")
        box.prop(bp_props, "mode")
        box.prop(bp_props, "old_group_name", text="From")
        box.prop(bp_props, "new_group_name", text="To")
        box.operator("lspotato.replace_node_groups")

        # --------------------------------------------------
        # Make Local
        box = layout.box()
        box.label(text="Save to Local File")
        box.operator("lspotato.make_local")
