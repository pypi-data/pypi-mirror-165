"""Interceptor to route `logging` calls from the stdlib to `[loguru][i1]`.

[i1]: https://pypi.org/project/loguru/

.. include:: ../../README.md
"""

__version__ = "0.1.1"

from .loguru import setup_loguru_interceptor
