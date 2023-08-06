# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oida', 'oida.checkers', 'oida.commands']

package_data = \
{'': ['*']}

install_requires = \
['libcst>=0.4.3,<0.5.0']

extras_require = \
{':python_version < "3.11"': ['tomli>=1.0.0']}

entry_points = \
{'console_scripts': ['oida = oida.console:main'],
 'flake8.extension': ['ODA = oida.flake8:Plugin']}

setup_kwargs = {
    'name': 'oida',
    'version': '0.1.0',
    'description': "Oida is Oda's linter that enforces code style and modularization in our Django projects.",
    'long_description': 'None',
    'author': 'Oda',
    'author_email': 'tech@oda.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
