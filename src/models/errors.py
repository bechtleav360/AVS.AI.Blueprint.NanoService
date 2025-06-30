"""
This module defines the error hierarchy for the application.

It provides a set of base exception classes for different HTTP status codes,
which can be used throughout the application to raise appropriate HTTP exceptions.
"""

from typing import Any, Dict, Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Standard error detail model for consistent error responses."""

    code: str = Field(..., description="A machine-readable error code")
    message: str = Field(..., description="A human-readable error message")
    details: Optional[Dict[str, Any]] = Field(
        None, description="Additional error details"
    )


class BaseAPIError(HTTPException):
    """Base class for all API errors.

    This should not be raised directly; use one of the subclasses instead.
    """

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    code: str = "internal_server_error"
    message: str = "An unexpected error occurred"

    def __init__(
        self,
        message: Optional[str] = None,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        self.code = code or self.code
        self.message = message or self.message
        self.details = details

        error_detail = ErrorDetail(
            code=self.code,
            message=self.message,
            details=self.details,
        )

        super().__init__(
            status_code=self.status_code,
            detail=error_detail.model_dump(exclude_none=True),
            headers=headers,
        )


# 4xx Client Errors
class ClientError(BaseAPIError):
    """Base class for all client errors (4xx)."""

    status_code = status.HTTP_400_BAD_REQUEST
    code = "bad_request"
    message = "The request could not be processed"


class BadRequestError(ClientError):
    """400 Bad Request - The request could not be understood or was missing required parameters."""

    code = "bad_request"
    message = "The request could not be processed"


class UnauthorizedError(ClientError):
    """401 Unauthorized - Authentication failed or user doesn't have permissions."""

    status_code = status.HTTP_401_UNAUTHORIZED
    code = "unauthorized"
    message = "Authentication failed or user doesn't have permissions"


class ForbiddenError(ClientError):
    """403 Forbidden - Access to the requested resource is forbidden."""

    status_code = status.HTTP_403_FORBIDDEN
    code = "forbidden"
    message = "Access to the requested resource is forbidden"


class NotFoundError(ClientError):
    """404 Not Found - The requested resource could not be found."""

    status_code = status.HTTP_404_NOT_FOUND
    code = "not_found"
    message = "The requested resource could not be found"


class ConflictError(ClientError):
    """409 Conflict - A conflict occurred while processing the request."""

    status_code = status.HTTP_409_CONFLICT
    code = "conflict"
    message = "A conflict occurred while processing the request"


class ValidationError(ClientError):
    """422 Unprocessable Entity - The request was well-formed but contained semantic errors."""

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    code = "validation_error"
    message = "The request contained validation errors"


# 5xx Server Errors
class ServerError(BaseAPIError):
    """Base class for all server errors (5xx)."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = "internal_server_error"
    message = "An unexpected error occurred"


class InternalServerError(ServerError):
    """500 Internal Server Error - A generic error message for unexpected conditions."""

    code = "internal_server_error"
    message = "An unexpected error occurred"


class NotImplementedError(ServerError):
    """501 Not Implemented - The server does not support the functionality required to fulfill the request."""

    status_code = status.HTTP_501_NOT_IMPLEMENTED
    code = "not_implemented"
    message = "The requested functionality is not implemented"


class ServiceUnavailableError(ServerError):
    """503 Service Unavailable - The server is currently unavailable."""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    code = "service_unavailable"
    message = "The service is currently unavailable"
