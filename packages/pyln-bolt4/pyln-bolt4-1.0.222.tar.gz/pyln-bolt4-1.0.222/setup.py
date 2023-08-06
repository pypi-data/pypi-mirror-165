# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bolt4']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyln-bolt4',
    'version': '1.0.222',
    'description': 'A pure python implementation of BOLT4',
    'long_description': None,
    'author': 'Rusty Russell',
    'author_email': 'rusty@blockstream.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
