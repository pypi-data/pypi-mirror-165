# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['divisible']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'divisible',
    'version': '0.1.3',
    'description': 'Great Python package to check for divisibility.',
    'long_description': '# Divisible\n\nGreat python package for all your hmm-is-this-number-divisible-by-this-number needs!\n\n### Installation:\n\n```\npip install divisible\n## --- OR ---\npoetry add divisible\n```\n**Voilà**, done.\n\n### Usage\n```\nfrom divisible import is_divisible\n\nis_divisible(200, 25) # --> True\n```\n\nNow supports is_even and is_odd, wow.\n\n```\nfrom divisible import is_odd\n\nis_odd(200) # --> False\n```\n\n```\nfrom divisible import is_even\n\nis_even(200) # --> True\n```\n',
    'author': 'DukeNgn',
    'author_email': 'triduc2311m@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DucNgn/divisible',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
