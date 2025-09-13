import bpy  # type: ignore
from .sync import check_and_sync_global


@bpy.app.handlers.persistent
def autosync_global_scene_update(scene):
    """Scene update handler for global autosync"""
    check_and_sync_global()


@bpy.app.handlers.persistent
def autosync_global_depsgraph_update(scene, depsgraph):
    """Depsgraph update handler for global autosync"""
    check_and_sync_global()