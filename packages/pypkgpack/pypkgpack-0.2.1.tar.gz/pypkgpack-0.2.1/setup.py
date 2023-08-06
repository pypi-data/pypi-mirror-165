# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypkgpack']

package_data = \
{'': ['*']}

install_requires = \
['ast-compat>=0.11.1,<0.12.0', 'wisepy2>=1.3,<2.0']

entry_points = \
{'console_scripts': ['pypkgpack = pypkgpack.bundle:CLI']}

setup_kwargs = {
    'name': 'pypkgpack',
    'version': '0.2.1',
    'description': '',
    'long_description': None,
    'author': 'thautwarm',
    'author_email': 'twshere@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
