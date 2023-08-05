# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docloudstuff', 'docloudstuff.events']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.2,<2.0.0']

setup_kwargs = {
    'name': 'docloudstuff',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Stephen Bawks',
    'author_email': 'stephen@bawks.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stephenbawks/docloudstuff',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
