"""
LSPotato Logger
Logging utility cho addon LSPotato
"""

import logging
import os
import sys
import tempfile
from datetime import datetime
from typing import Optional


class BlenderConsoleHandler(logging.Handler):
    """Custom handler để in INFO messages ra Blender console"""

    def emit(self, record):
        """
        Emit log record ra stdout (Blender console)
        Chỉ xử lý INFO level
        """
        if record.levelno == logging.INFO:
            try:
                msg = self.format(record)
                # In ra stdout để hiển thị trong Blender console
                print(msg)
                sys.stdout.flush()
            except Exception:
                self.handleError(record)


class LSPotatoLogger:
    """Logger singleton cho LSPotato addon"""

    _instance: Optional[logging.Logger] = None
    _initialized: bool = False

    @classmethod
    def get_logger(cls, name: str = "LSPotato") -> logging.Logger:
        """
        Get logger instance

        Args:
            name: Logger name (default: "LSPotato")

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
        Set up logger with handlers

        Args:
            name: Logger name

        Returns:
            Configured logger
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # Remove old handlers if they exist
        logger.handlers.clear()

        # Blender Console Handler - chỉ hiển thị INFO
        blender_console_handler = BlenderConsoleHandler()
        blender_console_handler.setLevel(logging.INFO)
        blender_console_formatter = logging.Formatter("[%(name)s] %(message)s")
        blender_console_handler.setFormatter(blender_console_formatter)
        logger.addHandler(blender_console_handler)

        # File Handler - ghi tất cả levels (DEBUG, INFO, WARNING, ERROR)
        cls._add_file_handler(logger)

        # Prevent propagation to avoid duplicate logs
        logger.propagate = False

        return logger

    @classmethod
    def _add_file_handler(cls, logger: logging.Logger):
        """
        Add file handler to log to temp directory

        Args:
            logger: Logger instance
        """
        # Create log directory in temp
        temp_dir = tempfile.gettempdir()
        log_dir = os.path.join(temp_dir, "lspotato_logs")

        try:
            os.makedirs(log_dir, exist_ok=True)

            # Create log file with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = os.path.join(log_dir, f"lspotato_{timestamp}.log")

            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                "%(asctime)s - [%(name)s] %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

            # Log thông tin về file log (chỉ xuất hiện trong file, không ra console)
            logger.debug(f"Log file created: {log_file}")

        except Exception as e:
            # If log file cannot be created, chỉ log ra console
            print(f"[LSPotato] Warning: Failed to create log file: {e}")

    @classmethod
    def set_level(cls, level: int):
        """
        Set logging level

        Args:
            level: Logging level (logging.DEBUG, logging.INFO, etc.)
        """
        if cls._instance:
            cls._instance.setLevel(level)
            # Chỉ thay đổi level của file handler, giữ nguyên console handler ở INFO
            for handler in cls._instance.handlers:
                if isinstance(handler, logging.FileHandler):
                    handler.setLevel(level)


# Convenience functions
def get_logger(name: str = "LSPotato") -> logging.Logger:
    """Get logger instance"""
    return LSPotatoLogger.get_logger(name)


def log_info(message: str, logger_name: str = "LSPotato"):
    """Log info message (sẽ hiển thị trong Blender console)"""
    logger = get_logger(logger_name)
    logger.info(message)


def log_warning(message: str, logger_name: str = "LSPotato"):
    """Log warning message (chỉ ghi vào file)"""
    logger = get_logger(logger_name)
    logger.warning(message)


def log_error(message: str, logger_name: str = "LSPotato"):
    """Log error message (chỉ ghi vào file)"""
    logger = get_logger(logger_name)
    logger.error(message)


def log_debug(message: str, logger_name: str = "LSPotato"):
    """Log debug message (chỉ ghi vào file)"""
    logger = get_logger(logger_name)
    logger.debug(message)


def log_exception(exception: Exception, logger_name: str = "LSPotato"):
    """
    Log exception with traceback (chỉ ghi vào file)

    Args:
        exception: Exception to log
        logger_name: Logger name
    """
    import traceback

    logger = get_logger(logger_name)
    logger.error(f"Exception: {type(exception).__name__}: {str(exception)}")
    logger.error(traceback.format_exc())
