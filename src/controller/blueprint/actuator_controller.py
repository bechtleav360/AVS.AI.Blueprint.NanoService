import logging

from fastapi import FastAPI, HTTPException
from prometheus_client import make_asgi_app

from src.config.config import ConfigurationManager
from src.config.params import ConfigParameter
from src.controller.blueprint import BaseController
from src.controller.dto.actuator import (
    HealthResponse,
    InfoResponse,
    LogsResponse,
    ReadinessResponse,
)


class ActuatorController(BaseController):
    """Actuator controller for health checks, status, info, and logs"""

    def __init__(self, settings: ConfigurationManager) -> None:
        self.settings = settings
        self.health: bool = True
        self.info: dict = {}
        self.logs: list = []
        self.logger = logging.getLogger("api.actuators")

    async def check_health(self) -> HealthResponse:
        """Returns current health state"""

        return HealthResponse(health=self.health)

    async def get_info(self) -> InfoResponse:
        """Returns info dictionary with hierarchical environment variables

        Builds a hierarchical JSON structure with the following structure:
        - info
          - app
            - name
            - description
            - ...
          - logs
            - level
            - ...
          - build
            - commit
            - ...
        """
        # Create the hierarchical structure
        info_dict = {"app": {}, "logs": {}, "build": {}}

        # Process app variables
        for key in dir(ConfigParameter):
            if key.startswith("APP_") and not key.startswith("__"):
                try:
                    param = getattr(ConfigParameter, key)
                    value = self.settings.get_config(param)
                    # Remove APP_ prefix and convert to lowercase
                    clean_key = key[4:].lower()
                    info_dict["app"][clean_key] = value
                except Exception:
                    pass

        # Process log variables
        for key in dir(ConfigParameter):
            if key.startswith("LOG_") and not key.startswith("__"):
                try:
                    param = getattr(ConfigParameter, key)
                    value = self.settings.get_config(param)
                    # Remove LOG_ prefix and convert to lowercase
                    clean_key = key[4:].lower()
                    info_dict["logs"][clean_key] = value
                except Exception:
                    pass

        # Process build variables
        for key in dir(ConfigParameter):
            if key.startswith("BUILD_") and not key.startswith("__"):
                try:
                    param = getattr(ConfigParameter, key)
                    value = self.settings.get_config(param)
                    # Remove BUILD_ prefix and convert to lowercase
                    clean_key = key[6:].lower()
                    info_dict["build"][clean_key] = value
                except Exception:
                    pass

        return InfoResponse(info=info_dict)

    async def get_logs(self, log_length: int = 100) -> LogsResponse:
        """Return the last log entries as text

        Args:
            log_length: Number of log lines to return (default: 100)
        """

        try:
            log_file = self.settings.get_config("log_file")
            with open(log_file, "r", encoding="utf-8") as f:
                log_lines = f.readlines()

            # Filter the last log_length lines, then reverse them
            last_logs = log_lines[-log_length:][::-1] if log_length > 0 else []

            processed_logs = []
            for line in last_logs:
                if "Starting flask app" in line:
                    processed_logs.append("\nRESTART\n\n")
                processed_logs.append(line.rstrip())

            return LogsResponse(logs=processed_logs)
        except Exception as e:
            self.logger.error(f"Error retrieving logs: {e}")
            raise HTTPException(status_code=500, detail="Could not read logs.")

    async def check_readiness(self) -> ReadinessResponse:
        """Kubernetes readiness probe endpoint"""

        # Check if configuration is valid using the is_valid() method
        if self.settings.is_valid():
            return ReadinessResponse(ready=True, reason="")
        else:
            reason = self.settings.get_reason()
            # Return HTTP 500 when not ready
            raise HTTPException(status_code=500, detail=reason)

    def register_routes(self, app: FastAPI, url_prefix: str = ""):
        """Register actuator endpoints with a FastAPI app"""

        app.add_api_route(
            path=f"{url_prefix}/health",
            endpoint=self.check_health,
            methods=["GET"],
            response_model=HealthResponse,
            summary="Health Check",
            description="Returns the current health status of the service",
            tags=["actuators"],
        )

        app.add_api_route(
            path=f"{url_prefix}/info",
            endpoint=self.get_info,
            methods=["GET"],
            response_model=InfoResponse,
            summary="Service Information",
            description="Returns metadata and information about the service",
            tags=["actuators"],
        )

        app.add_api_route(
            path=f"{url_prefix}/logs",
            endpoint=self.get_logs,
            methods=["GET"],
            response_model=LogsResponse,
            summary="Service Logs",
            description="Returns log entries as structured data with configurable length",
            tags=["actuators"],
        )

        app.add_api_route(
            path=f"{url_prefix}/ready",
            endpoint=self.check_readiness,
            methods=["GET"],
            response_model=ReadinessResponse,
            summary="Kubernetes Readiness Probe",
            description="Kubernetes readiness probe endpoint that returns true when the service is ready",
            tags=["actuators"],
        )

        # Add prometheus metrics endpoint
        metrics_app = make_asgi_app()
        app.mount("/metrics", metrics_app)

        # FastAPI has built-in OpenAPI/Swagger support
        app.title = self.settings.get_config(ConfigParameter.APP_NAME)
        app.description = self.settings.get_config(ConfigParameter.APP_DESCRIPTION)
        app.version = self.settings.get_config(ConfigParameter.APP_VERSION)
        app.openapi_url = f"{url_prefix}/openapi.json"

        return app
