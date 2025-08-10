import os


def get_used_groups(node_tree):
    """Get set of node groups used in this node tree."""
    used = set()
    for node in node_tree.nodes:
        if (
            node.bl_idname in {"ShaderNodeGroup", "GeometryNodeGroup"}
            and node.node_tree
        ):
            used.add(node.node_tree)
    return used


def get_namespace(nt):
    """Build namespace from file path."""
    if not nt.library:
        return "Local"

    file_path = nt.library.filepath
    dir_path = os.path.dirname(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0].replace(" ", "")

    # Normalize and split directory parts
    norm_dir = os.path.normpath(dir_path).lstrip(os.sep)
    parts = [p for p in norm_dir.split(os.sep) if p]

    namespace = ".".join(parts) + "." + base_name
    return namespace
