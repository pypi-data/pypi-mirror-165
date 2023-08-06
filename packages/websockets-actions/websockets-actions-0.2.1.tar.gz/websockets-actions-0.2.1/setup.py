# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['websockets_actions']

package_data = \
{'': ['*']}

install_requires = \
['starlette>=0.20.4,<0.21.0', 'uvicorn[standart]>=0.18.3,<0.19.0']

setup_kwargs = {
    'name': 'websockets-actions',
    'version': '0.2.1',
    'description': 'Using Actions for Websockets',
    'long_description': None,
    'author': 'Omelchenko Michael',
    'author_email': 'socanime@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
