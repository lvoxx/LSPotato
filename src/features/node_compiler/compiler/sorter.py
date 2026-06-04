"""
Topological Sorter
Returns node groups in bottom-up order (leaves first, roots last),
so that when a parent group is compiled its child groups already exist.
"""

from __future__ import annotations
import bpy  # type: ignore
from collections import defaultdict, deque


def topological_sort(node_groups: list) -> list:
    """
    Sort *node_groups* so that each group appears AFTER all groups
    it depends on (i.e. uses as nested ShaderNodeGroup / GeometryNodeGroup).

    Groups that form a cycle are appended at the end (best-effort).
    """
    # Build name → ng map and dependency sets
    all_ngs: dict[str, object] = {ng.name: ng for ng in node_groups}
    deps: dict[str, set[str]] = defaultdict(set)

    for ng in node_groups:
        for node in ng.nodes:
            if node.type == 'GROUP' and node.node_tree:
                child = node.node_tree.name
                if child in all_ngs and child != ng.name:
                    deps[ng.name].add(child)

    # Kahn's algorithm
    in_degree: dict[str, int] = {n: 0 for n in all_ngs}
    # A depends on B → B must come first → B's "out-edges" decrement A's in-degree
    for name, children in deps.items():
        for child in children:
            in_degree[name] += 1  # name depends on child → in_degree[name]++

    queue = deque(n for n in all_ngs if in_degree[n] == 0)
    sorted_names: list[str] = []

    while queue:
        name = queue.popleft()
        sorted_names.append(name)
        # Find who depends on `name` and decrement their in-degree
        for other, other_deps in deps.items():
            if name in other_deps:
                in_degree[other] -= 1
                if in_degree[other] == 0:
                    queue.append(other)

    # Any remaining (cycles) appended at end
    remaining = [n for n in all_ngs if n not in sorted_names]
    sorted_names.extend(remaining)

    return [all_ngs[n] for n in sorted_names if n in all_ngs]


def get_all_node_groups() -> list:
    """
    Return the shader node groups currently loaded in bpy.data.

    Geometry node groups are excluded — geometry support is deferred, and they
    must never be compiled into the shader node library (they would register as
    geometry nodes inside the shader Add menu and break). This is the single
    gate every group passes through before compilation.
    """
    return [ng for ng in bpy.data.node_groups if ng.type == 'SHADER']
