import os
import shutil
import zipfile
from . import rarfile
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
            f"Version {version} found at {extract_path}, use the local version instead.",
        )
        return extract_path

    os.makedirs(extract_path, exist_ok=True)

    # Get URL from version_urls
    url = version_urls.get(version, "")
    if not url:
        self.report({"ERROR"}, f"No download URL found for version {version}")
        return None

    self.report({"INFO"}, f"Found version {version} at {url}")

    # Xác định đuôi file
    ext = ".rar" if url.lower().endswith(".rar") else ".zip"
    archive_path = os.path.join(lscherry_dir, f"LSCherry-{version}{ext}")

    # Download file
    urlretrieve(url, archive_path)
    self.report({"INFO"}, f"Downloaded to {archive_path}")

    # Extract file
    try:
        if ext == ".zip":
            with zipfile.ZipFile(archive_path, "r") as zip_ref:
                zip_ref.extractall(extract_path)
        else:  # .rar
            with rarfile.RarFile(archive_path, "r") as rar_ref:
                rar_ref.extractall(extract_path)
    except Exception as e:
        self.report({"ERROR"}, f"Failed to extract archive: {e}")
        return None

    # Clean up archive
    os.remove(archive_path)

    # Nếu trong extract_path chỉ có 1 thư mục LSCherry-xxx → move nội dung lên 1 cấp
    items = os.listdir(extract_path)
    if len(items) == 1 and items[0].startswith("LSCherry-"):
        inner_dir = os.path.join(extract_path, items[0])
        for sub in os.listdir(inner_dir):
            shutil.move(os.path.join(inner_dir, sub), extract_path)
        shutil.rmtree(inner_dir)

    self.report({"INFO"}, f"Extracted to {extract_path}")

    return extract_path
