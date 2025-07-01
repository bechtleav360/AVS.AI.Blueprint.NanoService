from typing import Any, Dict, List

from pydantic import BaseModel, Field


# Define Pydantic models for responses
class HealthResponse(BaseModel):
    health: bool = Field(description="Indicates if the service is healthy")


class StatusResponse(BaseModel):
    status: str = Field(description="Current status of the service")


class InfoResponse(BaseModel):
    info: Dict[str, Any] = Field(
        description="Service information and metadata", default_factory=dict
    )


class LogsResponse(BaseModel):
    logs: List[str] = Field(description="Recent log entries", default_factory=list)


class ReadinessResponse(BaseModel):
    ready: bool = Field(description="Indicates if the service is ready for Kubernetes")
    reason: str = Field(description="Reason for not being ready if ready is false", default="")
