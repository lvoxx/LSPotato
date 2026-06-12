# LSPotato - a collection of utility tools for the LSCherry toon-shader project
# Copyright (C) 2025  Lvoxx
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


# Extension metadata now lives in blender_manifest.toml (Blender 4.2+ extension
# format) — the legacy `bl_info` dict has been removed. Third-party deps (PyYAML)
# ship as wheels declared in the manifest, so the old sys.path vendor shim is gone.

import bpy  # type: ignore

from .utils.logger import get_logger


logger = get_logger("LSPotato")

from .constants.blend_mode import BLEND_MODE

# Import LSCherry Properties
from .features.lscherry_props import LSCherryProperties

# Import Node Compiler
from .features.node_compiler.properties import NodeCompilerProperties
from .features.node_compiler.operators import LSPOTATO_OT_compile_node_groups

# Import Node Library
from .nodes.node_info import ng_register, ng_unregister, register_restore_handler, unregister_restore_handler
from .nodes.node_impl import NodeLib
from .nodes.node import register_node_class, clear_node_registry
from .nodes.geometry.loader import register_geometry_handler, unregister_geometry_handler
from .nodes.refresh import register_reconcile_handler, unregister_reconcile_handler

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

# Import UI Panel
from .features.panels import LSPotatoPanel

# Import Addon Preferences
from .features.addon_preferences import (
    LSPotatoAddonPreferences,
    filter_enabled_node_classes,
)

rgt_classes = [
    LSPotatoAddonPreferences,
    LSCherryProperties,
    LSCHERRY_OT_toggle_autosync,
    LSCHERRY_OT_set_autosync_tab,
    NodeCompilerProperties,
    LSPOTATO_OT_compile_node_groups,
    LSPotatoPanel,
]


def _register_node_library():
    """Register the enabled compiled node classes and the Add Shader menu.

    Starter-pack nodes are gated by the addon preferences — only packs the user
    enabled are registered and surfaced in the menu.
    """
    enabled_classes = filter_enabled_node_classes(NodeLib.get_node_classes())
    for cls in enabled_classes:
        # Record every class by stable key so nested groups resolve even if the
        # Blender registration below fails for this class.
        register_node_class(cls)
        try:
            bpy.utils.register_class(cls)
        except Exception as e:
            logger.error(f"Cannot register compiled node '{cls.__name__}': {e}")

    # Register the Add Shader → LSCherry/... menu for the enabled classes only.
    ng_register(enabled_classes)


def _unregister_node_library():
    """Tear down the Add Shader menu and every compiled node class.

    Iterates the *full* class set (not the enabled subset) so classes registered
    under a previous preference selection are always cleaned up.
    """
    ng_unregister()

    for cls in reversed(NodeLib.get_node_classes()):
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass

    clear_node_registry()


def refresh_node_library():
    """Re-register the node library so a starter-pack preference change takes
    effect without a Blender restart. Called from the preferences update hook."""
    _unregister_node_library()
    _register_node_library()


def _is_dev_mode():
    """True when the addon-preferences Dev Mode toggle is on.

    Dev Mode suppresses the load-time node handlers (shader restore/reconcile and
    geometry verify) so a developer editing/compiling the source .blend isn't
    fighting the addon rewriting their shader trees or appending the geometry
    library. Defaults to False when preferences can't be read."""
    try:
        addon = bpy.context.preferences.addons.get(__package__)
        return bool(addon and addon.preferences.dev_mode)
    except Exception:
        return False


def register():
    for cls in rgt_classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.lscherry = bpy.props.PointerProperty(type=LSCherryProperties)

    bpy.types.Scene.lspotato_compiler = bpy.props.PointerProperty(
        type=NodeCompilerProperties
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

    #-------------------------------------------------------------------
    # Register node classes + the Add Shader → LSCherry/... menu
    # (starter packs are gated by preferences inside this helper)
    _register_node_library()

    # Dev Mode (addon preferences) suppresses every load-time node mutation so a
    # developer compiling/editing the source .blend isn't fighting the addon
    # rewriting their shader trees or appending the geometry library. The Add
    # Shader menu + node classes above still register, so the library stays usable.
    if _is_dev_mode():
        logger.info(
            "Dev Mode enabled — skipping shader node init and geometry verify handlers."
        )
    else:
        # Handler that restores NodeUndefined entries when loading a file
        register_restore_handler()

        # Handler that refreshes stale shader node trees (saved by an older addon
        # version) to the current definition whenever a file is opened. Runs after
        # the restore handler so freshly-restored nodes are reconciled too.
        register_reconcile_handler()

        # Handler that appends the geometry node library whenever a file is opened
        register_geometry_handler()

    # Re-apply debug mode preference so the console handler level is correct
    # after a reload (the logger singleton resets to INFO on each startup).
    try:
        import logging
        addon = bpy.context.preferences.addons.get(__package__)
        if addon and addon.preferences.debug_mode:
            from .utils.logger import LSPotatoLogger
            LSPotatoLogger.set_console_level(logging.DEBUG)
    except Exception:
        pass


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

    del bpy.types.Scene.lspotato_compiler
    del bpy.types.Scene.lscherry

    for cls in reversed(rgt_classes):
        bpy.utils.unregister_class(cls)

    #-------------------------------------------------------------------
    # Unregister nodes
    unregister_geometry_handler()
    unregister_reconcile_handler()
    unregister_restore_handler()
    _unregister_node_library()

if __name__ == "__main__":
    register()
