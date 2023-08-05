# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['secretset']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'openpyxl>=3.0.10,<4.0.0', 'pandas>=1.4.3,<2.0.0']

entry_points = \
{'console_scripts': ['secretset = secretset.main:main']}

setup_kwargs = {
    'name': 'secretset',
    'version': '0.1.1',
    'description': 'Command line interface to anonymize data.',
    'long_description': '[![ci](https://github.com/cnpryer/secretset/workflows/ci/badge.svg)](https://github.com/cnpryer/secretset/actions)\n[![PyPI Latest Release](https://img.shields.io/pypi/v/secretset.svg)](https://pypi.org/project/secretset/)\n\n# secretset\n\nCommand line interface to anonymize data.\n\n## Installation\n\n```console\n$ pip install secretset\n```\n\n## Usage\n\nFor information on commands available run `secretset --help`.\n\n### Compatible sources\n\n- Excel\n- CSV\n\n### Anonymize files\n\nYou can anonymize files using:\n\n```\n$ secretset file.xlsx --target col1\n```\n\n### Anonymize multiple files\n\nYou can anonymize multiple related files using:\n\n```\n$ secretset file1.xlsx file2.csv \\\n    --align col1 \\\n    --target col2 \\\n    --target col3\n```\n',
    'author': 'Chris Pryer',
    'author_email': 'cnpryer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
