# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pineko', 'pineko.cli']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'a3b2bbc3ced97675ac3a71df45f55ba>=6.4.0,<7.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'click>=8.0.4,<9.0.0',
 'eko>=0.10.2,<0.11.0',
 'numpy>=1.21.0,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pineappl>=0.5.5,<0.6.0',
 'rich>=11.2.0,<12.0.0',
 'tomli>=2.0.1,<3.0.0']

extras_require = \
{'docs': ['Sphinx>=4.3.2,<5.0.0',
          'sphinx-rtd-theme>=1.0.0,<2.0.0',
          'sphinxcontrib-bibtex>=2.4.1,<3.0.0']}

entry_points = \
{'console_scripts': ['pineko = pineko:command']}

setup_kwargs = {
    'name': 'pineko',
    'version': '0.2.0',
    'description': 'Combine PineAPPL grids and EKOs into FK tables',
    'long_description': '<p align="center">\n  <a href="https://pineko.readthedocs.io/"><img alt="PINEKO" src="https://raw.githubusercontent.com/N3PDF/pineko/main/docs/source/img/Logo.png" width=200></a>\n</p>\n\n<p align="center">\n  <a href="https://github.com/N3PDF/pineko/actions/workflows/unittests.yml"><img alt="Tests" src="https://github.com/N3PDF/pineko/actions/workflows/unittests.yml/badge.svg" /></a>\n  <a href="https://pineko.readthedocs.io/en/latest/?badge=latest"><img alt="Docs" src="https://readthedocs.org/projects/pineko/badge/?version=latest"></a>\n  <a href="https://codecov.io/gh/N3PDF/pineko"><img src="https://codecov.io/gh/N3PDF/pineko/branch/main/graph/badge.svg" /></a>\n  <a href="https://www.codefactor.io/repository/github/n3pdf/pineko"><img src="https://www.codefactor.io/repository/github/n3pdf/pineko/badge" alt="CodeFactor" /></a>\n</p>\n\nPINEKO is a Python module to produce fktables from interpolation grids and EKOs.\n\n## Installation\nPINEKO is available via\n- PyPI: <a href="https://pypi.org/project/pineko/"><img alt="PyPI" src="https://img.shields.io/pypi/v/pineko"/></a>\n```bash\npip install pineko\n```\n\n### Development\n\nIf you want to install from source you can run\n```bash\ngit clone git@github.com:N3PDF/pineko.git\ncd pineko\npoetry install\n```\n\nTo setup `poetry`, and other tools, see [Contribution\nGuidelines](https://github.com/N3PDF/pineko/blob/main/.github/CONTRIBUTING.md).\n\n## Documentation\n- The documentation is available here: <a href="https://pineko.readthedocs.io/en/latest/"><img alt="Docs" src="https://readthedocs.org/projects/pineko/badge/?version=latest"></a>\n- To build the documentation from source run\n```bash\ncd docs\npoetry run make html\n```\n\n## Tests and benchmarks\n- To run unit test you can do\n```bash\npoetry run pytest\n```\n\n## Contributing\n- Your feedback is welcome! If you want to report a (possible) bug or want to ask for a new feature, please raise an issue: <a href="https://github.com/N3PDF/pineko/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/N3PDF/pineko"/></a>\n- Please follow our [Code of Conduct](https://github.com/N3PDF/pineko/blob/main/.github/CODE_OF_CONDUCT.md) and read the\n  [Contribution Guidelines](https://github.com/N3PDF/pineko/blob/main/.github/CONTRIBUTING.md)\n',
    'author': 'Alessandro Candido',
    'author_email': 'alessandro.candido@mi.infn.it',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/N3PDF/pineko',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
