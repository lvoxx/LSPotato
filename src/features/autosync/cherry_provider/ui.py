def draw_autosync_cherry_panel(layout, context, lscherry_available):
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

    # Disable if no LSCherry collection found
    if not lscherry_available:
        row.enabled = False
        row.prop(
            ls_props,
            "autosync_provider_enabled",
            text="AutoSync: No LSCherry Collection",
            toggle=True,
            icon="ERROR",
        )
        # Auto disable if was enabled
        if ls_props.autosync_provider_enabled:
            ls_props.autosync_provider_enabled = False
    else:
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
