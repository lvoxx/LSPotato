import os
import bpy  # type: ignore
from .lscherry_path import get_version_path

from ...constants.lscherry_version import version_urls
from ...constants.app_const import CHERRY_OBJECT


def get_version_items(self, context):
    """Generate items for EnumProperty with version status."""
    items = []

    # Ensure version_urls is not empty
    if not version_urls:
        items.append(
            ("NONE", "No versions available", "No LSCherry versions found", "ERROR", 0)
        )
        return items

    for v in sorted(version_urls.keys(), reverse=True):
        extract_path = get_version_path(v)
        downloaded = os.path.exists(extract_path)
        collection_name = f"LSCherry-{v}"
        is_linked = any(
            coll.name == collection_name and CHERRY_OBJECT in coll.objects
            for coll in bpy.data.collections
        )
        if is_linked:
            desc = "Linked in file"
            display_name = f"* {v}"
        elif downloaded:
            desc = "Downloaded to your device"
            display_name = f"+ {v}"
        else:
            desc = "Available for download"
            display_name = f"- {v}"
            
        items.append((v, display_name, desc))

    # If no items, add a default one to avoid empty EnumProperty
    if not items:
        items.append(
            ("NONE", "No versions available", "No LSCherry versions found", "ERROR", 0)
        )

    return items


def update_version(self, context):
    """Callback to update the UI when selected_version changes."""
    # Force UI redraw to ensure the EnumProperty reflects the latest state
    for area in context.screen.areas:
        if area.type == "PROPERTIES":
            area.tag_redraw()


class LSCherryProperties(bpy.types.PropertyGroup):
    selected_version: bpy.props.EnumProperty(
        name="Version",
        items=get_version_items,
        update=update_version,  # Trigger UI update when version changes
    )  # type: ignore
