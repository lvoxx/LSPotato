import bpy  # type: ignore


def clean_linked_libraries(version):
    to_remove_libs = [lib for lib in bpy.data.libraries if version not in lib.filepath]
    for lib in to_remove_libs:
        bpy.data.libraries.remove(lib)


def clean_lscherry_collections(version):
    to_remove_cols = [
        col
        for col in bpy.data.collections
        if "LSCherry-" in col.name and version not in col.name
    ]
    for col in to_remove_cols:
        bpy.data.collections.remove(col)


def clean_unsual_lscherry(version):
    clean_linked_libraries(version)
    clean_lscherry_collections(version)
