# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['huak']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'huak',
    'version': '0.0.0',
    'description': '',
    'long_description': None,
    'author': 'Chris Pryer',
    'author_email': 'cnpryer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
