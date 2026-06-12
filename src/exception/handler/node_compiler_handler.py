"""
NodeCompiler Exception Handler
Handler for NodeCompiler feature - HANDLES EXCEPTIONS ONLY
"""

from ..base_handler import BaseExceptionHandler
from ..model.node_compiler_exceptions import (
    NodeCompilerException,
    BlendFileNotSavedException,
    NodeGroupAnalysisException,
    NodeGroupCompileException,
    ExportIOException,
)


class NodeCompilerHandler(BaseExceptionHandler):
    """Handler for NodeCompiler feature"""

    def __init__(self):
        super().__init__("NodeCompiler")

    def get_icon_for_exception(self, exception: Exception) -> str:
        if isinstance(exception, BlendFileNotSavedException):
            return 'FILE_BLEND'
        if isinstance(exception, (NodeGroupAnalysisException, NodeGroupCompileException)):
            return 'NODETREE'
        if isinstance(exception, ExportIOException):
            return 'FILE_FOLDER'
        if isinstance(exception, NodeCompilerException):
            return 'ERROR'
        return super().get_icon_for_exception(exception)
