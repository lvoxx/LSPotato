import bpy  # type: ignore
import os
import zipfile
import shutil
from urllib.request import urlretrieve

from ...constants.lscherry_version import VERSION_URLS
from ...constants.app_const import (
    LSCHERRY_FILE_WITH_EXTENSION,
    CHERRY_OBJECT,
)


def download_and_extract(self, version):
    addon_dir = os.path.dirname(__file__)
    lscherry_dir = os.path.join(addon_dir, "LSCherry")

    os.makedirs(lscherry_dir, exist_ok=True)

    # Get URL from version_urls
    url = VERSION_URLS.get(version, "")
    if not url:
        return None

    self.report({"INFO"}, f"🔎 Found version {version} at {url}")

    zip_path = os.path.join(lscherry_dir, f"LSCherry-{version}.zip")
    extract_path = os.path.join(lscherry_dir, version)

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


class DownloadAndLinkLSCherry(bpy.types.Operator):
    bl_idname = "lscherry.download_and_link_cherry"
    bl_label = "Get"
    bl_description = "Download and link Cherry object"

    def execute(self, context):
        props = context.scene.lscherry
        version = props.selected_version
        if not version:
            self.report({"ERROR"}, "No version selected")
            return {"CANCELLED"}

        extract_path = download_and_extract(self, version)

        if extract_path and os.path.exists(extract_path):
            blend_file = os.path.join(extract_path, LSCHERRY_FILE_WITH_EXTENSION)
            if os.path.exists(blend_file):
                object_dir = blend_file + "/Object/"
                print(f"Linking object '{CHERRY_OBJECT}' from directory: {object_dir}")

                try:
                    result = bpy.ops.wm.link(
                        directory=object_dir,
                        filename=CHERRY_OBJECT,
                        link=True,
                    )
                    print(f"✅ Linked object with operation result: {result}")
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
                self.report({"INFO"}, "🗑️ Successfully removed all downloaded LSCherry versions")
            except Exception as e:
                self.report({"ERROR"}, f"❌ Failed to remove LSCherry directory: {str(e)}")
                return {"CANCELLED"}
        else:
            self.report({"INFO"}, "❓ No LSCherry directory found to clean")

        return {"FINISHED"}