# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['disrepair']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0',
 'packaging>=21.0',
 'pypi-simple>=0.8.0',
 'requests>=2.0',
 'requirements-parser>=0.5.0',
 'rich>=12.0']

entry_points = \
{'console_scripts': ['disrepair = disrepair:check']}

setup_kwargs = {
    'name': 'disrepair',
    'version': '0.2.1',
    'description': 'Checks for out-of-date Python packages in requirements files',
    'long_description': '# disrepair\nChecks for out-of-date Python packages in requirements files\n\n## Install\n\nRun\n\n```pip install disrepair```\n\n## Usage\n\nPass the requirements file to disrepair:\n\n```disrepair path/to/requirements.in```\n\nThere are several options:\n\n```\n  -v, --verbose           Show all package statuses\n  -i, --info              Show likely package changelog/info links\n  -b, --boring            Disable the rich text formatting\n  -j, --json-repo TEXT    Repository URL for the JSON API\n  -s, --simple-repo TEXT  Repository URL for the Simple API\n  -S, --simple-only       Only use the Simple API to lookup versions\n  -J, --json-only         Only use the JSON API to lookup versions\n  -p, --pin-warn          Warn when a package version is not pinned\n```',
    'author': 'David Bell',
    'author_email': 'dave@evad.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/divad/disrepair',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
