# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['treedir']

package_data = \
{'': ['*']}

install_requires = \
['anytree>=2.8.0,<3.0.0', 'click>=8.1.3,<9.0.0']

setup_kwargs = {
    'name': 'treedir',
    'version': '29082022',
    'description': 'Module to create tree graphs for files and directories based in a simple structured language',
    'long_description': None,
    'author': 'David Pineda',
    'author_email': 'dahalpi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
