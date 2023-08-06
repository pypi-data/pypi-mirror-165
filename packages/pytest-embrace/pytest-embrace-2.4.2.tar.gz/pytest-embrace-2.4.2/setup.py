# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_embrace']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.3.0,<23.0.0',
 'isort>=5.10.1,<6.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'pyperclip>=1.8.2,<2.0.0',
 'pytest>=7.0,<8.0']

extras_require = \
{':python_version == "3.8"': ['typing-extensions>=4.2.0,<5.0.0']}

entry_points = \
{'console_scripts': ['embrace = pytest_embrace.cli:main'],
 'pytest11': ['pytest_embrace = pytest_embrace.plugin']}

setup_kwargs = {
    'name': 'pytest-embrace',
    'version': '2.4.2',
    'description': '💝  Dataclasses-as-tests. Describe the runtime once and multiply coverage with no boilerplate.',
    'long_description': '[![PyPI version](https://badge.fury.io/py/pytest-embrace.svg)](https://badge.fury.io/py/pytest-embrace) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/pytest-embrace.svg)](https://pypi.python.org/pypi/pytest-embrace/) ![CI](https://github.com/ainsleymcgrath/pytest-embrace/actions/workflows/ci.yml/badge.svg)\n\n![logotype](https://raw.githubusercontent.com/ainsleymcgrath/pytest-embrace/master/docs/logotype.svg)\n\nThe `pytest-embrace` plugin enables judicious, repeatable, lucid unit testing using.\n\nCheck out [the docs](https://ainsleymcgrath.github.io/pytest-embrace/) for more.\n',
    'author': 'Ainsley McGrath',
    'author_email': 'mcgrath.ainsley@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
