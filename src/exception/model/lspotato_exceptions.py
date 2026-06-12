"""
LSPotato Custom Exceptions
Defines runtime exceptions for the LSPotato addon
"""


class LSPotatoException(Exception):
    """Base exception for all LSPotato exceptions"""
    def __init__(self, message: str, details: str = None):
        self.message = message
        self.details = details
        super().__init__(self.message)
    
    def __str__(self):
        if self.details:
            return f"{self.message}\nDetails: {self.details}"
        return self.message


# ============= AUTOSYNC EXCEPTIONS =============

class AutosyncException(LSPotatoException):
    """Base exception for Autosync feature"""
    pass


class CherryProviderSyncException(AutosyncException):
    """Exception when syncing Cherry Provider fails"""
    pass


class CollectionNotFoundException(CherryProviderSyncException):
    """Exception when the specified collection is not found"""
    def __init__(self, collection_name: str):
        super().__init__(
            f"Collection not found: '{collection_name}'",
            "Please check the collection name or ensure the collection exists in the scene"
        )
        self.collection_name = collection_name


class SunLightNotFoundException(CherryProviderSyncException):
    """Exception when the specified sun light is not found"""
    def __init__(self, light_name: str):
        super().__init__(
            f"Sun Light not found: '{light_name}'",
            "Please ensure a light with the exact name exists and is of type SUN"
        )
        self.light_name = light_name


class GeometryNodesModifierException(CherryProviderSyncException):
    """Exception when adding/configuring geometry nodes modifier fails"""
    def __init__(self, object_name: str, reason: str):
        super().__init__(
            f"Failed to add Geometry Nodes modifier to object '{object_name}'",
            reason
        )
        self.object_name = object_name


class GlobalConfigSyncException(AutosyncException):
    """Exception when syncing global configuration fails"""
    pass


class InvalidBlendModeException(GlobalConfigSyncException):
    """Exception for invalid blend mode"""
    def __init__(self, blend_mode: str):
        super().__init__(
            f"Invalid blend mode: '{blend_mode}'",
            "Valid blend modes: MIX, ADD, MULTIPLY, SCREEN, OVERLAY"
        )
        self.blend_mode = blend_mode


class InvalidColorValueException(GlobalConfigSyncException):
    """Exception for invalid color value"""
    def __init__(self, color_value: any):
        super().__init__(
            f"Invalid color value: {color_value}",
            "Color must be a tuple/list with 3 or 4 float values in range [0, 1]"
        )
        self.color_value = color_value


# ============= GENERAL EXCEPTIONS =============

class FileSystemException(LSPotatoException):
    """Exception for file system related errors"""
    def __init__(self, operation: str, path: str, reason: str):
        super().__init__(
            f"{operation} error for file/folder: {path}",
            reason
        )
        self.operation = operation
        self.path = path


class NetworkException(LSPotatoException):
    """Exception for network related errors"""
    def __init__(self, url: str, reason: str):
        super().__init__(
            f"Network connection error: {url}",
            reason
        )
        self.url = url


class ConfigurationException(LSPotatoException):
    """Exception for configuration errors"""
    def __init__(self, config_key: str, reason: str):
        super().__init__(
            f"Configuration error for '{config_key}'",
            reason
        )
        self.config_key = config_key