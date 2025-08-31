import os
import tempfile

def get_lscherry_path() -> str:
    temp_dir = tempfile.gettempdir()
    cache_dir = os.path.join(temp_dir, "LSCherry")
    os.makedirs(cache_dir, exist_ok=True)  # Tạo folder nếu chưa tồn tại
    return cache_dir


def get_version_path(version: str) -> str:
    return os.path.join(get_lscherry_path(), version)
