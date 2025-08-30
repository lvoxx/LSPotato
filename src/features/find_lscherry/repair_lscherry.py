import os
import shutil
from .lscherry_path import get_version_path
from .operators import download_and_extract


def repair_broken_version(self, version):
    """Repair a broken LSCherry version by re-downloading and extracting it"""
    extract_path = get_version_path(version)

    # Remove broken version folder if it exists
    if os.path.exists(extract_path):
        try:
            shutil.rmtree(extract_path)
            self.report({"INFO"}, "message.info.removed_broken_folder".format(path=extract_path))
        except Exception as e:
            self.report(
                {"WARNING"}, "message.warning.failed_remove_broken_folder".format(path=extract_path, error=e)
            )

    # Re-download and extract the version
    return download_and_extract(self, version)
