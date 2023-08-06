# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deeplife']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'deeplife',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Yann Beauxis',
    'author_email': 'yann.beauxis@deeplife.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
