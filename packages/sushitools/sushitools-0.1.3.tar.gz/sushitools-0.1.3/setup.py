# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sushitools', 'sushitools.cf', 'sushitools.types']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sushitools',
    'version': '0.1.3',
    'description': 'python package with various different utilities and tools to make life easier.',
    'long_description': '## 🍣 sushitools\n\npython package with various different utilities and tools to make life easier.\n',
    'author': 'munchii',
    'author_email': 'daniellmunch@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Dmunch04/sushitools',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
