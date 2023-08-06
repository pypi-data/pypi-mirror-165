# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdbfairy', 'pdbfairy.commands']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.74,<2.0',
 'click>=7.0,<8.0',
 'dimagi-memoized>=1.1.3,<2.0.0',
 'numpy>=1.23,<1.24']

entry_points = \
{'console_scripts': ['pdbfairy = pdbfairy.main:main']}

setup_kwargs = {
    'name': 'pdbfairy',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'Danny Roberts',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
