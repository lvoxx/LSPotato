"""
Replace Nodes Exception Handler
Handler cho Replace Nodes feature - CHỈ XỬ LÝ EXCEPTIONS
"""

from ..base_handler import BaseExceptionHandler
from ..model.lspotato_exceptions import (
    ReplaceNodesException,
    NodeNotFoundException,
    SocketIncompatibilityException,
    SocketCountMismatchException,
    SocketTypeMismatchException,
    InvalidNodeTreeTypeException,
    NodeReplacementFailedException
)


class ReplaceNodesHandler(BaseExceptionHandler):
    """
    Handler cho Replace Nodes feature
    CHỈ override các method để customize cách hiển thị error
    """
    
    def __init__(self):
        super().__init__("ReplaceNodes")
    
    def get_icon_for_exception(self, exception: Exception) -> str:
        """Customize icon cho ReplaceNodes exceptions"""
        
        if isinstance(exception, NodeNotFoundException):
            return 'ERROR'
        
        if isinstance(exception, (
            SocketIncompatibilityException,
            SocketCountMismatchException,
            SocketTypeMismatchException
        )):
            return 'ERROR'
        
        if isinstance(exception, InvalidNodeTreeTypeException):
            return 'ERROR'
        
        if isinstance(exception, NodeReplacementFailedException):
            return 'ERROR'
        
        return super().get_icon_for_exception(exception)


# Convenience function
def get_replace_nodes_handler() -> ReplaceNodesHandler:
    """Tạo và trả về ReplaceNodesHandler instance"""
    return ReplaceNodesHandler()