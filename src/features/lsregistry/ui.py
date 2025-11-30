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
        # Multi-line registry input field
        col = box.row()
        col.label(text="Registries (one per line):")
        
        col = box.row()
        col.prop(props, "registry_input", text="")
        
        # Show currently installed registries if exists
        if props.current_registries:
            installed_box = box.box()
            installed_box.label(text="Installed:", icon='CHECKMARK')
            for registry in props.current_registries.split(','):
                if registry.strip():
                    installed_box.label(text=f"  • {registry.strip()}")
        
        # Get and Repair buttons in one row
        row = box.row(align=True)
        
        # Get button
        if props.is_downloading:
            row.enabled = False
        row.operator("lsregistry.get", text="Get", icon='IMPORT')
        
        # Repair button
        repair_row = row.row(align=True)
        if props.is_downloading or not props.current_registries:
            repair_row.enabled = False
        repair_row.operator("lsregistry.repair", text="Repair", icon='TOOL_SETTINGS')
        
        # Show downloading status
        if props.is_downloading:
            box.label(text="Downloading...", icon='TIME')
        
        # Credentials section
        cred_box = box.box()
        cred_row = cred_box.row()
        cred_row.label(text="Credentials", icon='KEYINGSET')
        cred_row.operator("lsregistry.add_credential", text="", icon='ADD')
        
        # List credentials
        if len(props.credentials) > 0:
            for i, cred in enumerate(props.credentials):
                cred_item_box = cred_box.box()
                item_row = cred_item_box.row()
                
                # Namespace and token fields
                col = item_row.column()
                col.prop(cred, "namespace", text="Namespace")
                col.prop(cred, "token", text="Token")
                
                # Remove button
                remove_col = item_row.column()
                remove_col.alignment = 'RIGHT'
                remove_op = remove_col.operator("lsregistry.remove_credential", text="", icon='X')
                remove_op.index = i
        else:
            cred_box.label(text="No credentials added", icon='INFO')