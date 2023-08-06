# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mc_server_interaction',
 'mc_server_interaction.interaction',
 'mc_server_interaction.server_manger']

package_data = \
{'': ['*']}

install_requires = \
['aioconsole>=0.5.0,<0.6.0',
 'aiofile>=3.8.1,<4.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'cached-property>=1.5.2,<2.0.0',
 'mcstatus>=9.4.0,<10.0.0',
 'psutil>=5.9.1,<6.0.0']

setup_kwargs = {
    'name': 'mc-server-interaction',
    'version': '0.1.0',
    'description': 'Module for interacting with Minecraft servers',
    'long_description': None,
    'author': 'Dummerle',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
