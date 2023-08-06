"""
Base module for storage catalog classes.
"""
from __future__ import annotations

from typing import Protocol


class StorageCatalog(Protocol):
    """
    Base definition for storage catalog classes.
    A storage catalog needs to implement the following methods:
    - __init__, which takes a config file path and protocol as an arguments
    - lfntopfn, which takes a logical filename and returns a physical filename"""

    def __init__(self, config: str | None = None, protocol: str | None = None) -> None:
        raise NotImplementedError()

    def lfn2pfn(self, lfn: str) -> str:
        """Converts logical filename to physical filename"""
        raise NotImplementedError()
