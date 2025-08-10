import bpy  # type: ignore


def replace_in_tree(tree, old_ng, new_ng, group_node_type):
    for node in list(tree.nodes):
        if node.type == "GROUP" and node.node_tree == old_ng:
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


class ReplaceNodeGroups(bpy.types.Operator):
    bl_idname = "bpotato.replace_node_groups"
    bl_label = "Replace Node Groups"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        props = context.scene.bpotato
        if not props.old_group_name.strip() or not props.new_group_name.strip():
            self.report({"WARNING"}, "Please select both From and To node groups.")
            return {"CANCELLED"}
        if props.old_group_name == props.new_group_name:
            self.report({"WARNING"}, "From and To node groups are the same.")
            return {"CANCELLED"}
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        props = context.scene.bpotato
        old_name = props.old_group_name
        new_name = props.new_group_name
        mode = props.mode

        old_ng = bpy.data.node_groups.get(old_name)
        new_ng = bpy.data.node_groups.get(new_name)

        if not old_ng:
            self.report({"ERROR"}, f"❗ Node group '{old_name}' not found.")
            return {"CANCELLED"}
        if not new_ng:
            self.report({"ERROR"}, f"❗ Node group '{new_name}' not found.")
            return {"CANCELLED"}
        if old_ng.type != mode or new_ng.type != mode:
            self.report({"ERROR"}, "❗ Node group type does not match the selected mode.")
            return {"CANCELLED"}

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
            return {"CANCELLED"}

        for t in trees:
            replace_in_tree(t, old_ng, new_ng, group_node_type)

        self.report(
            {"INFO"}, f"✅ Replaced '{old_name}' with '{new_name}' in {mode} nodes."
        )
        return {"FINISHED"}
