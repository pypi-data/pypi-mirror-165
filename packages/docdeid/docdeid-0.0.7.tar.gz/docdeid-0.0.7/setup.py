# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docdeid',
 'docdeid.annotation',
 'docdeid.datastructures',
 'docdeid.document',
 'docdeid.string',
 'docdeid.tokenizer']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.1,<2.0.0']

setup_kwargs = {
    'name': 'docdeid',
    'version': '0.0.7',
    'description': 'Under construction.',
    'long_description': None,
    'author': 'Vincent Menger',
    'author_email': 'vmenger@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
