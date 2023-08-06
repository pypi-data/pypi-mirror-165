"""The backends module contains the backend classes for the xrdsum program."""
from __future__ import annotations

from ._base import XrdsumBackend
from ._cephfs import CephFSBackend
from ._hdfs import HDFSBackend

FILE_SYSTEMS: dict[str, type[XrdsumBackend]] = {
    "HDFS": HDFSBackend,
    "CephFS": CephFSBackend,
}

__all__ = ["FILE_SYSTEMS"]
