"""
Init Geometry Nodes — operator.

Manual button that appends the shipped LSCherry geometry node groups into the
current .blend (skipping unchanged ones, refreshing stale ones). Applying them
as modifiers onto objects is handled separately by autosync.
"""

import bpy  # type: ignore

from ...exception.base_handler import OperatorExceptionMixin
from ...utils.logger import get_logger
from ...nodes.geometry.loader import init_geometry_nodes

logger = get_logger("InitGeometry")


class LSPOTATO_OT_init_geometry_nodes(bpy.types.Operator, OperatorExceptionMixin):
    """Append the LSCherry geometry node groups into this file"""

    bl_idname  = "lspotato.init_geometry_nodes"
    bl_label   = "Init Geometry Nodes"
    bl_description = (
        "Append the shipped LSCherry geometry node groups into the current file. "
        "Unchanged groups are skipped; out-of-date groups are refreshed."
    )
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        # Mutates the open file, so confirm first.
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        return self.safe_execute(self._execute_impl, context)

    def _execute_impl(self, context):
        result = init_geometry_nodes()

        if result["missing"]:
            self.report(
                {"WARNING"},
                f"Geometry library missing ({result['missing']}). Initialization skipped.",
            )
            return {"CANCELLED"}

        msg = (
            f"Geometry nodes: {result['appended']} appended, "
            f"{result['overwritten']} updated, {result['skipped']} unchanged"
        )
        if result["failed"]:
            msg += f", {result['failed']} failed (see console)"
            self.report({"WARNING"}, msg)
        else:
            self.report({"INFO"}, msg)
        return {"FINISHED"}
