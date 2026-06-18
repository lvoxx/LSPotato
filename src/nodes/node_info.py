import bpy  # type: ignore
from bpy.app.handlers import persistent # type: ignore
from ..utils.logger import get_logger
from .node_impl import NodeLib
from .node import get_node_class_by_idname


logger = get_logger("NodeInfo")


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
    # ── External ──────────────────────────────────────────────────
    ("lscherry.external.michos.honkai_impact_3.",  "LSCherry/External/Michos/Honkai Impact 3"),
    ("lscherry.external.michos.genshin_impact.",   "LSCherry/External/Michos/Genshin Impact"),
    ("lscherry.external.michos.honkai_star_rail.", "LSCherry/External/Michos/Honkai Star Rail"),
    ("lscherry.external.michos.",                  "LSCherry/External/Michos"),
    ("lscherry.external.festivities.Gi_Enviroment.",     "LSCherry/External/Festivities/GI Enviroment"),
    ("lscherry.external.festivities.",     "LSCherry/External/Festivities"),
    ("lscherry.external.GloTAni.",         "LSCherry/External/GloTAni"),
    ("lscherry.external.AVR.",             "LSCherry/External/AVR"),
    ("lscherry.external.XTR.",             "LSCherry/External/XTR"),
    ("lscherry.external.MMD.",             "LSCherry/External/MMD"),
    ("lscherry.external.MICA.GF2.",            "LSCherry/External/MICA/GF2"),
    ("lscherry.external.MICA.",            "LSCherry/External/MICA"),
    ("lscherry.external.",                         "LSCherry/External"),

    # ── Utils subgroups ────────────────────────────────────────────────────
    ("lscherry.utils.bnodes.",     "LSCherry/Utils/BNodes"),
    ("lscherry.utils.procedural.", "LSCherry/Utils/Procedural"),
    ("lscherry.utils.ramp_style.", "LSCherry/Utils/Ramp Style"),
    ("lscherry.utils.separator.",  "LSCherry/Utils/Separator"),
    ("lscherry.utils.normal.",     "LSCherry/Utils/Normal"),
    ("lscherry.utils.",            "LSCherry/Utils"),
    
    # ── Starter Packs ──────────────────────────────────────────────────────
    ("lscherry.starters.strinova.",         "LSCherry/Starters/Strinova"),
    ("lscherry.starters.wutherings_waves.",         "LSCherry/Starters/Wutherings Waves"),
    ("lscherry.starters.world_builder.",         "LSCherry/Starters/World Builder"),
    ("lscherry.starters.",         "LSCherry/Starters"),

    # ── Standalone categories ──────────────────────────────────────────────
    ("lscherry.combiner.",        "LSCherry/Combiner"),
    ("lscherry.core.",            "LSCherry/Core"),
    ("lscherry.post_production.", "LSCherry/Post Production"),
    ("lscherry.general.",         "LSCherry/General"),
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
# Add operator
#
# Stock `node.add_node` builds a compiled node's tree DURING the node's init(),
# inside the operator — which leaves deeply-nested sub-groups unresolved
# ("Missing Data Block") on the very first add of a session. This thin wrapper
# builds the whole tree up front (the same path a working "second add" takes),
# then delegates to the stock operator so drag-to-place behaviour is preserved.
# ---------------------------------------------------------------------------

class LSPOTATO_OT_add_lscherry_node(bpy.types.Operator):
    """Add an LSCherry node, pre-building its node tree first"""

    bl_idname  = "lspotato.add_lscherry_node"
    bl_label   = "Add LSCherry Node"
    bl_options = {"REGISTER", "UNDO"}

    node_idname: bpy.props.StringProperty()  # type: ignore

    @classmethod
    def poll(cls, context):
        sd = getattr(context, "space_data", None)
        return sd is not None and getattr(sd, "edit_tree", None) is not None

    def invoke(self, context, event):
        cls = get_node_class_by_idname(self.node_idname)
        if cls is not None:
            try:
                # Build the whole tree (and every nested child) detached, before
                # init() runs, so init() hits the "tree already exists" fast path.
                cls.create_node_group()
            except Exception as e:
                logger.error(f"add_lscherry_node: pre-build failed for '{self.node_idname}': {e}")
        # Delegate to the stock add so the node follows the cursor as usual.
        return bpy.ops.node.add_node(
            "INVOKE_DEFAULT", type=self.node_idname, use_transform=True
        )


# ---------------------------------------------------------------------------
# Menu classes
# ---------------------------------------------------------------------------
_registered_menu_classes: list = []


def _build_menu_classes(node_classes: list) -> list:
    from collections import defaultdict

    # ── Pass 0: group nodes by their exact category path ─────────────────
    groups: dict[str, list] = defaultdict(list)
    for cls in node_classes:
        cat  = _get_category(cls.bl_label)
        name = _display_name(cls.bl_label)
        groups[cat].append((cls.bl_idname, name))

    # ── Pass 1: collect every path that needs a menu (leaves + ancestors) ─
    all_paths: set[str] = set()
    for cat in groups:
        parts = cat.split("/")
        for i in range(1, len(parts) + 1):
            all_paths.add("/".join(parts[:i]))

    # Assign stable menu IDs (root keeps the pre-defined _ROOT_MENU_ID)
    cat_to_menu_id: dict[str, str] = {}
    for path in sorted(all_paths):
        if path == _ROOT_MENU_LABEL:
            cat_to_menu_id[path] = _ROOT_MENU_ID
        else:
            safe = "LSPOTATO_MT_" + path.upper().replace("/", "_").replace(" ", "_")
            cat_to_menu_id[path] = safe

    # ── Pass 2: build parent → direct-children map ────────────────────────
    children_map: dict[str, list[str]] = defaultdict(list)
    for path in sorted(all_paths):
        parts = path.split("/")
        if len(parts) > 1:
            children_map["/".join(parts[:-1])].append(path)

    # ── Pass 3: create a menu class per path ─────────────────────────────
    # All IDs are known, so closures capture final values at build time.
    def make_draw(nodes, child_items):
        """child_items: [(menu_id, label), ...] for direct children."""
        def draw(self, context):
            layout = self.layout
            for child_id, child_label in child_items:
                layout.menu(child_id, text=child_label)
            if child_items and nodes:
                layout.separator()
            for bl_idname, display in nodes:
                # Route through our Add operator so the whole node tree (and its
                # nested groups) is built BEFORE Blender's init() runs — this is
                # the path that avoids the first-add "Missing Data Block" desync.
                op = layout.operator("lspotato.add_lscherry_node", text=display)
                op.node_idname = bl_idname
        return draw

    menu_classes: list = []
    for path in sorted(all_paths):
        safe_id     = cat_to_menu_id[path]
        label       = path.split("/")[-1]
        direct      = groups.get(path, [])
        child_items = [
            (cat_to_menu_id[c], c.split("/")[-1])
            for c in sorted(children_map.get(path, []))
        ]
        cls = type(safe_id, (bpy.types.Menu,), {
            "bl_label":  label,
            "bl_idname": safe_id,
            "draw":      make_draw(direct, child_items),
        })
        menu_classes.append(cls)

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

    try:
        bpy.utils.register_class(LSPOTATO_OT_add_lscherry_node)
    except Exception as e:
        logger.error(f"node_info: cannot register add operator: {e}")

    _registered_menu_classes = _build_menu_classes(node_classes)
    for cls in _registered_menu_classes:
        try:
            bpy.utils.register_class(cls)
        except Exception as e:
            logger.error(f"node_info: cannot register menu '{cls.__name__}': {e}")

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

    try:
        bpy.utils.unregister_class(LSPOTATO_OT_add_lscherry_node)
    except Exception:
        pass


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
            logger.error(f"restore_undefined_nodes: '{node.name}': {e}")


def register_restore_handler():
    if restore_undefined_nodes not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(restore_undefined_nodes)


def unregister_restore_handler():
    if restore_undefined_nodes in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(restore_undefined_nodes)
