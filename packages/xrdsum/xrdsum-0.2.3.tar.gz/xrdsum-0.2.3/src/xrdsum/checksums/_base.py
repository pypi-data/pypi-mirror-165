"""Definition of the Checksum protocol."""
from __future__ import annotations

from typing import Any, Iterable, Protocol


class Checksum(Protocol):
    """Base protocol for checksum implementations."""

    name: str = "Unknown"
    value: str = "N/A"
    bytes_read: int = 0
    number_of_buffers_read: int = 0

    def int_to_hex(self, value: int) -> str:
        """Converts integer to hex representation"""
        raise NotImplementedError()

    def hex_to_int(self, value: str) -> int:
        """Converts hex representation to integer"""
        raise NotImplementedError()

    def calculate(self, file_buffer: Iterable[Any]) -> str:
        """Calculates the checksum"""
        raise NotImplementedError()
