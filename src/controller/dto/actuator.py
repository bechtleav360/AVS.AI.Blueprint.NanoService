from pydantic import BaseModel, Field
from typing import Dict, List, Any

# Define Pydantic models for responses
class HealthResponse(BaseModel):
    health: bool = Field(
        description="Indicates if the service is healthy"
    )

class StatusResponse(BaseModel):
    status: str = Field(
        description="Current status of the service"
    )

class InfoResponse(BaseModel):
    info: Dict[str, Any] = Field(
        description="Service information and metadata",
        default_factory=dict
    )

class LogsResponse(BaseModel):
    logs: List[str] = Field(
        description="Recent log entries",
        default_factory=list
    )