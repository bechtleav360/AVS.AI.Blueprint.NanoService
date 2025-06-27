import logging

from fastapi import FastAPI, HTTPException
from prometheus_client import make_asgi_app

from src.config.config import ConfigurationManager
from src.config.params import ConfigParameter
from src.controller.base_controller import BaseController
from src.controller.dto.actuator import (
    HealthResponse,
    InfoResponse,
    LogsResponse,
    StatusResponse,
)


class ActuatorController(BaseController):
    """Actuator controller for health checks, status, info, and logs"""

    def __init__(self, settings: ConfigurationManager) -> None:
        self.settings = settings
        self.health: bool = True
        self.status: str = "OK"
        self.info: dict = {}
        self.logs: list = []
        self.logger = logging.getLogger("api.actuators")

    async def check_health(self) -> HealthResponse:
        """Returns current health state"""

        return HealthResponse(health=self.health)

    async def get_status(self) -> StatusResponse:
        """Returns current status"""

        return StatusResponse(status=self.status)

    async def get_info(self) -> InfoResponse:
        """Returns info dictionary"""

        return InfoResponse(info=self.info)

    async def get_logs(self) -> LogsResponse:
        """Return the last 300 log entries as text"""

        try:
            log_file = self.settings.get_config("log_file")
            with open(log_file, "r", encoding="utf-8") as f:
                log_lines = f.readlines()

            # Filter the last 300 lines, then reverse them
            last_300_logs = log_lines[-300:][::-1]

            processed_logs = []
            for line in last_300_logs:
                if "Starting flask app" in line:
                    processed_logs.append("\nRESTART\n\n")
                processed_logs.append(line.rstrip())

            return LogsResponse(logs=processed_logs)
        except Exception as e:
            self.logger.error(f"Error retrieving logs: {e}")
            raise HTTPException(status_code=500, detail="Could not read logs.")

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
            path=f"{url_prefix}/status",
            endpoint=self.get_status,
            methods=["GET"],
            response_model=StatusResponse,
            summary="Service Status",
            description="Returns the current status of the service",
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
            description="Returns the last 300 log entries as structured data",
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
