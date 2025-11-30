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
    "version": (1, 0, 14),
    "blender": (4, 3, 0),
    "location": "3D View > Properties > LSPotato",
    "description": "A collection of utility tools for the LSCherry project, including node groups management and additional workflow helpers.",
    "tracker_url": "https://github.com/lvoxx/LSCherry/issues",
    "doc_url": "https://github.com/lvoxx/LSCherry",
    "category": "Tool",
}

import bpy  # type: ignore

# ==========================================
# - DO NOT DELETE THIS, FOR LOADING VENDOR -
# ==========================================
import sys
import os

addon_root = os.path.dirname(__file__)
if addon_root not in sys.path:
    sys.path.append(addon_root)
# ==========================================
# - DO NOT DELETE THIS, FOR LOADING VENDOR -
# ==========================================

# Import Updater
from .features.checkfor_update.properties import GitHubUpdaterProperties
from .constants.blend_mode import BLEND_MODE
from .features.checkfor_update.operators import (
    LSPOTATO_OT_check_updates,
    LSPOTATO_OT_dismiss_update,
    LSPOTATO_OT_install_update,
)

# Import LSCherry Version Management
from .features.find_lscherry.properties import LSCherryProperties
from .features.find_lscherry.operators import (
    DownloadAndLinkLSCherry,
    RepairLSCherry,
    CleanDiskLSCherry,
)

# Import Replace Nodes
from .features.replace_nodes.properties import LSPotatoProperties
from .features.replace_nodes.operators import ReplaceNodeGroups

# Import Make Local
from .features.make_local.operators import MakeLocalOperator

# Import AutoSync Cherry Provider components
from .features.autosync.cherry_provider.operators import LSCHERRY_OT_toggle_autosync
from .features.autosync.cherry_provider.handlers import (
    autosync_provider_scene_update,
    autosync_provider_depsgraph_update,
)
from .features.autosync.cherry_provider.properties import toggle_autosync_provider

# Import AutoSync Global Configuration components
from .features.autosync.global_configuration.operators import (
    LSCHERRY_OT_set_autosync_tab,
)
from .features.autosync.global_configuration.handlers import (
    autosync_global_scene_update,
    autosync_global_depsgraph_update,
)
from .features.autosync.global_configuration.properties import (
    toggle_autosync_global,
    update_global_blend_mode,
    update_global_value_enhance,
    update_global_world_value_enhance,
    update_global_world_color,
)

# Import LSRegistry components
from .features.lsregistry.properties import (
    LSRegistryProperties,
    LSRegistryCredentialItem,
)
from .features.lsregistry.operators import (
    LSREGISTRY_OT_get,
    LSREGISTRY_OT_repair,
    LSREGISTRY_OT_add_credential,
    LSREGISTRY_OT_remove_credential,
)

# Import UI Panel
from .features.panels import LSPotatoPanel

rgt_classes = [
    LSCherryProperties,
    LSPotatoProperties,
    GitHubUpdaterProperties,
    LSRegistryCredentialItem,  # Add this BEFORE LSRegistryProperties
    LSRegistryProperties,  # Add this
    LSPOTATO_OT_check_updates,
    LSPOTATO_OT_install_update,
    LSPOTATO_OT_dismiss_update,
    DownloadAndLinkLSCherry,
    RepairLSCherry,
    CleanDiskLSCherry,
    LSCHERRY_OT_toggle_autosync,
    LSCHERRY_OT_set_autosync_tab,
    LSREGISTRY_OT_get,  # Add this
    LSREGISTRY_OT_repair,  # Add this
    LSREGISTRY_OT_add_credential,  # Add this
    LSREGISTRY_OT_remove_credential,  # Add this
    ReplaceNodeGroups,
    MakeLocalOperator,
    LSPotatoPanel,
]

def register():
    for cls in rgt_classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.lspotato = bpy.props.PointerProperty(type=LSPotatoProperties)
    bpy.types.Scene.lscherry = bpy.props.PointerProperty(type=LSCherryProperties)
    bpy.types.Scene.lsregistry = bpy.props.PointerProperty(type=LSRegistryProperties)

    # Add property for collapsible panel
    bpy.types.Scene.lsregistry_expanded = bpy.props.BoolProperty(
        name="LSRegistry Expanded",
        description="Expand or collapse LSRegistry section",
        default=False,  # Default collapsed
    )

    # Add autosync provider properties directly to LSCherryProperties class
    LSCherryProperties.autosync_collection_name = bpy.props.StringProperty(
        name="Collection", description="Target collection for auto sync", default="_LS"
    )

    LSCherryProperties.autosync_object_name = bpy.props.StringProperty(
        name="Sun", description="Target object for auto sync", default="MLight"
    )

    LSCherryProperties.autosync_provider_enabled = bpy.props.BoolProperty(
        name="AutoSync Provider",
        description="Enable/disable automatic LSCherryProvider synchronization",
        default=False,
        update=toggle_autosync_provider,
    )

    # Add autosync global properties
    LSCherryProperties.autosync_global_enabled = bpy.props.BoolProperty(
        name="AutoSync Global",
        description="Enable/disable automatic global settings synchronization",
        default=False,
        update=toggle_autosync_global,
    )

    LSCherryProperties.global_blend_mode = bpy.props.EnumProperty(
        name="Blend Mode",
        description="Global blend mode setting",
        items=[
            (
                BLEND_MODE["Light Sources"]["value"],
                BLEND_MODE["Light Sources"]["label"],
                BLEND_MODE["Light Sources"]["description"],
            ),
            (
                BLEND_MODE["Background"]["value"],
                BLEND_MODE["Background"]["label"],
                BLEND_MODE["Background"]["description"],
            ),
            (
                BLEND_MODE["None"]["value"],
                BLEND_MODE["None"]["label"],
                BLEND_MODE["None"]["description"],
            ),
        ],
        default="1",
        update=update_global_blend_mode,
    )

    LSCherryProperties.global_value_enhance = bpy.props.FloatProperty(
        name="Value Enhance",
        description="Global value enhance setting",
        default=0.1,
        min=0.0,
        max=1.0,
        update=update_global_value_enhance,
    )

    LSCherryProperties.global_world_value_enhance = bpy.props.FloatProperty(
        name="World Value Enhance",
        description="Global world value enhance setting",
        default=0.5,
        min=0.0,
        max=1.0,
        update=update_global_world_value_enhance,
    )

    LSCherryProperties.global_world_color = bpy.props.FloatVectorProperty(
        name="World Color",
        description="Global world color setting",
        subtype="COLOR",
        default=(1.0, 1.0, 1.0),
        min=0.0,
        max=1.0,
        update=update_global_world_color,
    )

    # Tab management property
    LSCherryProperties.autosync_active_tab = bpy.props.EnumProperty(
        name="AutoSync Tab",
        description="Active AutoSync tab",
        items=[
            ("PROVIDER", "Provider", "Cherry Provider AutoSync"),
            ("GLOBAL", "Global", "Global Configuration AutoSync"),
        ],
        default="PROVIDER",
    )

    # Internal tracking properties for provider
    LSCherryProperties.autosync_last_collection = bpy.props.StringProperty(default="")
    LSCherryProperties.autosync_last_object = bpy.props.StringProperty(default="")

    # Internal tracking properties for global
    LSCherryProperties.autosync_last_global_state = bpy.props.StringProperty(default="")

    LSPotatoProperties.github_updater = bpy.props.PointerProperty(
        type=GitHubUpdaterProperties
    )

    # Register AutoSync Provider handlers
    if autosync_provider_scene_update not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(autosync_provider_scene_update)

    if autosync_provider_depsgraph_update not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(
            autosync_provider_depsgraph_update
        )

    # Register AutoSync Global handlers
    if autosync_global_scene_update not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(autosync_global_scene_update)

    if autosync_global_depsgraph_update not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(autosync_global_depsgraph_update)


def unregister():
    # Remove AutoSync Provider handlers
    if autosync_provider_scene_update in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(autosync_provider_scene_update)

    if autosync_provider_depsgraph_update in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(
            autosync_provider_depsgraph_update
        )

    # Remove AutoSync Global handlers
    if autosync_global_scene_update in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(autosync_global_scene_update)

    if autosync_global_depsgraph_update in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(autosync_global_depsgraph_update)

    del bpy.types.Scene.lsregistry  # Add this
    del bpy.types.Scene.lsregistry_expanded  # Add this
    del bpy.types.Scene.lspotato
    del bpy.types.Scene.lscherry

    for cls in reversed(rgt_classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
