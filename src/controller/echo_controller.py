import logging
from typing import Any, Dict

from fastapi import FastAPI, HTTPException

from src.config import ConfigurationManager
from src.controller import BaseController
from src.controller.dto.echo import EchoRequest, EchoResponse
from src.models import BaseAPIError
from src.services.echo_service import EchoService


class EchoController(BaseController):
    """Controller for handling echo requests.

    This controller maps between API DTOs and domain models,
    handles request/response formatting, and delegates business
    logic to the service layer.
    """

    def __init__(self, settings: ConfigurationManager) -> None:
        """Initialize the echo controller with dependencies."""
        super().__init__(settings)
        self.logger = logging.getLogger("api.echo")
        self.service = EchoService()

    def _request_to_domain(self, request: EchoRequest) -> Dict[str, Any]:
        """Convert an EchoRequest DTO to domain model format.

        Args:
            request: The incoming request DTO

        Returns:
            Dict containing the domain data
        """
        return request.to_domain()

    def _domain_to_response(self, domain_obj: Any) -> EchoResponse:
        """Convert a domain model to an EchoResponse DTO.

        Args:
            domain_obj: The domain model to convert

        Returns:
            EchoResponse: The API response DTO
        """
        return EchoResponse.from_domain(domain_obj)

    async def echo(self, echo_input: EchoRequest) -> EchoResponse:
        """Handle an echo request.

        Args:
            echo_input: The incoming echo request

        Returns:
            EchoResponse: The echo response

        Raises:
            HTTPException: If there's an error processing the request
        """
        try:
            self.logger.info("Processing echo request")

            # Process using domain model
            result = self.service.process_input(echo_input.to_domain())

            self.logger.info("Successfully processed echo request")
            return EchoResponse.from_domain(result)

        except BaseAPIError as e:
            self.logger.exception("API error processing echo request")
            raise HTTPException(status_code=e.status_code, detail=str(e))

        except Exception:
            self.logger.exception("Unexpected error processing echo request")
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while processing your request",
            )

    def register_routes(self, app: FastAPI, url_prefix: str = "") -> None:
        """Register echo endpoints with the FastAPI application.

        Args:
            app: The FastAPI application instance
            url_prefix: Optional URL prefix for all routes
        """
        app.add_api_route(
            path=f"{url_prefix}/echo",
            endpoint=self.echo,
            methods=["POST"],
            response_model=EchoResponse,
            summary="Echo Endpoint",
            description=(
                "Accepts any valid JSON and returns it with additional "
                "processing metadata. Useful for testing and debugging."
            ),
            tags=["echo"],
        )
