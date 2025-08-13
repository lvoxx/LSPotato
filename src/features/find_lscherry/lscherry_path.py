import os


def get_lscherry_path() -> str:
    addon_dir = os.path.dirname(__file__)
    return os.path.join(addon_dir, "LSCherry")


def get_version_path(version: str) -> str:
    return os.path.join(get_lscherry_path(), version)
