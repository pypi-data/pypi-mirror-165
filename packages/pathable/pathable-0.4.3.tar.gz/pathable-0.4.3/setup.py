# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pathable']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pathable',
    'version': '0.4.3',
    'description': 'Object-oriented paths',
    'long_description': '********\npathable\n********\n\n\nAbout\n#####\n\nObject-oriented paths\n\nKey features\n************\n\n* Traverse resources like paths\n* Access resources on demand with separate accessor layer\n\nUsage\n#####\n\n.. code-block:: python\n\n   from pathable import DictPath\n   \n   d = {\n       "parts": {\n           "part1": {\n               "name": "Part One",\n           },\n           "part2": {\n               "name": "Part Two",\n           },\n       },\n   }\n   \n   dp = DictPath(d)\n   \n   # Concatenate paths with /\n   parts = dp / "parts"\n   \n   # Stat path keys\n   "part2" in parts\n   \n   # Open path dict\n   with parts.open() as parts_dict:\n       print(parts_dict)\n\n',
    'author': 'Artur Maciag',
    'author_email': 'maciag.artur@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/p1c2u/pathable',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
