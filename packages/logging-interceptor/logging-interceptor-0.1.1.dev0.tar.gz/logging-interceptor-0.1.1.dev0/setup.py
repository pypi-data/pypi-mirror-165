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
    'version': '0.1.1.dev0',
    'description': "Intercept Python's standard logging and re-route the messages.",
    'long_description': '# Python Logging Interceptor\n\n*Capture Python\'s stdlib `logging` messages and route them to other logging frameworks.*\n\n(Modified and packaged for PyPI from Matthew Scholefield\'s\n[loguru-logging-intercept][r1].)\n\nCurrently supported targets:\n\n* [Loguru][r2]\n\n**Loguru** is a great alternative logging library for Python. However, if you use\n(potentially external) code that already integrates with Python\'s default logger, you\'ll\nget a combination of the two logging styles. This code provides code for setting up an\nintercept handler to route calls to Python\'s default `logging` module to Loguru.\n\n## Usage\n\nBefore calls that use Python\'s default `logging` module, call the provided\n`setup_loguru_interceptor()` as shown below:\n\n```python\nfrom logging_interceptor import setup_loguru_interceptor\n\n\nsetup_loguru_interceptor(modules=("foo", "foo.bar", "foo.baz"))\n\n# now call functions from `foo` that use getLogger(__name__)\n```\n\n## Installation\n\nInstall via `pip`:\n\n```bash\npip3 install logging-interceptor\n```\n\n[r1]: https://github.com/MatthewScholefield/loguru-logging-intercept\n[r2]: https://github.com/Delgan/loguru\n',
    'author': 'Matthew D. Scholefield',
    'author_email': 'matthew331199@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/imcf/logging-interceptor',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
