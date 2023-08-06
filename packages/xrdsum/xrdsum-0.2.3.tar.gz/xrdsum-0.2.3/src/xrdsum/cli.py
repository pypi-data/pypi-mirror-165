"""Entry point for the "xrdsum" command"""
from __future__ import annotations

import logging
from typing import Any

import typer
from codetiming import Timer

from .backends import FILE_SYSTEMS
from .checksums import AVAILABLE_CHECKSUM_TYPES, Checksum
from .logger import APP_LOGGER_NAME, setup_logger
from .storage_catalog import resolve_file_path

app = typer.Typer()
log = logging.getLogger(APP_LOGGER_NAME)


@app.callback()
def logging_callback(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Debug output"),
    log_file: str = typer.Option(None, "--log-file", "-l", help="Log file"),
) -> Any:
    """Callback to give the --verbose and --debug options to all commands"""
    # verbose is debug
    trace = verbose and debug
    verbose = debug or verbose
    debug = verbose
    log_level = logging.INFO

    if debug:
        log_level = logging.DEBUG
    if trace:
        log_level = logging.TRACE  # type: ignore[attr-defined]
    setup_logger(log_level, log_file)
    log.debug("Logging to %s", log_file)


@app.command()
def get(
    file_path: str,
    store_result: bool = False,
    checksum_type: str = "adler32",
    read_size: int = typer.Option(
        default=64,
        help="""
Size [in MB] of the chunks to read from the file.
Should be a power of 2, and near (but not larger than) the stripe size.
Smaller values will use less memory, larger sizes may have benefits in IO performance.
""",
    ),
    storage_catalog: str = typer.Option(
        default="cms|/etc/xrootd/storage.xml?direct",
        help="Path to the CMS storage catalog",
    ),
    file_system: str = typer.Option(
        default="HDFS",
        help="File system to use for reading the file",
    ),
) -> None:
    """
    Get the checksum of a file.
    """
    # convert from MB to bytes
    read_size *= 1024 * 1024
    file_path = resolve_file_path(file_path, storage_catalog=storage_catalog)
    try:
        fs_handle = FILE_SYSTEMS[file_system](file_path, read_size)
    except KeyError as exception:
        log.error("Unknown file system %s", file_system)
        raise typer.Exit(code=1) from exception
    try:
        checksum: Checksum = AVAILABLE_CHECKSUM_TYPES[checksum_type]()
    except KeyError as exception:
        log.error("Unknown checksum type %s", checksum_type)
        raise typer.Exit(code=1) from exception
    with Timer(
        text=f"HDFS checksum took {{:.3f}}s for {file_path}",
        logger=log.timing,  # type: ignore[attr-defined]
    ):
        checksum = fs_handle.get_checksum(checksum)
    if store_result:
        with Timer(
            text=f"Storing checksum took {{:.3f}}s for {file_path}",
            logger=log.timing,  # type: ignore[attr-defined]
        ):
            fs_handle.store_checksum(checksum)
    typer.echo(checksum.value)


@app.command()
def verify(
    file_path: str,
    checksum_value: str,
    checksum_type: str = "adler32",
) -> None:
    """
    Check if a file has the correct checksum.
    """
    raise NotImplementedError()


def main() -> Any:
    """Entry point for the "xrdsum" command"""
    return app()
