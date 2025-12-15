"""
Make Local Operators
Operators cho Make Local feature với exception handling
"""

import bpy # type: ignore

from ...exception.base_handler import OperatorExceptionMixin
from ...exception.handler.make_local_handler import MakeLocalHandler
from ...exception.model.lspotato_exceptions import (
    LocalizationFailedException
)
from ...utils.logger import get_logger


logger = get_logger("MakeLocal")


class MakeLocalOperator(bpy.types.Operator, OperatorExceptionMixin):
    """Make all objects local, removing links"""
    
    bl_idname = "lspotato.make_local"
    bl_label = "Make Local"
    bl_description = "Makes all objects local, removing links. This can help lock the version and make it shareable with others."
    bl_options = {"REGISTER", "UNDO"}
    
    # Chỉ định handler class
    handler_class = MakeLocalHandler

    def invoke(self, context, event):
        # Show confirmation popup
        return context.window_manager.invoke_confirm(self, event)
    
    def execute(self, context):
        return self.safe_execute(self._execute_impl, context)
    
    def _execute_impl(self, context):
        try:
            # Select all objects
            bpy.ops.object.select_all(action="SELECT")
            
            # Make everything local
            bpy.ops.object.make_local(type="ALL")
            
            # Purge unused data
            bpy.ops.outliner.orphans_purge(
                do_local_ids=True, do_linked_ids=True, do_recursive=True
            )
            
        except Exception as e:
            # Throw exception thay vì report error
            raise LocalizationFailedException(
                "all objects",
                f"Không thể make local: {str(e)}"
            )
        
        # Success - report bình thường
        self.report({"INFO"}, "✅ All objects and data made local.")
        logger.info("All objects and data made local.")
        
        return {"FINISHED"}