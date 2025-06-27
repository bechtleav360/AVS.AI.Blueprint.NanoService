"""Base DTO (Data Transfer Object) module.

This module provides base classes for DTOs with common functionality
for converting between DTOs and domain models.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Optional, Type, TypeVar

from pydantic import BaseModel

# Type variables for domain model types
D = TypeVar("D")  # Domain type
R = TypeVar("R")  # Request DTO type
S = TypeVar("S")  # Response DTO type


class BaseRequestDTO(BaseModel, ABC, Generic[D]):
    """Base class for all request DTOs.

    Request DTOs are used to validate and convert incoming request data
    to domain models.
    """

    @abstractmethod
    def to_domain(self) -> D:
        """Convert this request DTO to a domain model object.

        Returns:
            The domain model object
        """
        raise NotImplementedError("Subclasses must implement to_domain")


class BaseResponseDTO(BaseModel, ABC, Generic[D]):
    """Base class for all response DTOs.

    Response DTOs are used to convert domain models to API responses.
    """

    @classmethod
    @abstractmethod
    def from_domain(cls: Type["BaseResponseDTO"], domain_obj: D) -> "BaseResponseDTO":
        """Create a response DTO from a domain model object.

        This is a factory method that creates a new response DTO instance
        from a domain model object.


        Args:
            domain_obj: The domain model object to convert from

        Returns:
            A new instance of the response DTO class
        """
        raise NotImplementedError("Subclasses must implement from_domain")

    @classmethod
    def from_domain_optional(
        cls: Type["BaseResponseDTO"], domain_obj: Optional[D]
    ) -> Optional["BaseResponseDTO"]:
        """Safely create a response DTO from an optional domain object.

        This is a convenience method that handles the case where the domain object
        might be None.

        Args:
            domain_obj: The domain model object to convert from, or None

        Returns:
            A new response DTO instance if domain_obj is not None, otherwise None
        """
        if domain_obj is None:
            return None
        return cls.from_domain(domain_obj)

    @classmethod
    def from_domain_list(
        cls: Type["BaseResponseDTO"], domain_objs: list[D]
    ) -> list["BaseResponseDTO"]:
        """Convert a list of domain objects to a list of response DTOs.

        This is a convenience method that converts a list of domain objects
        to a list of response DTOs using the class's from_domain method.

        Args:
            domain_objs: List of domain model objects to convert

        Returns:
            List of new response DTO instances
        """
        return [cls.from_domain(obj) for obj in domain_objs]

    @classmethod
    def from_domain_dict(
        cls: Type["BaseResponseDTO"], domain_objs: Dict[Any, D]
    ) -> Dict[Any, "BaseResponseDTO"]:
        """Convert a dictionary of domain objects to a dictionary of response DTOs.

        This is a convenience method that converts a dictionary of domain objects
        to a dictionary of response DTOs using the class's from_domain method.

        Args:
            domain_objs: Dictionary mapping keys to domain model objects

        Returns:
            Dictionary mapping the same keys to new response DTO instances
        """
        return {k: cls.from_domain(v) for k, v in domain_objs.items()}
