"""Define the AppStrap exceptions module."""
from __future__ import annotations


class AppStrapException(Exception):
    """Define the base AppStrap exception."""

    pass


class AppStrapBinaryNotFound(AppStrapException):
    """Define the exception raised when binary is not found in PATH."""

    pass
