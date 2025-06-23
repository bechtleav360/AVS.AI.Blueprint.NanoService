"""This file contains the main logic of the sidecar. 
The process method is registered as an api endpoint in flask."""

import logging

from fastapi import HTTPException, FastAPI

from src.api.base_controller import BaseController
from src.common.model.dto.echo import EchoInput, EchoOutput
from src.services.echo_service import EchoService


class EchoController(BaseController):
    """A simple controller for echoing back the input. Should be removed from the actual python service"""

    def __init__(self) -> None:
        self.logger = logging.getLogger("api.process")
        self.service = EchoService()

    async def echo(self, echo_input: EchoInput) -> EchoOutput:
        """Echos the input"""
        try:
            self.logger.info("Received request for echoing")

            step_output = self.service.process_input(echo_input)

            self.logger.info("Echo successfully created")
            
            return step_output
        except Exception as e:
            self.logger.exception("Error processing request")
            raise HTTPException(status_code=400, detail=str(e))

    def register_routes(self, app: FastAPI, url_prefix: str=""):
        """Register Sidecar specific logic endpoints with Flask app
        (other common endpoints like actuators are registered elsewhere)"""

        app.add_api_route(
            path=f"{url_prefix}/echo",
            endpoint=self.echo,
            methods=["POST"],
            response_model=EchoOutput,
            summary="Echo Endpoint",
            description="Accepts any valid JSON and echoes it back with processing metadata",
            tags=["echo"]
        )
