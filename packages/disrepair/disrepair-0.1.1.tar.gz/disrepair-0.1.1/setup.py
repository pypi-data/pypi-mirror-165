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
    'version': '0.1.1',
    'description': 'Checks for out-of-date Python packages in requirements files',
    'long_description': '# disrepair\nChecks for out-of-date Python packages in requirements files\n',
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
