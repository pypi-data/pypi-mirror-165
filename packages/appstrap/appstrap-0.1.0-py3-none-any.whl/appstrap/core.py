"""Define the appstrap core logic."""
from __future__ import annotations

import json
import logging
from functools import cached_property

from .utils import setup_logger

logger: logging.Logger = setup_logger(name=__name__)


class AppStrap:
    """Define the configuration interface.

    Args:
        create_config_file (bool, optional): Whether or not to create a configuration file (if absent).
            Defaults to: False.

    """

    def __init__(
        self,
        create_config_file: bool = False,
    ) -> None:
        """Initialize the AppStrap configuration object."""
        logger.info("Initializing AppStrap...")
        self._create_config_file: bool = create_config_file
        logger.info("Creating config file (if absent)?: (%s)", self._create_config_file)

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"<{self.__class__.__name__} - Creating Config File?: ({self._create_config_file})>"

    @cached_property
    def to_json(self) -> str:
        """Return a JSON string representation of the object."""
        return json.dumps(self.__dict__)
