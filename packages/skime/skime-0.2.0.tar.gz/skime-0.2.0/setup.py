# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skime', 'skime.compiler', 'skime.types']

package_data = \
{'': ['*'], 'skime': ['scheme/*']}

setup_kwargs = {
    'name': 'skime',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
