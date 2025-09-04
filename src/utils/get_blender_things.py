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
