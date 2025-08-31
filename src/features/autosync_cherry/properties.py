import bpy  # type: ignore


def toggle_autosync(self, context):
    """Callback when autosync toggle changes"""
    from .sync import sync_collection_objects, sync_target_object
    from .utils import get_collection_state, get_object_state, has_lscherry_collection

    # Check if LSCherry collection exists before enabling
    if self.auto_sync_enabled and not has_lscherry_collection():
        self.auto_sync_enabled = False
        return

    if self.auto_sync_enabled:
        # Perform immediate sync for existing objects without Provider
        sync_collection_objects(self.collection_name)
        sync_target_object(self.object_name)

        # Initialize tracking data AFTER initial sync
        self._last_collection_objects = get_collection_state(self.collection_name)
        self._last_object_data = get_object_state(self.object_name)


class AutoSyncCherryProperties(bpy.types.PropertyGroup):
    collection_name: bpy.props.StringProperty(
        name="Collection", description="Target collection for auto sync", default="_LS"
    )  # type: ignore

    object_name: bpy.props.StringProperty(
        name="Sun", description="Target sun object for auto sync", default="MLight"
    )  # type: ignore

    auto_sync_enabled: bpy.props.BoolProperty(
        name="AutoSync",
        description="Enable/disable automatic LSCherryProvider synchronization",
        default=False,
        update=toggle_autosync,
    )  # type: ignore

    # Internal tracking properties
    _last_collection_objects: bpy.props.StringProperty(default="")  # type: ignore
    _last_object_data: bpy.props.StringProperty(default="")  # type: ignore
