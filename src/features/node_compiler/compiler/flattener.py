"""
Attribute-subtree flattener.

Blender does not bind geometry attributes when a ``ShaderNodeAttribute`` lives in
a plain node group that is *nested inside* a ``ShaderNodeCustomGroup``'s tree —
the attribute reads as zero and the object renders black. The same group works
when the Attribute node sits directly in the custom group's own tree.

To dodge that, every nested group that *transitively contains* an Attribute node
is inlined ("ungrouped") into the tree that references it, so all Attribute nodes
end up directly in each compiled node's own tree. Attribute-free sub-groups are
left as shared ``ensure_node_group`` references, so the modular structure and
datablock sharing are preserved everywhere else.

This operates on the plain-dict ``info`` produced by analyzer.analyze_node_group
(reroutes already inlined, links already node-to-node), so no live bpy data is
touched here.
"""

from __future__ import annotations
import copy

_GI = "GROUP_INPUT"
_GO = "GROUP_OUTPUT"


# ---------------------------------------------------------------------------
# Detection
# ---------------------------------------------------------------------------

def group_has_attribute(name: str, infos: dict, memo: dict | None = None,
                        _visiting: set | None = None) -> bool:
    """
    True if the group *name* contains an ATTRIBUTE node, or any of its nested
    compiled groups transitively does. ``infos`` maps ng.name → analyzed info.
    """
    if memo is None:
        memo = {}
    if name in memo:
        return memo[name]
    info = infos.get(name)
    if info is None:
        return False
    if _visiting is None:
        _visiting = set()
    if name in _visiting:          # cycle guard (Blender forbids these anyway)
        return False
    _visiting.add(name)

    found = False
    for n in info["nodes"]:
        if n["type"] == "ATTRIBUTE":
            found = True
            break
        if n["type"] == "GROUP" and n.get("node_tree_name") in infos:
            if group_has_attribute(n["node_tree_name"], infos, memo, _visiting):
                found = True
                break

    _visiting.discard(name)
    memo[name] = found
    return found


def needs_flatten(info: dict, infos: dict, memo: dict) -> bool:
    """True if *info* references any nested compiled group that is attribute-bearing."""
    for n in info["nodes"]:
        if (n["type"] == "GROUP"
                and n.get("node_tree_name") in infos
                and group_has_attribute(n["node_tree_name"], infos, memo)):
            return True
    return False


# ---------------------------------------------------------------------------
# Flatten
# ---------------------------------------------------------------------------

def flatten_info(info: dict, infos: dict, memo: dict) -> dict:
    """
    Return a NEW info dict whose attribute-bearing nested groups are inlined.

    The top interface, name, type, color_tag, description and bl_label are kept
    unchanged — only ``nodes`` / ``links`` (and the derived image/uv/nested-group
    bookkeeping) change.
    """
    nodes = copy.deepcopy(info["nodes"])
    links = copy.deepcopy(info["links"])
    inlined_children: list[str] = []

    while True:
        target = None
        for n in nodes:
            if (n["type"] == "GROUP"
                    and n.get("node_tree_name") in infos
                    and group_has_attribute(n["node_tree_name"], infos, memo)):
                target = n
                break
        if target is None:
            break
        nodes, links = _inline_one(target, nodes, links, infos)
        inlined_children.append(target["node_tree_name"])

    new_info = dict(info)
    new_info["nodes"] = nodes
    new_info["links"] = links
    new_info["has_image_nodes"] = [
        n["var_name"] for n in nodes
        if n["type"] == "TEX_IMAGE" and not n.get("image_name")
    ]
    new_info["placeholder_image_node_names"] = [
        n["name"] for n in nodes
        if n["type"] == "TEX_IMAGE" and not n.get("image_name")
    ]
    new_info["placeholder_images"] = [
        {"node_name": n["name"], "label": n.get("label") or ""}
        for n in nodes
        if n["type"] == "TEX_IMAGE" and not n.get("image_name")
    ]
    new_info["has_uv_nodes"] = [n["var_name"] for n in nodes if n["type"] == "UVMAP"]

    seen: set[str] = set()
    nested: list[str] = []
    for n in nodes:
        tn = n.get("node_tree_name")
        if n["type"] == "GROUP" and tn and tn not in seen:
            seen.add(tn)
            nested.append(tn)
    new_info["nested_groups"] = nested

    # Carry forward predefined (packed) textures from every inlined child so the
    # exporter still writes them; the caller dedupes by filename.
    predefined = list(info.get("_predefined_images", []))
    for cname in inlined_children:
        cinfo = infos.get(cname)
        if cinfo:
            predefined.extend(cinfo.get("_predefined_images", []))
    new_info["_predefined_images"] = predefined

    return new_info


def _inline_one(group_node: dict, nodes: list, links: list, infos: dict):
    """
    Splice the child group referenced by *group_node* into the parent node/link
    lists (standard recursive 'ungroup'). Returns new (nodes, links) lists.
    """
    child = infos[group_node["node_tree_name"]]
    gvar = group_node["var_name"]
    prefix = gvar + "__"

    gi_vars = {n["var_name"] for n in child["nodes"] if n["type"] == _GI}
    go_vars = {n["var_name"] for n in child["nodes"] if n["type"] == _GO}

    # child INPUT interface socket name → its index in the group node's inputs
    name_to_idx: dict[str, int] = {}
    idx = 0
    for s in child["interface"]:
        if s.get("item_kind", "socket") == "socket" and s["in_out"] == "INPUT":
            name_to_idx[s["name"]] = idx
            idx += 1

    group_defaults = group_node.get("input_defaults", {})

    # Parent links touching the group node, indexed by boundary socket name.
    in_source: dict[str, list[tuple]] = {}    # sockName → [(from_var, fsn, fsi), ...]
    out_consumers: dict[str, list[tuple]] = {}  # sockName → [(to_var, tsn, tsi), ...]
    for lnk in links:
        if lnk["to_var"] == gvar:
            in_source.setdefault(lnk["to_socket_name"], []).append(
                (lnk["from_var"], lnk["from_socket_name"], lnk["from_socket_index"])
            )
        if lnk["from_var"] == gvar:
            out_consumers.setdefault(lnk["from_socket_name"], []).append(
                (lnk["to_var"], lnk["to_socket_name"], lnk["to_socket_index"])
            )

    # Copy the child's interior nodes (drop Group In/Out) with prefixed var names.
    remap: dict[str, str] = {}
    new_child_nodes: list[dict] = []
    for cn in child["nodes"]:
        if cn["type"] in (_GI, _GO):
            continue
        nc = copy.deepcopy(cn)
        nc["var_name"] = prefix + cn["var_name"]
        remap[cn["var_name"]] = nc["var_name"]
        new_child_nodes.append(nc)

    nc_by_var = {nc["var_name"]: nc for nc in new_child_nodes}
    parent_by_var = {n["var_name"]: n for n in nodes}

    def _set_default(node_dict, sock_index, value):
        node_dict.setdefault("input_defaults", {})[sock_index] = value

    def _parent_default(sock_name):
        i = name_to_idx.get(sock_name)
        if i is not None and i in group_defaults:
            return True, group_defaults[i]
        return False, None

    new_links: list[dict] = []
    for lnk in child["links"]:
        f, t = lnk["from_var"], lnk["to_var"]
        f_gi, t_go = f in gi_vars, t in go_vars

        if f_gi and t_go:
            # passthrough: group input → group output
            sources = in_source.get(lnk["from_socket_name"], [])
            consumers = out_consumers.get(lnk["to_socket_name"], [])
            if sources:
                for fv, fsn, fsi in sources:
                    for tv, tsn, tsi in consumers:
                        new_links.append(_link(fv, fsn, fsi, tv, tsn, tsi))
            else:
                has, val = _parent_default(lnk["from_socket_name"])
                if has:
                    for tv, tsn, tsi in consumers:
                        pn = parent_by_var.get(tv)
                        if pn is not None:
                            _set_default(pn, tsi, val)
            continue

        if f_gi:
            # group input → interior consumer
            consumer = remap.get(t)
            if consumer is None:
                continue
            sources = in_source.get(lnk["from_socket_name"], [])
            if sources:
                for fv, fsn, fsi in sources:
                    new_links.append(
                        _link(fv, fsn, fsi, consumer, lnk["to_socket_name"], lnk["to_socket_index"])
                    )
            else:
                has, val = _parent_default(lnk["from_socket_name"])
                if has:
                    _set_default(nc_by_var[consumer], lnk["to_socket_index"], val)
            continue

        if t_go:
            # interior producer → group output
            producer = remap.get(f)
            if producer is None:
                continue
            for tv, tsn, tsi in out_consumers.get(lnk["to_socket_name"], []):
                new_links.append(
                    _link(producer, lnk["from_socket_name"], lnk["from_socket_index"], tv, tsn, tsi)
                )
            continue

        # interior → interior
        fv, tv = remap.get(f), remap.get(t)
        if fv is None or tv is None:
            continue
        nl = dict(lnk)
        nl["from_var"], nl["to_var"] = fv, tv
        new_links.append(nl)

    result_nodes = [n for n in nodes if n["var_name"] != gvar] + new_child_nodes
    result_links = [
        lnk for lnk in links if lnk["from_var"] != gvar and lnk["to_var"] != gvar
    ] + new_links
    return result_nodes, result_links


def _link(fv, fsn, fsi, tv, tsn, tsi) -> dict:
    return {
        "from_var": fv, "from_socket_name": fsn, "from_socket_index": fsi,
        "to_var": tv, "to_socket_name": tsn, "to_socket_index": tsi,
    }
