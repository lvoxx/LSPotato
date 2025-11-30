import bpy  # type: ignore


def draw_lsregistry_panel(layout, context):
    """Draw LSRegistry section in the main panel"""
    scene = context.scene
    
    # Check if lsregistry properties exist
    if not hasattr(scene, 'lsregistry'):
        return
    
    props = scene.lsregistry
    
    # LSRegistry collapsible box
    box = layout.box()
    row = box.row()
    
    # Check if expanded property exists
    is_expanded = getattr(scene, 'lsregistry_expanded', False)
    
    row.prop(
        scene,
        "lsregistry_expanded",
        icon="TRIA_DOWN" if is_expanded else "TRIA_RIGHT",
        icon_only=True,
        emboss=False
    )
    row.label(text="LSRegistry", icon='PACKAGE')
    
    # Expanded content
    if is_expanded:
        # Registry input field
        box.prop(props, "registry_input", text="Registry")
        
        # Show current installed registry if exists
        if props.current_registry:
            row = box.row()
            row.label(text=f"Installed: {props.current_registry}", icon='CHECKMARK')
        
        # Get and Repair buttons in one row
        row = box.row(align=True)
        
        # Get button
        if props.is_downloading:
            row.enabled = False
        row.operator("lsregistry.get", text="Get", icon='IMPORT')
        
        # Repair button
        repair_row = row.row(align=True)
        if props.is_downloading or not props.current_registry:
            repair_row.enabled = False
        repair_row.operator("lsregistry.repair", text="Repair", icon='TOOL_SETTINGS')
        
        # Show downloading status
        if props.is_downloading:
            box.label(text="Downloading...", icon='TIME')