"""
Geometry node-tree hashing.

Single source of truth for the hash algorithm, shared by:
  * the NodeCompiler  (compiler/geometry_exporter.py) — hashes the source groups
    in the dev .blend and writes the canonical values into geometry/hashes.json.
  * the runtime loader (loader.py)                    — hashes an in-file group
    and compares it against the shipped JSON value to decide skip / overwrite.

Because both sides call the *same* function, the numbers line up.

This module is intentionally bpy-free: it operates on duck-typed node-tree
objects (anything exposing ``.nodes`` / ``.links`` with the expected attrs), so
it can be unit-tested with plain fakes under system Python (the dev venv is
broken — use system Python 3.14).
"""

from __future__ import annotations
import json
import hashlib


# Node attributes that are layout / transient UI state rather than content.
# These can legitimately differ between the source group and a freshly-appended
# copy of it, so they MUST be excluded — otherwise the runtime hash of an
# untouched appended group would never match its own shipped hash and every run
# would needlessly "overwrite". ``location`` is handled separately (rounded).
_VOLATILE_NODE_ATTRS = frozenset({
    "select",
    "dimensions",
    "width",
    "height",
    "width_hidden",
    "location",
    "location_absolute",
})

_LOCATION_NDIGITS = 2


def to_serializable(val):
    """Coerce a socket default_value (or any value) into a JSON-safe form."""
    # None / basic scalars pass straight through.
    if val is None or isinstance(val, (int, float, str, bool)):
        return val

    # bpy_prop_array (colours, vectors, ...) → list, recursively.
    if hasattr(val, "__len__") and hasattr(val, "__getitem__"):
        try:
            return [to_serializable(v) for v in val]
        except Exception:
            pass

    # Fallback: stable string representation.
    return str(val)


def _node_location(node):
    """Return the node location rounded to a few decimals, or None."""
    loc = getattr(node, "location", None)
    if loc is None:
        return None
    try:
        return [round(float(c), _LOCATION_NDIGITS) for c in loc]
    except Exception:
        return None


def _scalar_props(node) -> dict:
    """
    Collect the node's content-bearing scalar properties via introspection.

    Iterates ``dir(node)`` (works on real bpy nodes and on plain fakes), keeps
    only int / float / str / bool values, and drops private and volatile-UI
    attributes. Anything that raises on access is skipped.
    """
    props: dict = {}
    for attr in dir(node):
        if attr.startswith("_") or attr in _VOLATILE_NODE_ATTRS:
            continue
        try:
            val = getattr(node, attr)
        except Exception:
            continue
        if isinstance(val, (int, float, str, bool)):
            props[attr] = val
    return props


def serialize_node_tree(nt, _ancestors=frozenset()) -> dict:
    """
    Build a deterministic, JSON-serialisable description of a node tree.

    Nodes are sorted by name and links by their full endpoint tuple so that
    iteration order can never perturb the resulting hash.

    Recurses into nested node groups (a node's ``.node_tree``) so a change deep
    inside an embedded group changes the parent's hash too. Without this, a
    wrapper like ``Core.LSCherryProvider`` whose own nodes/links never change
    hashes identically even after its inner groups were updated — and the loader
    skips it as 'up to date', so objects keep the old effect. Nested trees are
    hashed by CONTENT, not datablock name, so a group named ``X`` and a copy
    named ``X.001`` with identical content compare equal. ``_ancestors`` carries
    the ids of trees on the current path to break reference cycles.
    """
    next_ancestors = _ancestors | {id(nt)}
    nodes = []
    for node in nt.nodes:
        inputs = []
        for inp in getattr(node, "inputs", []):
            try:
                inputs.append(to_serializable(getattr(inp, "default_value", None)))
            except Exception:
                inputs.append(None)

        entry = {
            "name": getattr(node, "name", ""),
            "type": getattr(node, "bl_idname", ""),
            "location": _node_location(node),
            "props": _scalar_props(node),
            "inputs": inputs,
        }

        # Fold the referenced group's CONTENT into the hash (group nodes expose
        # the nested tree via ``.node_tree``). Cycle-guarded; name is ignored.
        sub = getattr(node, "node_tree", None)
        if sub is not None:
            entry["group"] = (
                "<cycle>" if id(sub) in next_ancestors
                else serialize_node_tree(sub, next_ancestors)
            )
        nodes.append(entry)

    links = []
    for link in nt.links:
        links.append({
            "from": [link.from_node.name, link.from_socket.name],
            "to": [link.to_node.name, link.to_socket.name],
        })

    nodes.sort(key=lambda n: n["name"])
    links.sort(key=lambda link: (
        link["from"][0], link["from"][1], link["to"][0], link["to"][1],
    ))

    return {"nodes": nodes, "links": links}


def hash_node_tree(nt) -> str:
    """Return the MD5 hex digest of a node tree's deterministic serialisation."""
    payload = json.dumps(serialize_node_tree(nt), sort_keys=True)
    return hashlib.md5(payload.encode("utf-8")).hexdigest()
