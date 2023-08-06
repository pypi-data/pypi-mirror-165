"""Implementation of the CephFS backend."""
# we want non-top-level imports to avoid pulling CephFS/cephsum dependencies early
# pylint: disable=import-outside-toplevel
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..checksums import Checksum
from ._base import XrdsumBackend

CONF = "/etc/ceph/ceph.conf"
KEYRING = "/etc/ceph/ceph.client.xrootd.keyring"
USER = "client.xrootd"


@dataclass
class CephSettings:
    """Settings for the CephFS backend."""

    config_file: str = CONF
    keyring: str = KEYRING
    user: str = USER
    read_size: int = 64 * 1024 * 1024


def get_ceph_client(settings: CephSettings) -> Any:
    """Retrieving the CephFS client to execute operations on CephFS."""
    import cephsum  # pylint: disable=import-error

    client = cephsum.cephtools.cluster_connect(
        conffile=settings.config_file,
        keyring=settings.keyring,
        name=settings.user,
    )
    return client


class CephFSBackend(XrdsumBackend):
    """Implementation of the CephFS backend."""

    client: Any
    settings: CephSettings

    def __init__(
        self, file_path: str, read_size: int, **kwargs: dict[str, Any]
    ) -> None:
        """CephFS backend requires at least the file_path and read_size"""
        self.file_path = file_path
        self.settings = CephSettings(
            read_size=read_size,
            **kwargs,  # type: ignore[arg-type]
        )

    def get_checksum(self, checksum: Checksum) -> Checksum:
        raise NotImplementedError()

    def store_checksum(self, checksum: Checksum, force: bool = False) -> None:
        raise NotImplementedError()
