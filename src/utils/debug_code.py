import os
import bpy  # type: ignore
from ..features.find_lscherry.repair_lscherry import (
    get_broken_libraries,
    is_valid_library,
)


def debug_modifier_sockets(modifier):
    """Debug function to print modifier socket information"""
    if not modifier or not modifier.node_group:
        return

    print(f"\n=== Debug: Modifier '{modifier.name}' sockets ===")

    # Print input sockets
    if hasattr(modifier.node_group, "interface") and hasattr(
        modifier.node_group.interface, "items_tree"
    ):
        print("Input sockets:")
        for i, socket in enumerate(modifier.node_group.interface.items_tree):
            if socket.item_type == "SOCKET" and socket.in_out == "INPUT":
                print(
                    f"  [{i}] {socket.name} - Type: {socket.socket_type} - Identifier: {socket.identifier}"
                )

    # Print current modifier inputs
    print("Current modifier inputs:")
    for key in modifier.keys():
        if not key.startswith("_"):
            print(f"  {key}: {modifier[key]}")
    print("=== End Debug ===\n")


def debug_geometry_modifier_inputs(obj, modifier_name="Core.LSCherryProvider"):
    """Print all sockets of a Geometry Nodes modifier to debug mapping"""
    modifier = obj.modifiers.get(modifier_name)
    if not modifier:
        print(f"❌ Object '{obj.name}' has no modifier '{modifier_name}'")
        return

    ng = modifier.node_group
    if not ng:
        print(f"❌ Modifier '{modifier_name}' on '{obj.name}' has no node_group")
        return

    print(f"Modifier '{modifier_name}' node group inputs on '{obj.name}':")
    for i, socket in enumerate(ng.interface.items_tree):
        if socket.item_type == "SOCKET":
            key = f"Input_{i}"
            current_value = modifier.get(key, "<empty>")
            print(
                f"  {i}: {socket.name} ({socket.socket_type}) → key = {key}, value = {current_value}"
            )


def debug_library_info():
    """Debug function để hiển thị thông tin về tất cả libraries"""
    print("=== LIBRARY DEBUG INFO ===")

    all_libs = list(bpy.data.libraries)
    print(f"Total libraries: {len(all_libs)}")

    valid_count = 0
    broken_count = 0

    for i, lib in enumerate(all_libs):
        try:
            is_valid = is_valid_library(lib)
            status = "VALID" if is_valid else "BROKEN"

            if is_valid:
                valid_count += 1
            else:
                broken_count += 1

            print(f"{i+1:2d}. {lib.name} - {status}")
            print(f"    Path: {lib.filepath}")
            print(
                f"    Exists: {os.path.exists(lib.filepath) if lib.filepath else False}"
            )
            print()

        except Exception as e:
            print(f"{i+1:2d}. {lib.name} - ERROR: {e}")
            broken_count += 1

    print(f"Summary: {valid_count} valid, {broken_count} broken")
    print("========================")


def get_library_stats():
    """Lấy thống kê libraries"""
    try:
        all_libs = list(bpy.data.libraries)
        broken_libs = get_broken_libraries()

        return {
            "total": len(all_libs),
            "broken": len(broken_libs),
            "valid": len(all_libs) - len(broken_libs),
            "broken_names": [lib.name for lib in broken_libs],
        }
    except Exception as e:
        return {
            "error": str(e),
            "total": 0,
            "broken": 0,
            "valid": 0,
            "broken_names": [],
        }
