import requests
import json
import zipfile
import os
import shutil
import tempfile
import re

from ...constants.app_const import GITHUB_API_URL, GITHUB_DOWNLOAD_URL


def get_current_version():
    """Get current addon version from bl_info"""
    from ... import bl_info

    return bl_info["version"]


def version_to_tuple(version_string, length=3):
    if not isinstance(version_string, str):
        return (0,) * length

    version_string = version_string.strip().lstrip("vV")

    try:
        nums = re.findall(r"\d+", version_string)
        nums = list(map(int, nums[:length]))
        return tuple(nums + [0] * (length - len(nums)))
    except (ValueError, TypeError):
        return (0,) * length

def normalize_version_tuple(version, length=3):
    if not isinstance(version, (tuple, list)):
        return (0,) * length
    version = list(version[:length])
    return tuple(version + [0] * (length - len(version)))


def check_for_updates():
    """Check GitHub for new version"""
    try:
        print("Checking GitHub API:", GITHUB_API_URL)
        response = requests.get(GITHUB_API_URL, timeout=10)
        print("Response status code:", response.status_code)
        if response.status_code != 200:
            return False, ""

        release_data = response.json()
        latest_tag = release_data.get("tag_name", "")

        current_version = normalize_version_tuple(get_current_version())
        latest_version = version_to_tuple(latest_tag)

        print("Current:", current_version, "Latest:", latest_version)

        if latest_version > current_version:
            return True, latest_tag

        return False, latest_tag

    except Exception as e:
        print(f"Failed to check for updates: {e}")
        return False, ""



def download_and_install_update():
    """Download and install update from GitHub"""
    try:
        # Create temp directory
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, "LSPotato-main.zip")

        # Download zip file
        response = requests.get(GITHUB_DOWNLOAD_URL, timeout=30)
        if response.status_code != 200:
            return False, "Failed to download update"

        # Save zip file
        with open(zip_path, "wb") as f:
            f.write(response.content)

        # Extract zip
        extract_dir = os.path.join(temp_dir, "extracted")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

        # Find the root directory (e.g., LSPotato-main)
        root_dir = None
        for item in os.listdir(extract_dir):
            item_path = os.path.join(extract_dir, item)
            if os.path.isdir(item_path) and "LSPotato" in item:
                root_dir = item_path
                break

        if not root_dir:
            return False, "Could not find addon root directory in downloaded files"

        # Find the src directory and move its contents to the root
        src_dir = os.path.join(root_dir, "src")
        if os.path.exists(src_dir):
            current_addon_path = os.path.dirname(
                os.path.dirname(os.path.dirname(__file__))
            )

            # Remove existing addon directory to avoid duplicates
            if os.path.exists(current_addon_path):
                shutil.rmtree(current_addon_path)

            # Create new addon directory
            os.makedirs(current_addon_path, exist_ok=True)

            # Move contents from src to current_addon_path
            for item in os.listdir(src_dir):
                source_item = os.path.join(src_dir, item)
                dest_item = os.path.join(current_addon_path, item)
                if os.path.isdir(source_item):
                    shutil.copytree(source_item, dest_item)
                else:
                    shutil.copy2(source_item, dest_item)

            # Move LICENSE and blender_manifest.toml from root_dir to current_addon_path
            for item in os.listdir(root_dir):
                if item in ["LICENSE", "blender_manifest.toml"]:
                    source_item = os.path.join(root_dir, item)
                    dest_item = os.path.join(current_addon_path, item)
                    if os.path.isfile(source_item):
                        shutil.copy2(source_item, dest_item)

        else:
            # If no src directory, copy the entire root_dir
            current_addon_path = os.path.dirname(
                os.path.dirname(os.path.dirname(__file__))
            )
            if os.path.exists(current_addon_path):
                shutil.rmtree(current_addon_path)
            shutil.copytree(root_dir, current_addon_path)

        # Cleanup temp files
        shutil.rmtree(temp_dir)

        return True, "Update installed successfully"

    except Exception as e:
        return False, f"Update failed: {str(e)}"
