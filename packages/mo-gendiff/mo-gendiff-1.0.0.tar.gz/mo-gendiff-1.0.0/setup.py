# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gendiff', 'gendiff.formatters', 'gendiff.scripts', 'gendiff.tests']

package_data = \
{'': ['*'], 'gendiff.tests': ['fixtures/*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'pytest-cov>=3.0.0,<4.0.0']

entry_points = \
{'console_scripts': ['gendiff = gendiff.scripts.gendiff:main']}

setup_kwargs = {
    'name': 'mo-gendiff',
    'version': '1.0.0',
    'description': 'Two files difference generator',
    'long_description': None,
    'author': 'Max Odinokiy',
    'author_email': 'max.odinokiy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
