"""
Runtime shader-node reconcile.

Custom shader nodes (ShaderNodeCustomGroup) bake their internal node_tree
datablock into the .blend file. On reload Blender restores each node pointing
at that saved datablock and never re-runs the addon's createNodetree(), so a
node saved by an OLDER LSPotato keeps its outdated tree even after the addon
ships a fixed implementation under the same bl_label.

This module closes that gap — the shader analogue of geometry/loader.py. On
file load (and once for the file already open at register) it rebuilds each
in-use node class's canonical tree, compares it against the saved one by hash,
and on mismatch overwrites via user_remap so every instance and parent group
is redirected to the refreshed version. Unchanged trees are left untouched.

Guards:
  * The load_post handler never raises (a handler must not).
  * Only node types actually present in the file are reconciled, so cost
    scales with the file, not with the whole shipped library.
"""

from __future__ import annotations
import re
import types

import bpy  # type: ignore
from bpy.app.handlers import persistent  # type: ignore

from ..utils.logger import get_logger
from .node import iter_registered_node_classes, get_node_class_by_idname
from .geometry.hashing import hash_node_tree

logger = get_logger("ShaderReconcile")

# Blender appends a ".001"-style suffix when a datablock name collides; the
# base of such a name is the stable key the class originally built under.
_DUP_SUFFIX_RE = re.compile(r"\.\d{3,}$")


def _base_name(name: str) -> str:
    """'.lscherry.core.Toon.001' -> '.lscherry.core.Toon' (drop suffix)."""
    return _DUP_SUFFIX_RE.sub("", name)


def _iter_shader_trees() -> list:
    """Snapshot of every shader tree a custom node could live in."""
    trees: list = []
    for mat in bpy.data.materials:
        if mat.use_nodes and mat.node_tree:
            trees.append(mat.node_tree)
    for world in bpy.data.worlds:
        if world.use_nodes and world.node_tree:
            trees.append(world.node_tree)
    for light in bpy.data.lights:
        if light.use_nodes and light.node_tree:
            trees.append(light.node_tree)
    for ng in bpy.data.node_groups:
        trees.append(ng)
    return trees


def _build_fresh(cls):
    """
    Build the class's canonical tree from scratch; return the new datablock.

    Mirrors Node.create_node_group's detached-proxy build but never takes the
    "already exists" fast path — bpy.data.node_groups.new() auto-suffixes the
    name when the stable key is taken, so the result is always a brand-new
    datablock we can hash-compare against the saved one.
    """
    key = cls._PREFIX + cls.bl_label
    proxy = types.SimpleNamespace(
        _PREFIX=cls._PREFIX,
        bl_label=cls.bl_label,
        node_tree=None,
        valuesUpdate=lambda *a, **k: None,
    )
    try:
        cls.createNodetree(proxy, key)
    except Exception as e:
        logger.error(f"reconcile: build failed for '{key}': {e}")
        return None
    return proxy.node_tree


def _reconcile_key(key: str, cls) -> None:
    """Refresh the canonical datablock for one class if it is stale/absent."""
    ng = bpy.data.node_groups
    canonical = ng.get(key)
    fresh = _build_fresh(cls)
    if fresh is None:
        return
    if canonical is None or canonical is fresh:
        # Absent before the build (fresh landed on the exact key) — done.
        if fresh.name != key:
            fresh.name = key
        return
    if hash_node_tree(canonical) == hash_node_tree(fresh):
        # Already current — discard the throwaway rebuild, touch nothing.
        ng.remove(fresh)
        return
    # Stale: redirect every user (instances + parent groups) to the rebuild,
    # drop the old datablock, and reclaim the canonical name.
    canonical.user_remap(fresh)
    ng.remove(canonical)
    fresh.name = key
    logger.info(f"reconcile: refreshed stale node tree '{key}'")


def _reconcile_instances() -> None:
    """
    Re-point any instance still bound to a stale or drifted tree.

    Covers what the datablock pass cannot: instances whose saved tree was named
    under an OLDER scheme (so user_remap of the canonical never reached them),
    and per-instance image copies ('<key>.001') that valuesUpdate forked from a
    now-outdated base. An already up-to-date fork is left alone to avoid churn.
    """
    ng = bpy.data.node_groups
    ctx = bpy.context
    for tree in _iter_shader_trees():
        for node in list(tree.nodes):
            cls = get_node_class_by_idname(node.bl_idname)
            if cls is None:
                continue
            key = cls._PREFIX + cls.bl_label
            target = ng.get(key)
            if target is None:
                continue
            cur = getattr(node, "node_tree", None)
            if cur is target:
                continue
            # Leave an up-to-date per-instance fork ('<key>.001') in place.
            if cur is not None and _base_name(cur.name) == key:
                try:
                    if hash_node_tree(cur) == hash_node_tree(target):
                        continue
                except Exception:
                    pass
            try:
                node.node_tree = target
                if hasattr(node, "valuesUpdate"):
                    node.valuesUpdate(ctx)
            except Exception as e:
                logger.error(f"reconcile: instance '{node.name}': {e}")


def _purge_orphans(keys: set) -> None:
    """Remove now-unused stale datablocks left behind by the passes above."""
    ng = bpy.data.node_groups
    for block in list(ng):
        if _base_name(block.name) not in keys:
            continue
        if block.users == 0 and not block.use_fake_user:
            try:
                ng.remove(block)
            except Exception:
                pass


def reconcile_shader_nodes() -> None:
    """Refresh every in-file shader node tree to the current definition."""
    registry = iter_registered_node_classes()
    if not registry:
        return
    classes_by_key = dict(registry)

    # Which canonical keys does this file actually use? Collect from live
    # instances (resolved by class) and from any datablock whose base name
    # matches a registered key — both bound the work to what is in the file.
    needed: set = set()
    for tree in _iter_shader_trees():
        for node in tree.nodes:
            cls = get_node_class_by_idname(node.bl_idname)
            if cls is not None:
                needed.add(cls._PREFIX + cls.bl_label)
    for block in bpy.data.node_groups:
        base = _base_name(block.name)
        if base in classes_by_key:
            needed.add(base)

    # Order is irrelevant: user_remap on each datablock redirects every parent
    # that embeds it, so a refreshed child reaches even unchanged parents.
    for key in needed:
        cls = classes_by_key.get(key)
        if cls is not None:
            _reconcile_key(key, cls)

    _reconcile_instances()
    _purge_orphans(set(classes_by_key.keys()))


# ---------------------------------------------------------------------------
# Automatic trigger — mirrors geometry/loader.py: run on every file open, plus
# a one-shot deferred pass for the file already open when the addon registers
# (load_post does not fire for the startup file).
# ---------------------------------------------------------------------------

@persistent
def shader_reconcile_load_post(dummy=None):
    """load_post handler — refresh stale shader node trees on file open."""
    try:
        reconcile_shader_nodes()
    except Exception as exc:  # noqa: BLE001 — a handler must never raise
        logger.error(f"shader_reconcile_load_post failed: {exc}")


def _deferred_init():
    """One-shot timer: cover the file already open at addon register."""
    try:
        reconcile_shader_nodes()
    except Exception as exc:  # noqa: BLE001
        logger.error(f"deferred shader reconcile failed: {exc}")
    return None  # returning None unregisters the timer (runs once)


def register_reconcile_handler():
    """Install the load_post handler and a one-shot init for the open file."""
    if shader_reconcile_load_post not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(shader_reconcile_load_post)
    try:
        if not bpy.app.timers.is_registered(_deferred_init):
            bpy.app.timers.register(_deferred_init, first_interval=0.6)
    except Exception as exc:  # noqa: BLE001
        logger.error(f"could not schedule deferred shader reconcile: {exc}")


def unregister_reconcile_handler():
    """Remove the load_post handler (and the deferred timer if pending)."""
    if shader_reconcile_load_post in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(shader_reconcile_load_post)
    try:
        if bpy.app.timers.is_registered(_deferred_init):
            bpy.app.timers.unregister(_deferred_init)
    except Exception:
        pass
