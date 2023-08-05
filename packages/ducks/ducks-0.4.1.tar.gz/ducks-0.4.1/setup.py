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
    'version': '0.4.1',
    'description': 'Provides Dex, a Python container for indexing objects of any type.',
    'long_description': '[![tests Actions Status](https://github.com/manimino/ducks/workflows/tests/badge.svg)](https://github.com/manimino/ducks/actions)\n[![Coverage - 100%](https://img.shields.io/static/v1?label=Coverage&message=100%&color=2ea44f)](test/cov.txt)\n[![license - MIT](https://img.shields.io/static/v1?label=license&message=MIT&color=2ea44f)](/LICENSE)\n![python - 3.7+](https://img.shields.io/static/v1?label=python&message=3.7%2B&color=2ea44f)\n\n# ducks\n\nProvides Dex, a Python container for indexing objects of any type.\n\n#### Install: \n\n```\npip install ducks\n```\n\n#### Usage:\n```\nfrom ducks import Dex\n\nobjects = [{\'x\': 4, \'y\': 1}, {\'x\': 6, \'y\': 2}, {\'x\': 8, \'y\': 5}]\n\n# Create a Dex containing objects. Index on x and y.\ndex = Dex(objects, [\'x\', \'y\'])  \n\n# find the ones you want\ndex[{                           # find objects\n    \'x\': {\'>\': 5, \'<\': 10},     # where x is between 5 and 10\n    \'y\': {\'in\': [1, 2, 3]}      # and y is 1, 2, or 3\n}]\n# result: [{\'x\': 6, \'y\': 2}]\n```\n\nValid operators are ==, !=, <, <=, >, >=, in, not in. \n\n#### Is Dex a database?\n\nNo. But like a database, Dex uses B-tree indexes and uses them to find results very quickly. It does\nnot any do other database things like SQL, tables, etc. This keeps Dex simple, light, and performant.\n\n#### Is Dex fast?\n\nYes. Here\'s how Dex compares to other object-finders on an example task.\n\n![Example benchmark](examples/img/perf_bench.png)\n\n[Benchmark code](examples/perf_demo.ipynb)\n\nThe closest thing to a Dex is an in-memory SQLite. While SQLite is a fantastic database, it requires\nmore overhead. As such, Dex is generally faster.\n\n### Class APIs\n\nThere are three containers.\n - Dex: Can `add`, `remove`, and `update` objects after creation.\n[API]((https://ducks.readthedocs.io/en/latest/ducks.mutable.html#ducks.mutable.main.Dex))\n - ConcurrentDex: Same as Dex, but thread-safe.\n[API](https://ducks.readthedocs.io/en/latest/ducks.concurrent.html#ducks.concurrent.main.ConcurrentDex)\n - FrozenDex: Cannot be changed after creation, it\'s read-only. But it\'s super fast, and of course thread-safe.\n[API](https://ducks.readthedocs.io/en/latest/ducks.frozen.html#ducks.frozen.main.FrozenDex)\n\nAll three can be pickled using the special functions `ducks.save(dex, file)` / `ducks.load(file)`. \n\n\n### Fancy Tricks\n\nExpand for sample code.\n\n<details>\n<summary>Use functions of the object as attributes</summary>\n<br />\nYou can also index on functions evaluated on the object, as if they were attributes.\n\nFind palindromes of length 5 or 7:\n```\nfrom ducks import Dex\nstrings = [\'bob\', \'fives\', \'kayak\', \'stats\', \'pullup\', \'racecar\']\n\n# define a function that takes the object as input\ndef is_palindrome(s):\n    return s == s[::-1]\n\ndex = Dex(strings, [is_palindrome, len])\ndex[{\n    is_palindrome: True, \n    len: {\'in\': [5, 7]}\n}]\n# result: [\'kayak\', \'racecar\', \'stats\']\n```\n\nFunctions are evaluated on the object when it is added to the Dex. \n\n</details>\n\n<details>\n<summary>Access nested data using functions</summary>\n<br />\nUse functions to get values from nested data structures.\n\n```\nfrom ducks import Dex\n\nobjs = [\n    {\'a\': {\'b\': [1, 2, 3]}},\n    {\'a\': {\'b\': [4, 5, 6]}}\n]\n\ndef get_nested(obj):\n    return obj[\'a\'][\'b\'][0]\n\ndex = Dex(objs, [get_nested])\ndex[{get_nested: 4}]\n# result: {\'a\': {\'b\': [4, 5, 6]}}\n```\n</details>\n\n<details>\n<summary>Handle missing attributes</summary>\n<br />\n\nObjects don\'t need to have every attribute.\n\n - Objects that are missing an attribute will not be stored under that attribute. This saves lots of memory.\n - To find all objects that have an attribute, match the special value <code>ANY</code>. \n - To find objects missing the attribute, exclude <code>ANY</code>.\n - In functions, raise <code>MissingAttribute</code> to tell Dex the object is missing.\n\nExample:\n```\nfrom ducks import Dex, ANY\nfrom ducks.exceptions import MissingAttribute\n\nobjs = [{\'a\': 1}, {\'a\': 2}, {}]\n\ndef get_a(obj):\n    try:\n        return obj[\'a\']\n    except KeyError:\n        raise MissingAttribute  # tell Dex this attribute is missing\n\ndex = Dex(objs, [\'a\', get_a])\n\ndex[{\'a\': ANY}]          # result: [{\'a\': 1}, {\'a\': 2}]\ndex[{get_a: ANY}]        # result: [{\'a\': 1}, {\'a\': 2}]\ndex[{\'a\': {\'!=\': ANY}}]  # result: [{}]\n```\n\nNote that `None` is treated as a normal value and is stored.\n</details>\n\n\n### Recipes\n \n - [Auto-updating](https://github.com/manimino/ducks/blob/main/examples/update.py) - Keep Dex updated when objects change\n - [Wordle solver](https://github.com/manimino/ducks/blob/main/examples/wordle.ipynb) - Solve string matching problems faster than regex\n - [Collision detection](https://github.com/manimino/ducks/blob/main/examples/collision.py) - Find objects based on type and proximity (grid-based)\n - [Percentiles](https://github.com/manimino/ducks/blob/main/examples/percentile.py) - Find by percentile (median, p99, etc.)\n\n\n## How Dex works\n\nFor each attribute in the Dex, it holds a B-tree that maps every unique value to the set of objects with \nthat value. \n\nThis is a rough idea of the data structure: \n```\nclass Dex:\n    indexes = {\n        \'attribute1\': BTree({10: set(some_obj_ids), 20: set(other_obj_ids)}),\n        \'attribute2\': BTree({\'abc\': set(some_obj_ids), \'def\': set(other_obj_ids)}),\n    }\n    obj_map = {obj_ids: objects}\n}\n```\n\nDuring a lookup, the object ID sets matching each query value are retrieved. Then set operations like `union`, \n`intersect`, and `difference` are applied to get the matching object IDs. Finally, the object IDs are converted\nto objects and returned.\n\nIn practice, Dex and FrozenDex have a bit more to them, as they are optimized to have much better\nmemory usage and speed than a naive implementation. For example, FrozenDex uses an array-based tree structure.\n\nSee the "how it works" pages for more detail:\n - [How Dex works](ducks/mutable/how_it_works.md)\n - [How ConcurrentDex works](ducks/concurrent/how_it_works.md)\n - [How FrozenDex works](ducks/frozen/how_it_works.md)\n',
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
