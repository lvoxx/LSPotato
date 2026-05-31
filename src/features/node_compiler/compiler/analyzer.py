"""
Node Group Analyzer
Reads a bpy NodeGroup and returns a plain-Python dict (NodeGroupInfo)
with all data needed for code generation.

Skips: Frame nodes (NodeFrame)
Inlines: Reroute nodes (NodeReroute) — links are resolved through them
"""

import bpy  # type: ignore
from .reroute_resolver import resolve_from_socket, get_socket_index

# ---------------------------------------------------------------------------
# Attribute lists per node type — only serialisable, code-relevant attrs
# ---------------------------------------------------------------------------
_NODE_ATTRS: dict[str, list[str]] = {
    'MATH':            ['operation', 'use_clamp'],
    'VECT_MATH':       ['operation'],
    'BOOLEAN_MATH':    ['operation'],
    'COMPARE':         ['data_type', 'operation', 'mode'],
    'MIX':             ['data_type', 'blend_type', 'clamp_result',
                        'clamp_factor', 'factor_mode'],
    'MIX_RGB':         ['blend_type', 'use_clamp'],
    'SEPCOLOR':        ['mode'],
    'COMBCOLOR':       ['mode'],
    'CURVE_FLOAT':     [],
    'CURVE_VEC':       [],
    'CURVE_RGB':       [],
    'TEX_IMAGE':       ['interpolation', 'projection', 'extension'],
    'TEX_NOISE':       ['noise_dimensions'],
    'TEX_MUSGRAVE':    ['musgrave_dimensions', 'musgrave_type'],
    'TEX_VORONOI':     ['distance', 'feature', 'voronoi_dimensions'],
    'TEX_WAVE':        ['wave_type', 'bands_direction', 'rings_direction', 'wave_profile'],
    'TEX_GRADIENT':    ['gradient_type'],
    'TEX_MAGIC':       [],
    'TEX_CHECKER':     [],
    'TEX_BRICK':       ['offset', 'offset_frequency', 'squash', 'squash_frequency'],
    'UVMAP':           ['from_instancer'],
    'MAPPING':         ['vector_type'],
    'NORMAL_MAP':      ['space', 'uv_map'],
    'BUMP':            ['invert'],
    'TANGENT':         ['direction_type', 'axis', 'uv_map'],
    'VECT_TRANSFORM':  ['vector_type', 'convert_from', 'convert_to'],
    'SEPXYZ':          [],
    'COMBXYZ':         [],
    'SEPHSV':          [],
    'COMBHSV':         [],
    'SEPRGB':          [],
    'COMBRGB':         [],
    'BLACKBODY':       [],
    'WAVELENGTH':      [],
    'HUE_SAT':         [],
    'GAMMA':           [],
    'BRIGHTCONTRAST':  [],
    'INVERT':          [],
    'BSDF_PRINCIPLED': [],
    'BSDF_DIFFUSE':    [],
    'BSDF_GLOSSY':     ['distribution'],
    'BSDF_TRANSPARENT':[],
    'BSDF_REFRACTION': ['distribution'],
    'BSDF_GLASS':      ['distribution'],
    'EMISSION':        [],
    'AMBIENT_OCCLUSION': ['samples', 'inside', 'only_local'],
    'SUBSURFACE_SCATTERING': ['falloff'],
    'VOLUME_ABSORPTION': [],
    'VOLUME_SCATTER':  [],
    'HOLDOUT':         [],
    'SHADERTOSRGB':    [],
    'FRESNEL':         [],
    'LAYER_WEIGHT':    [],
    'LIGHT_PATH':      [],
    'GEOMETRY':        [],
    'OBJECT_INFO':     ['transform_space'],
    'PARTICLE_INFO':   [],
    'HAIR_INFO':       [],
    'POINT_INFO':      [],
    'WIREFRAME':       ['use_pixel_size'],
    'RGB':             [],
    'VALUE':           [],
    'CLAMP':           ['clamp_type'],
    'MAP_RANGE':       ['data_type', 'interpolation_type', 'clamp'],
    'SMOOTHSTEP':      [],
    'SMOOTHERSTEP':    [],
    'FLOATCURVE':      [],
    'SCRIPT':          ['mode'],
    'ATTRIBUTE':       ['attribute_name', 'attribute_type'],
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
        "has_image_nodes": [],
        "has_uv_nodes":    [],
        "nested_groups":   [],
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
            info["has_image_nodes"].append(var_name)
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

def _analyze_interface(ng: bpy.types.NodeTree) -> list[dict]:
    sockets = []
    for item in ng.interface.items_tree:
        if not hasattr(item, 'item_type') or item.item_type != 'SOCKET':
            continue
        s: dict = {
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
        sockets.append(s)
    return sockets


def _analyze_node(node, var_name: str) -> dict:
    return {
        "var_name":       var_name,
        "name":           node.name,
        "type":           node.type,
        "bl_idname":      node.bl_idname,
        "location":       (round(node.location.x, 2), round(node.location.y, 2)),
        "width":          round(node.width, 2),
        "label":          node.label or '',
        "hide":           node.hide,
        "attributes":     _get_node_attrs(node),
        "input_defaults": _get_input_defaults(node),
        "node_tree_name": node.node_tree.name if node.type == 'GROUP' and node.node_tree else None,
        "bl_idname":      node.bl_idname,
        # Zone-specific
        "repeat_items":   _get_repeat_items(node),
    }


def _get_node_attrs(node) -> dict:
    attrs = {}
    for attr in _NODE_ATTRS.get(node.type, []):
        if hasattr(node, attr):
            try:
                attrs[attr] = getattr(node, attr)
            except Exception:
                pass
    return attrs


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


def _safe_default(item):
    try:
        return _serialise(item.default_value)
    except Exception:
        return None


def _serialise(v):
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
