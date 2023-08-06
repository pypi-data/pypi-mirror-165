# Python Logging Interceptor

*Capture Python's stdlib `logging` messages and route them to other logging frameworks.*

(Modified and packaged for PyPI from Matthew Scholefield's
[loguru-logging-intercept][r1].)

Currently supported targets:

* [Loguru][r2]

**Loguru** is a great alternative logging library for Python. However, if you use
(potentially external) code that already integrates with Python's default logger, you'll
get a combination of the two logging styles. This code provides code for setting up an
intercept handler to route calls to Python's default `logging` module to Loguru.

## Usage

Before calls that use Python's default `logging` module, call the provided
`setup_loguru_interceptor()` as shown below:

```python
from logging_interceptor import setup_loguru_interceptor


setup_loguru_interceptor(modules=("foo", "foo.bar", "foo.baz"))

# now call functions from `foo` that use getLogger(__name__)
```

## Installation

Install via `pip`:

```bash
pip3 install logging-interceptor
```

[r1]: https://github.com/MatthewScholefield/loguru-logging-intercept
[r2]: https://github.com/Delgan/loguru
