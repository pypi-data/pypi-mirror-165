# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tads', 'tads.actors', 'tads.actors.documents', 'tads.core']

package_data = \
{'': ['*']}

install_requires = \
['numpy', 'openpyxl', 'pandas', 'python-multipart', 'xlrd']

setup_kwargs = {
    'name': 'tads',
    'version': '0.1.3',
    'description': 'Tads is reserved for ...',
    'long_description': '',
    'author': 'FL03',
    'author_email': 'jo3mccain@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.jetbrains.space/scattered-systems/tads/py-tads.git',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
