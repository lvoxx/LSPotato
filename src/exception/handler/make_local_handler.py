"""
Make Local Exception Handler
Handler for Make Local feature - HANDLES EXCEPTIONS ONLY
"""

from ..base_handler import BaseExceptionHandler
from ..model.lspotato_exceptions import (
    MakeLocalException,
    NoObjectSelectedException,
    ObjectNotLinkedException,
    LocalizationFailedException
)


class MakeLocalHandler(BaseExceptionHandler):
    """
    Handler for Make Local feature
    ONLY override methods to customize error display
    """
    
    def __init__(self):
        super().__init__("MakeLocal")
    
    def get_icon_for_exception(self, exception: Exception) -> str:
        """Customize icon for MakeLocal exceptions"""
        
        if isinstance(exception, NoObjectSelectedException):
            return 'INFO'
        
        if isinstance(exception, ObjectNotLinkedException):
            return 'ERROR'
        
        if isinstance(exception, LocalizationFailedException):
            return 'ERROR'
        
        return super().get_icon_for_exception(exception)
    
    def get_error_level(self, exception: Exception) -> str:
        """Customize error level"""
        
        if isinstance(exception, NoObjectSelectedException):
            return 'WARNING'
        
        return super().get_error_level(exception)


# Convenience function
def get_make_local_handler() -> MakeLocalHandler:
    """Create and return MakeLocalHandler instance"""
    return MakeLocalHandler()