import bpy  # type: ignore
import subprocess
import tempfile
import os
from bpy.props import StringProperty  # type: ignore
from .utils import get_used_groups, get_namespace


# Thêm properties để lưu workspace path
class LinkedGraphProperties(bpy.types.PropertyGroup):
    workspace_path: StringProperty(
        name="Workspace Path",
        description="Path to workspace directory",
        subtype="DIR_PATH",
        default="",
    )  # pyright: ignore[reportInvalidTypeForm]


class BrowseWorkspaceOperator(bpy.types.Operator):
    """Browse for workspace directory"""

    bl_idname = "node.browse_workspace"
    bl_label = "Browse Workspace"
    filepath: StringProperty(
        subtype="DIR_PATH"
    )  # pyright: ignore[reportInvalidTypeForm]

    def execute(self, context):
        context.scene.linked_graph_props.workspace_path = self.filepath
        return {"FINISHED"}

    def invoke(self, context, event):
        # Set default path là thư mục file hiện tại nếu chưa có
        if not context.scene.linked_graph_props.workspace_path:
            if bpy.data.filepath:
                default_path = os.path.dirname(bpy.data.filepath)
                self.filepath = default_path
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


class GenerateLinkedGraphOperator(bpy.types.Operator):
    """Generate Graph of Linked Node Groups"""

    bl_idname = "node.generate_linked_graph"
    bl_label = "Generate Linked Nodes Graph"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.linked_graph_props
        workspace_path = props.workspace_path

        # Nếu không có workspace path, sử dụng thư mục file hiện tại
        if not workspace_path and bpy.data.filepath:
            workspace_path = os.path.dirname(bpy.data.filepath)
            props.workspace_path = workspace_path  # Cập nhật lại property

        # Collect all relevant node groups (shader and geometry)
        all_node_groups = [
            g
            for g in bpy.data.node_groups
            if g.bl_idname in {"ShaderNodeTree", "GeometryNodeTree"}
        ]

        # Build dependencies
        dependencies = {g: get_used_groups(g) for g in all_node_groups}

        # Generate DOT content
        dot_content = "digraph G {\n"
        dot_content += "    node [shape=box];\n"

        for nt in all_node_groups:
            namespace = get_namespace(nt)
            label = f"{nt.name}\\n({namespace})"
            dot_content += f'    "{nt.name}" [label="{label}"];\n'

        for nt, useds in dependencies.items():
            for used in useds:
                dot_content += f'    "{nt.name}" -> "{used.name}";\n'

        dot_content += "}\n"

        # Write to temporary DOT file
        try:
            with tempfile.NamedTemporaryFile(
                suffix=".dot", delete=False, mode="w"
            ) as f:
                f.write(dot_content)
                dot_path = f.name

            # Generate PNG using graphviz (requires graphviz installed)
            png_path = dot_path.replace(".dot", ".png")
            result = subprocess.run(
                ["dot", "-Tpng", dot_path, "-o", png_path], capture_output=True
            )

            if result.returncode == 0:
                # Load the image into Blender
                img = bpy.data.images.load(png_path, check_existing=True)
                self.report(
                    {"INFO"}, f"Graph image loaded: {img.name}. View in Image Editor."
                )
                # Optionally clean up
                os.remove(dot_path)
                os.remove(png_path)
            else:
                self.report(
                    {"WARNING"},
                    f"Graphviz not found or failed. DOT file saved at: {dot_path}",
                )
        except Exception as e:
            self.report({"ERROR"}, f"Error generating graph: {str(e)}")

        return {"FINISHED"}
