"""Initialize the appstrap top-level module."""

__version__: str = "0.1.0"

from .core import AppStrap


class DefaultAppStrap(AppStrap):
    """Define the default implementation of AppStrap."""

    def __init__(self, create_config_file: bool = False) -> None:
        """Initialize the default AppStrap object."""
        super().__init__(create_config_file)
