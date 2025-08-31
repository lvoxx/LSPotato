import bpy  # type: ignore


class GitHubUpdaterProperties(bpy.types.PropertyGroup):
    update_available: bpy.props.BoolProperty(default=False)  # type: ignore
    latest_version: bpy.props.StringProperty(default="")  # type: ignore
    update_dismissed: bpy.props.BoolProperty(default=False)  # type: ignore
    checking_update: bpy.props.BoolProperty(default=False)  # type: ignore
    last_check_time: bpy.props.FloatProperty(default=0.0)  # type: ignore
