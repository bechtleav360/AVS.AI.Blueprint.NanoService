from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class EchoInput(BaseModel, extra="allow"):
    """
    A flexible input model that can accept any valid JSON structure.
    This allows for dynamic payloads while maintaining validation.
    """
    # This field can accept any JSON-serializable data
    data: Dict[str, Any] = Field(
        default_factory=dict,
        description="Any JSON data to be echoed back"
    )

    # Optional metadata about the request
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional metadata about the request"
    )


class EchoOutput(BaseModel, extra="allow"):
    """
    Response model for the echo endpoint.
    Returns the input data along with processing information.
    """

    # Echo back the input data
    input_data: Dict[str, Any] = Field(
        description="The original input data that was received"
    )

    # Add processing metadata
    processed: bool = Field(
        default=True,
        description="Indicates if the request was processed successfully"
    )

    processed_timestamp: str = Field(
        description="Timestamp when the request was processed"
    )

    up_timestamp: str = Field(
        description="Timestamp when the service was started"
    )