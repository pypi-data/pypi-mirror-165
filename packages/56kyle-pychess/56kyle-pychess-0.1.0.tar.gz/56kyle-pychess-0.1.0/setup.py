# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chess',
 'chess.board',
 'chess.game',
 'chess.gui',
 'chess.notation',
 'chess.unit']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.2,<2.0.0']

setup_kwargs = {
    'name': '56kyle-pychess',
    'version': '0.1.0',
    'description': 'A python chess engine',
    'long_description': None,
    'author': 'kyle',
    'author_email': '56kyleoliver@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
