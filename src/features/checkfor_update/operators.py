import bpy  # type: ignore
from .utils import check_for_updates, download_and_install_update


class LSPOTATO_OT_check_updates(bpy.types.Operator):
    bl_idname = "lspotato.check_updates"
    bl_label = "Check for Updates"
    bl_description = "Check GitHub for addon updates"

    def execute(self, context):
        props = context.scene.lspotato.github_updater
        props.checking_update = True

        try:
            has_update, latest_version = check_for_updates()
            props.update_available = has_update
            props.latest_version = latest_version
            props.last_check_time = bpy.context.scene.frame_current

            if has_update:
                self.report({"INFO"}, f"Update available: {latest_version}")
            else:
                self.report({"INFO"}, "You have the latest version")

        except Exception as e:
            self.report({"ERROR"}, f"Failed to check updates: {str(e)}")

        props.checking_update = False
        # Làm mới giao diện
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()
                break

        return {"FINISHED"}


class LSPOTATO_OT_install_update(bpy.types.Operator):
    bl_idname = "lspotato.install_update"
    bl_label = "Install Update"
    bl_description = "Download and install update from GitHub"

    def execute(self, context):
        self.report({"INFO"}, "Downloading update...")

        success, message = download_and_install_update()

        if success:
            self.report({"INFO"}, message)
            # Reset update flags
            props = context.scene.lspotato.github_updater
            props.update_available = False
            props.update_dismissed = False
            # Show restart message
            self.report({"WARNING"}, "Please restart Blender to complete update")
        else:
            self.report({"ERROR"}, message)

        return {"FINISHED"}


class LSPOTATO_OT_dismiss_update(bpy.types.Operator):
    bl_idname = "lspotato.dismiss_update"
    bl_label = "Dismiss Update"
    bl_description = "Temporarily dismiss update notification"

    def execute(self, context):
        props = context.scene.lspotato.github_updater
        props.update_dismissed = True
        return {"FINISHED"}
