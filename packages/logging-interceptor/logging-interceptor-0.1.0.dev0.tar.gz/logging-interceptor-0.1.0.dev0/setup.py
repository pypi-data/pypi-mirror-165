# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['logging_interceptor']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'logging-interceptor',
    'version': '0.1.0.dev0',
    'description': "Capture Python's standard logging messages and route them to Loguru.",
    'long_description': '# Python Logging Interceptor\n\n*Capture Python\'s stdlib `logging` messages and route them to other logging frameworks.*\n\n(Modified and packaged for PyPI from Matthew Scholefield\'s[loguru-logging-intercept][r1].)\n\nCurrently supported targets:\n\n* [Loguru](https://github.com/Delgan/loguru)\n\n[Loguru](https://github.com/Delgan/loguru) is a great alternative logging library for\nPython. However, if you use (potentially external) code that already integrates with\nPython\'s default logger, you\'ll get a combination of the two logging styles. This code\nprovides code for setting up an intercept handler to route calls to Python\'s default\n`logging` module to Loguru.\n\n## Usage\n\nBefore calls that use Python\'s default `logging` module, call the provided\n`setup_loguru_logging_intercept()` as shown below:\n\n```python\nfrom logging_interceptor import setup_loguru_interceptor\n\n\nsetup_loguru_interceptor(modules=("foo", "foo.bar", "foo.baz"))\n\n# now call functions from `foo` that use getLogger(__name__)\n```\n\n## Installation\n\nInstall via `pip`:\n\n```bash\npip3 install loguru-logging-intercept\n```\n\n[r1]: https://github.com/MatthewScholefield/loguru-logging-intercept\n',
    'author': 'Matthew D. Scholefield',
    'author_email': 'matthew331199@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/imcf/logging-interceptor',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
