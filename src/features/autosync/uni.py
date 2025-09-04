# File: features/autosync/uni.py
import bpy  # type: ignore
from .cherry_provider.ui import draw_autosync_cherry_panel
from .global_configuration.ui import draw_autosync_global_panel
from ...utils.get_lscherry_things import has_lscherry_collection


def draw_autosync_panel(layout, context):
    """Draw unified autosync UI with tabs"""
    ls_props = context.scene.lscherry
    lscherry_available = has_lscherry_collection()

    # AutoSync section
    box = layout.box()
    box.label(text="AutoSync", icon="AUTO")

    # Tab selector
    row = box.row()
    row.scale_y = 1.1
    
    # Provider tab
    provider_op = row.operator(
        "lscherry.set_autosync_tab", 
        text="Provider",
        depress=(ls_props.autosync_active_tab == "PROVIDER")
    )
    provider_op.tab = "PROVIDER"
    
    # Global tab
    global_op = row.operator(
        "lscherry.set_autosync_tab",
        text="Global", 
        depress=(ls_props.autosync_active_tab == "GLOBAL")
    )
    global_op.tab = "GLOBAL"

    # Tab content
    if ls_props.autosync_active_tab == "PROVIDER":
        draw_autosync_cherry_panel(box, context, lscherry_available)
    elif ls_props.autosync_active_tab == "GLOBAL":
        draw_autosync_global_panel(box, context, lscherry_available)