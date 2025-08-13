import bpy  # type: ignore
import os
import zipfile
import shutil
from urllib.request import urlretrieve

from .lscherry_path import get_lscherry_path, get_version_path
from ...constants.lscherry_version import version_urls
from ...constants.app_const import (
    LSCHERRY_FILE_WITH_EXTENSION,
    CHERRY_OBJECT,
)


def download_and_extract(self, version):
    lscherry_dir = get_lscherry_path()
    extract_path = get_version_path(version)

    # Check if version already exists
    if os.path.exists(extract_path):
        self.report({"INFO"}, f"✅ Version {version} already exists at {extract_path}")
        return extract_path

    os.makedirs(lscherry_dir, exist_ok=True)

    # Get URL from version_urls
    url = version_urls.get(version, "")
    if not url:
        return None

    self.report({"INFO"}, f"🔎 Found version {version} at {url}")

    zip_path = os.path.join(lscherry_dir, f"LSCherry-{version}.zip")

    # Download zip
    urlretrieve(url, zip_path)

    self.report({"INFO"}, f"⬇️ Downloaded to {zip_path}")

    # Extract and rename
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(lscherry_dir)
    for item in os.listdir(lscherry_dir):
        if item.startswith("LSCherry-") and not item.endswith(".zip"):
            shutil.move(os.path.join(lscherry_dir, item), extract_path)
            break

    # Clean up zip
    os.remove(zip_path)

    self.report({"INFO"}, f"📦 Extracted to {extract_path}")

    return extract_path


def clean_linked_libraries():
    """Remove all linked libraries and their associated collections"""
    # Remove linked libraries
    for lib in bpy.data.libraries:
        if lib.name.startswith("LSCherry"):
            bpy.data.libraries.remove(lib)

    # Remove LSCherry collections
    for coll in bpy.data.collections:
        if coll.name.startswith("LSCherry-"):
            bpy.data.collections.remove(coll)


class DownloadAndLinkLSCherry(bpy.types.Operator):
    bl_idname = "lscherry.download_and_link_cherry"
    bl_label = "Get"
    bl_description = "Download and link Cherry object"

    @classmethod
    def poll(cls, context):
        # Disable button if Cherry object exists in a collection
        version = context.scene.lscherry.selected_version
        collection_name = f"LSCherry-{version}"
        return not any(
            coll.name == collection_name and CHERRY_OBJECT in coll.objects
            for coll in bpy.data.collections
        )

    def execute(self, context):
        props = context.scene.lscherry
        version = props.selected_version
        if not version:
            self.report({"ERROR"}, "No version selected")
            return {"CANCELLED"}

        # Clean existing linked libraries and collections
        clean_linked_libraries()

        extract_path = download_and_extract(self, version)
        # If other version then getting new linked libraries
        if extract_path and os.path.exists(extract_path):
            blend_file = os.path.join(extract_path, LSCHERRY_FILE_WITH_EXTENSION)
            if os.path.exists(blend_file):
                object_dir = blend_file + "/Object/"
                print(f"Linking object '{CHERRY_OBJECT}' from directory: {object_dir}")

                try:
                    # Create version-specific collection
                    collection_name = f"LSCherry-{version}"
                    if collection_name not in bpy.data.collections:
                        new_collection = bpy.data.collections.new(collection_name)
                        context.scene.collection.children.link(new_collection)

                    # Link the object
                    result = bpy.ops.wm.link(
                        directory=object_dir,
                        filename=CHERRY_OBJECT,
                        link=True,
                    )
                    print(f"✅ Linked object with operation result: {result}")

                    # Move linked object to version-specific collection
                    linked_obj = bpy.data.objects.get(CHERRY_OBJECT)
                    if linked_obj:
                        for coll in linked_obj.users_collection:
                            coll.objects.unlink(linked_obj)

                        target_collection = bpy.data.collections[collection_name]
                        target_collection.objects.link(linked_obj)

                        # Set red color and exclude from view
                        target_collection.color_tag = "COLOR_01"

                        # Exclude from view layer
                        for layer_coll in context.view_layer.layer_collection.children:
                            if layer_coll.collection == target_collection:
                                layer_coll.exclude = True
                                break

                except Exception as e:
                    print(f"❌ Link operation failed with exception: {e}")
            else:
                print(f"❓ Blend file not found at: {blend_file}")

        return {"FINISHED"}


class CleanDiskLSCherry(bpy.types.Operator):
    bl_idname = "lscherry.clean_disk"
    bl_label = "Clean Disk"
    bl_description = "Remove all previously downloaded LSCherry versions"

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        addon_dir = os.path.dirname(__file__)
        lscherry_dir = os.path.join(addon_dir, "LSCherry")

        if os.path.exists(lscherry_dir):
            try:
                shutil.rmtree(lscherry_dir)
                self.report(
                    {"INFO"}, "🗑️ Successfully removed all downloaded LSCherry versions"
                )
            except Exception as e:
                self.report(
                    {"ERROR"}, f"❌ Failed to remove LSCherry directory: {str(e)}"
                )
                return {"CANCELLED"}
        else:
            self.report({"INFO"}, "❓ No LSCherry directory found to clean")

        return {"FINISHED"}
