"""
Centralized logging configuration module for the challenge.

Log format: YYYY-MM-DD HH:MM:SS [FILENAME] - LEVEL - MESSAGE

Usage:
    from logger_config import get_logger
    logger = get_logger(__name__)
    logger.info("Processing started")
"""

import logging


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Creates and returns a logger configured with the project format.

    Args:
        name: Module name (use __name__).
        level: Logging level (default: INFO).

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if called multiple times
    if logger.handlers:
        return logger

    logger.setLevel(level)

    # Format: YYYY-MM-DD HH:MM:SS [FILENAME] - LEVEL - MESSAGE
    # %(filename)s automatically resolves to the calling file's name
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(filename)s] - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger
