"""Application level logger for xrdsum"""
from __future__ import annotations

import logging
from typing import Any

from rich.logging import RichHandler

APP_LOGGER_NAME = "xrdsum"
DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_TIME_FORMAT = "%H:%M:%S"
TRACE = 5
TIMING = 11  # log level for timing, between DEBUG (10) and WARNING (30)
LOGGER = logging.getLogger(APP_LOGGER_NAME)


def log_function_factory(custom_log_level: int) -> Any:
    """Factory function for creating a function that logs at a custom level"""

    def log_function(
        self: logging.Logger, message: str, *args: list[Any], **kws: dict[str, Any]
    ) -> None:
        """Log at custom_log_level"""
        if self.isEnabledFor(custom_log_level):
            # pylint: disable=protected-access
            self._log(custom_log_level, message, args, **kws)  # type: ignore[arg-type]

    return log_function


trace = log_function_factory(custom_log_level=TRACE)
timing = log_function_factory(custom_log_level=TIMING)


class LevelFormatter(logging.Formatter):
    """
    From https://stackoverflow.com/a/28636024/362457
    """

    def __init__(self, fmt: str, datefmt: str, level_fmts: dict[int, str]):
        self._level_formatters = {}
        for level, _format in level_fmts.items():
            # Could optionally support level names too
            self._level_formatters[level] = logging.Formatter(
                fmt=_format, datefmt=datefmt
            )
        # self._fmt will be the default format
        super().__init__(fmt=fmt, datefmt=datefmt)

    def format(self, record: logging.LogRecord) -> str:
        if record.levelno in self._level_formatters:
            return self._level_formatters[record.levelno].format(record)

        return super().format(record)


# add TRACE log level and function to logger
logging.addLevelName(TRACE, "TRACE")
logging.TRACE = TRACE  # type: ignore[attr-defined]
logging.addLevelName(TIMING, "TIMING")
logging.TIMING = TIMING  # type: ignore[attr-defined]


def setup_logger(
    default_level: int = logging.INFO, log_file: str | None = None
) -> logging.Logger:
    """Sets up a logging.Logger with specified log level and log file.
    If log_file is None, logs to stdout."""
    console_formatter = LevelFormatter(
        fmt="%(asctime)s [%(name)s]  %(levelname)s: %(message)s",
        datefmt=f"[{DEFAULT_DATE_FORMAT} {DEFAULT_TIME_FORMAT}]",
        level_fmts={
            logging.INFO: "%(message)s",
            logging.WARNING: "[bold dark_orange]%(levelname)s[/]: %(message)s",
            logging.ERROR: "[bold red]%(levelname)s[/]: %(message)s",
            logging.DEBUG: "[bold hot_pink]%(levelname)s[/]: %(message)s",
            logging.TRACE: "[bold hot_pink]%(levelname)s[/]: %(message)s",  # type: ignore[attr-defined]
            logging.TIMING: "[bold hot_pink]%(levelname)s[/]: %(message)s",  # type: ignore[attr-defined]
            logging.CRITICAL: "[bold blink bright_red]%(levelname)s[/]: %(message)s",
        },
    )
    console_handler = RichHandler(
        # rich_tracebacks=True, # does not work with custom formatters
        markup=True,
        show_level=False,
        show_time=False,
        show_path=False,
    )
    console_handler.setLevel(default_level)
    console_handler.setFormatter(console_formatter)
    console_handler.formatter = console_formatter

    logger = logging.getLogger(APP_LOGGER_NAME)
    logging.getLoggerClass().trace = trace  # type: ignore[attr-defined]
    logging.getLoggerClass().timing = timing  # type: ignore[attr-defined]

    if not log_file:
        # only log to console if no log file is specified
        logger.addHandler(console_handler)
        logger.setLevel(default_level)
        return logger

    logfile_formatter = logging.Formatter(
        "%(asctime)s [%(name)s]  %(levelname)s: %(message)s"
    )
    logfile_handler = logging.FileHandler(log_file)
    logfile_handler.setLevel(default_level)
    logfile_handler.setFormatter(logfile_formatter)
    logger.addHandler(logfile_handler)
    logger.setLevel(default_level)
    return logger
