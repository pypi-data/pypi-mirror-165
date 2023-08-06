# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['divisible']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['is_divisible = divisible.main:is_divisible',
                     'is_even = divisible.main:is_even',
                     'is_odd = divisible.main:is_odd']}

setup_kwargs = {
    'name': 'divisible',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'DukeNgn',
    'author_email': 'triduc2311m@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
