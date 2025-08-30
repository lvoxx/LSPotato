import bpy  # type: ignore


def get_node_groups(self, context):
    mode = self.mode
    items = []
    for ng in bpy.data.node_groups:
        if ng.type == mode:
            desc = ng.library.filepath if ng.library else ""
            items.append((ng.name, ng.name, desc))
    return items


class LSPotatoProperties(bpy.types.PropertyGroup):
    mode: bpy.props.EnumProperty(
        name="Mode",
        items=[
            ("SHADER", "Shader", "Shader node groups"),
            ("GEOMETRY", "Geometry", "Geometry node groups"),
            ("COMPOSITING", "Composition", "Compositing node groups"),
        ],
        default="SHADER",
    )  # type: ignore
    old_group_name: bpy.props.EnumProperty(name="Old Node Group", items=get_node_groups)  # type: ignore
    new_group_name: bpy.props.EnumProperty(name="New Node Group", items=get_node_groups)  # type: ignore
