import os
import shutil
import zipfile
from urllib.request import urlretrieve
from ...constants.lscherry_version import version_urls
from .lscherry_path import get_lscherry_path, get_version_path


def download_and_extract(self, new_version):
    lscherry_dir = get_lscherry_path()
    extract_path = get_version_path(new_version)

    # Check if version already exists
    if os.path.exists(extract_path):
        self.report(
            {"INFO"},
            f"Version {new_version} found at {extract_path}, use the local version instead.",
        )
        return extract_path

    os.makedirs(lscherry_dir, exist_ok=True)

    # Get URL from version_urls
    url = version_urls.get(new_version, "")
    if not url:
        return None

    self.report({"INFO"}, f"Found version {new_version} at {url}")

    zip_path = os.path.join(lscherry_dir, f"LSCherry-{new_version}.zip")

    # Download zip
    urlretrieve(url, zip_path)

    self.report({"INFO"}, f"Downloaded to {zip_path}")

    # Extract and rename
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(lscherry_dir)
    for item in os.listdir(lscherry_dir):
        if item.startswith("LSCherry-") and not item.endswith(".zip"):
            shutil.move(os.path.join(lscherry_dir, item), extract_path)
            break

    # Clean up zip
    os.remove(zip_path)

    self.report({"INFO"}, f"Extracted to {extract_path}")

    return extract_path
