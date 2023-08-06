# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['descarts']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'descarts',
    'version': '0.0.1',
    'description': 'Data Science Algorithms for Time Series',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
