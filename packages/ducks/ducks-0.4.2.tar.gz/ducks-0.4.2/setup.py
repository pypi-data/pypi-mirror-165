# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ducks', 'ducks.concurrent', 'ducks.frozen', 'ducks.mutable']

package_data = \
{'': ['*']}

install_requires = \
['cykhash>=2.0.0,<3.0.0',
 'numpy>=1.14,<2.0',
 'readerwriterlock>=1.0.9,<2.0.0',
 'sortednp>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'ducks',
    'version': '0.4.2',
    'description': 'Provides Dex, a Python container for indexing objects of any type.',
    'long_description': "[![tests Actions Status](https://github.com/manimino/ducks/workflows/tests/badge.svg)](https://github.com/manimino/ducks/actions)\n[![Coverage - 100%](https://img.shields.io/static/v1?label=Coverage&message=100%&color=2ea44f)](test/cov.txt)\n[![license - MIT](https://img.shields.io/static/v1?label=license&message=MIT&color=2ea44f)](/LICENSE)\n![python - 3.7+](https://img.shields.io/static/v1?label=python&message=3.7%2B&color=2ea44f)\n\n# ducks 🦆\n\nProvides Dex, a Python container for indexing objects of any type.\n\n#### Install\n\n```\npip install ducks\n```\n\n#### Usage\n\n```\nfrom ducks import Dex\n\nobjects = [{'x': 4, 'y': 1}, {'x': 6, 'y': 2}, {'x': 8, 'y': 5}]\n\n# Create a Dex containing the objects. Index on x and y.\ndex = Dex(objects, ['x', 'y'])  \n\n# find the ones you want\ndex[{                           # find objects\n    'x': {'>': 5, '<': 10},     # where x is between 5 and 10\n    'y': {'in': [1, 2, 3]}      # and y is 1, 2, or 3\n}]\n# result: [{'x': 6, 'y': 2}]\n```\n\nValid operators are ==, !=, <, <=, >, >=, in, not in. \n\n#### Docs\n\nThere's more to `ducks` than making a `Dex` of `dict`s. [See the docs.](https://ducks.readthedocs.io)\n",
    'author': 'Theo Walker',
    'author_email': 'theo.ca.walker@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/manimino/ducks/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
