"""Define utility logic for appstrap."""
from __future__ import annotations

import logging
import os


def setup_logger(
    name: str, log_level: str = "", enable_log_file: bool = False, log_file_level: str = "", log_format: str = ""
) -> logging.Logger:
    """Set up the logger.

    Args:
        name: The name of the logger.
        log_level: The log level.
        enable_log_file: Whether to enable logging to a file.
        log_file_level: The log level for the log file.
        log_format: The log format.

    Returns:
        The logger.

    """
    # Setup logger input values.
    _log_level: str = log_level or os.getenv("APPSTRAP_LOG_LEVEL", "INFO")
    _log_format: str = log_format or os.getenv(
        "APPSTRAP_LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(_log_level)

    # Create the console handler and set level based on input or environment log level.
    log_handler: logging.StreamHandler = logging.StreamHandler()
    log_handler.setLevel(_log_level)

    # Define the log format.
    formatter: logging.Formatter = logging.Formatter(_log_format)
    log_handler.setFormatter(formatter)

    if enable_log_file:
        _log_file_level: str = log_file_level or os.getenv("APPSTRAP_LOG_FILE_LEVEL", "INFO")
        log_file_handler: logging.FileHandler = logging.FileHandler(filename=f"{name}.log", mode="w", encoding="utf-8")
        log_file_handler.setLevel(_log_file_level)

        # Add the log handler to the logger.
        logger.addHandler(log_file_handler)

    # Add the log handler to the logger.
    logger.addHandler(log_handler)
    return logger
