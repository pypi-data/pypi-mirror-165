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

extras_require = \
{'tf': ['tensorflow==2.8.0', 'protobuf==3.20.1']}

entry_points = \
{'console_scripts': ['dinora = dinora.cli:cli']}

setup_kwargs = {
    'name': 'dinora',
    'version': '0.0.3',
    'description': 'Dinora Chess Engine',
    'long_description': '# Dinora\n\n[Documentation](https://dinora.readthedocs.io/en/latest/) | [Installation](https://dinora.readthedocs.io/en/latest/installation.html)\n\nDinora is alphazero-like chess engine. It uses \nkeras/tensorflow for position evaluation and Monte Carlo Tree Search for \ncalculating best move.\n\n### Features\n- Working chess engine\n- Minimal example of alpazero-like engine NN + MCTS\n- All code included in this repo - for playing and training\n- Everything written in python\n\n## Status\nYou can play against Dinora in standard chess variation, with or without increment.\nI assume engine strength is about 1400 Lichess Elo, I evaluate engine rating \nbasing on a few games against me, so it\'s not accurate.  \nYou can see example game below  \n(10+0) Dinora (100-200 nodes in search) vs Me (2200 Rapid Lichess rating)  \n\n<img src="https://github.com/Saegl/dinora/raw/main/assets/gif/gfychess-example.gif" width="350">\n\n# Acknowledgements\n\nThis engine based on https://github.com/Zeta36/chess-alpha-zero and \nhttps://github.com/dkappe/a0lite and Alphazero from Deepmind.\n\nA lot of tutorials about chess engines from https://www.chessprogramming.org/ was super helpful.\n',
    'author': 'Saegl',
    'author_email': 'saegl@protonmail.com',
    'maintainer': 'Saegl',
    'maintainer_email': 'saegl@protonmail.com',
    'url': 'https://github.com/DinoraChess/dinora',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
