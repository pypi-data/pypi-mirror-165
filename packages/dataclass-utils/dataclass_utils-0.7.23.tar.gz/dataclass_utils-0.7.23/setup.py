# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dataclass_utils', 'dataclass_utils._internal']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=3.10']

setup_kwargs = {
    'name': 'dataclass-utils',
    'version': '0.7.23',
    'description': '',
    'long_description': None,
    'author': 'Yohei Tamura',
    'author_email': 'tamuhey@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
