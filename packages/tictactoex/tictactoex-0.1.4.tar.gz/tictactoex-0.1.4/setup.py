# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tictactoex']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tictactoex',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Caetano',
    'author_email': 'ricardo.caetano@fabamaq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3',
}


setup(**setup_kwargs)
