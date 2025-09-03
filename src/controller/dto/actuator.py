"""Actuator DTO module."""

from typing import Any, Dict, List

from pydantic import BaseModel, Field


# Define Pydantic models for responses
class HealthResponse(BaseModel):
    """Health response model."""

    health: bool = Field(description="Indicates if the service is healthy")


class ReadinessResponse(BaseModel):
    """Readiness response model."""

    status: str = Field(description="Current status of the service")


class InfoResponse(BaseModel):
    """Info response model."""

    info: Dict[str, Any] = Field(description="Service information and metadata", default_factory=dict)


class LogsResponse(BaseModel):
    """Logs response model."""

    logs: List[str] = Field(description="Recent log entries", default_factory=list)
