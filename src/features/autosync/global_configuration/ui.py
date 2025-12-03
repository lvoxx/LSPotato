# File: features/autosync/global_configuration/ui.py


from ....constants.blend_mode import BLEND_MODE


def draw_autosync_global_panel(layout, context, lscherry_available):
    """Draw Global Configuration autosync UI elements"""
    ls_props = context.scene.lscherry

    # Global settings
    row = layout.row()
    row.prop(ls_props, "global_blend_mode")

    row = layout.row()
    row.prop(ls_props, "global_value_enhance", slider=True)

    # "1" = Light Sources
    # "2" = Background
    # "3" = None
    # Only show World Value Enhance when blend mode is 'Light Sources' or 'Background'
    if (
        ls_props.global_blend_mode == BLEND_MODE["Background"]["value"]
    ):  
        row = layout.row()
        row.prop(ls_props, "global_world_value_enhance", slider=True)
    if (
        ls_props.global_blend_mode == BLEND_MODE["None"]["value"]
    ):
        row = layout.row()
        row.prop(ls_props, "global_world_color")

    # AutoSync toggle button
    row = layout.row()
    row.scale_y = 1.2

    # Disable if no LSCherry collection found
    if not lscherry_available:
        row.enabled = False
        row.prop(
            ls_props,
            "autosync_global_enabled",
            text="AutoSync: No LSCherry Collection",
            toggle=True,
            icon="ERROR",
        )
        # Auto disable if was enabled
        if ls_props.autosync_global_enabled:
            ls_props.autosync_global_enabled = False
    else:
        if ls_props.autosync_global_enabled:
            row.alert = False
            row.prop(
                ls_props,
                "autosync_global_enabled",
                text="AutoSync: ON",
                toggle=True,
                icon="PLAY",
            )
        else:
            row.alert = True
            row.prop(
                ls_props,
                "autosync_global_enabled",
                text="AutoSync: OFF",
                toggle=True,
                icon="PAUSE",
            )
