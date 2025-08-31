import bpy  # type: ignore
from .utils import has_lscherry_collection


def draw_autosync_panel(layout, context):
    """Draw autosync UI elements"""
    ls_props = context.scene.lscherry
    lscherry_available = has_lscherry_collection()

    # AutoSync Cherry section
    box = layout.box()
    box.label(text="AutoSync Cherry", icon="AUTO")

    # Collection and Object inputs
    row = box.row()
    row.prop(ls_props, "autosync_collection_name")

    row = box.row()
    row.prop(ls_props, "autosync_object_name")

    # AutoSync toggle button
    row = box.row()
    row.scale_y = 1.2

    # Disable if no LSCherry collection found
    if not lscherry_available:
        row.enabled = False
        row.prop(
            ls_props,
            "autosync_enabled",
            text="AutoSync: No LSCherry Collection",
            toggle=True,
            icon="ERROR",
        )
        # Auto disable if was enabled
        if ls_props.autosync_enabled:
            ls_props.autosync_enabled = False
    else:
        if ls_props.autosync_enabled:
            row.alert = False
            row.prop(
                ls_props,
                "autosync_enabled",
                text="AutoSync: ON",
                toggle=True,
                icon="PLAY",
            )
        else:
            row.alert = True
            row.prop(
                ls_props,
                "autosync_enabled",
                text="AutoSync: OFF",
                toggle=True,
                icon="PAUSE",
            )
