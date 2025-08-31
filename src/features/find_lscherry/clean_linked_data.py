import os
import bpy  # type: ignore
from ...utils.get_blender_things import get_2remove_collections, get_2remove_libs


def clean_linked_libraries(self, new_version: str):
    to_remove_libs = get_2remove_libs(new_version)
    # No execution check
    if not to_remove_libs:
        self.report(
            {"INFO"},
            f"No LSCherry linked libraries to be removed. Skip",
        )
        return
    for lib in to_remove_libs:
        bpy.data.libraries.remove(lib)
    self.report(
        {"INFO"},
        f"Removed linked LSCherry-{new_version}",
    )


def clean_lscherry_collection(self, new_version):
    to_remove_cols = get_2remove_collections(new_version)
    if not to_remove_cols:
        self.report(
            {"INFO"},
            f"No old LSCherry collection to be removed. Skip",
        )
        return None
    removed_name = to_remove_cols[0].name  # Lấy tên collection đầu tiên
    for col in to_remove_cols:
        del_col = col.name
        bpy.data.collections.remove(col)
        self.report(
            {"INFO"},
            f"Removed LSCherry collection {del_col}",
        )
    return removed_name  # Trả về tên collection đầu tiên đã xoá


def reload_lscherry(self, new_version):
    clean_linked_libraries(self, new_version)
    return clean_lscherry_collection(self, new_version)  # Return old version name
