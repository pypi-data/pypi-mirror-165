"""xrdsum.checksums package"""
from __future__ import annotations

from ._base import Checksum
from .adler32 import Adler32

AVAILABLE_CHECKSUM_TYPES = {
    "adler32": Adler32,
}
__all__ = ["Adler32", "Checksum", "AVAILABLE_CHECKSUM_TYPES"]
