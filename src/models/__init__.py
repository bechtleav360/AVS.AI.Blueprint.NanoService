"""Models package for AVS AI Blueprint NanoService.

This package contains all domain models, DTOs, and data structures used
throughout the application.
"""

# Import models here as they are created
# Example:
# from .user import User, UserCreate, UserResponse
from .errors import (
    BadRequestError,
    BaseAPIError,
    ClientError,
    ConflictError,
    ForbiddenError,
    InternalServerError,
    NotFoundError,
    NotImplementedError,
    ServerError,
    ServiceUnavailableError,
    UnauthorizedError,
    ValidationError,
)

__all__: list[str] = [
    "BadRequestError",
    "BaseAPIError",
    "ClientError",
    "ConflictError",
    "ForbiddenError",
    "InternalServerError",
    "NotFoundError",
    "NotImplementedError",
    "ServerError",
    "ServiceUnavailableError",
    "UnauthorizedError",
    "ValidationError",
    # Add model names here as they are added
]
