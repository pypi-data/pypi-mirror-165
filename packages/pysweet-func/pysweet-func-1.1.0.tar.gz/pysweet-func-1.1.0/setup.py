# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysweet']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pysweet-func',
    'version': '1.1.0',
    'description': 'Composable Python via syntactic sugar',
    'long_description': "pysweet-func\n============\n\n|test| |codecov| |Documentation Status| |PyPI version|\n\nWhy ``pysweet``?\n----------------\n\nPython can sometimes be unwieldy.\n\nConsider the following variants\nof the same logic:\n\n.. code:: python\n\n   acc = []\n\n   for x in range(10):\n       y = x + 1\n\n       if y % 2 == 0:\n           acc.extend([y, y * 2])\n\n.. code:: python\n\n   acc = [\n       z for y in (x + 1 for x in range(10))\n       for z in [y, y * 2] if y % 2 == 0\n   ]\n\n.. code:: python\n\n   from itertools import chain\n\n   acc = list(chain.from_iterable(map(\n       lambda x: [x, x * 2],\n       filter(\n           lambda x: x % 2 == 0,\n           map(lambda x: x + 1, range(10)),\n       ),\n   )))\n\n* The imperative style\n  can grow complex as requirements evolve;\n\n* The comprehension style\n  can get complicated when nested;\n\n* The functional style\n  is not very readable in Python.\n\nIn JavaScript, the same logic can be written:\n\n.. code:: js\n\n   acc = [...Array(10).keys()]\n       .map(x => x + 1)\n       .filter(x => x % 2 === 0)\n       .flatMap(x => [x, x * 2])\n\nWith ``pysweet``, we can analogously write:\n\n.. code:: python\n\n   from pysweet import Iterable_\n\n   acc = (\n       Iterable_(range(10))\n       .map(lambda x: x + 1)\n       .filter(lambda x: x % 2 == 0)\n       .flat_map(lambda x: [x, x * 2])\n       .to_list()\n   )\n\n``pysweet`` offers many other similar features.\n\n``pysweet`` is:\n\n* lightweight, with ~100 lines of code;\n\n* mostly syntactic sugar, hence\n  performant, easy to debug, and easy to learn;\n\n* in production use.\n\nSweeten Python with ``pysweet``!\n\nSelect features\n---------------\n\n* Iterable with method chaining,\n  cf. JavaScript and Scala:\n\n.. code:: python\n\n   from pysweet import Iterable_\n\n   (\n       Iterable_([1, 2])\n       .map(lambda x: x + 1)\n       .to_list()\n   )\n   # [2, 3]\n\n* Multi-expression lambda,\n  common in modern languages:\n\n.. code:: python\n\n   from pysweet import block_\n\n   val = lambda: block_(\n       x := 1,\n       x + 1,\n   )\n   # val() == 2\n\n* Statement as expression,\n  cf. Scala and Haskell:\n\n  (``if_`` is also the ternary operator)\n\n.. code:: python\n\n   from pysweet import if_, try_, raise_\n\n   if_(\n       True,\n       lambda: 1,\n       lambda: 2,\n   )\n   # 1\n\n   try_(\n       lambda: raise_(Exception('test')),\n       catch=lambda e: str(e),\n   )\n   # 'test'\n\nResources\n---------\n\n-  `Read the Docs <https://pysweet-func.readthedocs.io>`__\n-  `PyPI <https://pypi.org/project/pysweet-func>`__\n\n.. |test| image:: https://github.com/natso26/pysweet-func/actions/workflows/test.yml/badge.svg?branch=main&event=push\n.. |codecov| image:: https://codecov.io/gh/natso26/pysweet-func/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/natso26/pysweet-func\n.. |Documentation Status| image:: https://readthedocs.org/projects/pysweet-func/badge/?version=latest\n   :target: https://pysweet-func.readthedocs.io/en/latest/?badge=latest\n.. |PyPI version| image:: https://badge.fury.io/py/pysweet-func.svg\n   :target: https://badge.fury.io/py/pysweet-func\n",
    'author': 'Nat Sothanaphan',
    'author_email': 'natsothanaphan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/natso26/pysweet-func',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
