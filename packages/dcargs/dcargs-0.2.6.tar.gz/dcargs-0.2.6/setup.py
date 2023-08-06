# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dcargs', 'dcargs.extras']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'docstring-parser>=0.14.1,<0.15.0',
 'frozendict>=2.3.4,<3.0.0',
 'termcolor>=1.1.0,<2.0.0',
 'typing-extensions>=4.3.0,<5.0.0']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['backports.cached-property>=1.0.2,<2.0.0'],
 ':sys_platform == "win32"': ['colorama>=0.4.0,<0.5.0']}

setup_kwargs = {
    'name': 'dcargs',
    'version': '0.2.6',
    'description': 'Strongly typed, zero-effort CLI interfaces',
    'long_description': '<h1 align="">dcargs</h1>\n\n<p align="">\n    <em><a href="https://brentyi.github.io/dcargs">Documentation</a></em>\n    &nbsp;&nbsp;&bull;&nbsp;&nbsp;\n    <em><code>pip install dcargs</code></em>\n</p>\n<p align="">\n    <img alt="build" src="https://github.com/brentyi/dcargs/workflows/build/badge.svg" />\n    <img alt="mypy" src="https://github.com/brentyi/dcargs/workflows/mypy/badge.svg?branch=master" />\n    <img alt="lint" src="https://github.com/brentyi/dcargs/workflows/lint/badge.svg" />\n    <a href="https://codecov.io/gh/brentyi/dcargs">\n        <img alt="codecov" src="https://codecov.io/gh/brentyi/dcargs/branch/master/graph/badge.svg" />\n    </a>\n    <a href="https://pypi.org/project/dcargs/">\n        <img alt="codecov" src="https://img.shields.io/pypi/pyversions/dcargs" />\n    </a>\n</p>\n\n<p align="">\n    <strong><code>dcargs</code></strong> is a library for typed CLI interfaces\n    and configuration objects.\n</p>\n\n<p align="">\n    Our core interface, <code>dcargs.cli()</code>, generates argument parsers from type-annotated\n    <br />callables: functions, dataclasses, classes, and <em>nested</em> dataclasses and classes.\n</p>\n\n<p align="">\n    This can be used as a replacement for <code>argparse</code>:\n</p>\n\n<table align="">\n<tr>\n    <td><strong>with argparse</strong></td>\n    <td><strong>with dcargs</strong></td>\n</tr>\n<tr>\n<td>\n\n```python\n"""Sum two numbers from argparse."""\n\nimport argparse\nparser = argparse.ArgumentParser()\nparser.add_argument(\n    "--a",\n    type=int,\n    required=True,\n)\nparser.add_argument(\n    "--b",\n    type=int,\n    default=3,\n)\nargs = parser.parse_args()\n\nprint(args.a + args.b)\n```\n\n</td>\n<td>\n\n```python\n"""Sum two numbers by calling a\nfunction with dcargs."""\n\nimport dcargs\n\ndef main(a: int, b: int = 3) -> None:\n    print(a + b)\n\ndcargs.cli(main)\n```\n\n---\n\n```python\n"""Sum two numbers by instantiating\na dataclass with dcargs."""\n\nfrom dataclasses import dataclass\n\nimport dcargs\n\n@dataclass\nclass Args:\n    a: int\n    b: int = 3\n\nargs = dcargs.cli(Args)\nprint(args.a + args.b)\n```\n\n</td>\n</tr>\n</table>\n\n<p align="">\n    For more sophisticated examples, see\n    <a href="https://brentyi.github.io/dcargs">our documentation</a>.\n</p>\n',
    'author': 'brentyi',
    'author_email': 'brentyi@berkeley.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/brentyi/dcargs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
