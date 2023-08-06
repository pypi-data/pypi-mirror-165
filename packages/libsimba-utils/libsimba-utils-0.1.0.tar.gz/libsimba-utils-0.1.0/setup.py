# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libsimba_utils']

package_data = \
{'': ['*']}

install_requires = \
['hdwallet==2.1.1', 'pycryptodome==3.15.0', 'web3==5.30.0']

setup_kwargs = {
    'name': 'libsimba-utils',
    'version': '0.1.0',
    'description': 'libsimba Utilities',
    'long_description': None,
    'author': 'SIMBA Chain Inc.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
