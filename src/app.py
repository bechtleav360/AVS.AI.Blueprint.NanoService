"""
Main FastAPI application module.

This module creates and configures the FastAPI application.
It automatically detects the environment from configuration and runs
with appropriate settings for development or production.
"""

import logging
from typing import Optional

from fastapi import FastAPI

from src.config import ConfigParameter, ConfigurationManager
from src.controller import configure_routes

# Initialize settings and logger
settings = ConfigurationManager()
logger = logging.getLogger("api")


def create_application() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance
    """
    is_production = settings.get_config(ConfigParameter.APP_ENVIRONMENT) == "production"

    app = FastAPI(
        title=settings.get_config(ConfigParameter.APP_NAME),
        description=settings.get_config(ConfigParameter.APP_DESCRIPTION),
        version=settings.get_config(ConfigParameter.APP_VERSION),
        # Disable docs in production for security
        docs_url=None if is_production else "/docs",
        redoc_url=None if is_production else "/redoc",
        openapi_url=None if is_production else "/openapi.json",
    )

    # Configure routes
    configure_routes(app, settings)

    return app


# Create the application instance
app = create_application()


def run_development(host: str = "0.0.0.0", port: Optional[int] = None) -> None:
    """Run the application in development mode using Uvicorn.

    This is the recommended way to run FastAPI during development.
    It provides auto-reload and debug features.

    Args:
        host: Host to bind to (default: 0.0.0.0)
        port: Port to bind to (default: from config)
    """
    import uvicorn

    if port is None:
        port = settings.get_config(ConfigParameter.APP_PORT)

    logger.info(f"Starting development server on http://{host}:{port}")
    logger.info("Auto-reload enabled. Watching for file changes in 'src/'")

    uvicorn.run(
        "src.app:app",
        host=host,
        port=port,
        reload=True,
        reload_dirs=["src"],
        log_level="debug",
        workers=1,
    )


def run_production(host: str = "0.0.0.0", port: Optional[int] = None) -> None:
    """Run the application in production mode using Uvicorn.

    In a real production environment, you would typically run this using Gunicorn
    with Uvicorn workers. This is provided as a fallback.

    Args:
        host: Host to bind to (default: 0.0.0.0)
        port: Port to bind to (default: from config)
    """
    import multiprocessing

    import uvicorn

    if port is None:
        port = settings.get_config(ConfigParameter.APP_PORT)

    workers = multiprocessing.cpu_count() * 2 + 1

    logger.info(f"Starting production server with {workers} workers on http://{host}:{port}")

    uvicorn.run(
        "src.app:app",
        host=host,
        port=port,
        log_level="info",
        workers=workers,
    )


if __name__ == "__main__":
    # Determine which mode to run in based on configuration
    environment = settings.get_config(ConfigParameter.APP_ENVIRONMENT, "development").lower()

    if environment == "production":
        run_production()
    else:
        run_development()
