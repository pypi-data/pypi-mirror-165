# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_changedetect']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0']

setup_kwargs = {
    'name': 'pydantic-changedetect',
    'version': '0.2.0',
    'description': 'Extend pydantic models to also detect and record changes made to the model attributes.',
    'long_description': None,
    'author': 'TEAM23 GmbH',
    'author_email': 'info@team23.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
