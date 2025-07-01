from abc import ABC, abstractmethod

from fastapi import FastAPI

from src.config import ConfigurationManager


class BaseController(ABC):
    """Base controller class that all controllers should inherit from"""

    def __init__(self, settings: ConfigurationManager):
        """
        Initialize the base controller with required settings.

        Args:
            settings: The application configuration manager
        """
        self.settings = settings

    @abstractmethod
    def register_routes(self, app: FastAPI, url_prefix: str = "") -> None:
        """
        Register all routes for this controller.

        Args:
            app: The FastAPI application instance
            url_prefix: Optional URL prefix for all routes in this controller
        """
        pass
