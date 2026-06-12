"""
NodeCompiler Exceptions
Append these classes into lspotato_exceptions.py manually,
or import from here directly.
"""

from .lspotato_exceptions import LSPotatoException


class NodeCompilerException(LSPotatoException):
    """Base exception for NodeCompiler feature"""
    pass


class BlendFileNotSavedException(NodeCompilerException):
    """Raised when the blend file has not been saved yet"""
    def __init__(self):
        super().__init__(
            "Blend file is not saved",
            "Please save your .blend file before compiling node groups."
        )


class NodeGroupAnalysisException(NodeCompilerException):
    """Raised when analysis of a node group fails"""
    def __init__(self, ng_name: str, reason: str):
        super().__init__(
            f"Failed to analyze node group: '{ng_name}'",
            reason
        )
        self.ng_name = ng_name


class NodeGroupCompileException(NodeCompilerException):
    """Raised when code generation for a node group fails"""
    def __init__(self, ng_name: str, reason: str):
        super().__init__(
            f"Failed to compile node group: '{ng_name}'",
            reason
        )
        self.ng_name = ng_name


class ExportIOException(NodeCompilerException):
    """Raised when writing compiled files fails"""
    def __init__(self, path: str, reason: str):
        super().__init__(
            f"Failed to write file: '{path}'",
            reason
        )
        self.path = path
