def draw_autosync_cherry_panel(layout, context):
    """Draw Cherry Provider autosync UI elements"""
    ls_props = context.scene.lscherry

    # Collection and Object inputs
    row = layout.row()
    row.prop(ls_props, "autosync_collection_name")

    row = layout.row()
    row.prop(ls_props, "autosync_object_name")

    # AutoSync toggle button
    row = layout.row()
    row.scale_y = 1.2

    if ls_props.autosync_provider_enabled:
        row.alert = False
        row.prop(
            ls_props,
            "autosync_provider_enabled",
            text="AutoSync: ON",
            toggle=True,
            icon="PLAY",
        )
    else:
        row.alert = True
        row.prop(
            ls_props,
            "autosync_provider_enabled",
            text="AutoSync: OFF",
            toggle=True,
            icon="PAUSE",
        )
