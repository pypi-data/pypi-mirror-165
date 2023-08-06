# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weevils']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.12,<3.0']

setup_kwargs = {
    'name': 'weevils',
    'version': '0.0.2a0',
    'description': '',
    'long_description': None,
    'author': 'weevils.io',
    'author_email': 'code@weevils.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://docs.weevils.io/api-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
