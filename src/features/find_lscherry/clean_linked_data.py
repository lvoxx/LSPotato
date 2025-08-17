import os
import bpy  # type: ignore


def clean_linked_libraries(version: str):
    target_name = f"LSCherry-{version}.blend"
    to_remove_libs = [
        lib
        for lib in bpy.data.libraries
        if os.path.basename(lib.filepath) != target_name
    ]
    for lib in to_remove_libs:
        bpy.data.libraries.remove(lib)

def clean_lscherry_collection(version):
    target_name = f"LSCherry-{version}"
    to_remove_cols = [
        col
        for col in bpy.data.collections
        if col.name.startswith("LSCherry-") and col.name != target_name
    ]
    if not to_remove_cols:
        return None
    removed_name = to_remove_cols[0].name  # Lấy tên collection đầu tiên
    for col in to_remove_cols:
        bpy.data.collections.remove(col)
    return removed_name  # Trả về tên collection đầu tiên đã xoá


def clean_unsual_lscherry(version):
    clean_linked_libraries(version)
    return clean_lscherry_collection(version)  # Return old version name
