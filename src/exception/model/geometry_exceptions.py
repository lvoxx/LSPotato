"""
Geometry-library Exceptions
Raised by the runtime geometry loader (src/nodes/geometry/loader.py) when the
shipped geometry library/manifest is missing or a node group cannot be appended.

These subclass LSPotatoException, so the default BaseExceptionHandler renders
them generically — no dedicated handler class is required.
"""

from .lspotato_exceptions import LSPotatoException


class GeometryLibraryException(LSPotatoException):
    """Base exception for the geometry-node library loader."""
    pass


class GeometryLibraryMissingException(GeometryLibraryException):
    """Raised when the shipped library.blend or hashes.json is absent."""
    def __init__(self, missing_path: str):
        super().__init__(
            "Geometry library is missing",
            f"Expected file not found: '{missing_path}'. "
            "Geometry initialization was skipped."
        )
        self.missing_path = missing_path


class GeometryAppendException(GeometryLibraryException):
    """Raised when a geometry node group cannot be appended from the library."""
    def __init__(self, group_name: str, reason: str):
        super().__init__(
            f"Failed to append geometry node group: '{group_name}'",
            reason
        )
        self.group_name = group_name
