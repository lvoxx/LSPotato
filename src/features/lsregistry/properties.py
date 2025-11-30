import bpy  # type: ignore


class LSRegistryProperties(bpy.types.PropertyGroup):
    """Properties for LSRegistry feature"""
    
    registry_input: bpy.props.StringProperty(
        name="Registry",
        description="Registry namespace and version (e.g., io.github.lvoxx.world-builder:1.0.0)",
        default=""
    )
    
    current_registry: bpy.props.StringProperty(
        name="Current Registry",
        description="Currently installed registry",
        default=""
    )
    
    is_downloading: bpy.props.BoolProperty(
        name="Is Downloading",
        description="Flag to indicate download in progress",
        default=False
    )