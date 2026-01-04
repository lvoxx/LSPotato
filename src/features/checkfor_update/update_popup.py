"""
Update Popup UI
Popup dialogs for update decision
"""

import bpy  # type: ignore
from ...utils.logger import get_logger

logger = get_logger("UpdateChecker")


class LSPOTATO_OT_update_decision_popup(bpy.types.Operator):
    """Popup to ask user about update preferences"""

    bl_idname = "lspotato.update_decision_popup"
    bl_label = "Update Available"
    bl_options = {"INTERNAL"}

    # Popup data
    current_version: bpy.props.StringProperty(default="")
    current_branch_update: bpy.props.StringProperty(default="")  # e.g., "1.0.19"
    major_update: bpy.props.StringProperty(default="")  # e.g., "2.0.0"
    has_branch_update: bpy.props.BoolProperty(default=False)
    has_major_update: bpy.props.BoolProperty(default=False)
    user_chosen_version: bpy.props.StringProperty(default="")  # Store user's choice

    def draw(self, context):
        layout = self.layout
        layout.label(text="Update Options Available", icon="INFO")

        # Current version info
        box = layout.box()
        box.label(text=f"Current Version: {self.current_version}", icon="BLENDER")

        layout.separator()

        # Branch update option (if available)
        if self.has_branch_update:
            box = layout.box()
            col = box.column(align=True)
            col.label(text="Small Update (Recommended)", icon="CHECKMARK")
            col.label(text=f"→ Version {self.current_branch_update}")
            col.separator(factor=0.5)
            col.label(text="• Bug fixes and improvements", icon="DOT")
            col.label(text="• Same feature set", icon="DOT")
            col.label(text="• Safest option", icon="DOT")

            box.separator()
            op = box.operator(
                "lspotato.install_specific_update",
                text=f"Update to {self.current_branch_update}",
                icon="IMPORT",
            )
            if op:
                op.version_tag = self.current_branch_update

        # Major update option (if available)
        if self.has_major_update:
            box = layout.box()
            col = box.column(align=True)
            col.label(text="Major Update", icon="ERROR")
            col.label(text=f"→ Version {self.major_update}")
            col.separator(factor=0.5)
            col.label(text="• New major features", icon="DOT")
            col.label(text="• May have breaking changes", icon="DOT")
            col.label(text="• Backup your work first!", icon="DOT")

            box.separator()
            row = box.row()
            row.alert = True
            op = row.operator(
                "lspotato.install_specific_update",
                text=f"Update to {self.major_update} (Advanced)",
                icon="IMPORT",
            )
            if op:
                op.version_tag = self.major_update

        layout.separator()

        # Cancel button
        layout.operator("lspotato.cancel_update_popup", text="Cancel", icon="CANCEL")

    def execute(self, context):
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=450)


class LSPOTATO_OT_confirm_major_update_popup(bpy.types.Operator):
    """Confirmation popup for major version update"""

    bl_idname = "lspotato.confirm_major_update"
    bl_label = "Confirm Major Update"
    bl_options = {"INTERNAL"}

    version_tag: bpy.props.StringProperty(default="")
    current_version: bpy.props.StringProperty(default="")

    def draw(self, context):
        layout = self.layout

        # Warning header
        box = layout.box()
        box.alert = True
        row = box.row()
        row.label(text="⚠️ MAJOR VERSION UPDATE", icon="ERROR")

        layout.separator()

        # Version info
        col = layout.column(align=True)
        col.label(text=f"Current: {self.current_version}")
        col.label(text=f"New: {self.version_tag}")

        layout.separator()

        # Warning messages
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Important Information:", icon="INFO")
        col.separator(factor=0.5)
        col.label(text="• This is a major version change")
        col.label(text="• May contain breaking changes")
        col.label(text="• Some features may work differently")
        col.label(text="• Backup your Blender files first")
        col.label(text="• You cannot easily downgrade")

        layout.separator()

        # Confirmation question
        box = layout.box()
        box.label(text="Are you sure you want to proceed?", icon="QUESTION")

    def execute(self, context):
        logger.info(f"User confirmed major update to {self.version_tag}")

        # Proceed with installation
        bpy.ops.lspotato.install_specific_update(version_tag=self.version_tag)

        return {"FINISHED"}

    def cancel(self, context):
        logger.info("User cancelled major update")
        self.report({"INFO"}, "Update cancelled")
        return None

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)


class LSPOTATO_OT_simple_update_notification(bpy.types.Operator):
    """Simple notification for single update option"""

    bl_idname = "lspotato.simple_update_notification"
    bl_label = "Update Available"
    bl_options = {"INTERNAL"}

    version_tag: bpy.props.StringProperty(default="")
    current_version: bpy.props.StringProperty(default="")
    update_type: bpy.props.StringProperty(default="patch")  # patch, minor, major

    def draw(self, context):
        layout = self.layout

        # Header based on update type
        if self.update_type == "major":
            layout.label(text="Major Update Available!", icon="ERROR")
        else:
            layout.label(text="Update Available", icon="INFO")

        layout.separator()

        # Version info
        box = layout.box()
        col = box.column(align=True)
        col.label(text=f"Current: {self.current_version}")
        col.label(text=f"New: {self.version_tag}")

        layout.separator()

        # Update description based on type
        box = layout.box()
        col = box.column(align=True)

        if self.update_type == "patch":
            col.label(text="Patch Update", icon="CHECKMARK")
            col.label(text="• Bug fixes and improvements")
            col.label(text="• Safe to update")
        elif self.update_type == "minor":
            col.label(text="Minor Update", icon="PLUS")
            col.label(text="• New features added")
            col.label(text="• Bug fixes included")
            col.label(text="• Recommended to update")
        elif self.update_type == "major":
            col.label(text="Major Update", icon="ERROR")
            col.label(text="• Significant changes")
            col.label(text="• May have breaking changes")
            col.label(text="• Backup your work first")

        layout.separator()

        # Install button
        if self.update_type == "major":
            row = layout.row()
            row.alert = True
            row.operator(
                "lspotato.confirm_major_update",
                text=f"Update to {self.version_tag}",
                icon="EXPORT",
            ).version_tag = self.version_tag
        else:
            layout.operator(
                "lspotato.install_specific_update",
                text=f"Update to {self.version_tag}",
                icon="IMPORT",
            ).version_tag = self.version_tag

        # Dismiss button
        layout.operator("lspotato.dismiss_update", text="Stay on Current Major and Update Minor/Patch", icon="CANCEL")

    def execute(self, context):
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)


class LSPOTATO_OT_cancel_update_popup(bpy.types.Operator):
    """Operator to cancel the update popup"""
    
    bl_idname = "lspotato.cancel_update_popup"
    bl_label = "Cancel Update"
    bl_description = "Cancel the update popup dialog"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        logger.info("User cancelled update popup")
        return {"CANCELLED"}
