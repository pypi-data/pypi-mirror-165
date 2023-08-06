# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybuoy', 'pybuoy.api', 'pybuoy.mixins', 'pybuoy.observation']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'pybuoy',
    'version': '0.4.1',
    'description': 'Python wrapper for NDBC data.',
    'long_description': "![PyPI - Version](https://img.shields.io/pypi/v/pybuoy?color=blue)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pybuoy)\n![PyPI - Monthly Downloads](https://img.shields.io/pypi/dm/pybuoy)\n\n# pybuoy\n\n`pybuoy` is a server-side Python package that was built to facilitate rapid discovery of new data from [NDBC](https://www.ndbc.noaa.gov/) with only a single dependency!\n\n## Installation\n\n`pybuoy` is supported on Python 3.10+ and can be installed with either `pip` or a package manager like [poetry](https://python-poetry.org):\n\n- **with pip**: `pip install pybuoy`\n  - recommended to install any third party library in python's virtualenv. ([ref](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments))\n- **with poetry**: `poetry add pybuoy`\n  - automatically creates and manages your virtualenvs. ([ref](https://realpython.com/dependency-management-python-poetry))\n\n## Quickstart\n\n```python\n# Demo in python/ipython shell\n# Don't forget to install pybuoy first\n\n>>> from pybuoy import Buoy\n\n>>> buoy = Buoy()\n\n>>> buoy\n<pybuoy.buoy.Buoy object at 0x10481fc10>\n```\n\n## Examples\n\n- [Get all active stations](./examples/get_activestations.py).\n\n- [Get realtime meteorological data](./examples/get_realtime_data.py#L12) for buoy by station_id.\n\n- [Get realtime wave summary data](./examples/get_realtime_data.py#L59) for buoy by station_id.\n",
    'author': 'Kyle J. Burda',
    'author_email': 'kylejbdev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
