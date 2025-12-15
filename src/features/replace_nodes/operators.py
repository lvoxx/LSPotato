"""
Replace Node Groups Operators
Operators for Replace Nodes feature with exception handling
"""

import bpy # type: ignore

from ...exception.base_handler import OperatorExceptionMixin
from ...exception.handler.replace_node_handler import ReplaceNodesHandler
from ...exception.model.lspotato_exceptions import (
    NodeNotFoundException,
    InvalidNodeTreeTypeException,
    NodeReplacementFailedException
)
from ...utils.logger import get_logger


logger = get_logger("ReplaceNodes")


def replace_in_tree(tree, old_ng, new_ng, group_node_type):
    """
    Replace node groups in a node tree
    
    Args:
        tree: Node tree
        old_ng: Old node group
        new_ng: New node group
        group_node_type: Type of group node ("ShaderNodeGroup", etc.)
        
    Raises:
        NodeReplacementFailedException: If replacement fails
    """
    for node in list(tree.nodes):
        if node.type == "GROUP" and node.node_tree == old_ng:
            try:
                new_node = tree.nodes.new(type=group_node_type)
                new_node.node_tree = new_ng
                new_node.location = node.location
                new_node.width = node.width
                new_node.label = node.label

                # Map inputs and outputs by identifier
                input_map = {inp.identifier: inp for inp in new_node.inputs}
                output_map = {out.identifier: out for out in new_node.outputs}

                # Copy default values and links for inputs
                for inp in node.inputs:
                    if inp.identifier in input_map:
                        target_inp = input_map[inp.identifier]
                        if not inp.is_linked:
                            target_inp.default_value = inp.default_value
                        for link in inp.links:
                            tree.links.new(link.from_socket, target_inp)

                # Copy links for outputs
                for out in node.outputs:
                    if out.identifier in output_map:
                        target_out = output_map[out.identifier]
                        for link in out.links:
                            tree.links.new(target_out, link.to_socket)

                # Remove old node
                tree.nodes.remove(node)
            
            except Exception as e:
                raise NodeReplacementFailedException(
                    node.name,
                    group_node_type,
                    f"Error replacing node in tree '{tree.name}': {str(e)}"
                )


class ReplaceNodeGroups(bpy.types.Operator, OperatorExceptionMixin):
    """Replace node groups across the entire file"""
    
    bl_idname = "lspotato.replace_node_groups"
    bl_label = "Replace"
    bl_options = {"REGISTER", "UNDO"}
    
    # Specify handler class
    handler_class = ReplaceNodesHandler

    def invoke(self, context, event):
        return self.safe_invoke(self._invoke_impl, context, event)
    
    def _invoke_impl(self, context, event):
        props = context.scene.lspotato
        
        # Throw exceptions thay vì report
        if not props.old_group_name.strip() or not props.new_group_name.strip():
            raise NodeNotFoundException(
                "old/new group",
                "scene.lspotato"
            )
        
        if props.old_group_name == props.new_group_name:
            raise InvalidNodeTreeTypeException(
                "From and To node groups are the same"
            )
        
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        return self.safe_execute(self._execute_impl, context)
    
    def _execute_impl(self, context):
        props = context.scene.lspotato
        old_name = props.old_group_name
        new_name = props.new_group_name
        mode = props.mode

        old_ng = bpy.data.node_groups.get(old_name)
        new_ng = bpy.data.node_groups.get(new_name)

        # Throw exceptions instead of report and return CANCELLED
        if not old_ng:
            raise NodeNotFoundException(old_name, "bpy.data.node_groups")
        
        if not new_ng:
            raise NodeNotFoundException(new_name, "bpy.data.node_groups")
        
        if old_ng.type != mode or new_ng.type != mode:
            raise InvalidNodeTreeTypeException(
                f"Node group type does not match mode {mode}"
            )

        # Get trees theo mode
        if mode == "SHADER":
            trees = (
                [mat.node_tree for mat in bpy.data.materials if mat.node_tree]
                + [w.node_tree for w in bpy.data.worlds if w.node_tree]
                + [ng for ng in bpy.data.node_groups if ng.type == "SHADER"]
            )
            group_node_type = "ShaderNodeGroup"
        
        elif mode == "GEOMETRY":
            # Replace top-level references in modifiers
            for obj in bpy.data.objects:
                for mod in obj.modifiers:
                    if mod.type == "NODES" and mod.node_group == old_ng:
                        mod.node_group = new_ng
            
            trees = [ng for ng in bpy.data.node_groups if ng.type == "GEOMETRY"]
            group_node_type = "GeometryNodeGroup"
        
        elif mode == "COMPOSITING":
            trees = [sc.node_tree for sc in bpy.data.scenes if sc.node_tree] + [
                ng for ng in bpy.data.node_groups if ng.type == "COMPOSITING"
            ]
            group_node_type = "CompositorNodeGroup"
        
        else:
            raise InvalidNodeTreeTypeException(f"Invalid mode: {mode}")

        # Replace in each tree
        for t in trees:
            replace_in_tree(t, old_ng, new_ng, group_node_type)

        # Success - normal report
        self.report(
            {"INFO"}, f"✅ Replaced '{old_name}' with '{new_name}' in {mode} nodes."
        )
        logger.info(f"Replaced '{old_name}' with '{new_name}' in {mode} nodes.")
        
        return {"FINISHED"}