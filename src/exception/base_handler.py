"""
Base Exception Handler
Handler cơ bản để xử lý exceptions - CHỈ XỬ LÝ EXCEPTIONS, KHÔNG CHỨA LOGIC
"""

import bpy # type: ignore
from typing import Optional, Callable
from functools import wraps

from .model.lspotato_exceptions import LSPotatoException, NetworkException
from ..utils.logger import get_logger, log_exception


class BaseExceptionHandler:
    """
    Base handler để xử lý exceptions
    CHỈ có nhiệm vụ:
    1. Nhận exception
    2. Log exception
    3. Hiển thị message cho user (popup/report)
    """
    
    def __init__(self, feature_name: str = "LSPotato"):
        """
        Initialize handler
        
        Args:
            feature_name: Tên feature (dùng cho logging)
        """
        self.feature_name = feature_name
        self.logger = get_logger(feature_name)
    
    def show_popup(self, title: str, message: str, icon: str = 'ERROR'):
        """
        Hiển thị popup message trong Blender
        
        Args:
            title: Tiêu đề
            message: Nội dung
            icon: Icon type ('ERROR', 'WARNING', 'INFO')
        """
        def draw(self, context):
            lines = message.split('\n')
            for line in lines:
                self.layout.label(text=line)
        
        bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)
    
    def report_to_operator(self, operator: bpy.types.Operator, message: str, level: str = 'ERROR'):
        """
        Report message cho operator
        
        Args:
            operator: Blender operator instance
            message: Message cần report
            level: Mức độ ('ERROR', 'WARNING', 'INFO')
        """
        if hasattr(operator, 'report'):
            operator.report({level}, message)
    
    def get_icon_for_exception(self, exception: Exception) -> str:
        """
        Xác định icon phù hợp cho exception
        Override method này trong subclass để customize
        
        Args:
            exception: Exception instance
            
        Returns:
            Icon name
        """
        if isinstance(exception, NetworkException):
            return 'ERROR'
        
        if isinstance(exception, LSPotatoException):
            return 'ERROR'
        
        return 'ERROR'
    
    def get_error_level(self, exception: Exception) -> str:
        """
        Xác định error level cho exception
        
        Args:
            exception: Exception instance
            
        Returns:
            Level string ('ERROR', 'WARNING', 'INFO')
        """
        if isinstance(exception, NetworkException):
            return 'WARNING'
        
        return 'ERROR'
    
    def handle_exception(
        self,
        exception: Exception,
        operator: Optional[bpy.types.Operator] = None,
        show_popup: bool = True,
        log_traceback: bool = True
    ) -> dict:
        """
        Xử lý exception: log + hiển thị message
        
        Args:
            exception: Exception cần xử lý
            operator: Blender operator (optional)
            show_popup: Có hiển thị popup không
            log_traceback: Có log traceback không
            
        Returns:
            dict: Blender operator return value {'CANCELLED'}
        """
        
        # 1. Log exception
        if log_traceback:
            log_exception(exception, self.feature_name)
        
        # 2. Xác định title, message, icon, level
        if isinstance(exception, LSPotatoException):
            title = type(exception).__name__.replace('Exception', '')
            message = str(exception)
            icon = self.get_icon_for_exception(exception)
            level = self.get_error_level(exception)
        else:
            # Exception không mong đợi
            title = "Lỗi không xác định"
            message = f"Đã xảy ra lỗi: {str(exception)}\n\nKiểm tra console để biết thêm chi tiết"
            icon = 'ERROR'
            level = 'ERROR'
        
        # 3. Report cho operator nếu có
        if operator:
            self.report_to_operator(operator, message, level)
        
        # 4. Hiển thị popup nếu cần
        if show_popup:
            self.show_popup(title, message, icon)
        
        # 5. Log message
        self.logger.error(f"{title}: {message}")
        
        return {'CANCELLED'}


class OperatorExceptionMixin:
    """
    Mixin class để thêm exception handling vào operators
    
    Usage:
        class MyOperator(bpy.types.Operator, OperatorExceptionMixin):
            handler_class = MyFeatureHandler
            
            def execute(self, context):
                return self.safe_execute(self._execute_impl, context)
            
            def _execute_impl(self, context):
                # Implementation - có thể raise exceptions
                return {'FINISHED'}
    """
    
    # Override này trong subclass
    handler_class = BaseExceptionHandler
    
    def _get_handler(self):
        """Lấy handler instance"""
        if not hasattr(self, '_exception_handler'):
            self._exception_handler = self.handler_class()
        return self._exception_handler
    
    def safe_execute(
        self,
        func: Callable,
        context: bpy.types.Context,
        show_popup: bool = True,
        log_traceback: bool = True
    ) -> dict:
        """
        Thực thi function với exception handling
        
        Args:
            func: Function cần thực thi
            context: Blender context
            show_popup: Có hiển thị popup không
            log_traceback: Có log traceback không
            
        Returns:
            dict: Blender operator return value
        """
        handler = self._get_handler()
        
        try:
            return func(context)
        except Exception as e:
            return handler.handle_exception(
                e,
                operator=self,
                show_popup=show_popup,
                log_traceback=log_traceback
            )
    
    def safe_invoke(
        self,
        func: Callable,
        context: bpy.types.Context,
        event: bpy.types.Event,
        show_popup: bool = True,
        log_traceback: bool = True
    ) -> dict:
        """
        Thực thi invoke function với exception handling
        
        Args:
            func: Function cần thực thi
            context: Blender context
            event: Blender event
            show_popup: Có hiển thị popup không
            log_traceback: Có log traceback không
            
        Returns:
            dict: Blender operator return value
        """
        handler = self._get_handler()
        
        try:
            return func(context, event)
        except Exception as e:
            return handler.handle_exception(
                e,
                operator=self,
                show_popup=show_popup,
                log_traceback=log_traceback
            )


def handle_errors(handler_class=BaseExceptionHandler, show_popup: bool = True, log_traceback: bool = True):
    """
    Function decorator để handle errors
    
    Usage:
        @handle_errors(handler_class=AutosyncHandler)
        def my_function(arg1, arg2):
            # your code
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            handler = handler_class()
            try:
                return func(*args, **kwargs)
            except Exception as e:
                handler.handle_exception(
                    e,
                    show_popup=show_popup,
                    log_traceback=log_traceback
                )
                return None
        return wrapper
    return decorator