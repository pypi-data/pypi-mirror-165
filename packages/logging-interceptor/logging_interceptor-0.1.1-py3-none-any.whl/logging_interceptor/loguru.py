import logging
import sys
from itertools import chain
from types import FrameType
from typing import cast

from loguru import logger


class InterceptHandler(logging.Handler):

    """Handler to route messages from Python logging module to loguru."""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def setup_loguru_interceptor(level=logging.DEBUG, modules=(), force=True):
    """Set up an interceptor routing messages to Loguru.

    Parameters
    ----------
    level : int, optional
        The log level (as defined by Python's standard `logging`). Messages with this
        level or above will be forwarded to Loguru. By default `logging.DEBUG`.
    modules : tuple, optional
        A list of module names whose `logging` messages should be intercepted, by
        default ().
    force : bool, optional
        Passed on to the `logging.basicConfig()` call, by default True.

    Example
    -------
    >>> setup_loguru_interceptor(modules=("foo", "foo.bar", "foo.baz"))
    """
    logging.basicConfig(handlers=[InterceptHandler()], level=level, force=force)
    for logger_name in chain(("",), modules):
        mod_logger = logging.getLogger(logger_name)
        mod_logger.handlers = [InterceptHandler(level=level)]
        mod_logger.propagate = False
