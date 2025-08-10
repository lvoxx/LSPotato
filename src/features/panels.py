import bpy  # type: ignore


class BPotatoPanel(bpy.types.Panel):
    bl_label = "BPotato"
    bl_idname = "VIEW3D_PT_bpotato"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPotato"

    def draw(self, context):
        layout = self.layout
        props = context.scene.bpotato

        box = layout.box()
        box.label(text="Replace Node Groups")
        box.prop(props, "mode")
        box.prop(props, "old_group_name", text="From")
        box.prop(props, "new_group_name", text="To")
        box.operator("bpotato.replace_node_groups")

        box = layout.box()
        box.label(text="Make Local")
        box.operator("bpotato.make_local")
