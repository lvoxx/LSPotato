import textwrap
import bpy  # type: ignore
import os
import shutil


from .lscherry_path import get_lscherry_path
from .clean_linked_data import reload_lscherry
from ..find_lscherry.download_and_extract import download_and_extract
from ..find_lscherry.repair_lscherry import repair_broken_version
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
        # Disable button if Cherry object exists in a collection
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

        # Clean old collection
        old_col = reload_lscherry(self, new_version)

        # Download and extract new version / Import new version
        extract_path = download_and_extract(self, new_version)

        new_collection = f"LSCherry-{new_version}"

        # If other version then getting new linked libraries
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
                    if new_collection not in bpy.data.collections:
                        lscherry_collection = bpy.data.collections.new(new_collection)
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

                        target_collection = bpy.data.collections[new_collection]
                        target_collection.objects.link(linked_obj)

                        # Set red color and exclude from view
                        target_collection.color_tag = "COLOR_01"

                        # Exclude from view layer
                        for layer_coll in context.view_layer.layer_collection.children:
                            if layer_coll.collection == target_collection:
                                layer_coll.exclude = True
                                break

                except Exception as e:
                    self.report({"ERROR"}, f"Link operation failed with exception: {e}")
            else:
                self.report({"WARNING"}, f"Blend file not found at: {blend_file}")

        if old_col:
            # If changes to another version
            self.report(
                {"INFO"},
                f"Successfully changed {old_col} to {new_collection}",
            )
        else:
            # If first time link version
            self.report(
                {"INFO"},
                f"Successfully downloaded and linked LSCherry version {new_version} at collection {new_collection}",
            )

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
        # Enable button if there are any linked LSCherry collections
        return any(
            coll.name.startswith("LSCherry-") and CHERRY_OBJECT in coll.objects
            for coll in bpy.data.collections
        )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=WIDTH_OF_CONFIRMATION_DIALOG)

    def draw(self, context):
        layout = self.layout
        wrapped = textwrap.wrap(self.confirmation_message, width=MAX_TEXT_PER_LINE)
        for line in wrapped:
            layout.label(text=line)

    def execute(self, context):
        repaired_versions = []
        failed_versions = []

        # Find all linked LSCherry collections
        linked_collections = [
            coll
            for coll in bpy.data.collections
            if coll.name.startswith("LSCherry-") and CHERRY_OBJECT in coll.objects
        ]

        if not linked_collections:
            self.report({"INFO"}, "No linked LSCherry collections found to repair")
            return {"FINISHED"}

        for coll in linked_collections:
            # Extract version from collection name
            version = coll.name.replace("LSCherry-", "")

            # Check if version exists in version_urls
            if version not in version_urls:
                self.report(
                    {"WARNING"}, f"Version {version} not found in available versions"
                )
                failed_versions.append(version)
                continue

            try:
                self.report({"INFO"}, f"Repairing LSCherry version {version}...")

                # Repair the broken version
                extract_path = repair_broken_version(self, version)

                if extract_path and os.path.exists(extract_path):
                    blend_file = os.path.join(
                        extract_path, LSCHERRY_FILE_WITH_EXTENSION
                    )
                    if os.path.exists(blend_file):
                        # Try to reload the library
                        for lib in bpy.data.libraries:
                            if version in lib.filepath:
                                try:
                                    # Update library path
                                    lib.filepath = blend_file
                                    lib.reload()
                                    self.report(
                                        {"INFO"},
                                        f"Reloaded library for version {version}",
                                    )
                                except Exception as e:
                                    self.report(
                                        {"WARNING"},
                                        f"Failed to reload library for {version}: {e}",
                                    )

                        repaired_versions.append(version)
                        self.report(
                            {"INFO"}, f"Successfully repaired LSCherry version {version}"
                        )
                    else:
                        self.report(
                            {"ERROR"},
                            f"Blend file not found after repairing version {version}",
                        )
                        failed_versions.append(version)
                else:
                    self.report({"ERROR"}, f"Failed to repair version {version}")
                    failed_versions.append(version)

            except Exception as e:
                self.report({"ERROR"}, f"Error repairing version {version}: {str(e)}")
                failed_versions.append(version)

        # Report results
        if repaired_versions:
            self.report(
                {"INFO"}, f"Successfully repaired versions: {', '.join(repaired_versions)}"
            )

        if failed_versions:
            self.report(
                {"WARNING"}, f"Failed to repair versions: {', '.join(failed_versions)}"
            )

        if not repaired_versions and not failed_versions:
            self.report({"INFO"}, "No versions needed repairing")

        return {"FINISHED"}


class CleanDiskLSCherry(bpy.types.Operator):
    bl_idname = "lscherry.clean_disk"
    bl_label = "Clean Disk"
    bl_description = "Remove all previously downloaded LSCherry versions"

    confirmation_message: bpy.props.StringProperty(
        name="Repair Confirmation Message",
        default="Do you want to clean all previously downloaded LSCherry versions?",
    )  # type: ignore

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=WIDTH_OF_CONFIRMATION_DIALOG)

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
