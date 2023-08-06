# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docloudstuff', 'docloudstuff.events']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'docloudstuff',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'Stephen Bawks',
    'author_email': 'stephen@bawks.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stephenbawks/docloudstuff',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
