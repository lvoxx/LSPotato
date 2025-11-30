import bpy  # type: ignore


class LSRegistryCredentialItem(bpy.types.PropertyGroup):
    """Individual credential item for registries"""
    
    namespace: bpy.props.StringProperty(
        name="Namespace",
        description="Registry namespace (e.g., io.github.user.repo)",
        default=""
    ) # pyright: ignore[reportInvalidTypeForm]
    
    token: bpy.props.StringProperty(
        name="Token",
        description="GitHub personal access token",
        default="",
        subtype='PASSWORD'
    ) # pyright: ignore[reportInvalidTypeForm]


class LSRegistryProperties(bpy.types.PropertyGroup):
    """Properties for LSRegistry feature"""
    
    registry_text: bpy.props.StringProperty(
        name="Registry",
        description="Registry namespaces and versions, one per line (e.g., io.github.lvoxx.world-builder:1.0.0)",
        default=""
    ) # pyright: ignore[reportInvalidTypeForm]
    
    current_registries: bpy.props.StringProperty(
        name="Current Registries",
        description="Currently installed registries (comma-separated)",
        default=""
    ) # pyright: ignore[reportInvalidTypeForm]
    
    is_downloading: bpy.props.BoolProperty(
        name="Is Downloading",
        description="Flag to indicate download in progress",
        default=False
    ) # pyright: ignore[reportInvalidTypeForm]
    
    # Collection property for credentials
    credentials: bpy.props.CollectionProperty(
        type=LSRegistryCredentialItem
    ) # pyright: ignore[reportInvalidTypeForm]
    
    credentials_index: bpy.props.IntProperty(
        name="Credentials Index",
        default=0
    ) # pyright: ignore[reportInvalidTypeForm]