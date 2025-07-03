from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class EchoMessage:
    """Domain model representing an echo message.

    This is the internal representation of an echo request/response
    and should not be exposed directly through the API.
    """

    data: Dict[str, Any]
    processed_timestamp: datetime
    service_start_time: datetime
    metadata: Optional[Dict[str, Any]] = None
    is_processed: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert the domain model to a dictionary."""
        return {
            "data": self.data,
            "metadata": self.metadata or {},
            "is_processed": self.is_processed,
            "processed_timestamp": self.processed_timestamp.isoformat(),
            "service_start_time": self.service_start_time.isoformat(),
            "processing_info": ({"message": "Echo successful"} if self.is_processed else {}),
        }
