import bpy  # type: ignore
from .operators import GenerateLinkedGraphOperator


class LinkedGraphPanel(bpy.types.Panel):
    """Panel for Linked Nodes Graph in 3D Viewport"""

    bl_label = "BPotato Tools"
    bl_idname = "VIEW3D_PT_bpotato_tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPotato"

    def draw(self, context):
        layout = self.layout
        props = context.scene.linked_graph_props

        # Ô nhập đường dẫn và nút browse
        box = layout.box()
        row = box.row(align=True)
        row.prop(props, "workspace_path", text="Workspace")
        row.operator("node.browse_workspace", icon="FILE_FOLDER", text="", emboss=True)

        # Nút chính
        layout.operator(
            GenerateLinkedGraphOperator.bl_idname,
            icon="NODETREE",
            text="Generate Node Graph",
        )
