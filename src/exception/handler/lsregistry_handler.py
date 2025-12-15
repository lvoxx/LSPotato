"""
LSRegistry Exception Handler
Handler for LSRegistry feature - HANDLES EXCEPTIONS ONLY
"""

from ..base_handler import BaseExceptionHandler
from ..model.lspotato_exceptions import (
    LSRegistryException,
    RegistryListNotFoundException,
    RegistryYMLNotFoundException,
    InvalidNamespaceException,
    CredentialsNotFoundException,
    InvalidCredentialsException,
    RegistryYMLParseException,
    RegistryDownloadException,
    RegistryExtractionException,
    RelativeLinkingException
)


class LSRegistryHandler(BaseExceptionHandler):
    """
    Handler for LSRegistry feature
    ONLY override methods to customize error display
    """
    
    def __init__(self):
        super().__init__("LSRegistry")
    
    def get_icon_for_exception(self, exception: Exception) -> str:
        """Customize icon for LSRegistry exceptions"""
        
        if isinstance(exception, (
            RegistryListNotFoundException,
            RegistryYMLNotFoundException
        )):
            return 'ERROR'
        
        if isinstance(exception, InvalidNamespaceException):
            return 'ERROR'
        
        if isinstance(exception, (
            CredentialsNotFoundException,
            InvalidCredentialsException
        )):
            return 'ERROR'
        
        if isinstance(exception, (
            RegistryDownloadException,
            RegistryExtractionException,
            RelativeLinkingException
        )):
            return 'ERROR'
        
        return super().get_icon_for_exception(exception)


# Convenience function
def get_registry_handler() -> LSRegistryHandler:
    """Create and return LSRegistryHandler instance"""
    return LSRegistryHandler()