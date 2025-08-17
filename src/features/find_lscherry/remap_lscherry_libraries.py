import re
import bpy  # type: ignore
import os

from ...constants.app_const import LSCHERRY_COL_REGEX


def get_old_version():
    """
    Tìm version cũ từ collection dạng LSCherry-<version>.
    Nếu không có thì return None.
    """
    pattern = re.compile(LSCHERRY_COL_REGEX)
    for col in bpy.data.collections:
        match = pattern.match(col.name)
        if match:
            return match.group(1)
    return None


def remap_lscherry_libraries(self, new_version):
    old_version = get_old_version()
    if not old_version:
        self.report({"INFO"}, "No old LSCherry collection found. Skip remap.")
        return

    if old_version == new_version:
        self.report({"INFO"}, "No remap needed (same version). Skip.")
        return

    old_ver_libs = [lib for lib in bpy.data.libraries if old_version in lib.filepath]
    if not old_ver_libs:
        self.report({"INFO"}, f"No libraries found with version {old_version}")
        return

    for lib in old_ver_libs:
        old_path = lib.filepath
        if "LSCherry" not in old_path:
            continue

        # Split path thành các phần
        parts = old_path.split(os.sep)
        try:
            idx = parts.index(old_version)
        except ValueError:
            if old_version not in old_path:
                self.report(
                    {"WARNING"}, f"Cannot find version '{old_version}' in: {old_path}"
                )
                continue

        parts[idx] = new_version
        new_path = os.sep.join(parts)

        if not os.path.exists(new_path):
            self.report({"WARNING"}, f"No file is found at: {new_path}")
            continue

        lib.filepath = new_path
        try:
            lib.reload()
            self.report({"INFO"}, f"Remapped: {old_version} → {new_version}")
        except Exception as e:
            self.report({"ERROR"}, f"Failed to reload {new_path}: {e}")
