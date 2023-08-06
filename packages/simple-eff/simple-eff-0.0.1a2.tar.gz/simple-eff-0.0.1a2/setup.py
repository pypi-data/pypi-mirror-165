# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_eff']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'simple-eff',
    'version': '0.0.1a2',
    'description': 'A simple tiny algebraic effects library for Python',
    'long_description': '# Simple Eff\nA Simple Tiny (only <100 lines) Algebraic Effects Library for Python.\n\n```python\nfrom simple_eff import Effect, eff\n\nnot_integer = Effect()\n\ndef parse_int(str):\n    try:\n        return int(str)\n    except:\n        return None\n\n\n@eff\ndef sum_lines(s: str) -> int:\n    lines = s.split()\n    sum = 0\n    for line in lines:\n        match parse_int(line):\n            case None:\n                sum += yield not_integer.perform(line)\n            case num:\n                sum += num\n    return sum\n\n\ndef handle_notinteger(k, v):\n    print(f"Parse Error: {v} is not an integer.")\n    return k(0)\n\n\nif __name__ == \'__main__\':\n    twelve = sum_lines("1\\n2\\nthree\\n4\\n5")\n    twelve.on(not_integer, handle_notinteger)\n    ret = twelve.run()\n    print(f"Sum: {ret}")\n```\n\n## Acknowledgement\nThis library is ...\n- inspired by [effective-rust](https://github.com/pandaman64/effective-rust) for the API design.\n- heavily based on [ruff](https://github.com/Nymphium/ruff) for the implementation.\n',
    'author': 'Catminusminus',
    'author_email': 'getomya@svk.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
