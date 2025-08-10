import bpy  # type: ignore
import subprocess
import tempfile
import os
from bpy.props import StringProperty  # type: ignore
from ..utils import get_used_groups, get_namespace
from ..config_manager import ConfigManager


class LinkedGraphProperties(bpy.types.PropertyGroup):
    workspace_path: StringProperty(
        name="Workspace Path",
        description="Path to workspace directory",
        subtype="DIR_PATH",
        default="",
    )  # type: ignore


class BrowseWorkspaceOperator(bpy.types.Operator):
    """Browse for workspace directory"""

    bl_idname = "node.browse_workspace"
    bl_label = "Browse Workspace"
    filepath: StringProperty(subtype="DIR_PATH")  # type: ignore

    def execute(self, context):
        context.scene.linked_graph_props.workspace_path = self.filepath
        return {"FINISHED"}

    def invoke(self, context, event):
        if not context.scene.linked_graph_props.workspace_path and bpy.data.filepath:
            self.filepath = os.path.dirname(bpy.data.filepath)
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

        # Set default workspace path if not specified
        if not workspace_path and bpy.data.filepath:
            workspace_path = os.path.dirname(bpy.data.filepath)
            props.workspace_path = workspace_path

        # Get Graphviz path from config
        graphviz_path = ConfigManager.get_graphviz_path()
        dot_executable = os.path.join(
            graphviz_path, "dot.exe" if os.name == "nt" else "dot"
        )

        # Collect node groups
        all_node_groups = [
            g
            for g in bpy.data.node_groups
            if g.bl_idname in {"ShaderNodeTree", "GeometryNodeTree"}
        ]

        # Build and generate DOT content
        dependencies = {g: get_used_groups(g) for g in all_node_groups}
        dot_content = self._generate_dot_content(all_node_groups, dependencies)

        try:
            # Process graph
            dot_path, png_path = self._process_graph(
                dot_content, workspace_path, dot_executable
            )

            if png_path:
                self.report({"INFO"}, f"Graph saved to: {png_path}")
            else:
                self.report({"WARNING"}, f"DOT file saved at: {dot_path}")

        except Exception as e:
            self.report({"ERROR"}, f"Error generating graph: {str(e)}")
            return {"CANCELLED"}

        return {"FINISHED"}

    def _generate_dot_content(self, node_groups, dependencies):
        """Generate DOT format graph content"""
        dot_content = ["digraph G {", "    node [shape=box];"]

        for nt in node_groups:
            namespace = get_namespace(nt)
            dot_content.append(f'    "{nt.name}" [label="{nt.name}\\n({namespace})"];')

        for nt, useds in dependencies.items():
            for used in useds:
                dot_content.append(f'    "{nt.name}" -> "{used.name}";')

        dot_content.append("}")
        return "\n".join(dot_content)

    def _process_graph(self, dot_content, workspace_path, dot_executable):
        """Handle graph generation process"""
        with tempfile.NamedTemporaryFile(suffix=".dot", delete=False, mode="w") as f:
            f.write(dot_content)
            dot_path = f.name

        png_path = dot_path.replace(".dot", ".png")
        result = subprocess.run(
            [dot_executable, "-Tpng", dot_path, "-o", png_path],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            # Save to workspace and clean up
            final_png = os.path.join(workspace_path, "node_graph.png")
            os.replace(png_path, final_png)
            os.remove(dot_path)
            return dot_path, final_png
        else:
            # Save DOT for debugging
            debug_dot = os.path.join(workspace_path, "debug_graph.dot")
            os.replace(dot_path, debug_dot)
            return debug_dot, None
