# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logistics_or_gym', 'logistics_or_gym.envs']

package_data = \
{'': ['*']}

install_requires = \
['gym', 'numpy>=1.23.2,<1.24.0']

setup_kwargs = {
    'name': 'logistics-or-gym',
    'version': '0.1.0',
    'description': 'or-problems formulated as gym environments to solve logisitcal-problems',
    'long_description': '',
    'author': 'hadisdev',
    'author_email': 'hadi.salameh@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HublyGroup/logistics-or-gym',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
