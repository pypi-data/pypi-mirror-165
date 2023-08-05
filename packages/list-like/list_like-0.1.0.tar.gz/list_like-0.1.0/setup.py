# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['list_like']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'list-like',
    'version': '0.1.0',
    'description': "Test whether an object is an iterable that's not a string or mapping",
    'long_description': None,
    'author': 'Corentin Moevus',
    'author_email': 'c.moevus@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
