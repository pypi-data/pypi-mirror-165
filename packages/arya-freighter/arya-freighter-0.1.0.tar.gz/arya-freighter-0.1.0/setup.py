# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['freighter', 'freighter.util']

package_data = \
{'': ['*']}

install_requires = \
['janus>=1.0.0,<2.0.0',
 'msgpack>=1.0.4,<2.0.0',
 'mypy>=0.971,<0.972',
 'pytest-asyncio>=0.19.0,<0.20.0',
 'pytest>=7.1.2,<8.0.0',
 'urllib3>=1.26.12,<2.0.0',
 'websockets>=10.3,<11.0']

setup_kwargs = {
    'name': 'arya-freighter',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'emiliano bonilla',
    'author_email': 'emilbon99@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
