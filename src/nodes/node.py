import os
import bpy  # type: ignore


# ---------------------------------------------------------------------------
# Compiled-node class registry
#
# Maps a stable node-tree key (cls._PREFIX + cls.bl_label) → the compiled class.
# Populated at addon registration time (see src/__init__.py).  It stores the
# *class object*, not a bpy.types lookup, so nested-group resolution keeps
# working even for classes whose Blender registration failed.
# ---------------------------------------------------------------------------
_NODE_CLASS_REGISTRY: dict = {}

# Parallel index by bl_idname so the Add operator can resolve a class straight
# from the menu's bl_idname (the registry above is keyed by node-tree key).
_NODE_CLASS_BY_IDNAME: dict = {}


def register_node_class(cls) -> None:
    """Record a compiled node class so nested references can resolve it by key."""
    _NODE_CLASS_REGISTRY[cls._PREFIX + cls.bl_label] = cls
    _NODE_CLASS_BY_IDNAME[cls.bl_idname] = cls


def clear_node_registry() -> None:
    """Drop every recorded class (called on addon unregister)."""
    _NODE_CLASS_REGISTRY.clear()
    _NODE_CLASS_BY_IDNAME.clear()


def get_node_class_by_idname(idname: str):
    """Return the compiled class for a bl_idname, or None if unknown."""
    return _NODE_CLASS_BY_IDNAME.get(idname)


def iter_registered_node_classes() -> list:
    """
    Return a snapshot list of (stable_key, cls) for every recorded compiled
    class.  Used by the load-time reconcile pass to refresh stale node trees
    that were saved into a .blend by an older addon version.

    Keyed by the same stable key (cls._PREFIX + cls.bl_label) that
    createNodetree names its datablock, so a saved tree can be matched back to
    the class that currently defines it.
    """
    return list(_NODE_CLASS_REGISTRY.items())


def ensure_node_group(key: str):
    """
    Resolve a nested node group by its stable key.

    Returns the existing datablock if already built, otherwise builds it from
    the registered compiled class.  Returns None only when the key is unknown.
    Generated code uses this instead of a fragile getattr(bpy.types, ...) +
    bpy.data.node_groups.get() fallback.
    """
    ng = bpy.data.node_groups.get(key)
    if ng is not None:
        return ng
    cls = _NODE_CLASS_REGISTRY.get(key)
    if cls is not None:
        return cls.create_node_group()
    return None


def load_packaged_image(filename: str):
    """
    Load a texture shipped inside the addon's nodes/shader/images/ folder.

    Used by compiled nodes whose source group already had an image assigned
    (a *predefined* texture, as opposed to an empty user-input placeholder).
    The image lives next to the lscherry/ tree at src/nodes/shader/images/;
    this file is src/nodes/node.py, so the path is resolved relative to this
    module and is independent of the calling node's folder depth.

    check_existing=True dedupes — a second node referencing the same file
    reuses the already-loaded datablock. A missing file degrades gracefully
    to None (the node behaves like an empty placeholder) instead of raising.
    """
    path = os.path.join(os.path.dirname(__file__), "shader", "images", filename)
    try:
        return bpy.data.images.load(path, check_existing=True)
    except Exception:
        return None


class Node:
    """
    Mixin providing helpers to build a node tree programmatically.
    Independent of any specific node group.
    """

    def draw_buttons(self, context, layout):
        pass

    def createNodetree(self, name):
        """Override in a subclass to build the node tree."""
        pass

    def getNodetree(self, name):
        """
        Called from init(). Locates or builds the shared node tree for this
        compiled node class, then binds it to this node instance.

        All instances of the same class share one node tree under the stable
        key  _PREFIX + bl_label  (matching Blender's own node-group sharing
        model). The tree is built *fully detached* via create_node_group()
        before it is assigned to self.node_tree, so self.inputs / self.outputs
        always sync from a COMPLETE interface in a single assignment.

        This is the same path nested children already use, and it matches the
        behaviour of adding a node when its tree already exists. Binding the
        node to a half-built tree (the old create-then-rebuild approach) left
        deeply-nested high-level nodes desynced on their first add; building
        first and assigning once eliminates that asymmetry.

        The legacy `name` argument is accepted for backward compatibility with
        already-generated init() calls but is no longer used for lookup.
        """
        stable_key = self._PREFIX + self.bl_label
        ng = bpy.data.node_groups.get(stable_key)
        if ng is None:
            # Build the whole tree (and its nested children) detached, then
            # hand back the finished datablock.
            ng = type(self).create_node_group()
        if ng is not None:
            self.node_tree = ng

    @classmethod
    def create_node_group(cls):
        """
        Ensure the class-level node tree exists and return it.

        Called from other compiled nodes' createNodetree when they embed this
        node type as a GROUP node.  Uses a SimpleNamespace proxy so the
        classmethod can drive createNodetree without needing a live Blender
        instance (which is unavailable outside of a node editor interaction).
        """
        key = cls._PREFIX + cls.bl_label
        if key in bpy.data.node_groups:
            return bpy.data.node_groups[key]
        import types
        # valuesUpdate is a no-op on the proxy: a freshly-built shared tree has
        # no image/uv assigned yet, and the proxy is not a real node instance,
        # so the generated trailing  self.valuesUpdate(None)  must not raise.
        proxy = types.SimpleNamespace(
            _PREFIX=cls._PREFIX,
            bl_label=cls.bl_label,
            node_tree=None,
            valuesUpdate=lambda *a, **k: None,
        )
        cls.createNodetree(proxy, key)
        # Return the datablock createNodetree actually created.  Blender clamps
        # ID names to 63 chars and suffixes duplicates, so re-looking-up by the
        # untruncated key can miss — prefer the object the proxy captured.
        if proxy.node_tree is not None:
            return proxy.node_tree
        return bpy.data.node_groups.get(key)

    def addSocket(self, is_output, sockettype, name):
        in_out = "OUTPUT" if is_output else "INPUT"
        return self.node_tree.interface.new_socket(
            name, in_out=in_out, socket_type=sockettype
        )

    def addNode(self, nodetype, attrs):
        node = self.node_tree.nodes.new(nodetype)
        for attr, value in attrs.items():
            self.value_set(node, attr, value)
        return node

    def getNode(self, nodename):
        if self.node_tree.nodes.find(nodename) > -1:
            return self.node_tree.nodes[nodename]
        return None

    def innerLink(self, socketin, socketout):
        SI = self.node_tree.path_resolve(socketin)
        SO = self.node_tree.path_resolve(socketout)
        self.node_tree.links.new(SI, SO)

    def value_set(self, obj, path, value):
        if "." in path:
            path_prop, path_attr = path.rsplit(".", 1)
            prop = obj.path_resolve(path_prop)
        else:
            prop = obj
            path_attr = path
        setattr(prop, path_attr, value)

    def free(self):
        if self.node_tree.users == 1:
            bpy.data.node_groups.remove(self.node_tree, do_unlink=True)


class ShaderNode(Node, bpy.types.ShaderNodeCustomGroup):
    """Base class for every Shader node group."""
    _PREFIX = "."


class GeometryNode(Node, bpy.types.GeometryNodeCustomGroup):
    """Base class for every Geometry node group."""
    _PREFIX = "."
