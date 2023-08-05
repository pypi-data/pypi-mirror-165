# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlite_clean']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.37,<2.0.0', 'click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['base = sqlite_clean.command:cli',
                     'fix = sqlite_clean.command:fix',
                     'lint = sqlite_clean.command:lint']}

setup_kwargs = {
    'name': 'sqlite-clean',
    'version': '0.0.3',
    'description': 'A SQLite data validation and cleanup tool.',
    'long_description': None,
    'author': 'd33bs',
    'author_email': 'dave.bunten@cuanschutz.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
