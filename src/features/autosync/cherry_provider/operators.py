import bpy  # type: ignore
from .sync import check_and_sync


class LSCHERRY_OT_toggle_autosync(bpy.types.Operator):
    bl_idname = "lscherry.toggle_autosync_provider"
    bl_label = "Toggle AutoSync"
    bl_description = "Toggle automatic synchronization"

    def execute(self, context):
        ls_props = context.scene.lscherry
        ls_props.autosync_provider_enabled = not ls_props.autosync_provider_enabled

        if ls_props.autosync_provider_enabled:
            self.report({"INFO"}, "AutoSync enabled")
            check_and_sync(context.scene)
        else:
            self.report({"INFO"}, "AutoSync disabled")

        return {"FINISHED"}
