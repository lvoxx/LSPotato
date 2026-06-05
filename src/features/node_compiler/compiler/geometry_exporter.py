"""
Geometry exporter (compile side).

Geometry node groups don't round-trip through GeometryNodeCustomGroup the way
shaders do, so instead of generating Python the NodeCompiler writes them verbatim
into a .blend library plus a hash manifest:

    <out_dir>/geometry/library.blend   — every GEOMETRY group (+ deps), one file
    <out_dir>/geometry/hashes.json     — { group_name: md5_hex }

The developer copies <out_dir>/geometry/ into src/nodes/geometry/; at runtime
loader.init_geometry_nodes() appends the groups and uses the manifest to decide
skip vs overwrite. Both sides hash with the SAME function so the values line up.
"""

from __future__ import annotations
import os
import json

import bpy  # type: ignore

from ....nodes.geometry.hashing import hash_node_tree

_GEOMETRY_SUBDIR = "geometry"
_LIBRARY_NAME    = "library.blend"
_HASHES_NAME     = "hashes.json"


def collect_geometry_groups() -> list:
    """
    Return every geometry node group in the current file.

    The geometry mirror of sorter.get_all_node_groups() (which is shader-only);
    that gate is left untouched so the shader pipeline is unaffected.
    """
    return [ng for ng in bpy.data.node_groups if ng.type == "GEOMETRY"]


def export_geometry_library(out_dir: str, groups: list) -> str:
    """
    Write *groups* (and their dependencies, automatically) into
    ``<out_dir>/geometry/library.blend``. Returns the file path.
    """
    geo_dir = os.path.join(out_dir, _GEOMETRY_SUBDIR)
    os.makedirs(geo_dir, exist_ok=True)
    lib_path = os.path.join(geo_dir, _LIBRARY_NAME)

    # fake_user keeps the (otherwise 0-user) groups alive inside the library so
    # they survive a save; dependencies are written by Blender automatically.
    bpy.data.libraries.write(
        lib_path, set(groups), fake_user=True, compress=True,
    )
    return lib_path


def write_geometry_hashes(out_dir: str, groups: list) -> str:
    """
    Write ``<out_dir>/geometry/hashes.json`` mapping each group's name to its
    canonical hash. Returns the file path.
    """
    geo_dir = os.path.join(out_dir, _GEOMETRY_SUBDIR)
    os.makedirs(geo_dir, exist_ok=True)
    hashes_path = os.path.join(geo_dir, _HASHES_NAME)

    manifest = {ng.name: hash_node_tree(ng) for ng in groups}
    with open(hashes_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)
    return hashes_path


def export_geometry(out_dir: str) -> int:
    """
    Collect geometry groups, write the library + hash manifest, and return the
    number of groups exported (0 if there are none).
    """
    groups = collect_geometry_groups()
    if not groups:
        return 0
    export_geometry_library(out_dir, groups)
    write_geometry_hashes(out_dir, groups)
    return len(groups)
