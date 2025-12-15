"""
Replace Nodes Exception Handler
Handler for Replace Nodes feature - HANDLES EXCEPTIONS ONLY
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
    Handler for Replace Nodes feature
    ONLY override methods to customize error display
    """
    
    def __init__(self):
        super().__init__("ReplaceNodes")
    
    def get_icon_for_exception(self, exception: Exception) -> str:
        """Customize icon for ReplaceNodes exceptions"""
        
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