import textwrap
import bpy  # type: ignore
import os
import shutil


from .clean_linked_data import clean_lscherry
from .lscherry_path import get_lscherry_path, get_blend_file
from .repair_lscherry import (
    get_broken_libraries,
    repair_lscherry_collection,
)
from ..find_lscherry.download_and_extract import download_and_extract
from ...utils.draw_ui import show_custom_popup
from ...constants.lscherry_version import version_urls
from ...constants.app_const import (
    LSCHERRY_FILE_WITH_EXTENSION,
    CHERRY_OBJECT,
)

MAX_TEXT_PER_LINE = 40
WIDTH_OF_CONFIRMATION_DIALOG = 300


class DownloadAndLinkLSCherry(bpy.types.Operator):
    bl_idname = "lscherry.download_and_link_cherry"
    bl_label = "Get"
    bl_description = "Download and link Cherry object"

    @classmethod
    def poll(cls, context):
        # Disable button if Cherry object exists in the selected version collection
        version = context.scene.lscherry.selected_version
        new_collection = f"LSCherry-{version}"
        return not any(
            coll.name == new_collection and CHERRY_OBJECT in coll.objects
            for coll in bpy.data.collections
        )

    def execute(self, context):
        props = context.scene.lscherry
        new_version = props.selected_version
        if not new_version:
            self.report({"ERROR"}, "No version selected")
            return {"CANCELLED"}

        new_collection_name = f"LSCherry-{new_version}"

        # Check if there's an existing LSCherry collection with Cherry object (different version)
        existing_lscherry_collection = None
        for coll in bpy.data.collections:
            if coll.name.startswith("LSCherry-") and CHERRY_OBJECT in coll.objects:
                existing_lscherry_collection = coll
                break

        if existing_lscherry_collection:
            # Case 2: Already has LSCherry collection with Cherry object but different version
            # Just rename collection and relocate
            old_collection_name = existing_lscherry_collection.name
            existing_lscherry_collection.name = new_collection_name

            # Relocate the linked library path
            cherry_obj = existing_lscherry_collection.objects.get(CHERRY_OBJECT)
            if cherry_obj and cherry_obj.library:
                new_blend_path = get_blend_file(new_version)
                if os.path.exists(new_blend_path):
                    try:
                        # Update library path
                        cherry_obj.library.filepath = new_blend_path
                        # Reload library
                        cherry_obj.library.reload()

                        self.report(
                            {"INFO"},
                            f"Successfully changed {old_collection_name} to {new_collection_name} and relocated library",
                        )
                    except Exception as e:
                        self.report({"ERROR"}, f"Failed to relocate library: {e}")
                        return {"CANCELLED"}
                else:
                    # If blend file doesn't exist for new version, download it first
                    extract_path = download_and_extract(self, new_version)
                    if extract_path and os.path.exists(get_blend_file(new_version)):
                        try:
                            cherry_obj.library.filepath = get_blend_file(new_version)
                            cherry_obj.library.reload()

                            self.report(
                                {"INFO"},
                                f"Successfully downloaded, changed {old_collection_name} to {new_collection_name} and relocated library",
                            )
                        except Exception as e:
                            self.report(
                                {"ERROR"},
                                f"Failed to relocate library after download: {e}",
                            )
                            return {"CANCELLED"}
                    else:
                        self.report(
                            {"ERROR"}, f"Failed to download version {new_version}"
                        )
                        return {"CANCELLED"}
            else:
                self.report({"WARNING"}, "Cherry object not found or not linked")
                return {"CANCELLED"}

        else:
            # Case 1: No LSCherry collection with Cherry object exists
            # Download and link new version

            # Clean old collection (if any empty ones exist)
            old_col = clean_lscherry(self, new_version)

            # Download and extract new version
            extract_path = download_and_extract(self, new_version)

            # Import new version
            if extract_path and os.path.exists(extract_path):
                blend_file = os.path.join(extract_path, LSCHERRY_FILE_WITH_EXTENSION)
                if os.path.exists(blend_file):
                    object_dir = blend_file + "/Object/"
                    self.report(
                        {"INFO"},
                        f"Linking object '{CHERRY_OBJECT}' from directory: {object_dir}",
                    )

                    try:
                        # Create version-specific collection
                        if new_collection_name not in bpy.data.collections:
                            lscherry_collection = bpy.data.collections.new(
                                new_collection_name
                            )
                            context.scene.collection.children.link(lscherry_collection)

                        # Link the object
                        bpy.ops.wm.link(
                            directory=object_dir,
                            filename=CHERRY_OBJECT,
                            link=True,
                        )

                        # Move linked object to version-specific collection
                        linked_obj = bpy.data.objects.get(CHERRY_OBJECT)
                        if linked_obj:
                            for coll in linked_obj.users_collection:
                                coll.objects.unlink(linked_obj)

                            target_collection = bpy.data.collections[
                                new_collection_name
                            ]
                            target_collection.objects.link(linked_obj)

                            # Set red color and exclude from view
                            target_collection.color_tag = "COLOR_01"

                            # Exclude from view layer
                            for (
                                layer_coll
                            ) in context.view_layer.layer_collection.children:
                                if layer_coll.collection == target_collection:
                                    layer_coll.exclude = True
                                    break

                        self.report(
                            {"INFO"},
                            f"Successfully downloaded and linked LSCherry version {new_version} at collection {new_collection_name}",
                        )

                    except Exception as e:
                        self.report(
                            {"ERROR"}, f"Link operation failed with exception: {e}"
                        )
                        return {"CANCELLED"}
                else:
                    self.report({"WARNING"}, f"Blend file not found at: {blend_file}")
                    return {"CANCELLED"}
            else:
                self.report(
                    {"ERROR"}, f"Failed to download and extract version {new_version}"
                )
                return {"CANCELLED"}

        return {"FINISHED"}


class RepairLSCherry(bpy.types.Operator):
    bl_idname = "lscherry.repair"
    bl_label = "Repair"
    bl_description = "Repair broken LSCherry versions by re-downloading them"

    confirmation_message: bpy.props.StringProperty(
        name="Repair Confirmation Message",
        default="Do you want to repair broken LSCherry versions?",
    )  # type: ignore

    @classmethod
    def poll(cls, context):
        # Enable nếu có LSCherry collection và có broken libraries
        has_lscherry_collection = any(
            coll.name.startswith("LSCherry-") for coll in bpy.data.collections
        )

        has_broken_libs = len(get_broken_libraries()) > 0

        return has_lscherry_collection and has_broken_libs

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(
            self, width=WIDTH_OF_CONFIRMATION_DIALOG
        )

    def draw(self, context):
        layout = self.layout
        wrapped = textwrap.wrap(self.confirmation_message, width=MAX_TEXT_PER_LINE)
        for line in wrapped:
            layout.label(text=line)

    def execute(self, context):
        # Sử dụng chức năng repair đã được tối ưu
        result = repair_lscherry_collection(self)

        if result == {"FINISHED"}:
            # Hiển thị popup thông báo hoàn thành
            show_custom_popup(
                "Repair completed!\nPlease save and restart Blender.",
                title="Repair Notification",
                icon="INFO",
            )

        return result


class CleanDiskLSCherry(bpy.types.Operator):
    bl_idname = "lscherry.clean_disk"
    bl_label = "Clean Disk"
    bl_description = "Remove all previously downloaded LSCherry versions"

    confirmation_message: bpy.props.StringProperty(
        name="Repair Confirmation Message",
        default="Do you want to clean all previously downloaded LSCherry versions?",
    )  # type: ignore

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(
            self, width=WIDTH_OF_CONFIRMATION_DIALOG
        )

    def draw(self, context):
        layout = self.layout
        wrapped = textwrap.wrap(self.confirmation_message, width=MAX_TEXT_PER_LINE)
        for line in wrapped:
            layout.label(text=line)

    def execute(self, context):
        lscherry_dir = get_lscherry_path()

        if os.path.exists(lscherry_dir):
            try:
                shutil.rmtree(lscherry_dir)
                self.report(
                    {"INFO"}, "Successfully removed all downloaded LSCherry versions"
                )
            except Exception as e:
                self.report({"ERROR"}, f"Failed to remove LSCherry directory: {str(e)}")
                return {"CANCELLED"}
        else:
            self.report({"INFO"}, "No LSCherry directory found to clean")

        return {"FINISHED"}
