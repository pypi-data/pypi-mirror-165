# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['reparsec', 'reparsec.core']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.1,<5.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.8,<0.9']}

setup_kwargs = {
    'name': 'reparsec',
    'version': '0.4.2',
    'description': 'Parser',
    'long_description': '[![Build status](https://github.com/ethframe/reparsec/workflows/Tests/badge.svg?branch=master)](https://github.com/ethframe/reparsec/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush)\n[![codecov.io](https://codecov.io/gh/ethframe/reparsec/branch/master/graph/badge.svg)](https://codecov.io/gh/ethframe/reparsec)\n[![Documentation status](https://readthedocs.org/projects/reparsec/badge/?version=latest)](https://reparsec.readthedocs.io/en/latest/?badge=latest)\n[![PyPI version](https://img.shields.io/pypi/v/reparsec)](https://pypi.org/project/reparsec)\n\n# reparsec\n\nSmall parsec-like parser combinators library with semi-automatic error recovery.\n\n## Installation\n\n```\npip install reparsec\n```\n\n## Usage\n\n* [Tutorial](https://reparsec.readthedocs.io/en/latest/pages/tutorial.html)\n* [Documentation](https://reparsec.readthedocs.io/en/latest/index.html)\n\n## Example\n\nWith `reparsec`, simple arithmetic expression parser and evaluator could be written like this:\n\n```python\nfrom typing import Callable\n\nfrom reparsec import Delay\nfrom reparsec.scannerless import literal, parse, regexp\nfrom reparsec.sequence import eof\n\n\ndef op_action(op: str) -> Callable[[int, int], int]:\n    return {\n        "+": lambda a, b: a + b,\n        "-": lambda a, b: a - b,\n        "*": lambda a, b: a * b,\n    }[op]\n\n\nspaces = regexp(r"\\s*")\nnumber = regexp(r"\\d+").fmap(int) << spaces\nmul_op = regexp(r"[*]").fmap(op_action) << spaces\nadd_op = regexp(r"[-+]").fmap(op_action) << spaces\nl_paren = literal("(") << spaces\nr_paren = literal(")") << spaces\n\nexpr = Delay[str, int]()\nexpr.define(\n    (\n        number |\n        expr.between(l_paren, r_paren)\n    )\n    .chainl1(mul_op)\n    .chainl1(add_op)\n)\n\nparser = expr << eof()\n```\n\nThis parser can:\n\n* evaluate an expression:\n  ```python\n  >>> parser.parse("1 + 2 * (3 + 4)").unwrap()\n  15\n  ```\n* report first syntax error:\n  ```python\n  >>> parser.parse("1 + 2 * * (3 + 4 5)").unwrap()\n  Traceback (most recent call last):\n    ...\n  reparsec.types.ParseError: at 8: expected \'(\'\n  ```\n* attempt to recover and report multiple syntax errors:\n  ```python\n  >>> parser.parse("1 + 2 * * (3 + 4 5)", recover=True).unwrap()\n  Traceback (most recent call last):\n    ...\n  reparsec.types.ParseError: at 8: expected \'(\' (skipped 2 tokens), at 17: expected \')\' (skipped 1 token)\n  ```\n* automatically repair input and return some result:\n  ```python\n  >>> parser.parse("1 + 2 * * (3 + 4 5)", recover=True).unwrap(recover=True)\n  15\n  ```\n* track line and column numbers:\n  ```python\n  >>> parse(parser, """1 +\n  ... 2 * * (\n  ... 3 + 4 5)""", recover=True).unwrap()\n  Traceback (most recent call last):\n    ...\n  reparsec.types.ParseError: at 2:5: expected \'(\' (skipped 2 tokens), at 3:7: expected \')\' (skipped 1 token)\n  ```\n\nMore examples:\n  * [JSON parser](https://github.com/ethframe/reparsec/blob/master/tests/parsers/json.py)\n  * [Scannerless JSON parser](https://github.com/ethframe/reparsec/blob/master/tests/parsers/json_scannerless.py)\n',
    'author': 'ethframe',
    'author_email': 'ethframe@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ethframe/reparsec',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
