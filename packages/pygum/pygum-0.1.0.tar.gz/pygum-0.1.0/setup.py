# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygum']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pygum',
    'version': '0.1.0',
    'description': 'A wrapper around Gum: https://github.com/charmbracelet/gum',
    'long_description': None,
    'author': 'Sam Phinizy',
    'author_email': 'sam@phin.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
