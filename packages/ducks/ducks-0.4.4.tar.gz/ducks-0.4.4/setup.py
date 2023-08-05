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
    'version': '0.4.4',
    'description': 'Provides Dex, a Python container for indexing objects of any type.',
    'long_description': '# ducks 🦆\n\nIndex your Python objects for fast lookup by their attributes.\n\n[![tests Actions Status](https://github.com/manimino/ducks/workflows/tests/badge.svg)](https://github.com/manimino/ducks/actions)\n[![Coverage - 100%](https://img.shields.io/static/v1?label=Coverage&message=100%&color=2ea44f)](test/cov.txt)\n[![license - MIT](https://img.shields.io/static/v1?label=license&message=MIT&color=2ea44f)](/LICENSE)\n![python - 3.7+](https://img.shields.io/static/v1?label=python&message=3.7%2B&color=2ea44f)\n\n### Install\n\n```\npip install ducks\n```\n\n### Usage\n\n```\nfrom ducks import Dex\n\nobjects = [\n    {\'x\': 4, \'y\': 1}, \n    {\'x\': 6, \'y\': 3}, \n    {\'x\': 8, \'y\': 5}\n]\n\n# Create a Dex containing the objects. \n# Index on x and y.\ndex = Dex(objects, [\'x\', \'y\'])  \n\n# get objects\ndex[{                        \n    \'x\': {\'>\': 5, \'<\': 10},  # where 5 < x < 10\n    \'y\': {\'in\': [1, 2, 3]}   # and y is 1, 2, or 3\n}]\n# result: [{\'x\': 6, \'y\': 3}]\n```\n\n### It\'s fast\n\n<img src="https://github.com/manimino/ducks/blob/tweaks/docs/img/perf_bench.png" width="500" />\n\nDucks outperforms other data structures for finding Python objects.\n\n### Docs\n\nThere\'s more to ducks than making a Dex of dicts. \n\n[Read the docs.](https://ducks.readthedocs.io)\n',
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
