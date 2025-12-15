"""
Find LSCherry Exception Handler
Handler for LSCherry feature - HANDLES EXCEPTIONS ONLY
"""

from ..base_handler import BaseExceptionHandler
from ..model.lspotato_exceptions import (
    FindLSCherryException,
    GithubAPIException,
    ReleaseNotFoundException,
    DownloadException,
    ExtractionException,
    LinkingException
)


class LSCherryHandler(BaseExceptionHandler):
    """
    Handler for LSCherry feature
    ONLY override methods to customize error display
    """
    
    def __init__(self):
        super().__init__("FindLSCherry")
    
    def get_icon_for_exception(self, exception: Exception) -> str:
        """Customize icon for LSCherry exceptions"""
        
        if isinstance(exception, GithubAPIException):
            return 'ERROR'
        
        if isinstance(exception, ReleaseNotFoundException):
            return 'ERROR'
        
        if isinstance(exception, (DownloadException, ExtractionException, LinkingException)):
            return 'ERROR'
        
        return super().get_icon_for_exception(exception)


# Convenience function
def get_lscherry_handler() -> LSCherryHandler:
    """Create and return LSCherryHandler instance"""
    return LSCherryHandler()