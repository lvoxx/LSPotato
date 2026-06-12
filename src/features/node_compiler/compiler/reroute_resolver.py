"""
Reroute Resolver
Traces NodeReroute chains to find the true source socket,
so compiled code never needs to create reroute nodes.
"""


def resolve_from_socket(socket):
    """
    Given an input socket, follow any chain of NodeReroute nodes upstream
    and return the real (non-reroute) from_node and from_socket.

    Returns (from_node, from_socket) or (None, None) if the socket is
    unlinked or the chain dead-ends.
    """
    if not socket.is_linked or not socket.links:
        return None, None

    link = socket.links[0]
    from_node = link.from_node
    from_socket = link.from_socket

    # Walk through reroutes
    while from_node.type == 'REROUTE':
        reroute_input = from_node.inputs[0]
        if not reroute_input.is_linked or not reroute_input.links:
            return None, None
        link = reroute_input.links[0]
        from_node = link.from_node
        from_socket = link.from_socket

    return from_node, from_socket


def get_socket_index(socket_collection, target_socket):
    """Return the index of target_socket in socket_collection."""
    for i, s in enumerate(socket_collection):
        if s == target_socket:
            return i
    return 0
