# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_api_soup']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pytest-api-soup',
    'version': '0.0.2',
    'description': 'Validate multiple endpoints with unit testing using a single source of truth.',
    'long_description': None,
    'author': 'Indi Harrington',
    'author_email': 'indigoharrington@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
