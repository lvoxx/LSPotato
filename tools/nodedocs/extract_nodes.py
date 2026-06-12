"""Dev tool: extract ground-truth socket/panel data from the compiled node
files under src/nodes/shader. Writes nodes_data.json next to this script.

This needs no bpy — it parses the generated Python with `ast`. Run with a
plain system Python (3.10+):  python tools/nodedocs/extract_nodes.py
Then run gen_node_docs.py to (re)build docs/nodes/*.md.
"""
import ast
import json
import os

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "src", "nodes", "shader")
ROOT = os.path.abspath(ROOT)


def _const(node):
    """Best-effort literal eval of an AST node."""
    try:
        return ast.literal_eval(node)
    except Exception:
        # tuples of floats etc. may include unary; literal_eval handles those.
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return node.attr
        return None


def kwarg(call, name):
    for kw in call.keywords:
        if kw.arg == name:
            return kw.value
    return None


def parse_file(path):
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)

    result = {
        "class_name": None,
        "bl_idname": None,
        "bl_label": None,
        "draw_label": None,
        "description": None,
        "panels": {},      # varname -> {name, description, parent}
        "panel_order": [],
        "outputs": [],
        "inputs": [],
    }

    cls = None
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            cls = node
            result["class_name"] = node.name
            break
    if cls is None:
        return None

    # class-level bl_idname / bl_label
    for stmt in cls.body:
        if isinstance(stmt, ast.Assign):
            for t in stmt.targets:
                if isinstance(t, ast.Name) and t.id in ("bl_idname", "bl_label"):
                    result[t.id] = _const(stmt.value)
        if isinstance(stmt, ast.FunctionDef) and stmt.name == "draw_label":
            for s in ast.walk(stmt):
                if isinstance(s, ast.Return):
                    result["draw_label"] = _const(s.value)

    # find createNodetree
    create = None
    for stmt in cls.body:
        if isinstance(stmt, ast.FunctionDef) and stmt.name == "createNodetree":
            create = stmt
            break
    if create is None:
        return result

    # socket varname -> dict (so later attr assigns can attach)
    sock_by_var = {}

    for stmt in create.body:
        # assignment: var = nt.interface.new_socket(...) / new_panel(...)
        if isinstance(stmt, ast.Assign) and isinstance(stmt.value, ast.Call):
            call = stmt.value
            func = call.func
            target = stmt.targets[0]
            varname = target.id if isinstance(target, ast.Name) else None
            if (isinstance(func, ast.Attribute) and func.attr == "new_socket"):
                name = _const(kwarg(call, "name"))
                in_out = _const(kwarg(call, "in_out"))
                stype = _const(kwarg(call, "socket_type"))
                parent = kwarg(call, "parent")
                parent_var = parent.id if isinstance(parent, ast.Name) else None
                d = {
                    "name": name,
                    "type": stype,
                    "panel": parent_var,
                    "default": None,
                    "min": None,
                    "max": None,
                    "subtype": None,
                    "description": None,
                }
                if varname:
                    sock_by_var[varname] = d
                if in_out == "OUTPUT":
                    result["outputs"].append(d)
                else:
                    result["inputs"].append(d)
            elif (isinstance(func, ast.Attribute) and func.attr == "new_panel"):
                name = _const(kwarg(call, "name"))
                if varname:
                    result["panels"][varname] = {
                        "name": name, "description": None,
                    }
                    result["panel_order"].append(varname)

        # attribute assignment: var.attr = value
        elif isinstance(stmt, ast.Assign) and isinstance(stmt.targets[0], ast.Attribute):
            tgt = stmt.targets[0]
            if isinstance(tgt.value, ast.Name):
                vn = tgt.value.id
                attr = tgt.attr
                val = _const(stmt.value)
                if vn == "nt" and attr == "description":
                    result["description"] = val
                elif vn in sock_by_var and attr in (
                    "default_value", "min_value", "max_value", "subtype",
                    "description",
                ):
                    key = {"default_value": "default", "min_value": "min",
                           "max_value": "max"}.get(attr, attr)
                    sock_by_var[vn][key] = val
                elif vn in result["panels"] and attr == "description":
                    result["panels"][vn]["description"] = val

    return result


def main():
    out = {}
    for dirpath, _dirs, files in os.walk(ROOT):
        for fn in files:
            if not fn.endswith(".py") or fn == "__init__.py":
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT).replace("\\", "/")
            try:
                data = parse_file(full)
            except Exception as e:
                data = {"error": str(e)}
            if data:
                out[rel] = data
    with open(os.path.join(os.path.dirname(__file__), "nodes_data.json"),
              "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print("files:", len(out))


if __name__ == "__main__":
    main()
