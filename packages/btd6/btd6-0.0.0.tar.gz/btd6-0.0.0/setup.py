# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['btd6']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1']

entry_points = \
{'console_scripts': ['btd6 = btd6.__main__:main']}

setup_kwargs = {
    'name': 'btd6',
    'version': '0.0.0',
    'description': 'btd6',
    'long_description': "# btd6\n\n[![PyPI](https://img.shields.io/pypi/v/btd6.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/btd6.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/btd6)][python version]\n[![License](https://img.shields.io/pypi/l/btd6)][license]\n\n[![Read the documentation at https://btd6.readthedocs.io/](https://img.shields.io/readthedocs/btd6/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/56kyle/btd6/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/56kyle/btd6/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/btd6/\n[status]: https://pypi.org/project/btd6/\n[python version]: https://pypi.org/project/btd6\n[read the docs]: https://btd6.readthedocs.io/\n[tests]: https://github.com/56kyle/btd6/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/56kyle/btd6\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _btd6_ via [pip] from [PyPI]:\n\n```console\n$ pip install btd6\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_btd6_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/56kyle/btd6/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/56kyle/btd6/blob/main/LICENSE\n[contributor guide]: https://github.com/56kyle/btd6/blob/main/CONTRIBUTING.md\n[command-line reference]: https://btd6.readthedocs.io/en/latest/usage.html\n",
    'author': 'Kyle Oliver',
    'author_email': '56kyleoliver@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/56kyle/btd6',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
