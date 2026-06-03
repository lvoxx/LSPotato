import bpy  # type: ignore


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
        """
        stable_key = self._PREFIX + self.bl_label
        legacy_key = self._PREFIX + name
        if stable_key in bpy.data.node_groups:
            self.node_tree = bpy.data.node_groups[stable_key]
        elif legacy_key in bpy.data.node_groups:
            self.node_tree = bpy.data.node_groups[legacy_key]
        else:
            self.createNodetree(name)

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
        proxy = types.SimpleNamespace(_PREFIX=cls._PREFIX, bl_label=cls.bl_label, node_tree=None)
        cls.createNodetree(proxy, key)
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
