from ..constants.app_const import LSCHERRY_PROVIDER

def has_core_lscherry_modifier(obj):
    """Check if object already has Core.LSCherryProvider modifier"""
    if not obj or not obj.modifiers:
        return False

    for modifier in obj.modifiers:
        if (
            modifier.type == "NODES"
            and modifier.node_group
            and LSCHERRY_PROVIDER in modifier.node_group.name
        ):
            return True
    return False