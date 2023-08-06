# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ctrlmaniac']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ctrlmaniac',
    'version': '0.1.0',
    'description': "Davide DC's GitHub Readme profile",
    'long_description': None,
    'author': 'Davide Di Criscito',
    'author_email': 'davide.dicriscito@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
