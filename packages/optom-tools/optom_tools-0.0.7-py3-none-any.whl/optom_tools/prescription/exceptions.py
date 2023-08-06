"""Custom exceptions related to the `prescrption` module."""

from typing import Any


class PrescriptionError(Exception):
    """Prescription input error."""

    def __init__(self, value: Any, message: str) -> None:
        """Construct exception."""
        self.value = value
        self.message = message
        super().__init__(message)
