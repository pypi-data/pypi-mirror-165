# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['syncthing']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.2,<3.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'python-syncthing-client',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'luke lombardi',
    'author_email': 'luke@slai.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
