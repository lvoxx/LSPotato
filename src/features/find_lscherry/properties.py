import bpy  # type: ignore


from ...constants.lscherry_version import VERSION_URLS


def get_version_items(self, context):
    return [(v, v, "") for v in sorted(VERSION_URLS.keys(), reverse=True)]


class LSCherryProperties(bpy.types.PropertyGroup):
    selected_version: bpy.props.EnumProperty(
        name="Version",
        items=get_version_items,
    )  # type: ignore
