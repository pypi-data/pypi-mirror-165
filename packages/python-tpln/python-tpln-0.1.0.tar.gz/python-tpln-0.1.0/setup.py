# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tpln', 'tpln.tasks']

package_data = \
{'': ['*']}

install_requires = \
['asyncio>=3.4.3,<4.0.0',
 'matplotlib>=3.5.3,<4.0.0',
 'networkx>=2.8.5,<3.0.0',
 'pygraphviz>=1.10,<2.0']

setup_kwargs = {
    'name': 'python-tpln',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Dylan',
    'author_email': 'dylan.robins@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
