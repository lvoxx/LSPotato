"""
LSPotato Custom Exceptions
Định nghĩa các runtime exception cho addon LSPotato
"""


class LSPotatoException(Exception):
    """Base exception cho tất cả LSPotato exceptions"""
    def __init__(self, message: str, details: str = None):
        self.message = message
        self.details = details
        super().__init__(self.message)
    
    def __str__(self):
        if self.details:
            return f"{self.message}\nChi tiết: {self.details}"
        return self.message


# ============= AUTOSYNC EXCEPTIONS =============

class AutosyncException(LSPotatoException):
    """Base exception cho Autosync feature"""
    pass


class CherryProviderSyncException(AutosyncException):
    """Exception khi sync Cherry Provider thất bại"""
    pass


class CollectionNotFoundException(CherryProviderSyncException):
    """Exception khi không tìm thấy collection được chỉ định"""
    def __init__(self, collection_name: str):
        super().__init__(
            f"Không tìm thấy collection: '{collection_name}'",
            "Kiểm tra lại tên collection hoặc đảm bảo collection tồn tại trong scene"
        )
        self.collection_name = collection_name


class SunLightNotFoundException(CherryProviderSyncException):
    """Exception khi không tìm thấy sun light được chỉ định"""
    def __init__(self, light_name: str):
        super().__init__(
            f"Không tìm thấy Sun Light: '{light_name}'",
            "Đảm bảo đã tạo light với tên chính xác và loại là SUN"
        )
        self.light_name = light_name


class GeometryNodesModifierException(CherryProviderSyncException):
    """Exception khi thêm/cấu hình geometry nodes modifier thất bại"""
    def __init__(self, object_name: str, reason: str):
        super().__init__(
            f"Không thể thêm Geometry Nodes modifier cho object '{object_name}'",
            reason
        )
        self.object_name = object_name


class GlobalConfigSyncException(AutosyncException):
    """Exception khi sync global configuration thất bại"""
    pass


class InvalidBlendModeException(GlobalConfigSyncException):
    """Exception khi blend mode không hợp lệ"""
    def __init__(self, blend_mode: str):
        super().__init__(
            f"Blend mode không hợp lệ: '{blend_mode}'",
            "Các blend mode hợp lệ: MIX, ADD, MULTIPLY, SCREEN, OVERLAY"
        )
        self.blend_mode = blend_mode


class InvalidColorValueException(GlobalConfigSyncException):
    """Exception khi giá trị màu không hợp lệ"""
    def __init__(self, color_value: any):
        super().__init__(
            f"Giá trị màu không hợp lệ: {color_value}",
            "Màu phải là tuple/list với 3 hoặc 4 giá trị float trong khoảng [0, 1]"
        )
        self.color_value = color_value


# ============= FIND LSCHERRY EXCEPTIONS =============

class FindLSCherryException(LSPotatoException):
    """Base exception cho Find LSCherry feature"""
    pass


class GithubAPIException(FindLSCherryException):
    """Exception khi gọi Github API thất bại"""
    def __init__(self, status_code: int, reason: str):
        super().__init__(
            f"Github API request thất bại (Status: {status_code})",
            reason
        )
        self.status_code = status_code


class ReleaseNotFoundException(FindLSCherryException):
    """Exception khi không tìm thấy release version được chỉ định"""
    def __init__(self, version: str, repo: str):
        super().__init__(
            f"Không tìm thấy release version '{version}' trong repo '{repo}'",
            "Kiểm tra lại version tag hoặc xem repo có release này không"
        )
        self.version = version
        self.repo = repo


class DownloadException(FindLSCherryException):
    """Exception khi download release thất bại"""
    def __init__(self, url: str, reason: str):
        super().__init__(
            f"Không thể download từ: {url}",
            reason
        )
        self.url = url


class ExtractionException(FindLSCherryException):
    """Exception khi extract file zip thất bại"""
    def __init__(self, zip_path: str, reason: str):
        super().__init__(
            f"Không thể extract file: {zip_path}",
            reason
        )
        self.zip_path = zip_path


class LinkingException(FindLSCherryException):
    """Exception khi link library vào project thất bại"""
    def __init__(self, library_path: str, reason: str):
        super().__init__(
            f"Không thể link library: {library_path}",
            reason
        )
        self.library_path = library_path


# ============= CHECK FOR UPDATE EXCEPTIONS =============

class CheckUpdateException(LSPotatoException):
    """Base exception cho Check for Update feature"""
    pass


class VersionComparisonException(CheckUpdateException):
    """Exception khi so sánh version thất bại"""
    def __init__(self, current_version: str, latest_version: str, reason: str):
        super().__init__(
            f"Không thể so sánh version: {current_version} vs {latest_version}",
            reason
        )
        self.current_version = current_version
        self.latest_version = latest_version


# ============= LSREGISTRY EXCEPTIONS =============

class LSRegistryException(LSPotatoException):
    """Base exception cho LSRegistry feature"""
    pass


class RegistryListNotFoundException(LSRegistryException):
    """Exception khi không tìm thấy Registry List file"""
    def __init__(self, file_path: str):
        super().__init__(
            f"Không tìm thấy Registry List file: {file_path}",
            "Đảm bảo file registry list tồn tại và có quyền đọc"
        )
        self.file_path = file_path


class RegistryYMLNotFoundException(LSRegistryException):
    """Exception khi không tìm thấy registry.yml trong namespace folder"""
    def __init__(self, namespace: str, folder_path: str):
        super().__init__(
            f"Không tìm thấy registry.yml cho namespace '{namespace}'",
            f"Đường dẫn tìm kiếm: {folder_path}"
        )
        self.namespace = namespace
        self.folder_path = folder_path


class InvalidNamespaceException(LSRegistryException):
    """Exception khi namespace format không hợp lệ"""
    def __init__(self, namespace: str):
        super().__init__(
            f"Namespace không hợp lệ: '{namespace}'",
            "Format hợp lệ: io.lvoxx.dummy (phân cách bằng dấu chấm)"
        )
        self.namespace = namespace


class CredentialsNotFoundException(LSRegistryException):
    """Exception khi credentials được yêu cầu nhưng không tìm thấy"""
    def __init__(self, namespace: str):
        super().__init__(
            f"Thiếu credentials cho namespace: '{namespace}'",
            "Registry này yêu cầu credentials. Cung cấp credentials trong UI"
        )
        self.namespace = namespace


class InvalidCredentialsException(LSRegistryException):
    """Exception khi credentials không hợp lệ"""
    def __init__(self, namespace: str, reason: str):
        super().__init__(
            f"Credentials không hợp lệ cho namespace: '{namespace}'",
            reason
        )
        self.namespace = namespace


class RegistryYMLParseException(LSRegistryException):
    """Exception khi parse registry.yml thất bại"""
    def __init__(self, file_path: str, reason: str):
        super().__init__(
            f"Không thể parse file registry.yml: {file_path}",
            reason
        )
        self.file_path = file_path


class RegistryDownloadException(LSRegistryException):
    """Exception khi download registry release thất bại"""
    def __init__(self, namespace: str, repo_url: str, reason: str):
        super().__init__(
            f"Không thể download registry '{namespace}' từ {repo_url}",
            reason
        )
        self.namespace = namespace
        self.repo_url = repo_url


class RegistryExtractionException(LSRegistryException):
    """Exception khi extract registry zip thất bại"""
    def __init__(self, namespace: str, zip_path: str, reason: str):
        super().__init__(
            f"Không thể extract registry '{namespace}' từ {zip_path}",
            reason
        )
        self.namespace = namespace
        self.zip_path = zip_path


class RelativeLinkingException(LSRegistryException):
    """Exception khi link registry relatively vào project thất bại"""
    def __init__(self, namespace: str, registry_path: str, reason: str):
        super().__init__(
            f"Không thể link registry '{namespace}' từ {registry_path}",
            reason
        )
        self.namespace = namespace
        self.registry_path = registry_path


# ============= MAKE LOCAL EXCEPTIONS =============

class MakeLocalException(LSPotatoException):
    """Base exception cho Make Local feature"""
    pass


class NoObjectSelectedException(MakeLocalException):
    """Exception khi không có object nào được chọn"""
    def __init__(self):
        super().__init__(
            "Không có object nào được chọn",
            "Chọn ít nhất một object linked để localize"
        )


class ObjectNotLinkedException(MakeLocalException):
    """Exception khi object không phải là linked object"""
    def __init__(self, object_name: str):
        super().__init__(
            f"Object '{object_name}' không phải là linked object",
            "Chỉ có thể localize các object được link từ library"
        )
        self.object_name = object_name


class LocalizationFailedException(MakeLocalException):
    """Exception khi localization thất bại"""
    def __init__(self, object_name: str, reason: str):
        super().__init__(
            f"Không thể localize object '{object_name}'",
            reason
        )
        self.object_name = object_name


# ============= REPLACE NODES EXCEPTIONS =============

class ReplaceNodesException(LSPotatoException):
    """Base exception cho Replace Nodes feature"""
    pass


class NodeNotFoundException(ReplaceNodesException):
    """Exception khi không tìm thấy node cần thay thế"""
    def __init__(self, node_name: str, node_tree_name: str):
        super().__init__(
            f"Không tìm thấy node '{node_name}' trong node tree '{node_tree_name}'",
            "Kiểm tra lại tên node và node tree"
        )
        self.node_name = node_name
        self.node_tree_name = node_tree_name


class SocketIncompatibilityException(ReplaceNodesException):
    """Exception khi socket không tương thích giữa node cũ và mới"""
    def __init__(self, old_node: str, new_node: str, details: str):
        super().__init__(
            f"Socket không tương thích khi thay '{old_node}' bằng '{new_node}'",
            details
        )
        self.old_node = old_node
        self.new_node = new_node


class SocketCountMismatchException(ReplaceNodesException):
    """Exception khi số lượng socket khác nhau"""
    def __init__(self, old_count: int, new_count: int, socket_type: str):
        super().__init__(
            f"Số lượng {socket_type} socket không khớp: {old_count} vs {new_count}",
            "Node mới phải có cùng số lượng input/output socket với node cũ"
        )
        self.old_count = old_count
        self.new_count = new_count
        self.socket_type = socket_type


class SocketTypeMismatchException(ReplaceNodesException):
    """Exception khi kiểu socket khác nhau"""
    def __init__(self, socket_name: str, old_type: str, new_type: str):
        super().__init__(
            f"Kiểu socket '{socket_name}' không khớp: {old_type} vs {new_type}",
            "Kiểu dữ liệu của socket phải tương thích"
        )
        self.socket_name = socket_name
        self.old_type = old_type
        self.new_type = new_type


class InvalidNodeTreeTypeException(ReplaceNodesException):
    """Exception khi node tree type không hợp lệ"""
    def __init__(self, node_tree_type: str):
        super().__init__(
            f"Node tree type không hợp lệ: '{node_tree_type}'",
            "Các loại hợp lệ: ShaderNodeTree, GeometryNodeTree, CompositorNodeTree"
        )
        self.node_tree_type = node_tree_type


class NodeReplacementFailedException(ReplaceNodesException):
    """Exception khi thay thế node thất bại"""
    def __init__(self, old_node: str, new_node: str, reason: str):
        super().__init__(
            f"Không thể thay '{old_node}' bằng '{new_node}'",
            reason
        )
        self.old_node = old_node
        self.new_node = new_node


# ============= GENERAL EXCEPTIONS =============

class FileSystemException(LSPotatoException):
    """Exception cho các lỗi liên quan đến file system"""
    def __init__(self, operation: str, path: str, reason: str):
        super().__init__(
            f"Lỗi {operation} file/folder: {path}",
            reason
        )
        self.operation = operation
        self.path = path


class NetworkException(LSPotatoException):
    """Exception cho các lỗi liên quan đến network"""
    def __init__(self, url: str, reason: str):
        super().__init__(
            f"Lỗi kết nối mạng: {url}",
            reason
        )
        self.url = url


class ConfigurationException(LSPotatoException):
    """Exception cho các lỗi cấu hình"""
    def __init__(self, config_key: str, reason: str):
        super().__init__(
            f"Lỗi cấu hình '{config_key}'",
            reason
        )
        self.config_key = config_key