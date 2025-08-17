import os
import bpy  # type: ignore


def get_library_paths():
    return bpy.data.libraries


def get_all_collections():
    return bpy.data.collections


def get_2remove_collections(new_version):
    return [
        col
        for col in bpy.data.collections
        if "LSCherry-" in col.name and new_version not in col.name
    ]


def get_2remove_libs(new_version):
    return [lib for lib in get_library_paths() if new_version not in lib.filepath]
