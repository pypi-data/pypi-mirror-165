# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mock_ppp',
 'mock_ppp..ipynb_checkpoints',
 'mock_ppp.module1',
 'mock_ppp.module1..ipynb_checkpoints',
 'mock_ppp.module2',
 'mock_ppp.module2..ipynb_checkpoints']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mock-ppp',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'malgar',
    'author_email': 'mglalvarezg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
