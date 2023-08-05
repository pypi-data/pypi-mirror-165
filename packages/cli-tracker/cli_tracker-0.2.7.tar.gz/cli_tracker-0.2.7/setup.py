# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cli_tracker', 'cli_tracker.integrations']

package_data = \
{'': ['*']}

install_requires = \
['sentry-sdk>=1.5.12,<2.0.0']

extras_require = \
{':sys_platform == "linux"': ['distro>=1.7.0,<2.0.0']}

setup_kwargs = {
    'name': 'cli-tracker',
    'version': '0.2.7',
    'description': '',
    'long_description': '# CLI tracker\n\nAllows to collect cli usage data to a Sentry instance.\n\nBuilt by:\n\n<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="./assets/Unikube-Logo-H-White.png">\n  <img alt="Unikube Logo" src="./assets/Unikube-Logo-H.png">\n</picture>\n\n',
    'author': 'Robert Stein',
    'author_email': 'robert@blueshoe.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
