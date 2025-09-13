import os
import tempfile

from ...constants.app_const import LSCHERRY_FILE_WITH_EXTENSION, LSCHERRY_ROOT_FOLDER


def get_lscherry_path() -> str:
    temp_dir = tempfile.gettempdir()
    cache_dir = os.path.join(temp_dir, LSCHERRY_ROOT_FOLDER)
    os.makedirs(cache_dir, exist_ok=True)  # Tạo folder nếu chưa tồn tại
    return cache_dir


def get_version_path(version: str) -> str:
    return os.path.join(get_lscherry_path(), version)


def get_blend_file(version: str) -> str:
    return os.path.join(get_version_path(version), LSCHERRY_FILE_WITH_EXTENSION)
