"""
Dynamic node attribute introspection.
Replaces the static _NODE_ATTRS lookup with runtime bl_rna inspection so
new Blender node types are handled automatically without table maintenance.
"""

import bpy  # type: ignore

_BASE_NODE_PROPS: frozenset | None = None

# RNA property types that map to plain Python scalars
_SCALAR_TYPES = frozenset({'BOOLEAN', 'INT', 'FLOAT', 'STRING', 'ENUM'})

# Scalar props inherited from or added by the Node base class that carry no
# node-type-specific meaning for code generation.
_SKIP_PROPS = frozenset({
    'select', 'show_options', 'show_preview',
    'use_custom_color', 'width_hidden', 'height',
})


def _base_props() -> frozenset:
    global _BASE_NODE_PROPS
    if _BASE_NODE_PROPS is None:
        _BASE_NODE_PROPS = frozenset(bpy.types.Node.bl_rna.properties.keys())
    return _BASE_NODE_PROPS


def get_serialisable_attrs(node) -> dict:
    """
    Return {attr_name: value} for all node-type-specific scalar attributes.

    Filters out:
    - Properties inherited from the Node base class
    - Read-only properties
    - Array properties (vectors, colors)
    - Pointer / Collection properties (e.g. color_ramp, node_tree, image)
    """
    base = _base_props()
    attrs = {}
    for prop in node.bl_rna.properties:
        name = prop.identifier
        if name in base or name in _SKIP_PROPS:
            continue
        if prop.type not in _SCALAR_TYPES or getattr(prop, 'is_array', False) or prop.is_readonly:
            continue
        try:
            val = getattr(node, name)
            if isinstance(val, (bool, int, float, str)):
                attrs[name] = val
        except Exception:
            pass
    return attrs
