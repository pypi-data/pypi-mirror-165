# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mc_server_interaction',
 'mc_server_interaction.interaction',
 'mc_server_interaction.server_manger',
 'mc_server_interaction.utils']

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
    'version': '0.1.2',
    'description': 'Module for interacting with Minecraft servers',
    'long_description': '# mc-server-interaction\nMC-Server-Interaction is a modern asyncio-based library for interacting with Minecraft servers on your local machine.\n\n## Features\n- Modern interface using asyncio and callbacks\n- Manage multiple servers\n  - Create Servers\n  - Start and stop servers\n  - Send commands\n- Retrieve player information\n\n\n## Roadmap\n- Much better cli interface\n- Interacting with worlds\n- Backup functions\n- ...\n\n## Requirements\n- Python 3.8 minimum\n- [Poetry](https://python-poetry.org/)\n',
    'author': 'Dummerle',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Uncooldevs/mc-server-interaction',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
