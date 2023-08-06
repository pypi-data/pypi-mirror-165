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
    'version': '0.2.2',
    'description': 'Bundling your Python project into a single Python file.',
    'long_description': "## PyPkgPack\n\n[![CI](https://github.com/Suzhou-Tongyuan/pypkgpack/actions/workflows/ci.yml/badge.svg)](https://github.com/Suzhou-Tongyuan/pypkgpack/actions/workflows/ci.yml)\n[![versions](https://img.shields.io/pypi/pyversions/pypkgpack.svg)](https://pypi.org/project/pypkgpack/#history)\n[![pypi](https://img.shields.io/pypi/v/pypkgpack.svg)](https://pypi.org/project/pypkgpack/)\n[![License](https://img.shields.io/badge/License-BSD_2--Clause-green.svg)](https://github.com/Suzhou-Tongyuan/pypkgpack/blob/main/LICENSE)\n\nBundling a pure Python package into a single Python file.\n\nUsage:\n\n```shell\n> pypkgpack /path/to/mypackage --out bundled_package.py\n\n> python\n\npython> import bundled_package\npython> from mypackage.mymodule import myfunction\npython> print(myfunction())\n```\n\nFeatures:\n\n- [x] bundling a Python package into a single Python file\n- [x] caching bytecode compilation and cache invalidation\n- [x] fixing the missing `__init__.py`\n- [x] allow multiple source code implementations for the same module\n- [x] respect Python's import semantics\n- [x] bundled modules need no extra dependencies\n- [ ] support bundling binaries and assets\n- [ ] allow lazy imports\n",
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
