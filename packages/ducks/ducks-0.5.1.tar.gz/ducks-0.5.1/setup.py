# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ducks', 'ducks.concurrent', 'ducks.frozen', 'ducks.mutable']

package_data = \
{'': ['*']}

install_requires = \
['BTrees>=4.10.0,<5.0.0',
 'cykhash>=2.0.0,<3.0.0',
 'numpy>=1.14,<2.0',
 'readerwriterlock>=1.0.9,<2.0.0',
 'sortednp>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'ducks',
    'version': '0.5.1',
    'description': 'Provides Dex, a Python container for indexing objects of any type.',
    'long_description': "=========\nducks  🦆\n=========\n\nIndex your Python objects for fast lookup by their attributes.\n\n.. image:: https://github.com/manimino/ducks/workflows/tests/badge.svg\n    :target: https://github.com/manimino/ducks/actions\n    :alt: tests Actions Status\n.. image:: https://img.shields.io/static/v1?label=Coverage&message=100%&color=2ea44f\n    :target: https://github.com/manimino/ducks/blob/main/test/cov.txt\n    :alt: Coverage - 100%\n.. image:: https://img.shields.io/static/v1?label=license&message=MIT&color=2ea44f\n    :target: https://github.com/manimino/ducks/blob/main/LICENSE\n    :alt: license - MIT\n.. image:: https://img.shields.io/static/v1?label=python&message=3.7%2B&color=2ea44f\n    :target: https://github.com/manimino/ducks/\n    :alt: python - 3.7+\n\n-------\nInstall\n-------\n\n.. code-block::\n\n    pip install ducks\n\n-----\nUsage\n-----\n\nThe main container in ducks is called Dex.\n\n.. code-block::\n\n    from ducks import Dex\n\n    # make some objects\n    objects = [\n        {'x': 3, 'y': 'a'},\n        {'x': 6, 'y': 'b'},\n        {'x': 9, 'y': 'c'}\n    ]\n\n    # Create a Dex containing the objects.\n    # Index on x and y.\n    dex = Dex(objects, ['x', 'y'])\n\n    # match objects\n    dex[{\n        'x': {'>': 5, '<': 10},  # where 5 < x < 10\n        'y': {'in': ['a', 'b']}  # and y is 'a' or 'b'\n    }]\n    # result: [{'x': 6, 'y': 'b'}]\n\nThis is a Dex of dicts, but the objects can be any type.\n\nDex supports ==, !=, in, not in, <, <=, >, >=.\n\nThe indexes can be dict keys, object attributes, or custom functions.\n\n------------\nIs Dex fast?\n------------\n\nYes. Here's how Dex compares to other object-finders on an example task.\n\n.. image:: https://raw.githubusercontent.com/manimino/ducks/main/docs/img/perf_bench.png\n    :width: 600\n\n`Benchmark source <https://github.com/manimino/ducks/blob/main/examples/perf_demo.ipynb>`_\n\nThe closest thing to a Dex is an in-memory SQLite. While SQLite is a fantastic database, it requires\nmore overhead. As such, Dex is generally faster.\n\n----\nDocs\n----\n\nThere's more to ducks than making a Dex of dicts. `Continue in the docs. <https://ducks.readthedocs.io/en/latest/quick_start.html>`_\n",
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
