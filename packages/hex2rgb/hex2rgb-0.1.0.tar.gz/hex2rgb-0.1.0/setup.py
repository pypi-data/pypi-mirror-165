# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hex2rgb']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hex2rgb',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Mohsin-Ul-Islam',
    'author_email': 'mohsinulislam180@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
