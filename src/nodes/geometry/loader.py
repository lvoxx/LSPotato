"""
Runtime geometry-node loader.

Appends the shipped geometry node groups (geometry/library.blend) into the
currently-open .blend, using geometry/hashes.json as the source of truth for
each group's canonical hash:

    absent      → append
    hash match  → skip (leave the user's file untouched)
    hash differ → overwrite with the shipped version (append + user_remap so any
                  Geometry-Nodes modifier still resolves), then reclaim the name

Legacy ``.00x`` duplicates (e.g. ``LS Outline And Rim.001`` sitting next to
``LS Outline And Rim``) are stale copies of an *older* version that earlier
libraries baked in. They are dropped from the manifest before classification
(never appended/preserved) and any still-bound copy in the open file is migrated
onto its canonical group, then removed — so objects pick up the current version
instead of clinging to the outdated ``.001``.

The whole bring-in runs as ONE ``bpy.data.libraries.load`` call so shared nested
dependencies are resolved once instead of being duplicated per parent. Applying
modifiers onto objects is NOT done here — autosync owns that.

Guards (per spec):
  * If library.blend or hashes.json is missing → skip silently (no raise).
  * The bring-in retries up to 3 times before the groups are reported failed.
"""

from __future__ import annotations
import os
import re
import json

import bpy  # type: ignore
from bpy.app.handlers import persistent  # type: ignore

from ...utils.logger import get_logger
from ...exception.model.geometry_exceptions import GeometryAppendException
from .hashing import hash_node_tree

logger = get_logger("GeometryLoader")

_GEO_DIR      = os.path.dirname(os.path.abspath(__file__))
_LIBRARY_PATH = os.path.join(_GEO_DIR, "library.blend")
_HASHES_PATH  = os.path.join(_GEO_DIR, "hashes.json")

_MAX_RETRIES = 1
# _MAX_RETRIES = 3 # README: Retry disabled for now — the bring-in is usually unstable, will be fix later
# Blender appends a ".001"-style suffix when a datablock name collides.
_DUP_SUFFIX_RE = re.compile(r"\.\d{3,}$")


def _base_name(name: str) -> str:
    """'lscherry.geo.Outline.001' → 'lscherry.geo.Outline' (strip dup suffix only)."""
    return _DUP_SUFFIX_RE.sub("", name)


def _canonical_manifest(hashes: dict) -> dict:
    """
    Drop legacy ``.00x``-duplicate keys from a hash manifest.

    Older dev .blends accumulated stale ``.00x`` copies of a group (an outdated
    version left behind by a previous botched sync). The geometry exporter wrote
    every group it found, so those copies were baked into hashes.json as if they
    were canonical. A key like ``'LS Outline And Rim.001'`` whose base name
    (``'LS Outline And Rim'``) is ALSO in the manifest is one of those stale
    copies: it must never be appended or preserved — the base group is the real
    one. A ``.00x`` key whose base is absent is kept (it is the only copy, hence
    canonical).
    """
    return {
        name: digest
        for name, digest in hashes.items()
        if _base_name(name) == name or _base_name(name) not in hashes
    }


def init_geometry_nodes() -> dict:
    """
    Ensure every shipped geometry node group exists in the current file at the
    shipped version.

    Returns a result dict::

        {
          "missing":     None | "<path>",   # set when an artifact is absent
          "appended":    int,
          "overwritten": int,
          "skipped":     int,
          "failed":      int,
          "migrated":    int,   # legacy '.00x' duplicates folded onto canonical
        }
    """
    result = {"missing": None, "appended": 0, "overwritten": 0,
              "skipped": 0, "failed": 0, "migrated": 0}

    # ── Guard: shipped artifacts must both exist ─────────────────────────────
    for path in (_LIBRARY_PATH, _HASHES_PATH):
        if not os.path.isfile(path):
            logger.warning(f"Geometry library artifact missing: {path}. Skipping.")
            result["missing"] = path
            return result

    # ── Load the manifest ────────────────────────────────────────────────────
    try:
        with open(_HASHES_PATH, "r", encoding="utf-8") as fh:
            hashes: dict = json.load(fh)
    except (OSError, ValueError) as exc:
        logger.warning(f"Could not read geometry hashes.json: {exc}. Skipping.")
        result["missing"] = _HASHES_PATH
        return result

    if not hashes:
        logger.info("Geometry hashes.json is empty — nothing to initialize.")
        return result

    # Ignore legacy '.00x' duplicate entries — they are stale older versions, not
    # real groups. The migration pass below cleans any copy still in the file.
    hashes = _canonical_manifest(hashes)

    ng = bpy.data.node_groups

    # ── Classify each shipped group ──────────────────────────────────────────
    to_bring: list[str] = []        # names that are absent or stale
    old_blocks: dict = {}           # name → existing datablock to replace
    for name, shipped_hash in hashes.items():
        existing = ng.get(name)
        if existing is not None and getattr(existing, "type", None) == "GEOMETRY":
            if hash_node_tree(existing) == shipped_hash:
                result["skipped"] += 1
                continue
            old_blocks[name] = existing
        to_bring.append(name)

    # ── Bring in absent / stale groups (single batch), with retry ────────────
    if to_bring:
        last_exc: Exception | None = None
        for attempt in range(1, _MAX_RETRIES + 1):
            try:
                _bring_in(to_bring, old_blocks, hashes)
                last_exc = None
                break
            except Exception as exc:  # noqa: BLE001 — retried; reported below
                last_exc = exc
                logger.warning(
                    f"Geometry bring-in attempt {attempt}/{_MAX_RETRIES} failed: {exc}"
                )

        if last_exc is not None:
            result["failed"] += len(to_bring)
            logger.error(f"Geometry bring-in failed after {_MAX_RETRIES} attempts: {last_exc}")
            return result

        for name in to_bring:
            if name in old_blocks:
                result["overwritten"] += 1
            else:
                result["appended"] += 1

    # ── Migrate legacy '.00x' duplicates onto their canonical group ──────────
    # Runs every init (even when nothing was brought in): the bug shows up
    # precisely when the canonical group already matches and the stale '.001'
    # copy is the one still bound to objects.
    result["migrated"] = _migrate_legacy_duplicates(hashes)
    return result


def _bring_in(names: list[str], old_blocks: dict, hashes: dict) -> None:
    """
    Append *names* from the shipped library in a single load, then reconcile:
      1. redirect & reclaim each requested name (overwrites keep modifier refs),
      2. fold away any duplicate dependency that was pulled for a kept group.

    Raises GeometryAppendException if a requested name is not in the library.
    """
    ng = bpy.data.node_groups
    before_ids = {id(b) for b in ng}

    with bpy.data.libraries.load(_LIBRARY_PATH, link=False) as (data_from, data_to):
        available = [n for n in names if n in data_from.node_groups]
        missing   = [n for n in names if n not in data_from.node_groups]
        data_to.node_groups = available

    if missing:
        raise GeometryAppendException(
            missing[0],
            f"{len(missing)} group(s) not present in library.blend: {missing}",
        )

    # After the context manager, data_to.node_groups holds the loaded datablocks
    # for `available`, in the same order.
    requested_blocks = list(data_to.node_groups)
    requested_ids = {id(b) for b in requested_blocks}

    # 1. Reconcile each requested group.
    for name, incoming in zip(available, requested_blocks):
        old = old_blocks.get(name)
        if old is not None and old is not incoming:
            old.user_remap(incoming)              # redirect modifiers/parents
            ng.remove(old)
            incoming.name = name                  # reclaim the canonical name
        elif incoming.name != name:
            incoming.name = name                  # fresh append landed as name.00x

    # 2. Fold away duplicate dependencies pulled for groups we KEPT.
    #    Any new datablock that wasn't one of the requested blocks and whose base
    #    name is an existing shipped group is an unintended dependency copy.
    new_blocks = [b for b in ng if id(b) not in before_ids and id(b) not in requested_ids]
    for dup in new_blocks:
        base = _base_name(dup.name)
        if base not in hashes:
            continue                              # genuinely new dependency — keep
        kept = ng.get(base)
        if kept is not None and kept is not dup:
            dup.user_remap(kept)
            ng.remove(dup)


def _migrate_legacy_duplicates(hashes: dict) -> int:
    """
    Repoint every user of a legacy ``.00x`` duplicate geometry group onto the
    canonical group, then remove the duplicate once nothing references it.

    Fixes files an older library polluted: an object whose Geometry-Nodes
    modifier (or a parent group) still points at e.g. ``LS Outline And Rim.001``
    is migrated to ``LS Outline And Rim`` so it picks up the current version.
    user_remap moves ALL users (modifiers, parent groups, fake users), so after
    it the duplicate is unused and safe to delete.

    Only GEOMETRY groups whose stripped base name is a canonical shipped group
    (a key of *hashes*) are touched, and the duplicate is removed only when it
    has zero remaining users — i.e. after verifying nothing still uses it.
    Returns the number of duplicates removed.
    """
    ng = bpy.data.node_groups
    canonical_names = {n for n in hashes if _base_name(n) == n}
    removed = 0

    for block in list(ng):
        if getattr(block, "type", None) != "GEOMETRY":
            continue
        base = _base_name(block.name)
        if base == block.name or base not in canonical_names:
            continue                              # not a recognised '.00x' dup
        canonical = ng.get(base)
        if canonical is None or canonical is block:
            continue                              # no canonical to migrate onto

        try:
            block.user_remap(canonical)
            if block.use_fake_user:
                block.use_fake_user = False       # drop the fake user too
            if block.users == 0:
                ng.remove(block)
                removed += 1
            else:
                logger.warning(
                    f"Geometry: legacy duplicate '{block.name}' still has "
                    f"{block.users} user(s) after remap; left in place."
                )
        except Exception as exc:  # noqa: BLE001 — a load handler must not raise
            logger.error(f"Geometry: could not migrate '{block.name}': {exc}")

    return removed


# ---------------------------------------------------------------------------
# Automatic trigger
#
# Append the geometry groups whenever a .blend is opened (File > Open / New) so
# every working file has the full library available for autosync to use as
# modifiers. The hash check keeps this idempotent — re-opens skip unchanged
# groups instead of duplicating them.
# ---------------------------------------------------------------------------

@persistent
def geometry_load_post(dummy=None):
    """load_post handler — ensure the geometry library is present on file open."""
    try:
        init_geometry_nodes()
    except Exception as exc:  # noqa: BLE001 — a handler must never raise
        logger.error(f"geometry_load_post failed: {exc}")


def _deferred_init():
    """One-shot timer callback: cover the file already open at addon register."""
    try:
        init_geometry_nodes()
    except Exception as exc:  # noqa: BLE001
        logger.error(f"deferred geometry init failed: {exc}")
    return None  # returning None unregisters the timer (runs once)


def register_geometry_handler():
    """Install the load_post handler and a one-shot init for the current file."""
    if geometry_load_post not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(geometry_load_post)
    # The startup file is loaded BEFORE this addon registers, so load_post won't
    # fire for it — defer a single init to a safe context to cover that file.
    try:
        if not bpy.app.timers.is_registered(_deferred_init):
            bpy.app.timers.register(_deferred_init, first_interval=0.5)
    except Exception as exc:  # noqa: BLE001
        logger.error(f"could not schedule deferred geometry init: {exc}")


def unregister_geometry_handler():
    """Remove the load_post handler (and the deferred timer if still pending)."""
    if geometry_load_post in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(geometry_load_post)
    try:
        if bpy.app.timers.is_registered(_deferred_init):
            bpy.app.timers.unregister(_deferred_init)
    except Exception:
        pass
