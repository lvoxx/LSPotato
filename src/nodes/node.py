import bpy  # type: ignore


class Node:
    """
    Mixin chứa các helper để tạo node tree bằng code.
    Không phụ thuộc vào bất kỳ node group cụ thể nào.
    """

    def draw_buttons(self, context, layout):
        pass

    def createNodetree(self, name):
        """Override trong subclass để build node tree."""
        pass

    def getNodetree(self, name):
        """
        Gọi khi init(). Tạo node tree mới nếu chưa tồn tại,
        hoặc reuse nếu đã tồn tại (tránh duplicate khi Blender reload).
        """
        if self._PREFIX + name in bpy.data.node_groups:
            self.node_tree = bpy.data.node_groups[self._PREFIX + name]
        else:
            self.createNodetree(name)

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
    """Base class cho tất cả compiled Shader node groups."""
    _PREFIX = "."


class GeometryNode(Node, bpy.types.GeometryNodeCustomGroup):
    """Base class cho tất cả compiled Geometry node groups."""
    _PREFIX = "."
