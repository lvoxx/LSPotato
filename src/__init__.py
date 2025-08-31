# ***** BEGIN MIT LICENSE BLOCK *****
# MIT License
#
# Copyright (c) 2025 [Lvoxx]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# ***** END MIT LICENSE BLOCK *****


bl_info = {
    "name": "LSPotato",
    "author": ("Lvoxx"),
    "version": (1, 0, 6),
    "blender": (4, 3, 0),
    "location": "3D View > Properties > LSPotato",
    "description": "A collection of utility tools for the LSCherry project, including node groups management and additional workflow helpers.",
    "tracker_url": "https://github.com/lvoxx/LSCherry/issues",
    "doc_url": "https://github.com/lvoxx/LSCherry",
    "category": "Tool",
}

import bpy  # type: ignore
from .features.checkfor_update.properties import GitHubUpdaterProperties
from .features.checkfor_update.operators import (
    LSPOTATO_OT_check_updates,
    LSPOTATO_OT_dismiss_update,
    LSPOTATO_OT_install_update,
)
from .features.find_lscherry.properties import LSCherryProperties
from .features.find_lscherry.operators import (
    DownloadAndLinkLSCherry,
    RepairLSCherry,
    CleanDiskLSCherry,
)
from .features.replace_nodes.properties import LSPotatoProperties
from .features.replace_nodes.operators import ReplaceNodeGroups
from .features.make_local.operators import MakeLocalOperator
from .features.panels import LSPotatoPanel

# Import AutoSync Cherry components
from .features.autosync_cherry.operators import LSCHERRY_OT_toggle_autosync
from .features.autosync_cherry.handlers import (
    autosync_scene_update,
    autosync_depsgraph_update,
)

rgt_classes = [
    LSCherryProperties,
    LSPotatoProperties,
    GitHubUpdaterProperties,
    LSPOTATO_OT_check_updates,
    LSPOTATO_OT_install_update,
    LSPOTATO_OT_dismiss_update,
    DownloadAndLinkLSCherry,
    RepairLSCherry,
    CleanDiskLSCherry,
    LSCHERRY_OT_toggle_autosync,
    ReplaceNodeGroups,
    MakeLocalOperator,
    LSPotatoPanel,
]


def register():
    for cls in rgt_classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.lspotato = bpy.props.PointerProperty(type=LSPotatoProperties)
    bpy.types.Scene.lscherry = bpy.props.PointerProperty(type=LSCherryProperties)

    # Add autosync properties directly to LSCherryProperties class
    LSCherryProperties.autosync_collection_name = bpy.props.StringProperty(
        name="Collection", description="Target collection for auto sync", default="_LS"
    )

    LSCherryProperties.autosync_object_name = bpy.props.StringProperty(
        name="Object", description="Target object for auto sync", default="MLight"
    )

    LSCherryProperties.autosync_enabled = bpy.props.BoolProperty(
        name="AutoSync",
        description="Enable/disable automatic LSCherryProvider synchronization",
        default=False,
    )

    # Internal tracking properties
    LSCherryProperties.autosync_last_collection = bpy.props.StringProperty(default="")
    LSCherryProperties.autosync_last_object = bpy.props.StringProperty(default="")
    LSPotatoProperties.github_updater = bpy.props.PointerProperty(type=GitHubUpdaterProperties)

    # Register AutoSync handlers
    if autosync_scene_update not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(autosync_scene_update)

    if autosync_depsgraph_update not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(autosync_depsgraph_update)


def unregister():
    # Remove AutoSync handlers
    if autosync_scene_update in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(autosync_scene_update)

    if autosync_depsgraph_update in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(autosync_depsgraph_update)

    del bpy.types.Scene.lspotato
    del bpy.types.Scene.lscherry

    for cls in reversed(rgt_classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
