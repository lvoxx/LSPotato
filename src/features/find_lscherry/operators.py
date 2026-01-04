import textwrap
import bpy  # type: ignore
import os
import shutil

from .clean_linked_data import clean_lscherry
from .lscherry_path import get_lscherry_path, get_blend_file
from .repair_lscherry import get_broken_libraries, repair_lscherry_collection
from ..find_lscherry.download_and_extract import download_and_extract
from ...utils.draw_ui import show_custom_popup
from ...constants.lscherry_version import version_urls
from ...constants.app_const import (
    LSCHERRY_COLLECTION_COLOR,
    LSCHERRY_FILE_WITH_EXTENSION,
    CHERRY_OBJECT,
)
from ...exception.base_handler import OperatorExceptionMixin
from ...exception.handler.lscherry_handler import LSCherryHandler
from ...exception.model.lspotato_exceptions import (
    LinkingException,
    ReleaseNotFoundException,
)
from ...utils.logger import get_logger

logger = get_logger("FindLSCherry")

MAX_TEXT_PER_LINE = 40
WIDTH_OF_CONFIRMATION_DIALOG = 300


class DownloadAndLinkLSCherry(bpy.types.Operator, OperatorExceptionMixin):
    bl_idname = "lscherry.download_and_link_cherry"
    bl_label = "Get"
    bl_description = "Download and link Cherry object"

    # Use LSCherryHandler for exception handling
    handler_class = LSCherryHandler

    @classmethod
    def poll(cls, context):
        version = context.scene.lscherry.selected_version
        new_collection = f"LSCherry-{version}"
        return not any(
            coll.name == new_collection and CHERRY_OBJECT in coll.objects
            for coll in bpy.data.collections
        )

    def execute(self, context):
        return self.safe_execute(self._execute_impl, context)

    def _execute_impl(self, context):
        """Implementation with exception handling"""
        props = context.scene.lscherry
        new_version = props.selected_version

        if not new_version:
            raise ReleaseNotFoundException(version="", repo="LSCherry")

        new_collection_name = f"LSCherry-{new_version}"

        # Check if there's an existing LSCherry collection with Cherry object
        existing_lscherry_collection = None
        for coll in bpy.data.collections:
            if coll.name.startswith("LSCherry-") and CHERRY_OBJECT in coll.objects:
                existing_lscherry_collection = coll
                break

        if existing_lscherry_collection:
            # Case 2: Already have LSCherry collection, just need to relocate
            message = self._relocate_existing_collection(
                existing_lscherry_collection, new_collection_name, new_version
            )
            logger.info(f"✓ {message}")
            self.report({"INFO"}, message)
        else:
            # Case 1: Don't have LSCherry collection yet, download and link new
            message = self._download_and_link_new_version(
                context, new_version, new_collection_name
            )
            logger.info(f"✓ {message}")
            self.report({"INFO"}, message)

        return {"FINISHED"}

    def _relocate_existing_collection(
        self, existing_collection, new_collection_name, new_version
    ):
        """Relocate existing collection to new version"""
        old_collection_name = existing_collection.name
        existing_collection.name = new_collection_name

        cherry_obj = existing_collection.objects.get(CHERRY_OBJECT)
        if not cherry_obj or not cherry_obj.library:
            raise LinkingException(
                library_path="", reason="Cherry object not found or not linked"
            )

        new_blend_path = get_blend_file(new_version)

        # Download if not available
        download_info = ""
        if not os.path.exists(new_blend_path):
            result = download_and_extract(new_version)
            if not result["extract_path"] or not os.path.exists(
                get_blend_file(new_version)
            ):
                raise ReleaseNotFoundException(version=new_version, repo="LSCherry")
            if result["was_downloaded"]:
                download_info = f" (downloaded {new_version})"

        try:
            cherry_obj.library.filepath = new_blend_path
            cherry_obj.library.reload()
            return f"Changed collection '{old_collection_name}' to '{new_collection_name}'{download_info}"
        except Exception as e:
            raise LinkingException(
                library_path=new_blend_path,
                reason=f"Failed to relocate library: {str(e)}",
            )

    def _download_and_link_new_version(self, context, new_version, new_collection_name):
        """Download and link new version"""
        messages = []

        # Clean old collection
        clean_result = clean_lscherry(new_version)
        if (
            clean_result["libraries"]["removed_count"] > 0
            or clean_result["collections"]["removed_count"] > 0
        ):
            messages.append(clean_result["message"])

        # Download and extract new version
        download_result = download_and_extract(new_version)

        if not download_result["extract_path"] or not os.path.exists(
            download_result["extract_path"]
        ):
            raise ReleaseNotFoundException(version=new_version, repo="LSCherry")

        if download_result["was_downloaded"]:
            messages.append(download_result["message"])

        blend_file = os.path.join(
            download_result["extract_path"], LSCHERRY_FILE_WITH_EXTENSION
        )
        if not os.path.exists(blend_file):
            raise LinkingException(
                library_path=blend_file, reason=f"Blend file not found at: {blend_file}"
            )

        object_dir = blend_file + "/Object/"

        try:
            # Create collection
            if new_collection_name not in bpy.data.collections:
                lscherry_collection = bpy.data.collections.new(new_collection_name)
                context.scene.collection.children.link(lscherry_collection)

            # Link the object
            bpy.ops.wm.link(
                directory=object_dir,
                filename=CHERRY_OBJECT,
                link=True,
            )

            # Move linked object to collection
            linked_obj = bpy.data.objects.get(CHERRY_OBJECT)
            if linked_obj:
                for coll in linked_obj.users_collection:
                    coll.objects.unlink(linked_obj)

                target_collection = bpy.data.collections[new_collection_name]
                target_collection.objects.link(linked_obj)
                target_collection.color_tag = LSCHERRY_COLLECTION_COLOR

                # Exclude from view layer
                for layer_coll in context.view_layer.layer_collection.children:
                    if layer_coll.collection == target_collection:
                        layer_coll.exclude = True
                        break

            messages.append(
                f"Successfully linked LSCherry {new_version} to collection '{new_collection_name}'"
            )
            return " | ".join(messages)

        except Exception as e:
            raise LinkingException(
                library_path=blend_file, reason=f"Link operation failed: {str(e)}"
            )


class RepairLSCherry(bpy.types.Operator, OperatorExceptionMixin):
    bl_idname = "lscherry.repair"
    bl_label = "Repair"
    bl_description = "Repair broken LSCherry versions by re-downloading them"

    # Use LSCherryHandler for exception handling
    handler_class = LSCherryHandler

    confirmation_message: bpy.props.StringProperty(
        name="Repair Confirmation Message",
        default="Do you want to repair broken LSCherry versions?",
    )  # type: ignore

    @classmethod
    def poll(cls, context):
        has_lscherry_collection = any(
            coll.name.startswith("LSCherry-") for coll in bpy.data.collections
        )
        has_broken_libs = len(get_broken_libraries()) > 0
        return has_lscherry_collection and has_broken_libs

    def invoke(self, context, event):
        return self.safe_invoke(self._invoke_impl, context, event)

    def _invoke_impl(self, context, event):
        return context.window_manager.invoke_props_dialog(
            self, width=WIDTH_OF_CONFIRMATION_DIALOG
        )

    def draw(self, context):
        layout = self.layout
        wrapped = textwrap.wrap(self.confirmation_message, width=MAX_TEXT_PER_LINE)
        for line in wrapped:
            layout.label(text=line)

    def execute(self, context):
        return self.safe_execute(self._execute_impl, context)

    def _execute_impl(self, context):
        """Implementation with exception handling"""
        result = repair_lscherry_collection()

        if result["repaired_count"] > 0:
            message = f"Repaired {result['repaired_count']} library(ies) for version {result['version']}"
            logger.info(f"✓ {message}")
            self.report({"INFO"}, message)

            show_custom_popup(
                f"Repair completed!\n{message}\n\nPlease save and restart Blender.",
                title="Repair Notification",
                icon="INFO",
            )
        else:
            message = "No libraries needed repair"
            logger.info(f"✓ {message}")
            self.report({"INFO"}, message)

        return {"FINISHED"}


class CleanDiskLSCherry(bpy.types.Operator, OperatorExceptionMixin):
    bl_idname = "lscherry.clean_disk"
    bl_label = "Clean Disk"
    bl_description = "Remove all previously downloaded LSCherry versions"

    # Use LSCherryHandler for exception handling
    handler_class = LSCherryHandler

    confirmation_message: bpy.props.StringProperty(
        name="Clean Disk Confirmation",
        default="Do you want to clean all previously downloaded LSCherry versions?",
    )  # type: ignore

    def invoke(self, context, event):
        return self.safe_invoke(self._invoke_impl, context, event)

    def _invoke_impl(self, context, event):
        return context.window_manager.invoke_props_dialog(
            self, width=WIDTH_OF_CONFIRMATION_DIALOG
        )

    def draw(self, context):
        layout = self.layout
        wrapped = textwrap.wrap(self.confirmation_message, width=MAX_TEXT_PER_LINE)
        for line in wrapped:
            layout.label(text=line)

    def execute(self, context):
        return self.safe_execute(self._execute_impl, context)

    def _execute_impl(self, context):
        """Implementation with exception handling"""
        lscherry_dir = get_lscherry_path()

        if os.path.exists(lscherry_dir):
            try:
                shutil.rmtree(lscherry_dir)
                message = f"Successfully cleaned disk: removed all downloaded LSCherry versions from {lscherry_dir}"
                logger.info(f"✓ {message}")
                self.report({"INFO"}, message)
            except PermissionError as e:
                from ...exception.model.lspotato_exceptions import FileSystemException

                raise FileSystemException(
                    operation="Remove",
                    path=lscherry_dir,
                    reason=f"Permission denied: {str(e)}",
                )
            except Exception as e:
                from ...exception.model.lspotato_exceptions import FileSystemException

                raise FileSystemException(
                    operation="Remove", path=lscherry_dir, reason=str(e)
                )
        else:
            message = "No LSCherry directory found on disk (nothing to clean)"
            logger.info(f"✓ {message}")
            self.report({"INFO"}, message)

        return {"FINISHED"}
