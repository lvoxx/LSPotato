from ..constants.app_const import LSCHERRY_PROVIDER

def get_core_lscherry_modifier(obj):
    """Return the Core.LSCherryProvider modifier on obj, or None.

    Matches on the node group name (substring) rather than the modifier
    name, so providers that are linked/appended in-file or renamed are
    still found.
    """
    if not obj or not obj.modifiers:
        return None

    for modifier in obj.modifiers:
        if (
            modifier.type == "NODES"
            and modifier.node_group
            and LSCHERRY_PROVIDER in modifier.node_group.name
        ):
            return modifier
    return None


def has_core_lscherry_modifier(obj):
    """Check if object already has Core.LSCherryProvider modifier"""
    return get_core_lscherry_modifier(obj) is not None