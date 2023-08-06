# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['habitshare_api_python']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'habitshare-api-python',
    'version': '1.0.0',
    'description': 'Unofficial Python API client for HabitShare social habit tracking app.',
    'long_description': None,
    'author': 'Cyrus Kirk',
    'author_email': 'cyrusjkirk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
