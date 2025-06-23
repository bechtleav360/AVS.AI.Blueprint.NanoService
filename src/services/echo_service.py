"""An Example on how a Service could look like.
In this case we are trying to create an echoing service that simply return back the input."""

from datetime import datetime

from src.common.model.dto.echo import EchoInput, EchoOutput


class EchoService:
    """An example service that simply echoes back the input"""

    def __init__(self) -> None:
        self.creation_timestamp = datetime.utcnow().isoformat()

    def process_input(self, echo_input: EchoInput) -> EchoOutput:
        """Echoes back the input"""

        return EchoOutput(
            input_data=echo_input.dict(),  # Echo back all input data
            processed_timestamp=datetime.utcnow().isoformat(),
            up_timestamp=self.creation_timestamp,
            processing_info={"message": "Echo successful"}
        )
