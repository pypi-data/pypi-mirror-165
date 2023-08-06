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
    'version': '0.1.2',
    'description': 'A python chess engine',
    'long_description': '\n# Pychess\n\n[![Status][status badge]][status badge]\n[![Tests][github actions badge]][github actions page]\n[![Codecov][codecov badge]][codecov page]\n[![Python Version][python version badge]][github page]\n[![License][license badge]][license]\n\n[code of conduct]: https://github.com/56kyle/pychess/blob/master/CODE_OF_CONDUCT.md\n[codecov badge]: https://codecov.io/gh/56kyle/pychess/branch/master/graph/badge.svg?token=0QDENTNTN7\n[codecov page]: https://app.codecov.io/gh/56kyle/pychess/branch/master\n[contributor covenant badge]: https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg\n[github actions badge]: https://github.com/56kyle/pychess/workflows/Tests/badge.svg\n[github actions page]: https://github.com/56kyle/pychess/actions?workflow=Tests\n[github page]: https://github.com/56kyle/pychess\n[license badge]: https://img.shields.io/github/license/56kyle/pychess\n[license]: https://opensource.org/licenses/MIT\n[python version badge]: https://img.shields.io/pypi/pyversions/56kyle-pychess\n[status badge]: https://img.shields.io/pypi/status/56kyle-pychess\n\nA chess game made in Python as a proof of concept to validate the importance of testing to a friend\n\n\n[Pychess](#Pychess)\n- []()\n\n',
    'author': 'kyle',
    'author_email': '56kyleoliver@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/56kyle/pychess',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
