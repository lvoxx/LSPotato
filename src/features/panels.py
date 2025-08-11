import bpy  # type: ignore


class BPotatoPanel(bpy.types.Panel):
    bl_label = "BPotato"
    bl_idname = "VIEW3D_PT_bpotato"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPotato"

    def draw(self, context):
        layout = self.layout
        bp_props = context.scene.bpotato
        ls_props = context.scene.lscherry

        # Find and download LSCherry
        box = layout.box()
        box.label(text="LSCherry Version Manager")

        # Populate versions from version_urls
        box.prop(ls_props, "selected_version", text="Version")
        box.operator("lscherry.download_and_link_cherry")
        # Add Clean Disk button with red color (alert=True)
        row = box.row()
        row.alert = True  # Makes the button red
        row.operator("lscherry.clean_disk", text="Clean Disk", icon="TRASH")
        row.alert = False  # Reset alert to avoid affecting other elements

        # Replace Node Groups
        box = layout.box()
        box.label(text="Replace Node Groups")
        box.prop(bp_props, "mode")
        box.prop(bp_props, "old_group_name", text="From")
        box.prop(bp_props, "new_group_name", text="To")
        box.operator("bpotato.replace_node_groups")

        # Make Local
        box = layout.box()
        box.label(text="Save to Local File")
        box.operator("bpotato.make_local")
