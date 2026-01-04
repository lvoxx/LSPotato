import bpy  # type: ignore

from .utils import check_for_updates, download_and_install_update
from ...exception.base_handler import OperatorExceptionMixin
from ...exception.handler.lspotato_updater_handler import UpdateCheckerHandler
from ...utils.logger import get_logger

logger = get_logger("UpdateChecker")


class LSPOTATO_OT_check_updates(bpy.types.Operator, OperatorExceptionMixin):
    bl_idname = "lspotato.check_updates"
    bl_label = "Check for Updates"
    bl_description = "Check GitHub for addon updates"
    
    # Override handler class for this operator
    handler_class = UpdateCheckerHandler

    def execute(self, context):
        return self.safe_execute(self._execute_impl, context)
    
    def _execute_impl(self, context):
        """Implementation with exception handling"""
        props = context.scene.lspotato.github_updater
        props.checking_update = True

        try:
            logger.info("Starting update check...")
            
            # This will raise exceptions if anything fails
            update_info = check_for_updates()
            
            current_version = update_info['current_version']
            branch_update = update_info['branch_update']
            major_update = update_info['major_update']
            has_update = update_info['has_update']
            
            # Update properties
            props.update_available = has_update
            props.latest_version = update_info['latest_tag']
            props.last_check_time = bpy.context.scene.frame_current

            if not has_update:
                logger.info("No updates available")
                self.report({"INFO"}, "You have the latest version")
                return {"FINISHED"}
            
            # Format current version for display
            current_version_str = f"{current_version[0]}.{current_version[1]}.{current_version[2]}"
            
            # Determine which popup to show
            if branch_update and major_update:
                # Both options available - show decision popup
                logger.info(f"Multiple updates available: branch={branch_update}, major={major_update}")
                bpy.ops.lspotato.update_decision_popup(
                    'INVOKE_DEFAULT',
                    current_version=current_version_str,
                    current_branch_update=branch_update,
                    major_update=major_update,
                    has_branch_update=True,
                    has_major_update=True
                )
                
            elif branch_update:
                # Only branch update available - show simple notification
                logger.info(f"Branch update available: {branch_update}")
                
                # Determine if it's patch or minor
                from .utils import version_to_tuple
                branch_ver = version_to_tuple(branch_update)
                if branch_ver[0] == current_version[0] and branch_ver[1] == current_version[1]:
                    update_type = "patch"
                else:
                    update_type = "minor"
                
                bpy.ops.lspotato.simple_update_notification(
                    'INVOKE_DEFAULT',
                    current_version=current_version_str,
                    version_tag=branch_update,
                    update_type=update_type
                )
                
            elif major_update:
                # Only major update available - show with warning
                logger.info(f"Major update available: {major_update}")
                bpy.ops.lspotato.simple_update_notification(
                    'INVOKE_DEFAULT',
                    current_version=current_version_str,
                    version_tag=major_update,
                    update_type="major"
                )

        finally:
            props.checking_update = False
            
            # Refresh UI
            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()
                    break

        return {"FINISHED"}


class LSPOTATO_OT_install_specific_update(bpy.types.Operator, OperatorExceptionMixin):
    bl_idname = "lspotato.install_specific_update"
    bl_label = "Install Specific Update"
    bl_description = "Download and install a specific version"
    bl_options = {'INTERNAL'}
    
    # Override handler class for this operator
    handler_class = UpdateCheckerHandler
    
    version_tag: bpy.props.StringProperty(default="")

    def execute(self, context):
        return self.safe_execute(self._execute_impl, context)
    
    def _execute_impl(self, context):
        """Implementation with exception handling"""
        if not self.version_tag:
            self.report({"ERROR"}, "No version specified")
            return {"CANCELLED"}
        
        logger.info(f"Starting installation of version: {self.version_tag}")
        self.report({"INFO"}, f"Downloading version {self.version_tag}...")

        # This will raise exceptions if anything fails
        success, message = download_and_install_update(self.version_tag)

        if success:
            logger.info(f"Successfully installed {self.version_tag}")
            self.report({"INFO"}, message)
            
            # Reset update flags
            props = context.scene.lspotato.github_updater
            props.update_available = False
            props.update_dismissed = False
            
            # Show restart message
            logger.info("Update complete - restart required")
            self.report({"WARNING"}, "Please restart Blender to complete update")
        
        return {"FINISHED"}


class LSPOTATO_OT_install_update(bpy.types.Operator, OperatorExceptionMixin):
    """Legacy operator - installs latest from main branch"""
    bl_idname = "lspotato.install_update"
    bl_label = "Install Update"
    bl_description = "Download and install latest update from GitHub"
    
    # Override handler class for this operator
    handler_class = UpdateCheckerHandler

    def execute(self, context):
        return self.safe_execute(self._execute_impl, context)
    
    def _execute_impl(self, context):
        """Implementation with exception handling"""
        logger.info("Starting installation of latest version from main branch")
        self.report({"INFO"}, "Downloading latest update...")

        # This will raise exceptions if anything fails
        success, message = download_and_install_update(version_tag=None)

        if success:
            logger.info(message)
            self.report({"INFO"}, message)
            
            # Reset update flags
            props = context.scene.lspotato.github_updater
            props.update_available = False
            props.update_dismissed = False
            
            # Show restart message
            logger.info("Update complete - restart required")
            self.report({"WARNING"}, "Please restart Blender to complete update")
        
        return {"FINISHED"}


class LSPOTATO_OT_dismiss_update(bpy.types.Operator):
    bl_idname = "lspotato.dismiss_update"
    bl_label = "Dismiss Update"
    bl_description = "Temporarily dismiss update notification"

    def execute(self, context):
        props = context.scene.lspotato.github_updater
        props.update_dismissed = True
        logger.info("Update notification dismissed")
        return {"FINISHED"}