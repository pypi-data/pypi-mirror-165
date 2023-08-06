# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tictactoex']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tictactoex',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Caetano',
    'author_email': 'ricardo.caetano@fabamaq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4',
}


setup(**setup_kwargs)
