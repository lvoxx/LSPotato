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


def register_node_class(cls) -> None:
    """Record a compiled node class so nested references can resolve it by key."""
    _NODE_CLASS_REGISTRY[cls._PREFIX + cls.bl_label] = cls


def clear_node_registry() -> None:
    """Drop every recorded class (called on addon unregister)."""
    _NODE_CLASS_REGISTRY.clear()


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
        Called from init(). Locates or creates the shared node tree for this
        compiled node class.

        New compiled nodes use the stable key  _PREFIX + bl_label  so all
        instances of the same class share one node tree (matching Blender's
        own node-group sharing model).  The instance-name-based legacy key is
        tried second so that older compiled files continue to work.

        After createNodetree() we re-assign self.node_tree even though it was
        already set inside createNodetree.  The reason: Blender syncs
        self.inputs / self.outputs from the node group interface at the moment
        of assignment, but createNodetree() adds sockets *after* that first
        assignment, so self.inputs is empty when init() tries to set defaults.
        The second assignment fires the RNA update again, this time with a
        fully-populated interface, making self.inputs ready for use.
        """
        stable_key = self._PREFIX + self.bl_label
        legacy_key = self._PREFIX + name
        if stable_key in bpy.data.node_groups:
            self.node_tree = bpy.data.node_groups[stable_key]
        elif legacy_key in bpy.data.node_groups:
            self.node_tree = bpy.data.node_groups[legacy_key]
        else:
            self.createNodetree(name)
            # Re-sync self.inputs after sockets were added to the new tree.
            if stable_key in bpy.data.node_groups:
                self.node_tree = bpy.data.node_groups[stable_key]

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
