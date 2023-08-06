# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wordnet_lookup', 'wordnet_lookup.os']

package_data = \
{'': ['*']}

install_requires = \
['baseblock']

setup_kwargs = {
    'name': 'wordnet-lookup',
    'version': '0.1.0',
    'description': 'Static Dictionaries for Rapid Wordnet Lookups',
    'long_description': None,
    'author': 'Craig Trim',
    'author_email': 'craigtrim@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.5',
}


setup(**setup_kwargs)
