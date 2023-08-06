# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['utils']

package_data = \
{'': ['*'], 'utils': ['data/*', 'documentation/drawIO/*']}

install_requires = \
['pandas>=1.4.3,<2.0.0']

setup_kwargs = {
    'name': 'datamonk-utils',
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': 'Vit Mrnavek',
    'author_email': 'vit.mrnavek@datamonk.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.0,<3.10.0',
}


setup(**setup_kwargs)
