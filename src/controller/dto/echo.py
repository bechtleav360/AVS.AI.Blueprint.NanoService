"""Echo DTOs for the echo endpoint.

This module contains the request and response DTOs for the echo endpoint.
"""

from datetime import datetime
from typing import Any, Dict, Optional, Union

from pydantic import Field

from src.models.domain import EchoMessage

from .base import BaseRequestDTO, BaseResponseDTO


class EchoRequest(BaseRequestDTO[Dict[str, Any]]):
    """Request DTO for the echo endpoint.

    A flexible input model that can accept any valid JSON structure.
    This allows for dynamic payloads while maintaining validation.
    """

    # This field can accept any JSON-serializable data
    data: Dict[str, Any] = Field(
        default_factory=dict, description="Any JSON data to be echoed back"
    )

    # Optional metadata about the request
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Optional metadata about the request"
    )

    def to_domain(self) -> Dict[str, Any]:
        """Convert this DTO to domain model format.

        Returns:
            Dict containing the domain data
        """
        return {"data": self.data, "metadata": self.metadata or {}}


class EchoResponse(BaseResponseDTO[Dict[str, Any]]):
    """
    Response DTO for the echo endpoint.

    Returns the input data along with processing information.
    """

    # Echo back the input data
    input_data: Dict[str, Any] = Field(
        description="The original input data that was received"
    )

    # Add processing metadata
    processed: bool = Field(
        default=True, description="Indicates if the request was processed successfully"
    )

    processed_timestamp: str = Field(
        description="Timestamp when the request was processed"
    )

    up_timestamp: str = Field(description="Timestamp when the service was started")

    @classmethod
    def from_domain(
        cls, domain_obj: Union[Dict[str, Any], EchoMessage]
    ) -> "EchoResponse":
        """Create an EchoResponse from a domain model object.

        Args:
            domain_obj: The domain model object to convert from, either a dict or EchoMessage

        Returns:
            EchoResponse: A new EchoResponse instance
        """
        if isinstance(domain_obj, EchoMessage):
            return cls(
                input_data=domain_obj.data,
                processed=domain_obj.is_processed,
                processed_timestamp=domain_obj.processed_timestamp.isoformat(),
                up_timestamp=domain_obj.service_start_time.isoformat(),
            )
        else:
            # Handle dict for backward compatibility
            return cls(
                input_data=domain_obj["data"],
                processed=domain_obj.get("is_processed", True),
                processed_timestamp=domain_obj.get(
                    "processed_timestamp", datetime.utcnow().isoformat()
                ),
                up_timestamp=domain_obj.get(
                    "service_start_time", datetime.utcnow().isoformat()
                ),
            )
