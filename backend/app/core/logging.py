"""
Logging configuration for the PlantBot application.

Sets up structured logging with appropriate handlers and formatters.
"""

import logging
import sys
from typing import Any
from app.core.config import get_settings


def setup_logging() -> None:
    """
    Configure application-wide logging with structured format.
    """
    settings = get_settings()

    # Create formatter
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.log_level)
    root_logger.addHandler(console_handler)

    # Application logger
    app_logger = logging.getLogger("plantbot")
    app_logger.setLevel(settings.log_level)

    # Suppress noisy third-party loggers
    logging.getLogger("boto3").setLevel(logging.WARNING)
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name.

    Args:
        name: Name of the logger (usually __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(f"plantbot.{name}")

