# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logger_hub']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'logger-hub',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Pablo Martin Fernandez',
    'author_email': 'pablo.martin.fernandez@pwc.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
