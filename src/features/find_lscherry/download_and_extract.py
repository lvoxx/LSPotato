import os
import shutil
import zipfile
from urllib.request import urlretrieve
from ...constants.lscherry_version import version_urls
from .lscherry_path import get_lscherry_path, get_version_path


import os
import shutil
import zipfile
from urllib.request import urlretrieve
from ...constants.lscherry_version import version_urls
from .lscherry_path import get_lscherry_path, get_version_path


def download_and_extract(self, version):
    lscherry_dir = get_lscherry_path()
    extract_path = get_version_path(version)

    # Check if version already exists
    if os.path.exists(extract_path):
        self.report(
            {"INFO"},
            f"Version {version} found at {extract_path}, using the local version instead.",
        )
        return extract_path

    os.makedirs(extract_path, exist_ok=True)

    # Get URL from version_urls
    url = version_urls.get(version, "")
    if not url:
        self.report({"ERROR"}, f"No download URL found for version {version}")
        return None

    self.report({"INFO"}, f"Found version {version} at {url}")

    # Always expect .zip
    archive_path = os.path.join(lscherry_dir, f"LSCherry-{version}.zip")

    # Download file
    urlretrieve(url, archive_path)
    self.report({"INFO"}, f"Downloaded to {archive_path}")

    # Extract file
    try:
        with zipfile.ZipFile(archive_path, "r") as zip_ref:
            zip_ref.extractall(extract_path)
    except Exception as e:
        self.report({"ERROR"}, f"Failed to extract archive: {e}")
        return None

    # Clean up archive
    os.remove(archive_path)

    # Fix double-nesting: if extract_path contains a single folder, move its content up
    items = os.listdir(extract_path)
    if len(items) == 1:
        inner_dir = os.path.join(extract_path, items[0])
        if os.path.isdir(inner_dir):
            # Move everything inside inner_dir up one level
            for sub in os.listdir(inner_dir):
                shutil.move(os.path.join(inner_dir, sub), extract_path)
            shutil.rmtree(inner_dir)

    self.report({"INFO"}, f"Extracted to {extract_path}")

    return extract_path
