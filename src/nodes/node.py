import bpy


class Node:

    def draw_buttons(self, context, layout):
        pass

    def createNodetree(self, name):
        pass

    def getNodetree(self, name):
        self.createNodetree(name)

    def addSocket(self, is_output, sockettype, name):
        if is_output == True:
            socket = self.node_tree.interface.new_socket(
                name, in_out="OUTPUT", socket_type=sockettype
            )
        else:
            socket = self.node_tree.interface.new_socket(
                name, in_out="INPUT", socket_type=sockettype
            )

        return socket

    def addNode(self, nodetype, attrs):
        node = self.node_tree.nodes.new(nodetype)
        for attr in attrs:
            self.value_set(node, attr, attrs[attr])
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
    VECT_TRANS_FIX_NAME_1 = ".VectTransFix.NoPanoramic"
    VECT_TRANS_FIX_NAME_2 = ".VectTransFix.Panoramic"
    VECT_TRANS_FIX_NAME_3 = ".VectTransFix.MirrorBall"

    def getMapFix(self):
        fix_mode = getattr(self, "vector_fix_mode", "NO_FIX")

        if fix_mode == "PANORAMIC":
            node_group_name = self.VECT_TRANS_FIX_NAME_2
        elif fix_mode == "MIRROR_BALL":
            node_group_name = self.VECT_TRANS_FIX_NAME_3
        else:
            node_group_name = self.VECT_TRANS_FIX_NAME_1

        if node_group_name in bpy.data.node_groups:
            return bpy.data.node_groups[node_group_name]

        nt = bpy.data.node_groups.new(node_group_name, "ShaderNodeTree")
        nt.color_tag = "VECTOR"
        nt.description = "Parallax vector transform fix"

        out_socket = nt.interface.new_socket(
            name="Result", in_out="OUTPUT", socket_type="NodeSocketVector"
        )
        out_socket.default_value = (0.0, 0.0, 0.0)
        out_socket.min_value = -3.4028234663852886e38
        out_socket.max_value = 3.4028234663852886e38
        out_socket.subtype = "NONE"
        out_socket.attribute_domain = "POINT"

        in_socket = nt.interface.new_socket(
            name="Vector", in_out="INPUT", socket_type="NodeSocketVector"
        )
        in_socket.default_value = (0.0, 0.0, 0.0)
        in_socket.min_value = -3.4028234663852886e38
        in_socket.max_value = 3.4028234663852886e38
        in_socket.subtype = "NONE"
        in_socket.attribute_domain = "POINT"

        GroupInput = nt.nodes.new("NodeGroupInput")
        GroupInput.location = (-600, 0)

        GroupOutput = nt.nodes.new("NodeGroupOutput")
        GroupOutput.location = (400, 0)

        VectorTransform = nt.nodes.new("ShaderNodeVectorTransform")
        VectorTransform.location = (-350, 0)
        VectorTransform.vector_type = "VECTOR"
        VectorTransform.convert_from = "WORLD"
        VectorTransform.convert_to = "CAMERA"

        nt.links.new(GroupInput.outputs["Vector"],
                     VectorTransform.inputs["Vector"])

        if fix_mode == "NO_FIX":
            nt.links.new(
                VectorTransform.outputs["Vector"], GroupOutput.inputs["Result"])
            return nt

        SeparateXYZ = nt.nodes.new("ShaderNodeSeparateXYZ")
        SeparateXYZ.location = (-100, 0)
        nt.links.new(
            VectorTransform.outputs["Vector"], SeparateXYZ.inputs["Vector"])

        CombineXYZ = nt.nodes.new("ShaderNodeCombineXYZ")
        CombineXYZ.location = (200, 0)

        if fix_mode == "PANORAMIC":
            NegateY = nt.nodes.new("ShaderNodeMath")
            NegateY.location = (20, 120)
            NegateY.operation = "MULTIPLY"
            NegateY.inputs[1].default_value = -1.0

            nt.links.new(SeparateXYZ.outputs["Y"], NegateY.inputs[0])
            nt.links.new(NegateY.outputs[0], CombineXYZ.inputs["X"])
            nt.links.new(SeparateXYZ.outputs["Z"], CombineXYZ.inputs["Y"])
            nt.links.new(SeparateXYZ.outputs["X"], CombineXYZ.inputs["Z"])
        else:
            NegateY = nt.nodes.new("ShaderNodeMath")
            NegateY.location = (20, -120)
            NegateY.operation = "MULTIPLY"
            NegateY.inputs[1].default_value = -1.0

            nt.links.new(SeparateXYZ.outputs["X"], CombineXYZ.inputs["X"])
            nt.links.new(SeparateXYZ.outputs["Z"], CombineXYZ.inputs["Y"])
            nt.links.new(SeparateXYZ.outputs["Y"], NegateY.inputs[0])
            nt.links.new(NegateY.outputs[0], CombineXYZ.inputs["Z"])

        nt.links.new(CombineXYZ.outputs["Vector"],
                     GroupOutput.inputs["Result"])

        return nt
