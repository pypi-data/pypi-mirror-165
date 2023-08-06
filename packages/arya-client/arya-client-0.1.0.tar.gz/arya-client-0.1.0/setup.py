# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arya', 'arya.channel', 'arya.segment', 'arya.telem', 'arya.util']

package_data = \
{'': ['*']}

install_requires = \
['arya-freighter>=0.1.0,<0.2.0',
 'mypy>=0.971,<0.972',
 'numpy>=1.23.1,<2.0.0',
 'websockets>=10.3,<11.0']

setup_kwargs = {
    'name': 'arya-client',
    'version': '0.1.0',
    'description': 'Arya Client Library',
    'long_description': None,
    'author': 'emiliano bonilla',
    'author_email': 'emilbon99@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://aryaanalytics.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
