# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dspf']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1',
 'factor_analyzer>=0.4.0',
 'matplotlib>=3.5.3',
 'numpy>=1.23.2',
 'pandas>=1.4.3',
 'scikit-learn>=1.1.2',
 'scipy>=1.9.0',
 'seaborn>=0.11.2']

entry_points = \
{'console_scripts': ['data-science-portfolio = '
                     'data_science_portfolio.__main__:main']}

setup_kwargs = {
    'name': 'dspf',
    'version': '0.0.1a2',
    'description': 'Data Science Portfolio',
    'long_description': "# Data Science Portfolio\n\n[![PyPI](https://img.shields.io/pypi/v/dspf.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/dspf.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/dspf)][python version]\n[![License](https://img.shields.io/pypi/l/dspf)][license]\n\n[![Read the documentation at https://dspf.readthedocs.io/](https://img.shields.io/readthedocs/dspf/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/MoritzM00/data-science-portfolio/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/MoritzM00/data-science-portfolio/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/dspf/\n[status]: https://pypi.org/project/dspf/\n[python version]: https://pypi.org/project/dspf\n[read the docs]: https://dspf.readthedocs.io/\n[tests]: https://github.com/MoritzM00/data-science-portfolio/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/MoritzM00/data-science-portfolio\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _Data Science Portfolio_ via [pip] from [PyPI]:\n\n```console\n$ pip install dspf\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Data Science Portfolio_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/MoritzM00/data-science-portfolio/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/MoritzM00/data-science-portfolio/blob/main/LICENSE\n[contributor guide]: https://github.com/MoritzM00/data-science-portfolio/blob/main/CONTRIBUTING.md\n[command-line reference]: https://dspf.readthedocs.io/en/latest/usage.html\n",
    'author': 'Moritz Mistol',
    'author_email': 'moritz.mistol@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MoritzM00/data-science-portfolio',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
