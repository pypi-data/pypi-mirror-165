# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['umnet_pyncs', 'umnet_pyncs.state', 'umnet_pyncs.state.models']

package_data = \
{'': ['*']}

install_requires = \
['multiprocessing-logging>=0.3.3,<0.4.0', 'ntc-templates>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'umnet-pyncs',
    'version': '0.1.2',
    'description': 'custom python module for NCS helpers',
    'long_description': None,
    'author': 'Nick Grundler',
    'author_email': 'grundler@umich.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
