import bpy  # type: ignore


def clean_linked_libraries():
    context = bpy.context
    version = context.scene.lscherry.selected_version
    to_remove = [lib for lib in bpy.data.libraries if version not in lib.filepath]
    for lib in to_remove:
        bpy.data.libraries.remove(lib)
