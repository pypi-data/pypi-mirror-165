# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deptry']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'cookiecutter-poetry>=0.3.7,<0.4.0',
 'isort>=5.10.1,<6.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['deptry = deptry.cli:deptry']}

setup_kwargs = {
    'name': 'deptry',
    'version': '0.0.2',
    'description': 'A repository to check for unused dependencies in a poetry managed python project',
    'long_description': "# deptry\n\n[![Release](https://img.shields.io/github/v/release/fpgmaas/deptry)](https://img.shields.io/github/v/release/fpgmaas/deptry)\n[![Build status](https://img.shields.io/github/workflow/status/fpgmaas/deptry/merge-to-main)](https://img.shields.io/github/workflow/status/fpgmaas/deptry/merge-to-main)\n[![Commit activity](https://img.shields.io/github/commit-activity/m/fpgmaas/deptry)](https://img.shields.io/github/commit-activity/m/fpgmaas/deptry)\n[![Docs](https://img.shields.io/badge/docs-gh--pages-blue)](https://fpgmaas.github.io/deptry/)\n[![Code style with black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports with isort](https://img.shields.io/badge/%20imports-isort-%231674b1)](https://pycqa.github.io/isort/)\n[![License](https://img.shields.io/github/license/fpgmaas/deptry)](https://img.shields.io/github/license/fpgmaas/deptry)\n\n---\n\n__deptry__ is a command line tool to check for unused dependencies in a poetry managed python project. It does so by scanning the imported modules within all `.py` files in \na directory and it's subdirectories, and comparing those to the dependencies listed in `pyproject.toml`. \n\n---\n\n**Documentation**: <https://fpgmaas.github.io/deptry/>\n\n---\n\n## Installation and usage\n\n### Installation\n\n__deptry__ can be added to your project with \n\n```\npoetry add deptry\n```\n\nAlternatively, it can be installed with `pip install deptry`.\n\n### Prerequisites\n\nIn order to check for obsolete imports, __deptry__ should be run directly within the directory that contains the __pyproject.toml__ file, and it requires the environment created with __pyproject.toml__ to be activated.\n\n### Usage\n\nTo scan your project for obsolete imports, run\n\n```sh\ndeptry check\n```\n\nor for a more verbose version\n\n```sh\ndeptry check -v\n```\n\n__deptry__ can be configured by using additional command line arguments, or \nby adding a `[tool.deptry]` section in __pyproject.toml__.\n\nFor more information, see the documentation. //TODO\n\n---\n\nRepository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).",
    'author': 'Florian Maas',
    'author_email': 'ffpgmaas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fpgmaas/deptry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
