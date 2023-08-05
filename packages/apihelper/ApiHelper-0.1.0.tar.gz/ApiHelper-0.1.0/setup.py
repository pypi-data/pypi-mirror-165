# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apihelper']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['ah = apihelper.__main__:main']}

setup_kwargs = {
    'name': 'apihelper',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Samuel Broster',
    'author_email': 'sam@broster.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
