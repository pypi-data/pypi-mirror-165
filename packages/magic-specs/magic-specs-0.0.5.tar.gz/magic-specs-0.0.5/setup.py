# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magic_specs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'magic-specs',
    'version': '0.0.5',
    'description': '',
    'long_description': '# Magic value specification utilities\n\n[![Coverage Status][coverage-badge]][coverage]\n[![GitHub Workflow Status][status-badge]][status]\n[![PyPI][pypi-badge]][pypi]\n[![GitHub][licence-badge]][licence]\n[![GitHub Last Commit][repo-badge]][repo]\n[![GitHub Issues][issues-badge]][issues]\n[![Python Version][version-badge]][pypi]\n\n```shell\npip install magic-specs\n```\n\n---\n\n**Documentation**: [https://mrthearman.github.io/magic-specs/](https://mrthearman.github.io/magic-specs/)\n\n**Source Code**: [https://github.com/MrThearMan/magic-specs/](https://github.com/MrThearMan/magic-specs/)\n\n---\n\n\nThis library contains utilities for making definitions for magic values.\n\n\n[coverage-badge]: https://coveralls.io/repos/github/MrThearMan/magic-specs/badge.svg?branch=main\n[status-badge]: https://img.shields.io/github/workflow/status/MrThearMan/magic-specs/Tests\n[pypi-badge]: https://img.shields.io/pypi/v/magic-specs\n[licence-badge]: https://img.shields.io/github/license/MrThearMan/magic-specs\n[repo-badge]: https://img.shields.io/github/last-commit/MrThearMan/magic-specs\n[issues-badge]: https://img.shields.io/github/issues-raw/MrThearMan/magic-specs\n[version-badge]: https://img.shields.io/pypi/pyversions/magic-specs\n\n[coverage]: https://coveralls.io/github/MrThearMan/magic-specs?branch=main\n[status]: https://github.com/MrThearMan/magic-specs/actions/workflows/main.yml\n[pypi]: https://pypi.org/project/magic-specs\n[licence]: https://github.com/MrThearMan/magic-specs/blob/main/LICENSE\n[repo]: https://github.com/MrThearMan/magic-specs/commits/main\n[issues]: https://github.com/MrThearMan/magic-specs/issues',
    'author': 'Matti Lamppu',
    'author_email': 'lamppu.matti.akseli@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MrThearMan/magic-specs',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
