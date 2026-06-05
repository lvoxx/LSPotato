"""
Node Group Analyzer
Reads a bpy NodeGroup and returns a plain-Python dict (NodeGroupInfo)
with all data needed for code generation.

Skips: Frame nodes (NodeFrame)
Inlines: Reroute nodes (NodeReroute) — links are resolved through them
"""

import os
import bpy  # type: ignore
from .reroute_resolver import resolve_from_socket, get_socket_index
from .node_attrs import get_serialisable_attrs

# Map Blender image file_format → file extension for saved/predefined textures.
_EXT_FOR_FORMAT: dict[str, str] = {
    'PNG':                 '.png',
    'JPEG':                '.jpg',
    'JPEG2000':            '.jp2',
    'BMP':                 '.bmp',
    'TARGA':               '.tga',
    'TARGA_RAW':           '.tga',
    'TIFF':                '.tif',
    'OPEN_EXR':            '.exr',
    'OPEN_EXR_MULTILAYER': '.exr',
    'HDR':                 '.hdr',
    'WEBP':                '.webp',
}


_SKIP_TYPES = {'FRAME'}
_REROUTE_TYPE = 'REROUTE'

# Blender 4.x+ zone / repeat pairs
_ZONE_INPUT_TYPES  = {'GeometryNodeRepeatInput', 'GeometryNodeSimulationInput'}
_ZONE_OUTPUT_TYPES = {'GeometryNodeRepeatOutput', 'GeometryNodeSimulationOutput'}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def analyze_node_group(ng: bpy.types.NodeTree) -> dict:
    """
    Return a NodeGroupInfo dict for *ng*.

    Keys
    ----
    name, type, color_tag, description,
    interface       : list of socket dicts
    nodes           : list of node dicts  (Frame & Reroute excluded)
    links           : list of link dicts  (reroutes inlined)
    zone_pairs      : list of (input_var, output_var) for Repeat/Simulation zones
    has_image_nodes : list of var_names whose nodes are TEX_IMAGE with no image
    has_uv_nodes    : list of var_names whose nodes are UVMAP with empty uv_map
    nested_groups   : list of node_tree.name strings used by GROUP nodes
    """
    info = {
        "name":            ng.name,
        "type":            ng.type,           # 'SHADER' | 'GEOMETRY' | 'COMPOSITING'
        "color_tag":       getattr(ng, 'color_tag', 'NONE'),
        "description":     getattr(ng, 'description', ''),
        "interface":       _analyze_interface(ng),
        "nodes":           [],
        "links":           [],
        "zone_pairs":      [],
        "has_image_nodes": [],          # placeholder TEX_IMAGE var_names (user input)
        "has_uv_nodes":    [],
        "nested_groups":   [],
        "placeholder_image_node_names": [],  # node.name of empty TEX_IMAGE nodes
        "_predefined_images": [],       # (filename, bpy.types.Image) for the exporter
    }

    # --- build var_name map and node list ---
    var_counter: dict[str, int] = {}
    var_map: dict[str, str] = {}   # node.name → var_name

    for node in ng.nodes:
        if node.type in _SKIP_TYPES:
            continue
        if node.type == _REROUTE_TYPE:
            # Still need var_map entries for reroutes (link resolution uses node.name)
            var_map[node.name] = _make_var(node.name, var_counter)
            continue

        var_name = _make_var(node.name, var_counter)
        var_map[node.name] = var_name

        node_info = _analyze_node(node, var_name)
        info["nodes"].append(node_info)

        if node.type == 'TEX_IMAGE':
            img = getattr(node, 'image', None)
            if img is not None:
                # Predefined texture baked into the source group: copy it out
                # and point the compiled node at the packaged file.
                filename = _image_filename(img)
                node_info["image_name"] = filename
                info["_predefined_images"].append((filename, img))
            else:
                # Empty placeholder: user supplies the image at runtime.
                info["has_image_nodes"].append(var_name)
                info["placeholder_image_node_names"].append(node.name)
        if node.type == 'UVMAP':
            info["has_uv_nodes"].append(var_name)
        if node.type == 'GROUP' and node.node_tree:
            if node.node_tree.name not in info["nested_groups"]:
                info["nested_groups"].append(node.node_tree.name)

    # --- zone pairs (Repeat / Simulation) ---
    for node in ng.nodes:
        if node.bl_idname in _ZONE_INPUT_TYPES:
            paired_out = getattr(node, 'paired_output', None)
            if paired_out and paired_out.name in var_map:
                info["zone_pairs"].append((var_map[node.name], var_map[paired_out.name]))

    # --- links (skip Frame, inline Reroute) ---
    for node in ng.nodes:
        if node.type in _SKIP_TYPES or node.type == _REROUTE_TYPE:
            continue

        to_var = var_map.get(node.name)
        if not to_var:
            continue

        for inp in node.inputs:
            from_node, from_socket = resolve_from_socket(inp)
            if from_node is None or from_node.type in _SKIP_TYPES:
                continue

            from_var = var_map.get(from_node.name)
            if not from_var:
                continue

            info["links"].append({
                "from_var":          from_var,
                "from_socket_name":  from_socket.name,
                "from_socket_index": get_socket_index(from_node.outputs, from_socket),
                "to_var":            to_var,
                "to_socket_name":    inp.name,
                "to_socket_index":   get_socket_index(node.inputs, inp),
            })

    return info


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _item_key(it):
    """
    Stable key used to link a socket/panel to its containing panel.

    NodeTreeInterfacePanel exposes no ``identifier`` (only sockets do), so the
    old identifier-based scheme keyed every panel as None and never parented
    sockets to them. ``persistent_uid`` is present on every interface item
    (panel and socket) in Blender 4.x/5.x; ``index`` is the fallback. Both
    panels and sockets are keyed the same way, so a socket's parent_id matches
    its panel's identifier.
    """
    if it is None:
        return None
    uid = getattr(it, 'persistent_uid', None)
    return uid if uid is not None else getattr(it, 'index', None)


def _analyze_interface(ng: bpy.types.NodeTree) -> list[dict]:
    """
    Walk the interface in display order, capturing BOTH panels and sockets.

    Blender 4.0+ organises group sockets into Panels (NodeTreeInterfacePanel).
    items_tree is a flat, depth-first ordered list; nesting is expressed via
    each item's .parent. We preserve order and record each item's identifier
    and parent identifier so code_gen can rebuild the panel tree and parent
    sockets correctly. Preserving order keeps socket indices aligned.
    """
    items: list[dict] = []
    for item in ng.interface.items_tree:
        item_type = getattr(item, 'item_type', None)
        parent_id = _item_key(getattr(item, 'parent', None))
        identifier = _item_key(item)

        if item_type == 'PANEL':
            items.append({
                "item_kind":      "panel",
                "name":           item.name,
                "description":    getattr(item, 'description', ''),
                "default_closed": getattr(item, 'default_closed', False),
                "identifier":     identifier,
                "parent_id":      parent_id,
            })
        elif item_type == 'SOCKET':
            s = _analyze_socket_item(item)
            s["item_kind"]  = "socket"
            s["identifier"] = identifier
            s["parent_id"]  = parent_id
            items.append(s)
    return items


def _analyze_socket_item(item) -> dict:
    return {
        "name":             item.name,
        "in_out":           item.in_out,           # 'INPUT' | 'OUTPUT'
        "socket_type":      item.socket_type,
        "description":      getattr(item, 'description', ''),
        "default_value":    _safe_default(item),
        "min_value":        _getf(item, 'min_value'),
        "max_value":        _getf(item, 'max_value'),
        "subtype":          getattr(item, 'subtype', 'NONE'),
        "hide_value":       getattr(item, 'hide_value', False),
        "hide_in_modifier": getattr(item, 'hide_in_modifier', False),
        "dimensions":       getattr(item, 'dimensions', None),
    }


def _analyze_node(node, var_name: str) -> dict:
    attrs        = get_serialisable_attrs(node)
    enum_items   = _get_enum_items(node)
    idx_sw_count = _get_index_switch_count(node)
    # active_index addresses a dynamic item list and only holds once the items
    # exist, so pull it out of the generic attribute pass — code_gen re-applies
    # it *after* rebuilding the items (otherwise Blender clamps it to 0).
    active_index = None
    if enum_items or idx_sw_count is not None:
        active_index = attrs.pop('active_index', None)
    return {
        "var_name":            var_name,
        "name":                node.name,
        "type":                node.type,
        "bl_idname":           node.bl_idname,
        "location":            (round(node.location.x, 2), round(node.location.y, 2)),
        "width":               round(node.width, 2),
        "label":               node.label or '',
        "hide":                node.hide,
        "attributes":          attrs,
        "input_defaults":      _get_input_defaults(node),
        "output_defaults":     _get_output_defaults(node),
        # Socket name rosters let code_gen pick name-vs-index per link endpoint
        # (a name that repeats on one side cannot disambiguate the socket).
        "input_socket_names":  [s.name for s in node.inputs],
        "output_socket_names": [s.name for s in node.outputs],
        "node_tree_name":      node.node_tree.name if node.type == 'GROUP' and node.node_tree else None,
        # Zone-specific
        "repeat_items":        _get_repeat_items(node),
        # Internal datablocks get_serialisable_attrs cannot reach (POINTER props)
        "color_ramp":          _get_color_ramp(node),
        "curve_mapping":       _get_curve_mapping(node),
        # Dynamic socket lists (Menu / Index Switch) + deferred selector
        "enum_items":          enum_items,
        "index_switch_count":  idx_sw_count,
        "active_index":        active_index,
    }


def _get_input_defaults(node) -> dict:
    defaults = {}
    for i, inp in enumerate(node.inputs):
        if inp.is_linked:
            continue
        try:
            v = inp.default_value
            defaults[i] = _serialise(v)
        except Exception:
            pass
    return defaults


def _get_repeat_items(node) -> list[dict]:
    """Extract RepeatOutput repeat_items for GeometryNodeRepeatOutput."""
    items = []
    ri = getattr(node, 'repeat_items', None)
    if ri is None:
        return items
    for item in ri:
        items.append({"socket_type": item.socket_type, "name": item.name})
    return items


# Nodes whose value lives in an OUTPUT socket (constant / field-input nodes)
# rather than an input — _get_input_defaults never sees them.
_OUTPUT_DEFAULT_NODES = frozenset({
    'ShaderNodeValue', 'ShaderNodeRGB',
    'CompositorNodeValue', 'CompositorNodeRGB',
    'FunctionNodeInputBool', 'FunctionNodeInputInt', 'FunctionNodeInputString',
    'FunctionNodeInputColor', 'FunctionNodeInputVector',
})


def _get_output_defaults(node) -> dict:
    """Capture output-socket defaults for constant/input nodes (Value, RGB, …)."""
    if node.bl_idname not in _OUTPUT_DEFAULT_NODES:
        return {}
    defaults = {}
    for i, out in enumerate(node.outputs):
        try:
            defaults[i] = _serialise(out.default_value)
        except Exception:
            pass
    return defaults


def _get_color_ramp(node) -> dict | None:
    """Serialise a ColorRamp datablock (ShaderNodeValToRGB and friends)."""
    cr = getattr(node, 'color_ramp', None)
    if cr is None or not hasattr(cr, 'elements'):
        return None
    return {
        "color_mode":        getattr(cr, 'color_mode', 'RGB'),
        "interpolation":     getattr(cr, 'interpolation', 'LINEAR'),
        "hue_interpolation": getattr(cr, 'hue_interpolation', 'NEAR'),
        "elements": [
            {"position": e.position, "color": _serialise(e.color)}
            for e in cr.elements
        ],
    }


def _get_curve_mapping(node) -> dict | None:
    """Serialise a CurveMapping datablock (RGB / Vector / Float curve nodes)."""
    m = getattr(node, 'mapping', None)
    if m is None or not hasattr(m, 'curves'):
        return None
    curves = [
        [
            {"location": _serialise(p.location),
             "handle_type": getattr(p, 'handle_type', 'AUTO')}
            for p in c.points
        ]
        for c in m.curves
    ]
    return {
        "use_clip":    getattr(m, 'use_clip', False),
        "clip_min_x":  _getf(m, 'clip_min_x'),
        "clip_min_y":  _getf(m, 'clip_min_y'),
        "clip_max_x":  _getf(m, 'clip_max_x'),
        "clip_max_y":  _getf(m, 'clip_max_y'),
        "extend":      getattr(m, 'extend', None),
        "black_level": _safe_attr_tuple(m, 'black_level'),
        "white_level": _safe_attr_tuple(m, 'white_level'),
        "curves":      curves,
    }


def _safe_attr_tuple(obj, attr):
    """Serialise a vector/color attribute to a tuple, or None if absent."""
    if not hasattr(obj, attr):
        return None
    try:
        return _serialise(getattr(obj, attr))
    except Exception:
        return None


def _get_enum_items(node) -> list[dict]:
    """Capture NodeMenuSwitch enum item definitions (GeometryNodeMenuSwitch)."""
    ed = getattr(node, 'enum_definition', None)
    items = getattr(ed, 'enum_items', None) if ed is not None else None
    if items is None:
        return []
    return [
        {"name": it.name, "description": getattr(it, 'description', '')}
        for it in items
    ]


def _get_index_switch_count(node) -> int | None:
    """Item count on a GeometryNodeIndexSwitch (None when not that node)."""
    items = getattr(node, 'index_switch_items', None)
    if items is None:
        return None
    try:
        return len(items)
    except Exception:
        return None


def _safe_default(item):
    try:
        return _serialise(item.default_value)
    except Exception:
        return None


def _serialise(v):
    # Explicit mathutils guard: Euler/Quaternion only expose __getitem__, not
    # __iter__, so the generic __iter__ check below would miss them.
    _tname = type(v).__name__
    if _tname in ('Euler', 'Vector', 'Color', 'Quaternion'):
        try:
            return tuple(v)
        except Exception:
            pass
    if _tname == 'Matrix':
        try:
            return tuple(tuple(row) for row in v)
        except Exception:
            pass
    if hasattr(v, 'to_tuple'):
        return tuple(v)
    if hasattr(v, '__iter__') and not isinstance(v, str):
        try:
            return tuple(v)
        except Exception:
            pass
    return v


def _getf(obj, attr):
    val = getattr(obj, attr, None)
    if val is None:
        return None
    # Clamp huge floats so repr stays readable
    try:
        if abs(val) > 3.0e38:
            return 3.4028234663852886e+38 * (1 if val > 0 else -1)
    except Exception:
        pass
    return val


def _image_filename(img) -> str:
    """
    Deterministic, filesystem-safe filename for a predefined/packed image.

    Prefers the basename of the image's filepath, falls back to the datablock
    name; the extension is forced to match the image's file_format so the
    saved file round-trips. Used both to name the file the exporter writes and
    the string the compiled node passes to load_packaged_image().
    """
    raw = bpy.path.basename(getattr(img, 'filepath_raw', '') or '') or img.name
    stem = os.path.splitext(raw)[0]
    stem = ''.join(c if (c.isalnum() or c in '-_.') else '_' for c in stem)
    stem = stem.strip('_. ') or 'image'
    ext = _EXT_FOR_FORMAT.get(getattr(img, 'file_format', 'PNG'), '.png')
    return f"{stem}{ext}"


def _make_var(node_name: str, counter: dict) -> str:
    """Sanitize node name into a valid Python identifier, deduplicating."""
    base = ''.join(c if c.isalnum() else '_' for c in node_name).strip('_')
    if not base:
        base = 'Node'
    # strip trailing _NNN duplicates Blender appends (e.g. "Math.001" → "Math")
    # but keep them since they are already unique in the original name
    key = base
    count = counter.get(key, 0)
    counter[key] = count + 1
    return base if count == 0 else f"{base}_{count}"
