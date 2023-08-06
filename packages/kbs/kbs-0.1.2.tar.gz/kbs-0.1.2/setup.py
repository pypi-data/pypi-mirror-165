# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kbs']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.4,<9.0.0', 'pykube-ng>=22.7.0,<23.0.0']

entry_points = \
{'console_scripts': ['kbs = kbs.cli:cli']}

setup_kwargs = {
    'name': 'kbs',
    'version': '0.1.2',
    'description': 'kbs is a command line tool to work with kubernetes secrets',
    'long_description': None,
    'author': 'Steinn Eldjárn Sigurðarson',
    'author_email': 'steinnes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
