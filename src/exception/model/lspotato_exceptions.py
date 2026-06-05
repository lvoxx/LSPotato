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


# ============= LSREGISTRY EXCEPTIONS =============

class LSRegistryException(LSPotatoException):
    """Base exception for LSRegistry feature"""
    pass


class RegistryListNotFoundException(LSRegistryException):
    """Exception when Registry List file is not found"""
    def __init__(self, file_path: str):
        super().__init__(
            f"Registry List file not found: {file_path}",
            "Please ensure the registry list file exists and has read permissions"
        )
        self.file_path = file_path
        
class GithubAPIException(LSRegistryException):
    """Exception when calling Github API fails"""
    def __init__(self, status_code: int, reason: str):
        super().__init__(
            f"Github API request failed (Status: {status_code})",
            reason
        )
        self.status_code = status_code


class RegistryYMLNotFoundException(LSRegistryException):
    """Exception when registry.yml is not found in namespace folder"""
    def __init__(self, namespace: str, folder_path: str):
        super().__init__(
            f"registry.yml not found for namespace '{namespace}'",
            f"Search path: {folder_path}"
        )
        self.namespace = namespace
        self.folder_path = folder_path


class InvalidNamespaceException(LSRegistryException):
    """Exception when namespace format is invalid"""
    def __init__(self, namespace: str):
        super().__init__(
            f"Invalid namespace: '{namespace}'",
            "Valid format: io.lvoxx.dummy (separated by dots)"
        )
        self.namespace = namespace


class CredentialsNotFoundException(LSRegistryException):
    """Exception when credentials are required but not found"""
    def __init__(self, namespace: str):
        super().__init__(
            f"Missing credentials for namespace: '{namespace}'",
            "This registry requires credentials. Please provide credentials in the UI"
        )
        self.namespace = namespace


class InvalidCredentialsException(LSRegistryException):
    """Exception when credentials are invalid"""
    def __init__(self, namespace: str, reason: str):
        super().__init__(
            f"Invalid credentials for namespace: '{namespace}'",
            reason
        )
        self.namespace = namespace


class RegistryYMLParseException(LSRegistryException):
    """Exception when parsing registry.yml fails"""
    def __init__(self, file_path: str, reason: str):
        super().__init__(
            f"Failed to parse registry.yml file: {file_path}",
            reason
        )
        self.file_path = file_path


class RegistryDownloadException(LSRegistryException):
    """Exception when downloading registry release fails"""
    def __init__(self, namespace: str, repo_url: str, reason: str):
        super().__init__(
            f"Failed to download registry '{namespace}' from {repo_url}",
            reason
        )
        self.namespace = namespace
        self.repo_url = repo_url


class RegistryExtractionException(LSRegistryException):
    """Exception when extracting registry zip fails"""
    def __init__(self, namespace: str, zip_path: str, reason: str):
        super().__init__(
            f"Failed to extract registry '{namespace}' from {zip_path}",
            reason
        )
        self.namespace = namespace
        self.zip_path = zip_path


class RelativeLinkingException(LSRegistryException):
    """Exception when relatively linking registry to project fails"""
    def __init__(self, namespace: str, registry_path: str, reason: str):
        super().__init__(
            f"Failed to link registry '{namespace}' from {registry_path}",
            reason
        )
        self.namespace = namespace
        self.registry_path = registry_path


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