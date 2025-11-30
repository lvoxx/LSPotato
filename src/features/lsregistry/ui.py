import bpy  # type: ignore


def draw_lsregistry_panel(layout, context):
    """Draw LSRegistry section in the main panel"""
    scene = context.scene

    # Check if lsregistry properties exist
    if not hasattr(scene, "lsregistry"):
        return

    props = scene.lsregistry

    # LSRegistry collapsible box
    box = layout.box()
    row = box.row()

    # Check if expanded property exists
    is_expanded = getattr(scene, "lsregistry_expanded", False)

    row.prop(
        scene,
        "lsregistry_expanded",
        icon="TRIA_DOWN" if is_expanded else "TRIA_RIGHT",
        icon_only=True,
        emboss=False,
    )
    row.label(text="LSRegistry", icon="PACKAGE")

    # Expanded content
    if is_expanded:
        # Multi-line registry input field
        col = box.column(align=True)
        row = col.row(align=True)
        row.label(text="Open in Text Editor")

        # If text is selected, show mini text editor
        if props.registry_text:
            text_block = bpy.data.texts.get(props.registry_text)
            if text_block:
                lines = text_block.as_string().split("\n")
                text_box = box.box()
                for i, line in enumerate(lines[:5]):
                    if line.strip():
                        text_box.label(text=line)
                if len(lines) > 5:
                    text_box.label(text="... (open in Text Editor for more)")
                text_box.operator("text.jump", text="Edit in Text Editor", icon="TEXT")
        else:
            # Create new text button
            row = col.row()
            row.operator(
                "lsregistry.create_registry_text",
                text="Create Registry List",
                icon="ADD",
            )

        # Show currently installed registries if exists
        if props.current_registries:
            installed_box = box.box()
            installed_box.label(text="Installed:", icon="CHECKMARK")
            for registry in props.current_registries.split(","):
                if registry.strip():
                    installed_box.label(text=f"  • {registry.strip()}")

        # Get and Repair buttons in one row
        row = box.row(align=True)

        # Get button
        if props.is_downloading:
            row.enabled = False
        row.operator("lsregistry.get", text="Get", icon="IMPORT")

        # Repair button
        repair_row = row.row(align=True)
        if props.is_downloading or not props.current_registries:
            repair_row.enabled = False
        repair_row.operator("lsregistry.repair", text="Repair", icon="TOOL_SETTINGS")

        # Show downloading status
        if props.is_downloading:
            box.label(text="Downloading...", icon="TIME")

        # Credentials section
        cred_box = box.box()
        cred_row = cred_box.row()
        cred_row.label(text="Credentials", icon="KEYINGSET")
        cred_row.operator("lsregistry.add_credential", text="", icon="ADD")

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
                remove_col.alignment = "RIGHT"
                remove_op = remove_col.operator(
                    "lsregistry.remove_credential", text="", icon="X"
                )
                remove_op.index = i
        else:
            cred_box.label(text="No credentials added", icon="INFO")
