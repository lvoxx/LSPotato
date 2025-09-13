import bpy  # type: ignore


class LSCHERRY_OT_set_autosync_tab(bpy.types.Operator):
    bl_idname = "lscherry.set_autosync_tab"
    bl_label = "Set AutoSync Tab"
    bl_description = "Switch between AutoSync tabs"

    tab: bpy.props.StringProperty()  # type: ignore

    def execute(self, context):
        ls_props = context.scene.lscherry
        ls_props.autosync_active_tab = self.tab
        return {"FINISHED"}
