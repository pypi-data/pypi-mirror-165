"""xrdsum.checksums package"""
from __future__ import annotations

from ._base import StorageCatalog
from .cms import CMSStorageCatalog

AVAILABLE_STORAGE_CATALOGS: dict[str, type[StorageCatalog]] = {
    "cms": CMSStorageCatalog,
}


def resolve_file_path(file_path: str, storage_catalog: str) -> str:
    """Resolve the file path given a file catalog."""
    if not storage_catalog:
        return file_path

    # split experiment, storage catalog and protocol
    # e.g. cms|/etc/xrootd/storage.xml?direct
    experiment, storage_catalog = storage_catalog.split("|", maxsplit=1)
    if experiment not in AVAILABLE_STORAGE_CATALOGS:
        raise ValueError(
            f"Unknown storage catalog {experiment}. Available: {AVAILABLE_STORAGE_CATALOGS.keys()}"
        )

    protocol = None
    if "?" in storage_catalog:
        storage_catalog, protocol = storage_catalog.split("?", maxsplit=1)

    catalog = AVAILABLE_STORAGE_CATALOGS[experiment](storage_catalog, protocol=protocol)
    return catalog.lfn2pfn(file_path)


__all__ = [
    "CMSStorageCatalog",
    "StorageCatalog",
    "AVAILABLE_STORAGE_CATALOGS",
    "resolve_file_path",
]
