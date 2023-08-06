# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['violetear']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'violetear',
    'version': '0.12.2',
    'description': 'A minimalist CSS generator',
    'long_description': None,
    'author': 'Alejandro Piad',
    'author_email': 'apiad@apiad.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
