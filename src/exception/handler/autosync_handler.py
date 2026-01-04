"""
Autosync Exception Handler
Handler for Autosync feature - HANDLES EXCEPTIONS ONLY
"""

from ..base_handler import BaseExceptionHandler
from ..model.lspotato_exceptions import (
    AutosyncException,
    CollectionNotFoundException,
    SunLightNotFoundException,
    GeometryNodesModifierException,
    InvalidBlendModeException,
    InvalidColorValueException
)


class AutosyncHandler(BaseExceptionHandler):
    """
    Handler for Autosync feature
    ONLY override methods to customize error display
    """
    
    def __init__(self):
        super().__init__("Autosync")
    
    def get_icon_for_exception(self, exception: Exception) -> str:
        """Customize icon for Autosync exceptions"""
        
        if isinstance(exception, (CollectionNotFoundException, SunLightNotFoundException)):
            return 'ERROR'
        
        if isinstance(exception, GeometryNodesModifierException):
            return 'ERROR'
        
        if isinstance(exception, (InvalidBlendModeException, InvalidColorValueException)):
            return 'ERROR'
        
        return super().get_icon_for_exception(exception)


# Convenience function
def get_autosync_handler() -> AutosyncHandler:
    """Create and return AutosyncHandler instance"""
    return AutosyncHandler()