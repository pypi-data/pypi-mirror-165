# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['constellate', 'constellate.cli', 'constellate.constellate']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0',
 'click-log>=0.4.0,<0.5.0',
 'click>=8.1.3,<9.0.0',
 'matplotlib>=3.5.2,<4.0.0',
 'python-slugify>=6.1.2,<7.0.0',
 'rho-plus>=0.4.0,<0.5.0',
 'watchdog>=2.1.9,<3.0.0',
 'yapf>=0.32.0,<0.33.0']

entry_points = \
{'console_scripts': ['constellate = constellate.cli.app:cli']}

setup_kwargs = {
    'name': 'constellate-app',
    'version': '0.1.0',
    'description': 'Render Jupyter Notebooks as beautiful interactive webapps',
    'long_description': None,
    'author': 'Nicholas Miklaucic',
    'author_email': 'nicholas.miklaucic@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
