"""
Find LSCherry Exception Handler
Handler cho Find LSCherry feature - CHỈ XỬ LÝ EXCEPTIONS
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
    Handler cho Find LSCherry feature
    CHỈ override các method để customize cách hiển thị error
    """
    
    def __init__(self):
        super().__init__("FindLSCherry")
    
    def get_icon_for_exception(self, exception: Exception) -> str:
        """Customize icon cho LSCherry exceptions"""
        
        if isinstance(exception, GithubAPIException):
            return 'ERROR'
        
        if isinstance(exception, ReleaseNotFoundException):
            return 'ERROR'
        
        if isinstance(exception, (DownloadException, ExtractionException, LinkingException)):
            return 'ERROR'
        
        return super().get_icon_for_exception(exception)


# Convenience function
def get_lscherry_handler() -> LSCherryHandler:
    """Tạo và trả về LSCherryHandler instance"""
    return LSCherryHandler()