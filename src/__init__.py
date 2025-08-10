from .config_manager import ConfigManager

# Load bl_info from config
bl_info = ConfigManager.get_bl_info()


def register():
    _ = ConfigManager  # Ensure config is initialized

    import bpy  # type: ignore
    from .panels import LinkedGraphPanel
    from .operators import (
        BrowseWorkspaceOperator,
        LinkedGraphProperties,
        GenerateLinkedGraphOperator,
    )

    bpy.utils.register_class(LinkedGraphPanel)
    bpy.utils.register_class(GenerateLinkedGraphOperator)
    bpy.utils.register_class(BrowseWorkspaceOperator)
    bpy.utils.register_class(LinkedGraphProperties)
    bpy.types.Scene.linked_graph_props = bpy.props.PointerProperty(
        type=LinkedGraphProperties
    )


def unregister():
    import bpy  # type: ignore
    from .panels import LinkedGraphPanel
    from .operators import (
        BrowseWorkspaceOperator,
        LinkedGraphProperties,
        GenerateLinkedGraphOperator,
    )

    bpy.utils.unregister_class(LinkedGraphPanel)
    bpy.utils.unregister_class(GenerateLinkedGraphOperator)
    bpy.utils.unregister_class(BrowseWorkspaceOperator)
    bpy.utils.unregister_class(LinkedGraphProperties)
    del bpy.types.Scene.linked_graph_props


if __name__ == "__main__":
    register()
