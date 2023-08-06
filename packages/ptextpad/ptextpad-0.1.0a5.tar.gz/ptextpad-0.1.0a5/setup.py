# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ptextpad', 'ptextpad.submod', 'ptextpad.ui']

package_data = \
{'': ['*'],
 'ptextpad': ['singlehtml/*', 'singlehtml/_images/*', 'singlehtml/_static/*'],
 'ptextpad.ui': ['images/*']}

install_requires = \
['PyQt5>=5.15.7,<6.0.0',
 'about-time>=4.1.0,<5.0.0',
 'cchardet>=2.1.7,<3.0.0',
 'chardet>=4.0.0,<5.0.0',
 'fastlid>=0.1.7,<0.2.0',
 'html2text>=2020.1.16,<2021.0.0',
 'icecream>=2.1.1,<3.0.0',
 'install>=1.3.5,<2.0.0',
 'logzero>=1.7.0,<2.0.0',
 'nltk>=3.7,<4.0',
 'nose>=1.3.7,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'pysrt>=1.1.2,<2.0.0',
 'pysubs2>=1.4.2,<2.0.0',
 'python-docx>=0.8.11,<0.9.0',
 'radio-mlbee-client>=0.1.0a0,<0.2.0',
 'requests>=2.28.1,<3.0.0',
 'seg-text>=0.1.2,<0.2.0',
 'set-loglevel>=0.1.2,<0.2.0',
 'stop-thread>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['ptextpad = ptextpad.__main__:main']}

setup_kwargs = {
    'name': 'ptextpad',
    'version': '0.1.0a5',
    'description': 'ptextpad',
    'long_description': '# ptextpad\n[![pytest](https://github.com/ffreemt/ptextpad/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/ptextpad/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8.3%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/ptextpad.svg)](https://badge.fury.io/py/ptextpad)\n\na parallel text editor\n\n## Install it\n\n```shell\npip install ptextpad --upgrade\n# pip install git+https://github.com/ffreemt/ptextpad\n# poetry add git+https://github.com/ffreemt/ptextpad\n# git clone https://github.com/ffreemt/ptextpad && cd ptextpad\n```\n\n## Use it\n```shell\npython -m ptextpad\n# or\n# ptextpad\n```\n\nSet `LOGLEVEL=10` to see loads of debug messages, e.g.\n```shell\nset LOGLEVEL=10  \n# linux/mac: export LOGLEVEL=10\npython -m ptextpad\n```\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/ptextpad',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)
