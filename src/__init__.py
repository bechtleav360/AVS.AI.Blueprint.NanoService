"""
AVS AI Blueprint NanoService

This is the main package for the AVS AI Blueprint NanoService.
It follows a clean architecture pattern with clear separation of concerns.
"""

__version__ = "0.1.0"

# Import subpackages to make them available at the package level
from . import clients, config, controller, models, repositories, services

# Re-export commonly used components
from .app import app

__all__ = [
    "app",
    "config",
    "models",
    "repositories",
    "services",
    "clients",
    "controller",
]
