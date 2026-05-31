import bpy
from .node_imp import NodeLib
from bpy.app.handlers import persistent


class Node_Info(bpy.types.PropertyGroup):
    is_noise_node: bpy.props.BoolProperty(default=False)
    bl_idname: bpy.props.StringProperty()
    dimension: bpy.props.StringProperty()
    ng_name: bpy.props.StringProperty()


@persistent
def convert_nodegroup(dummy=None):
    shadernodes = NodeLib.get_node_sets()
    shader_nodes = [node.__name__ for node in shadernodes]

    # Process Shader Nodes
    for mat in bpy.data.materials:
        if mat.use_nodes and mat.node_tree:
            for node in mat.node_tree.nodes:
                if node.bl_idname in shader_nodes:
                    process_node(mat.node_tree, node)



@persistent
def convert_node(dummy=None):
    is_legacy = False
    nds = []
    # Process Shader Nodes
    for mat in bpy.data.materials:
        if mat.use_nodes and mat.node_tree:
            for node in mat.node_tree.nodes:
                if node.type == 'GROUP' and hasattr(node, 'Node_Info') and node.Node_Info.is_noise_node:
                    itm = process_node_group(mat.node_tree, node)
                    nds.append(itm)
                elif node.bl_idname == "NodeUndefined":
                    is_legacy = True
                    
    


    # Clean up unused node groups
    for nd in bpy.data.node_groups:
        if nd.users == 0:
            bpy.data.node_groups.remove(nd, do_unlink=True)

    # Process node groups
    for nd in nds:
        nd[0].name = nd[1]

    if is_legacy:
        handle_legacy_nodes()
    

def handle_legacy_nodes():
    from .nodes.utils import ShaderNode
    shadernodes = NodeLib.get_node_sets()
    dynamic_classes = []
    # Register dynamic classes
    for shadernode in shadernodes:
        # Define default methods if not present in original node
        def default_init(self, context):
            pass

        def default_createNodetree(self, name):
            node_tree = bpy.data.node_groups.new(name, 'ShaderNodeTree')
            return node_tree

        # Get init and createNodetree methods from original node, or use defaults
        init_method = getattr(shadernode, 'init', default_init)
        createNodetree_method = getattr(
            shadernode, 'createNodetree', default_createNodetree)

        # Create dynamic class inheriting from ShaderNode
        class_dict = {
            'bl_idname': shadernode.bl_label,
            'bl_label': shadernode.bl_label,
            'init': init_method,
            'createNodetree': createNodetree_method
        }
        DynamicSubClass = type(shadernode.bl_label, (ShaderNode,), class_dict)

        
        bpy.utils.register_class(DynamicSubClass)
        dynamic_classes.append(DynamicSubClass)

    # Process materials
    for mat in bpy.data.materials:
        if mat.use_nodes and mat.node_tree:
            for node in mat.node_tree.nodes:
                for shadernode in shadernodes:
                    if node.bl_idname == shadernode.bl_label or node.bl_idname == "NodeUndefined":
                        replace_legacy_node(
                            mat.node_tree, node, shadernode.__name__)
                        break

    # Unregister dynamic classes
    for _class in dynamic_classes:
        bpy.utils.unregister_class(_class)


@persistent
def check_linked_nodes(dummy=None):
    """Check nodes when data is linked or appended."""
    # Check Shader Nodes
    for mat in bpy.data.materials:
        if mat.use_nodes and mat.node_tree:
            for node in mat.node_tree.nodes:
                if hasattr(node, 'Node_Info'):
                    if node.type == 'GROUP' and node.Node_Info.is_noise_node:
                        process_node_group(mat.node_tree, node)



def process_node(node_tree, node):
    try:
        # Determine if this is a shader or geometry node tree
        group_type = "ShaderNodeGroup" if node_tree.type == 'SHADER' else "GeometryNodeGroup"
        new_node = node_tree.nodes.new(group_type)
        new_node.node_tree = node.node_tree
        temp_name = node.name
        new_node.label = node.label
        new_node.location = node.location

        if not hasattr(new_node, 'Node_Info'):
            return

        new_node.Node_Info.is_noise_node = True
        new_node.Node_Info.bl_idname = node.bl_idname
        new_node.Node_Info.ng_name = node.node_tree.name

        if hasattr(node, 'dimension'):
            new_node.Node_Info.dimension = node.dimension

        for input in node.inputs:
            new_input = new_node.inputs.get(input.name)
            if new_input:
                new_input.default_value = input.default_value
                if input.is_linked and input.links:
                    link_out = input.links[0].from_socket
                    node_tree.links.new(link_out, new_input)

        for output in node.outputs:
            new_output = new_node.outputs.get(output.name)
            if new_output and output.is_linked and output.links:
                for link in output.links:
                        link_in = link.to_socket
                        node_tree.links.new(new_output, link_in)

        node_tree.nodes.remove(node)
        new_node.name = temp_name

    except Exception as e:
        print(f"Error processing node {node.name}: {str(e)}")


def process_node_group(node_tree, node):
    try:
        if not hasattr(node, 'Node_Info'):
            return

        new_node = node_tree.nodes.new(node.Node_Info.bl_idname)
        new_node.location = node.location
        temp_name = node.name
        new_node.label = node.label
        ng_name = node.Node_Info.ng_name
        if hasattr(new_node, 'dimension') and node.Node_Info.dimension:
            new_node.dimension = node.Node_Info.dimension

        for input in node.inputs:
            new_input = new_node.inputs.get(input.name)
            if new_input:
                new_input.default_value = input.default_value
                if input.is_linked and input.links:
                    link_out = input.links[0].from_socket
                    node_tree.links.new(link_out, new_input)

        for output in node.outputs:
            new_output = new_node.outputs.get(output.name)
            if new_output and output.is_linked and output.links:
                for link in output.links:
                    if hasattr(link, 'to_socket'):
                        link_in = link.to_socket
                        node_tree.links.new(new_output, link_in)
        node_tree.nodes.remove(node)
        new_node.name = temp_name
        return (new_node.node_tree ,ng_name)

    except Exception as e:
        print(f"Error processing node group {node.name}: {str(e)}")

def replace_legacy_node(node_tree, node , shadernode_id):
    new_node = node_tree.nodes.new(shadernode_id)
    new_node.location = node.location
    new_node.label = node.label
    temp_name = node.name  # Preserve name directly

    # Copy inputs
    for input in node.inputs:
        new_input = new_node.inputs.get(input.name)
        if new_input:
            new_input.default_value = input.default_value
            if input.is_linked and input.links:
                link_out = input.links[0].from_socket
                node_tree.links.new(link_out, new_input)

    # Copy outputs
    for output in node.outputs:
        new_output = new_node.outputs.get(output.name)
        if new_output and output.is_linked and output.links:
            for link in output.links:
                    link_in = link.to_socket
                    node_tree.links.new(new_output, link_in)

    node_tree.nodes.remove(node)
    new_node.name = temp_name
    


@persistent
def convert_legacy_nodes(dummy=None):

    for mat in bpy.data.materials:
        if mat.use_nodes and mat.node_tree:
            for node in mat.node_tree.nodes:
                if node.bl_idname == "ShaderNodeParallax":
                    new_node = mat.node_tree.nodes.new("ShaderNodeParallaxImage")
                    new_node.location = node.location

                    for output in node.outputs:
                        new_output = new_node.outputs.get(output.name)
                        if new_output and output.is_linked and output.links:
                            for link in output.links:
                                link_in = link.to_socket
                                mat.node_tree.links.new(new_output, link_in)

                    new_node.elevation_image = node["elevation_image"]
                    new_node.uv_map = node["uv_map"]
                    new_node.inputs["Iterations"].default_value = node["iterations"]
                    new_node.inputs["Bias"].default_value = node["bias"]
                    new_node.inputs["Depth"].default_value = node["stength"]
                    
                    mat.node_tree.nodes.remove(node)
                    

def ng_register():

    bpy.app.handlers.load_post.append(convert_legacy_nodes)


def ng_unregister():
    pass
