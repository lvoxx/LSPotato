import os
import shutil
from ...features.find_lscherry.lscherry_path import get_version_path
from ...features.find_lscherry.operators import download_and_extract


def fix_broken_version(self, version):
    """Fix a broken LSCherry version by re-downloading and extracting it"""
    extract_path = get_version_path(version)

    # Remove broken version folder if it exists
    if os.path.exists(extract_path):
        try:
            shutil.rmtree(extract_path)
            self.report({"INFO"}, f"Removed broken version folder: {extract_path}")
        except Exception as e:
            self.report(
                {"WARNING"}, f"Failed to remove broken folder {extract_path}: {e}"
            )

    # Re-download and extract the version
    return download_and_extract(self, version)
