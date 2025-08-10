import bpy  # type: ignore
from .operators import GenerateLinkedGraphOperator


class LinkedGraphPanel(bpy.types.Panel):
    """Panel for Linked Nodes Graph"""

    bl_label = "Linked Nodes Graph"
    bl_idname = "NODE_PT_linked_graph"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        props = context.scene.linked_graph_props

        # Thêm ô nhập workspace
        row = layout.row()
        row.prop(props, "workspace_path", text="Workspace")

        # Nút browse để chọn thư mục
        row.operator("node.browse_workspace", icon="FILE_FOLDER", text="")

        layout.operator(GenerateLinkedGraphOperator.bl_idname)
