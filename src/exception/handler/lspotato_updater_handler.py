"""
Check for Update Exception Handler
Handler cho Check for Update feature - CHỈ XỬ LÝ EXCEPTIONS
"""

from ..base_handler import BaseExceptionHandler
from ..model.lspotato_exceptions import (
    CheckUpdateException,
    VersionComparisonException,
    GithubAPIException
)


class UpdateCheckerHandler(BaseExceptionHandler):
    """
    Handler cho Check for Update feature
    CHỈ override các method để customize cách hiển thị error
    """
    
    def __init__(self):
        super().__init__("UpdateChecker")
    
    def get_icon_for_exception(self, exception: Exception) -> str:
        """Customize icon cho UpdateChecker exceptions"""
        
        if isinstance(exception, VersionComparisonException):
            return 'INFO'
        
        if isinstance(exception, GithubAPIException):
            return 'ERROR'
        
        return super().get_icon_for_exception(exception)
    
    def get_error_level(self, exception: Exception) -> str:
        """Customize error level"""
        
        if isinstance(exception, VersionComparisonException):
            return 'WARNING'
        
        return super().get_error_level(exception)


# Convenience function
def get_update_checker_handler() -> UpdateCheckerHandler:
    """Tạo và trả về UpdateCheckerHandler instance"""
    return UpdateCheckerHandler()