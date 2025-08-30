import bpy  # type: ignore


def has_lscherry_collection():
    """Check if any collection with LSCherry- prefix exists"""
    for collection in bpy.data.collections:
        if collection.name.startswith("LSCherry-"):
            return True
    return False


def get_collection_state(collection_name):
    """Get current state of collection objects"""
    try:
        collection = bpy.data.collections.get(collection_name)
        if not collection:
            return ""

        # Create a hash-like string of object names and their basic properties
        objects_state = []
        for obj in collection.objects:
            obj_info = f"{obj.name}:{len(obj.modifiers) if obj.modifiers else 0}"
            if obj.data:
                if hasattr(obj.data, "vertices"):
                    obj_info += f":{len(obj.data.vertices)}"
                elif hasattr(obj.data, "splines"):
                    obj_info += f":{len(obj.data.splines)}"
            objects_state.append(obj_info)

        return "|".join(sorted(objects_state))
    except:
        return ""


def get_object_state(object_name):
    """Get current state of specific object"""
    try:
        obj = bpy.data.objects.get(object_name)
        if not obj:
            return ""

        state_info = []
        # Object transformation
        state_info.append(f"loc:{obj.location[:]}")
        state_info.append(f"rot:{obj.rotation_euler[:]}")
        state_info.append(f"scale:{obj.scale[:]}")

        # Object data changes
        if obj.data:
            if hasattr(obj.data, "vertices"):
                state_info.append(f"verts:{len(obj.data.vertices)}")
            elif hasattr(obj.data, "splines"):
                state_info.append(f"splines:{len(obj.data.splines)}")

        return "|".join(state_info)
    except:
        return ""


def has_core_lscherry_modifier(obj):
    """Check if object already has Core.LSCherryProvider modifier"""
    if not obj or not obj.modifiers:
        return False

    for modifier in obj.modifiers:
        if (
            modifier.type == "NODES"
            and modifier.node_group
            and modifier.node_group.name == "Core.LSCherryProvider"
        ):
            return True
    return False
