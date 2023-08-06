"""Module for calculating Adler32 checksums."""
from __future__ import annotations

import logging
import struct
import zlib
from typing import Any, Iterable

from ..logger import APP_LOGGER_NAME
from ._base import Checksum

log = logging.getLogger(APP_LOGGER_NAME)


class Adler32(Checksum):
    """Adler32 checksum
    from https://github.com/snafus/cephsum/blob/master/cephsum/adler32.py"""

    name: str = "adler32"

    def int_to_hex(self, value: int) -> str:
        # return hex(value)[2:]
        return "".join([f"{x:02x}" for x in struct.pack(">I", value)]).lower()

    def hex_to_int(self, value: str) -> int:
        return int(value, 16)

    def calculate(self, file_buffer: Iterable[Any]) -> str:
        value = 1
        bytes_read = 0
        number_of_buffers_read = 0
        for buffer in file_buffer:
            value = zlib.adler32(buffer, value)
            bytes_read += len(buffer)
            number_of_buffers_read += 1
            log.trace(  # type: ignore[attr-defined]
                "%s: %s %s %s",
                self.name,
                self.int_to_hex(value),
                len(buffer),
                bytes_read,
            )

        self.value = self.int_to_hex(value)
        self.bytes_read = bytes_read
        self.number_of_buffers_read = number_of_buffers_read

        return self.value
