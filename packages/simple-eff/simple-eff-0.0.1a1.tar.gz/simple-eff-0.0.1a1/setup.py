# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_eff']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'simple-eff',
    'version': '0.0.1a1',
    'description': 'A simple tiny algebraic effects library for Python',
    'long_description': None,
    'author': 'Catminusminus',
    'author_email': 'getomya@svk.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
