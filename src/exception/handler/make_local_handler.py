"""
Make Local Exception Handler
Handler cho Make Local feature - CHỈ XỬ LÝ EXCEPTIONS
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
    Handler cho Make Local feature
    CHỈ override các method để customize cách hiển thị error
    """
    
    def __init__(self):
        super().__init__("MakeLocal")
    
    def get_icon_for_exception(self, exception: Exception) -> str:
        """Customize icon cho MakeLocal exceptions"""
        
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
    """Tạo và trả về MakeLocalHandler instance"""
    return MakeLocalHandler()