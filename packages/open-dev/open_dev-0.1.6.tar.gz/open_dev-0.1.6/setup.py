# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['open_dev', 'open_dev.src', 'tests', 'tests.app']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0',
 'click==8.0.2',
 'mkdocs-material-extensions>=1.0.3,<2.0.0',
 'rich-click>=1.5.2,<2.0.0',
 'yamllint>=1.27.1,<2.0.0']

extras_require = \
{':extra == "dev"': ['tox>=3.25.1,<4.0.0',
                     'pip>=22.2.2,<23.0.0',
                     'twine>=4.0.1,<5.0.0',
                     'pre-commit>=2.20.0,<3.0.0',
                     'toml>=0.10.2,<0.11.0',
                     'bump2version>=1.0.1,<2.0.0'],
 ':extra == "doc"': ['mkdocs>=1.3.1,<2.0.0',
                     'mkdocs-include-markdown-plugin>=3.6.1,<4.0.0',
                     'mkdocs-material>=8.4.0,<9.0.0',
                     'mkdocstrings>=0.19.0,<0.20.0',
                     'mkdocs-autorefs>=0.4.1,<0.5.0'],
 ':extra == "test"': ['black>=22.6.0,<23.0.0',
                      'isort>=5.10.1,<6.0.0',
                      'mypy>=0.971,<0.972',
                      'pytest-cov>=3.0.0,<4.0.0',
                      'pylama[all]>=8.4.1,<9.0.0']}

entry_points = \
{'console_scripts': ['odev = open_dev.cli:main']}

setup_kwargs = {
    'name': 'open-dev',
    'version': '0.1.6',
    'description': 'A collection of tooling to enable open source development..',
    'long_description': '# open_dev\n\n\n[![pypi](https://img.shields.io/pypi/v/open_dev.svg)](https://pypi.org/project/open_dev/)\n[![python](https://img.shields.io/pypi/pyversions/open_dev.svg)](https://pypi.org/project/open_dev/)\n[![Build Status](https://github.com/8ball030/open_dev/actions/workflows/dev.yml/badge.svg)](https://github.com/8ball030/open_dev/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/8ball030/open_dev/branch/main/graphs/badge.svg)](https://codecov.io/github/8ball030/open_dev)\n\n\nInstall Dependencies.\n\n(Poetry) Is used to managed the dependencies. (https://python-poetry.org/docs/#installation)\n# osx / linux / bashonwindows install instructions\n```bash\ncurl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -\n```\n```\n# windows install instructions\n```\n```\n(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python `\n```\n\n\nA collection of tooling to enable open source development.\n\n\n* Documentation: <https://8ball030.github.io/open_dev>\n* GitHub: <https://github.com/8ball030/open_dev>\n* PyPI: <https://pypi.org/project/open_dev/>\n* Free software: Apache-2.0\n\n\n## Features\n\n* TODO\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.\n',
    'author': '8Baller',
    'author_email': '8ball030@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/8ball030/open_dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0',
}


setup(**setup_kwargs)
