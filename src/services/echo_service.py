"""Echo service implementation.

This service handles the business logic for echoing messages.
"""

from datetime import datetime, timezone
from typing import Any, Dict

from src.models.domain import EchoMessage


class EchoService:
    """Service that processes echo requests.

    This service is responsible for handling the business logic
    related to echoing messages.
    """

    def __init__(self):
        """Initialize the echo service with a creation timestamp."""
        self.creation_time = datetime.now(timezone.utc)

    def process_input(self, input_data: Dict[str, Any]) -> EchoMessage:
        """Process the input data and return an echo message.

        Args:
            input_data: The input data to echo back

        Returns:
            EchoMessage: The processed echo message
        """
        # In a real service, this would contain actual business logic
        return EchoMessage(
            data=input_data,
            processed_timestamp=datetime.now(timezone.utc),
            service_start_time=self.creation_time,
            metadata={"source": "echo_service"},
            is_processed=True,
        )
