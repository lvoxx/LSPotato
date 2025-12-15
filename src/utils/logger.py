"""
LSPotato Logger
Logging utility cho addon LSPotato
"""

import logging
import os
import tempfile
from datetime import datetime
from typing import Optional


class LSPotatoLogger:
    """Logger singleton cho LSPotato addon"""
    
    _instance: Optional[logging.Logger] = None
    _initialized: bool = False
    
    @classmethod
    def get_logger(cls, name: str = "LSPotato") -> logging.Logger:
        """
        Lấy logger instance
        
        Args:
            name: Tên logger (default: "LSPotato")
            
        Returns:
            logging.Logger instance
        """
        if cls._instance is None:
            cls._instance = cls._setup_logger(name)
            cls._initialized = True
        
        return cls._instance
    
    @classmethod
    def _setup_logger(cls, name: str) -> logging.Logger:
        """
        Setup logger với các handlers
        
        Args:
            name: Tên logger
            
        Returns:
            Configured logger
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        # Xóa handlers cũ nếu có
        logger.handlers.clear()
        
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '[%(name)s] %(levelname)s: %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # File Handler - ghi vào temp directory
        cls._add_file_handler(logger)
        
        return logger
    
    @classmethod
    def _add_file_handler(cls, logger: logging.Logger):
        """
        Thêm file handler để log vào temp directory
        
        Args:
            logger: Logger instance
        """
        # Tạo log directory trong temp
        temp_dir = tempfile.gettempdir()
        log_dir = os.path.join(temp_dir, 'lspotato_logs')
        
        try:
            os.makedirs(log_dir, exist_ok=True)
            
            # Tạo log file với timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_file = os.path.join(log_dir, f'lspotato_{timestamp}.log')
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s - [%(name)s] %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
            
            logger.info(f"Log file created: {log_file}")
        
        except Exception as e:
            # Nếu không tạo được file log, chỉ log console
            logger.warning(f"Không thể tạo log file: {e}")
    
    @classmethod
    def set_level(cls, level: int):
        """
        Set logging level
        
        Args:
            level: Logging level (logging.DEBUG, logging.INFO, etc.)
        """
        if cls._instance:
            cls._instance.setLevel(level)
            for handler in cls._instance.handlers:
                if isinstance(handler, logging.StreamHandler):
                    handler.setLevel(level)


# Convenience functions
def get_logger(name: str = "LSPotato") -> logging.Logger:
    """Lấy logger instance"""
    return LSPotatoLogger.get_logger(name)


def log_info(message: str, logger_name: str = "LSPotato"):
    """Log info message"""
    logger = get_logger(logger_name)
    logger.info(message)


def log_warning(message: str, logger_name: str = "LSPotato"):
    """Log warning message"""
    logger = get_logger(logger_name)
    logger.warning(message)


def log_error(message: str, logger_name: str = "LSPotato"):
    """Log error message"""
    logger = get_logger(logger_name)
    logger.error(message)


def log_debug(message: str, logger_name: str = "LSPotato"):
    """Log debug message"""
    logger = get_logger(logger_name)
    logger.debug(message)


def log_exception(exception: Exception, logger_name: str = "LSPotato"):
    """
    Log exception với traceback
    
    Args:
        exception: Exception cần log
        logger_name: Tên logger
    """
    import traceback
    logger = get_logger(logger_name)
    logger.error(f"Exception: {type(exception).__name__}: {str(exception)}")
    logger.error(traceback.format_exc())