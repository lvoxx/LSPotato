"""
Autosync Exception Handler
Handler cho Autosync feature - CHỈ XỬ LÝ EXCEPTIONS
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
    Handler cho Autosync feature
    CHỈ override các method để customize cách hiển thị error
    """
    
    def __init__(self):
        super().__init__("Autosync")
    
    def get_icon_for_exception(self, exception: Exception) -> str:
        """Customize icon cho Autosync exceptions"""
        
        if isinstance(exception, (CollectionNotFoundException, SunLightNotFoundException)):
            return 'ERROR'
        
        if isinstance(exception, GeometryNodesModifierException):
            return 'ERROR'
        
        if isinstance(exception, (InvalidBlendModeException, InvalidColorValueException)):
            return 'ERROR'
        
        return super().get_icon_for_exception(exception)


# Convenience function
def get_autosync_handler() -> AutosyncHandler:
    """Tạo và trả về AutosyncHandler instance"""
    return AutosyncHandler()