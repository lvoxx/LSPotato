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


# ============= FIND LSCHERRY EXCEPTIONS =============

class FindLSCherryException(LSPotatoException):
    """Base exception for Find LSCherry feature"""
    pass


class GithubAPIException(FindLSCherryException):
    """Exception when calling Github API fails"""
    def __init__(self, status_code: int, reason: str):
        super().__init__(
            f"Github API request failed (Status: {status_code})",
            reason
        )
        self.status_code = status_code


class ReleaseNotFoundException(FindLSCherryException):
    """Exception when the specified release version is not found"""
    def __init__(self, version: str, repo: str):
        super().__init__(
            f"Release version '{version}' not found in repo '{repo}'",
            "Please check the version tag or verify the release exists in the repo"
        )
        self.version = version
        self.repo = repo


class DownloadException(FindLSCherryException):
    """Exception when downloading release fails"""
    def __init__(self, url: str, reason: str):
        super().__init__(
            f"Failed to download from: {url}",
            reason
        )
        self.url = url


class ExtractionException(FindLSCherryException):
    """Exception when extracting zip file fails"""
    def __init__(self, zip_path: str, reason: str):
        super().__init__(
            f"Failed to extract file: {zip_path}",
            reason
        )
        self.zip_path = zip_path


class LinkingException(FindLSCherryException):
    """Exception when linking library to project fails"""
    def __init__(self, library_path: str, reason: str):
        super().__init__(
            f"Failed to link library: {library_path}",
            reason
        )
        self.library_path = library_path


# ============= CHECK FOR UPDATE EXCEPTIONS =============

class CheckUpdateException(LSPotatoException):
    """Base exception for Check for Update feature"""
    pass


class VersionComparisonException(CheckUpdateException):
    """Exception when version comparison fails"""
    def __init__(self, current_version: str, latest_version: str, reason: str):
        super().__init__(
            f"Failed to compare versions: {current_version} vs {latest_version}",
            reason
        )
        self.current_version = current_version
        self.latest_version = latest_version


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


# ============= MAKE LOCAL EXCEPTIONS =============

class MakeLocalException(LSPotatoException):
    """Base exception for Make Local feature"""
    pass


class NoObjectSelectedException(MakeLocalException):
    """Exception when no object is selected"""
    def __init__(self):
        super().__init__(
            "No object is selected",
            "Please select at least one linked object to localize"
        )


class ObjectNotLinkedException(MakeLocalException):
    """Exception when object is not a linked object"""
    def __init__(self, object_name: str):
        super().__init__(
            f"Object '{object_name}' is not a linked object",
            "Only objects linked from a library can be localized"
        )
        self.object_name = object_name


class LocalizationFailedException(MakeLocalException):
    """Exception when localization fails"""
    def __init__(self, object_name: str, reason: str):
        super().__init__(
            f"Failed to localize object '{object_name}'",
            reason
        )
        self.object_name = object_name


# ============= REPLACE NODES EXCEPTIONS =============

class ReplaceNodesException(LSPotatoException):
    """Base exception for Replace Nodes feature"""
    pass


class NodeNotFoundException(ReplaceNodesException):
    """Exception when the node to be replaced is not found"""
    def __init__(self, node_name: str, node_tree_name: str):
        super().__init__(
            f"Node '{node_name}' not found in node tree '{node_tree_name}'",
            "Please check the node name and node tree"
        )
        self.node_name = node_name
        self.node_tree_name = node_tree_name


class SocketIncompatibilityException(ReplaceNodesException):
    """Exception when sockets are incompatible between old and new nodes"""
    def __init__(self, old_node: str, new_node: str, details: str):
        super().__init__(
            f"Socket incompatibility when replacing '{old_node}' with '{new_node}'",
            details
        )
        self.old_node = old_node
        self.new_node = new_node


class SocketCountMismatchException(ReplaceNodesException):
    """Exception when socket counts don't match"""
    def __init__(self, old_count: int, new_count: int, socket_type: str):
        super().__init__(
            f"{socket_type} socket count mismatch: {old_count} vs {new_count}",
            "New node must have the same number of input/output sockets as the old node"
        )
        self.old_count = old_count
        self.new_count = new_count
        self.socket_type = socket_type


class SocketTypeMismatchException(ReplaceNodesException):
    """Exception when socket types don't match"""
    def __init__(self, socket_name: str, old_type: str, new_type: str):
        super().__init__(
            f"Socket type mismatch for '{socket_name}': {old_type} vs {new_type}",
            "Socket data types must be compatible"
        )
        self.socket_name = socket_name
        self.old_type = old_type
        self.new_type = new_type


class InvalidNodeTreeTypeException(ReplaceNodesException):
    """Exception when node tree type is invalid"""
    def __init__(self, node_tree_type: str):
        super().__init__(
            f"Invalid node tree type: '{node_tree_type}'",
            "Valid types: ShaderNodeTree, GeometryNodeTree, CompositorNodeTree"
        )
        self.node_tree_type = node_tree_type


class NodeReplacementFailedException(ReplaceNodesException):
    """Exception when node replacement fails"""
    def __init__(self, old_node: str, new_node: str, reason: str):
        super().__init__(
            f"Failed to replace '{old_node}' with '{new_node}'",
            reason
        )
        self.old_node = old_node
        self.new_node = new_node


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