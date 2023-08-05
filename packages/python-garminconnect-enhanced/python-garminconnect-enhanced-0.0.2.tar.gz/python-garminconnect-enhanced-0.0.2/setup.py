# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['garminconnect']

package_data = \
{'': ['*']}

install_requires = \
['cloudscraper>=1.2.63,<2.0.0',
 'poetryup>=0.10.0,<0.11.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'python-garminconnect-enhanced',
    'version': '0.0.2',
    'description': 'A fork of python-garminconnect with additional functionality to upload activities',
    'long_description': None,
    'author': 'Marvin Straathof',
    'author_email': 'marvinstraathof@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
