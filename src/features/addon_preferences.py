import bpy  # type: ignore
import logging
import os

# The add-on's top-level package name (e.g. "bl_ext.<repo>.LSPotato"). As a
# sub-module we must import the *parent* package's __package__ so the value is
# the add-on root, not this sub-package — see the Blender extension docs:
# https://docs.blender.org/manual/en/dev/advanced/extensions/addons.html
from .. import __package__ as base_package

STARTER_PACKS = [
    ("aether_gazer",         "Aether Gazer",          "aether-gazer"),
    ("genshin_impact",       "Genshin Impact",        "genshin-impact"),
    ("girls_frontline_2",    "Girls Frontline 2",     "girls-frontline-2"),
    ("honkai_impact_3",      "Honkai Impact 3",       "honkai-impact-3"),
    ("honkai_star_rail",     "Honkai Star Rail",      "honkai-star-rail"),
    ("punishing_gray_raven", "Punishing: Gray Raven", "punishing-gray-raven"),
    ("strinova",             "Strinova / Calabiyou",  "strinova"),
    ("wuthering_waves",      "Wuthering Waves",       "wuthering-waves"),
    ("zenless_zone_zero",    "Zenless Zone Zero",     "zenless-zone-zero"),
]

# Resolved once at import time; stays valid for the lifetime of the addon session.
_STARTERS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "nodes", "shader", "lscherry", "starters",
)


def _is_starter_supported(folder_name: str) -> bool:
    return os.path.isdir(os.path.join(_STARTERS_DIR, folder_name))


def get_addon_prefs(context=None):
    ctx = context or bpy.context
    addon = ctx.preferences.addons.get(base_package)
    return addon.preferences if addon else None


# ── Starter-pack gating ──────────────────────────────────────────────────────
# Starter node bl_labels are namespaced as "lscherry.starters.<pack>.<NodeName>".
# Only packs the user explicitly enabled in preferences should be registered or
# surfaced in the Add Shader menu — the scan in NodeLib returns *all* of them.
_STARTER_LABEL_PREFIX = "lscherry.starters."


def _starter_pack_id(bl_label):
    """Return the starter-pack id encoded in a node's bl_label, or None.

    e.g. 'lscherry.starters.strinova.Face' -> 'strinova'.
    Non-starter labels return None (they are never gated).
    """
    if not bl_label:
        return None
    low = bl_label.lower()
    if not low.startswith(_STARTER_LABEL_PREFIX):
        return None
    return low[len(_STARTER_LABEL_PREFIX):].split(".", 1)[0].strip() or None


def filter_enabled_node_classes(node_classes, context=None):
    """Drop starter-pack node classes whose pack is not enabled in preferences.

    Non-starter classes are always kept. If preferences are unavailable, every
    starter pack is treated as disabled (matches each property's default=False).
    """
    prefs = get_addon_prefs(context)
    kept = []
    for cls in node_classes:
        pack = _starter_pack_id(getattr(cls, "bl_label", ""))
        if pack is None:
            kept.append(cls)
        elif prefs is not None and getattr(prefs, pack, False):
            kept.append(cls)
    return kept


def _on_starter_toggle(self, context):
    """Re-register the node library so the Add Shader menu reflects the new
    starter-pack selection without requiring a Blender restart."""
    try:
        from .. import refresh_node_library
        refresh_node_library()
    except Exception as e:  # defensive — never let a UI toggle raise
        logging.getLogger("LSPotato.AddonPrefs").error(
            "Failed to refresh node library after starter toggle: %s", e
        )


def _update_debug_mode(self, context):
    from ..utils.logger import LSPotatoLogger
    level = logging.DEBUG if self.debug_mode else logging.INFO
    LSPotatoLogger.set_console_level(level)


class LSPotatoAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = base_package

    dev_mode: bpy.props.BoolProperty(
        name="Dev Mode",
        description=(
            "Show the Node Group Compiler in the sidebar panel and stop the addon "
            "from touching the open file on load — no shader-node init/reconcile and "
            "no geometry-node verify. Requires a Blender restart to take effect"
        ),
        default=False,
    )  # type: ignore

    debug_mode: bpy.props.BoolProperty(
        name="Debug Mode",
        description="Print DEBUG-level messages to the Blender console (default is INFO only)",
        default=False,
        update=_update_debug_mode,
    )  # type: ignore

    starter_packs_expanded: bpy.props.BoolProperty(
        name="Starter Packs",
        description="Expand or collapse the Starter Packs section",
        default=False,
    )  # type: ignore

    # ── Starter pack selections ──────────────────────────────────────────────
    # Each toggle re-registers the node library so the Add Shader menu updates
    # live, without a Blender restart.
    aether_gazer: bpy.props.BoolProperty(name="Aether Gazer", default=False, update=_on_starter_toggle)  # type: ignore
    genshin_impact: bpy.props.BoolProperty(name="Genshin Impact", default=False, update=_on_starter_toggle)  # type: ignore
    girls_frontline_2: bpy.props.BoolProperty(name="Girls Frontline 2", default=False, update=_on_starter_toggle)  # type: ignore
    honkai_impact_3: bpy.props.BoolProperty(name="Honkai Impact 3", default=False, update=_on_starter_toggle)  # type: ignore
    honkai_star_rail: bpy.props.BoolProperty(name="Honkai Star Rail", default=False, update=_on_starter_toggle)  # type: ignore
    punishing_gray_raven: bpy.props.BoolProperty(name="Punishing: Gray Raven", default=False, update=_on_starter_toggle)  # type: ignore
    strinova: bpy.props.BoolProperty(name="Strinova / Calabiyou", default=False, update=_on_starter_toggle)  # type: ignore
    wuthering_waves: bpy.props.BoolProperty(name="Wuthering Waves", default=False, update=_on_starter_toggle)  # type: ignore
    zenless_zone_zero: bpy.props.BoolProperty(name="Zenless Zone Zero", default=False, update=_on_starter_toggle)  # type: ignore

    def draw(self, context):
        layout = self.layout

        # ── Top row: Dev Mode / Debug Mode ───────────────────────────────────
        row = layout.row()
        row.prop(self, "dev_mode")
        row.prop(self, "debug_mode")

        layout.separator()

        # ── Starter Packs (collapsible) ──────────────────────────────────────
        header = layout.row()
        header.prop(
            self, "starter_packs_expanded",
            icon="TRIA_DOWN" if self.starter_packs_expanded else "TRIA_RIGHT",
            icon_only=True,
            emboss=False,
        )
        header.label(text="Starter Packs")

        if self.starter_packs_expanded:
            box = layout.box()
            for prop_name, label, folder_name in STARTER_PACKS:
                supported = _is_starter_supported(folder_name)
                row = box.row()
                if supported:
                    row.prop(self, prop_name, text=label)
                else:
                    row.enabled = False
                    split = row.split(factor=0.45)
                    split.prop(self, prop_name, text=label)
                    split.label(text="Not yet supported — coming in future updates", icon="INFO")
