import bpy  # type: ignore
from bpy.app.handlers import persistent
from .node_impl import NodeLib


# ---------------------------------------------------------------------------
# Category map — maps bl_label prefix → menu path inside Add Shader
#
# Naming convention for shader node bl_label:
#   "<folder_path>.<NodeName>"
# Example:
#   bl_label = "lscherry.PBR"                    → LSCherry  (root)
#   bl_label = "lscherry.combiner.Combiner"      → LSCherry/Combiner
#   bl_label = "lscherry.core.NormalBlend"       → LSCherry/Core
#   bl_label = "lscherry.external.michos.honkai_impact_3.SomeNode"
#                                              → LSCherry/External/Michos/Honkai Impact 3
#   bl_label = "lscherry.utils.bnodes.NodeName"  → LSCherry/Utils/BNodes
#   bl_label = "lscherry.plugin.Pattern"         → LSCherry/Plugin
#   bl_label = "lscherry.vfx.Something"          → LSCherry/VFX
#
# Order: MOST SPECIFIC → MOST GENERIC (match the first prefix found)
# ---------------------------------------------------------------------------
_CATEGORY_MAP: list[tuple[str, str]] = [
    # ── External / Michos ──────────────────────────────────────────────────
    ("lscherry.external.michos.honkai_impact_3.",  "LSCherry/External/Michos/Honkai Impact 3"),
    ("lscherry.external.michos.genshin_impact.",   "LSCherry/External/Michos/Genshin Impact"),
    ("lscherry.external.michos.honkai_star_rail.", "LSCherry/External/Michos/Honkai Star Rail"),
    ("lscherry.external.michos.",                  "LSCherry/External/Michos"),
    ("lscherry.external.",                         "LSCherry/External"),

    # ── Utils subgroups ────────────────────────────────────────────────────
    ("lscherry.utils.bnodes.",     "LSCherry/Utils/BNodes"),
    ("lscherry.utils.procedural.", "LSCherry/Utils/Procedural"),
    ("lscherry.utils.ramp_style.", "LSCherry/Utils/Ramp Style"),
    ("lscherry.utils.separator.",  "LSCherry/Utils/Separator"),
    ("lscherry.utils.normal.",     "LSCherry/Utils/Normal"),
    ("lscherry.utils.",            "LSCherry/Utils"),

    # ── Standalone categories ──────────────────────────────────────────────
    ("lscherry.combiner.",        "LSCherry/Combiner"),
    ("lscherry.core.",            "LSCherry/Core"),
    ("lscherry.festivities.",     "LSCherry/Festivities"),
    ("lscherry.glotani.",         "LSCherry/GloTAni"),
    ("lscherry.avr.",             "LSCherry/AVR"),
    ("lscherry.xtr.",             "LSCherry/XTR"),
    ("lscherry.mmd.",             "LSCherry/MMD"),
    ("lscherry.mica.",            "LSCherry/MICA"),
    ("lscherry.post_production.", "LSCherry/Post Production"),
    ("lscherry.global.",          "LSCherry/Global"),
    ("lscherry.dev.",             "LSCherry/Dev"),
    ("lscherry.plugin.",          "LSCherry/Plugin"),
    ("lscherry.vfx.",             "LSCherry/VFX"),

    # ── Root LSCherry (fallback) ───────────────────────────────────────────
    ("lscherry.",                 "LSCherry"),
]

_ROOT_MENU_LABEL = "LSCherry"
_ROOT_MENU_ID    = "LSPOTATO_MT_LSCHERRY_ROOT"


def _get_category(bl_label: str) -> str:
    lower = bl_label.lower()
    for prefix, category in _CATEGORY_MAP:
        if lower.startswith(prefix):
            return category
    return _ROOT_MENU_LABEL


def _display_name(bl_label: str) -> str:
    """Returns the trailing segment of the label for display in the menu, stripping the path prefix."""
    parts = bl_label.split(".")
    return parts[-1].strip() if parts else bl_label


# ---------------------------------------------------------------------------
# Menu classes
# ---------------------------------------------------------------------------
_registered_menu_classes: list = []


def _build_menu_classes(node_classes: list) -> list:
    from collections import defaultdict, OrderedDict

    # Group: full_category_path → [(bl_idname, display_name)]
    groups: dict[str, list] = defaultdict(list)
    for cls in node_classes:
        cat  = _get_category(cls.bl_label)
        name = _display_name(cls.bl_label)
        groups[cat].append((cls.bl_idname, name))

    menu_classes: list = []
    # map: category path → menu bl_idname  (used when building parent menus)
    cat_to_menu_id: dict[str, str] = {}

    # Create a menu class for each category
    for category, nodes in groups.items():
        safe_id  = "LSPOTATO_MT_" + category.upper().replace("/", "_").replace(" ", "_")
        label    = category.split("/")[-1]
        nodes_ss = list(nodes)

        def make_draw(node_list):
            def draw(self, context):
                layout = self.layout
                for bl_idname, display in node_list:
                    op = layout.operator("node.add_node", text=display)
                    op.type          = bl_idname
                    op.use_transform = True
            return draw

        cls = type(safe_id, (bpy.types.Menu,), {
            "bl_label":   label,
            "bl_idname":  safe_id,
            "draw":       make_draw(nodes_ss),
        })
        menu_classes.append(cls)
        cat_to_menu_id[category] = safe_id

    # ── Root "LSCherry" menu ─────────────────────────────────────────────
    # Collect all top-level categories (direct children of LSCherry)
    top_level_cats: list[str] = sorted({
        c.split("/")[1] if "/" in c else c
        for c in groups.keys()
        if c != _ROOT_MENU_LABEL
    })

    # Nodes placed directly at the root (category == "LSCherry")
    root_nodes = groups.get(_ROOT_MENU_LABEL, [])

    def draw_root(self, context):
        layout = self.layout
        # Submenu for each child category
        for top in top_level_cats:
            full_path = f"LSCherry/{top}"
            sub_id    = cat_to_menu_id.get(full_path)
            if sub_id:
                layout.menu(sub_id, text=top)
        # Nodes directly at the root
        if top_level_cats and root_nodes:
            layout.separator()
        for bl_idname, display in root_nodes:
            op = layout.operator("node.add_node", text=display)
            op.type          = bl_idname
            op.use_transform = True

    root_cls = type(_ROOT_MENU_ID, (bpy.types.Menu,), {
        "bl_label":  _ROOT_MENU_LABEL,
        "bl_idname": _ROOT_MENU_ID,
        "draw":      draw_root,
    })
    menu_classes.append(root_cls)

    return menu_classes


def _add_to_shader_add_menu(self, context):
    """Appends to NODE_MT_add → surfaces the 'LSCherry' entry."""
    if getattr(context.space_data, "tree_type", None) != "ShaderNodeTree":
        return
    self.layout.menu(_ROOT_MENU_ID, text=_ROOT_MENU_LABEL)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def ng_register(node_classes: list):
    """Registers every menu. Call after registering the node classes."""
    global _registered_menu_classes

    _registered_menu_classes = _build_menu_classes(node_classes)
    for cls in _registered_menu_classes:
        try:
            bpy.utils.register_class(cls)
        except Exception as e:
            print(f"[LSPotato] node_info: cannot register menu '{cls.__name__}': {e}")

    bpy.types.NODE_MT_add.append(_add_to_shader_add_menu)


def ng_unregister():
    """Unregisters every menu. Call before unregistering the node classes."""
    global _registered_menu_classes

    bpy.types.NODE_MT_add.remove(_add_to_shader_add_menu)

    for cls in reversed(_registered_menu_classes):
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass
    _registered_menu_classes = []


# ---------------------------------------------------------------------------
# Handler: restore NodeUndefined → shader node when loading a file
# ---------------------------------------------------------------------------

@persistent
def restore_undefined_nodes(dummy=None):
    known = {cls.bl_idname for cls in NodeLib.get_node_classes()}
    if not known:
        return
    for mat in bpy.data.materials:
        if mat.use_nodes and mat.node_tree:
            _restore_in_tree(mat.node_tree, known)
    for ng in bpy.data.node_groups:
        _restore_in_tree(ng, known)


def _restore_in_tree(tree, known_idnames: set):
    for node in list(tree.nodes):
        if node.bl_idname != "NodeUndefined":
            continue
        original = getattr(node, "type", None)
        if original not in known_idnames:
            continue
        try:
            new = tree.nodes.new(original)
            new.location = node.location
            new.label    = node.label
            for si, di in zip(node.inputs, new.inputs):
                try:
                    if not si.is_linked:
                        di.default_value = si.default_value
                except Exception:
                    pass
                if si.is_linked and si.links:
                    tree.links.new(si.links[0].from_socket, di)
            for so, do in zip(node.outputs, new.outputs):
                for lnk in list(so.links):
                    tree.links.new(do, lnk.to_socket)
            saved = node.name
            tree.nodes.remove(node)
            new.name = saved
        except Exception as e:
            print(f"[LSPotato] restore_undefined_nodes: '{node.name}': {e}")


def register_restore_handler():
    if restore_undefined_nodes not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(restore_undefined_nodes)


def unregister_restore_handler():
    if restore_undefined_nodes in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(restore_undefined_nodes)
