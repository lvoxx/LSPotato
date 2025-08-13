import bpy  # type: ignore


def clean_linked_libraries(version):
    to_remove_libs = [lib for lib in bpy.data.libraries if version not in lib.filepath]
    for lib in to_remove_libs:
        bpy.data.libraries.remove(lib)


def clean_lscherry_collection(version):
    to_remove_cols = [
        col
        for col in bpy.data.collections
        if "LSCherry-" in col.name and version not in col.name
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
