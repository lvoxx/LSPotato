import bpy  # type: ignore
from .sync import check_and_sync


@bpy.app.handlers.persistent
def autosync_provider_scene_update(scene):
    """Scene update handler for autosync"""
    check_and_sync(scene)


@bpy.app.handlers.persistent
def autosync_provider_depsgraph_update(scene, depsgraph):
    """Depsgraph update handler for autosync"""
    check_and_sync(scene)
