import bpy  # type: ignore
from ....utils.get_lscherry_things import (
    has_core_lscherry_modifier,
    has_lscherry_collection,
)
from ....utils.get_blender_things import (
    get_collection_state,
    get_object_state
)
from ....constants.app_const import LSCHERRY_PROVIDER


def add_core_lscherry_modifier(obj):
    """Add Core.LSCherryProvider modifier to object at first position"""
    try:
        # Check if Core.LSCherryProvider node group exists
        node_group = bpy.data.node_groups.get(LSCHERRY_PROVIDER)
        if not node_group:
            print("Warning: Core.LSCherryProvider node group not found")
            return False

        # Add geometry nodes modifier
        modifier = obj.modifiers.new(name=LSCHERRY_PROVIDER, type="NODES")
        modifier.node_group = node_group

        # Move to first position
        if len(obj.modifiers) > 1:
            while obj.modifiers.find(modifier.name) > 0:
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.modifier_move_up(modifier=modifier.name)

        print(f"Successfully added modifier to {obj.name}")
        print(
            f"Modifier position for {obj.name}: {obj.modifiers.find(modifier.name)}"
        )  # Should be 0
        return True

    except Exception as e:
        print(f"Error adding modifier to {obj.name}: {e}")
        return False


def set_modifier_input(modifier, socket_identifier, target_object):
    """Set input for a modifier socket using identifier"""
    if not modifier or not modifier.node_group:
        return False

    # Use the socket identifier directly
    modifier[socket_identifier] = target_object
    print(f"AutoSync: {modifier.name} → {socket_identifier} = {target_object.name}")
    return True


def sync_collection_objects(collection_name, target_object_name):
    """Add Core.LSCherryProvider to all objects in collection if not present, excluding target object"""
    try:
        collection = bpy.data.collections.get(collection_name)
        target_obj = bpy.data.objects.get(target_object_name)

        if not collection or not target_obj:
            print(
                f"AutoSync: Collection '{collection_name}' or target object '{target_object_name}' not found, skipping"
            )
            return False

        synced_count = 0
        for obj in collection.objects:
            if (
                obj.type == "MESH" and obj.name != target_object_name
            ):  # Exclude target object to avoid double sync
                if not has_core_lscherry_modifier(obj):
                    if add_core_lscherry_modifier(obj):
                        modifier = obj.modifiers.get(LSCHERRY_PROVIDER)
                    else:
                        continue
                else:
                    modifier = obj.modifiers.get(LSCHERRY_PROVIDER)

                if modifier and isinstance(modifier, bpy.types.Modifier):
                    if set_modifier_input(modifier, "Input_2", target_obj):
                        synced_count += 1

        if synced_count > 0:
            print(
                f"AutoSync: Synced Core.LSCherryProvider (Input_2 → {target_object_name}) "
                f"for {synced_count} objects in '{collection_name}'"
            )

        return True

    except Exception as e:
        print(f"Error syncing collection '{collection_name}': {e}")
        return False


def sync_target_object(object_name, target_object_name):
    """Add Core.LSCherryProvider to specific object if not present"""
    try:
        obj = bpy.data.objects.get(object_name)
        target_obj = bpy.data.objects.get(target_object_name)

        if not obj or not target_obj:
            print(
                f"AutoSync: Object '{object_name}' or target object '{target_object_name}' not found, skipping"
            )
            return False

        if obj.type == "MESH":
            if not has_core_lscherry_modifier(obj):
                if add_core_lscherry_modifier(obj):
                    modifier = obj.modifiers.get(LSCHERRY_PROVIDER)
                else:
                    return False
            else:
                modifier = obj.modifiers.get(LSCHERRY_PROVIDER)

            if modifier and isinstance(modifier, bpy.types.Modifier):
                if set_modifier_input(modifier, "Input_2", target_obj):
                    print(
                        f"AutoSync: Synced Core.LSCherryProvider (Input_2 → {target_object_name}) "
                        f"on '{object_name}'"
                    )
                    return True

        return False

    except Exception as e:
        print(f"Error syncing object '{object_name}': {e}")
        return False


def check_and_sync(scene):
    """Check for changes and sync if needed"""
    if not hasattr(scene, "lscherry"):
        return

    ls_props = scene.lscherry

    if not ls_props.autosync_provider_enabled:
        return

    if not has_lscherry_collection():
        ls_props.autosync_provider_enabled = False
        return

    # Validate target object exists
    target_obj = bpy.data.objects.get(ls_props.autosync_object_name)
    if not target_obj:
        print(
            f"AutoSync: Target object '{ls_props.autosync_object_name}' not found, autosync skipped"
        )
        return

    # Check collection changes
    current_collection_state = get_collection_state(ls_props.autosync_collection_name)
    if current_collection_state != ls_props.autosync_last_collection:
        sync_collection_objects(
            ls_props.autosync_collection_name, ls_props.autosync_object_name
        )
        ls_props.autosync_last_collection = current_collection_state

    # Check target object changes
    current_object_state = get_object_state(ls_props.autosync_object_name)
    if current_object_state != ls_props.autosync_last_object:
        sync_target_object(ls_props.autosync_object_name, ls_props.autosync_object_name)
        ls_props.autosync_last_object = current_object_state
