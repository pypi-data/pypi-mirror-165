# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dinora', 'dinora.board_representation']

package_data = \
{'': ['*']}

install_requires = \
['chess>=1.6.1,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'numpy>=1.19.2,<2.0.0',
 'pylru>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['dinora = dinora.cli:cli']}

setup_kwargs = {
    'name': 'dinora',
    'version': '0.0.1',
    'description': 'Dinora Chess Engine',
    'long_description': 'None',
    'author': 'Saegl',
    'author_email': 'saegl@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
