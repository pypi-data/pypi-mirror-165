# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot',
 'nonebot.adapters.console',
 'nonebot.adapters.console.terminal',
 'nonebot.adapters.console.terminal.widgets']

package_data = \
{'': ['*']}

install_requires = \
['nonebot2>=2.0.0-beta.1,<3.0.0', 'textual==0.1.18']

setup_kwargs = {
    'name': 'nonebot-adapter-console',
    'version': '0.2.0',
    'description': 'console adapter for nonebot2',
    'long_description': 'None',
    'author': 'MelodyKnit',
    'author_email': 'yanximelody@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
