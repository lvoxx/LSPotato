import bpy  # type: ignore
import logging
import os

ADDON_ID = "LSPotato"

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
    addon = ctx.preferences.addons.get(ADDON_ID)
    return addon.preferences if addon else None


def _update_debug_mode(self, context):
    from ..utils.logger import LSPotatoLogger
    level = logging.DEBUG if self.debug_mode else logging.INFO
    LSPotatoLogger.set_console_level(level)


class LSPotatoAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = ADDON_ID

    dev_mode: bpy.props.BoolProperty(
        name="Dev Mode",
        description="Show the Node Group Compiler section in the sidebar panel",
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
    aether_gazer: bpy.props.BoolProperty(name="Aether Gazer", default=False)  # type: ignore
    genshin_impact: bpy.props.BoolProperty(name="Genshin Impact", default=False)  # type: ignore
    girls_frontline_2: bpy.props.BoolProperty(name="Girls Frontline 2", default=False)  # type: ignore
    honkai_impact_3: bpy.props.BoolProperty(name="Honkai Impact 3", default=False)  # type: ignore
    honkai_star_rail: bpy.props.BoolProperty(name="Honkai Star Rail", default=False)  # type: ignore
    punishing_gray_raven: bpy.props.BoolProperty(name="Punishing: Gray Raven", default=False)  # type: ignore
    strinova: bpy.props.BoolProperty(name="Strinova / Calabiyou", default=False)  # type: ignore
    wuthering_waves: bpy.props.BoolProperty(name="Wuthering Waves", default=False)  # type: ignore
    zenless_zone_zero: bpy.props.BoolProperty(name="Zenless Zone Zero", default=False)  # type: ignore

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
