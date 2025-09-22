import bpy  # type: ignore
from ....utils.get_lscherry_things import has_core_lscherry_modifier
from ....constants.app_const import LSCHERRY_PROVIDER

def set_global_modifier_input(modifier, socket_name, value):
    """Set global input for a modifier socket by name"""
    if not modifier or not modifier.node_group:
        return False

    try:
        if hasattr(modifier.node_group, "interface") and hasattr(modifier.node_group.interface, "items_tree"):
            for socket in modifier.node_group.interface.items_tree:
                if socket.item_type == "SOCKET" and socket.in_out == "INPUT" and socket.name == socket_name:
                    if socket.socket_type == "NodeSocketBool" and isinstance(value, bool):
                        modifier[socket.identifier] = value
                    elif socket.socket_type == "NodeSocketFloat" and isinstance(value, (int, float)):
                        modifier[socket.identifier] = float(value)
                    elif socket.socket_type == "NodeSocketInt" and isinstance(value, int):
                        modifier[socket.identifier] = value
                    elif socket.socket_type == "NodeSocketColor" and isinstance(value, (list, tuple)):
                        if len(value) == 3:
                            value = (*value, 1.0)
                        modifier[socket.identifier] = value
                    else:
                        return False
                    print(f"GlobalSync: {modifier.name} → {socket_name} ({socket.identifier}) = {value}")
                    return True
        print(f"GlobalSync: Socket '{socket_name}' not found in modifier '{modifier.name}'")
        return False
    except Exception as e:
        print(f"Error setting global modifier input {socket_name}: {e}")
        return False

def sync_global_settings():
    """Sync global settings to all objects with Core.LSCherryProvider"""
    try:
        scene = bpy.context.scene
        if not hasattr(scene, "lscherry") or not scene.lscherry.autosync_global_enabled:
            return False

        ls_props = scene.lscherry
        synced_count = 0

        # Convert blend mode enum to integer value for modifier
        blend_mode_value = int(ls_props.global_blend_mode)

        for obj in bpy.data.objects:
            if obj.type == "MESH" and has_core_lscherry_modifier(obj):
                modifier = obj.modifiers.get(LSCHERRY_PROVIDER)
                if modifier and isinstance(modifier, bpy.types.Modifier):
                    success_count = sum(
                        1 for _ in filter(
                            None,
                            [
                                set_global_modifier_input(modifier, "Blend Mode", blend_mode_value),
                                set_global_modifier_input(modifier, "Value Enhance", ls_props.global_value_enhance),
                                set_global_modifier_input(modifier, "World Value Enhance", ls_props.global_world_value_enhance),
                                set_global_modifier_input(modifier, "World Color", (*ls_props.global_world_color, 1.0) if len(ls_props.global_world_color) == 3 else ls_props.global_world_color)
                            ]
                        )
                    )
                    if success_count > 0:
                        # Force update the object and modifier to trigger shader refresh
                        obj.data.update()
                        modifier.node_group.interface_update(bpy.context)
                        synced_count += 1
                        print(f"GlobalSync: Synced {success_count} values for '{obj.name}' and updated shader")

        if synced_count > 0:
            print(f"GlobalSync: Applied settings to {synced_count} objects")
        return synced_count > 0
    except Exception as e:
        print(f"Error syncing global settings: {e}")
        return False

def get_global_settings_state():
    """Get current state of global settings for change detection"""
    try:
        scene = bpy.context.scene
        if not hasattr(scene, "lscherry"):
            return ""
        ls_props = scene.lscherry
        return "|".join([
            f"blend_mode:{ls_props.global_blend_mode}",
            f"value_enhance:{ls_props.global_value_enhance:.3f}",
            f"world_color:{ls_props.global_world_color[0]:.3f},{ls_props.global_world_color[1]:.3f},{ls_props.global_world_color[2]:.3f}"
        ])
    except Exception:
        return ""

def check_and_sync_global():
    """Check for global settings changes and sync if needed"""
    try:
        scene = bpy.context.scene
        if not hasattr(scene, "lscherry") or not scene.lscherry.autosync_global_enabled:
            return
        ls_props = scene.lscherry
        current_state = get_global_settings_state()
        if current_state != ls_props.autosync_last_global_state:
            sync_global_settings()
            ls_props.autosync_last_global_state = current_state
    except Exception as e:
        print(f"Error in check_and_sync_global: {e}")