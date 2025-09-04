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
        if socket.item_type == 'SOCKET':
            key = f"Input_{i}"
            current_value = modifier.get(key, "<empty>")
            print(f"  {i}: {socket.name} ({socket.socket_type}) → key = {key}, value = {current_value}")