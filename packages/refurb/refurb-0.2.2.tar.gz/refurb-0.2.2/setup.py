# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['refurb',
 'refurb.checks',
 'refurb.checks.builtin',
 'refurb.checks.builtin.list_extend',
 'refurb.checks.contextlib',
 'refurb.checks.function',
 'refurb.checks.iterable',
 'refurb.checks.iterable.in_tuple',
 'refurb.checks.logical',
 'refurb.checks.pathlib',
 'refurb.checks.readability',
 'refurb.checks.string']

package_data = \
{'': ['*']}

install_requires = \
['mypy>=0.971,<0.972']

entry_points = \
{'console_scripts': ['refurb = refurb.__main__:main']}

setup_kwargs = {
    'name': 'refurb',
    'version': '0.2.2',
    'description': 'A tool for refurbish and modernize Python codebases',
    'long_description': '# Refurb\n\nA tool for refurbishing and modernizing Python codebases.\n\n## Example\n\n```python\n# main.py\n\nwith open("file.txt") as f:\n    contents = f.read()\n```\n\nRunning:\n\n```\n$ refurb main.py\ntmp.py:3:1 [FURB101]: Use `y = Path(x).read_text()` instead of `with open(x, ...) as f: y = f.read()`\n```\n\n## Installing\n\nBefore installing, it is recommended that you setup a [virtual environment](https://docs.python.org/3/tutorial/venv.html).\n\n```\n$ pip3 install refurb\n$ refurb file.py\n```\n\n## Installing (for development)\n\n```\n$ make install\n```\n\nTests can be ran all at once with `make test`, or you can run each tool on its own using\n`make black`, `make flake8`, and so on.\n\nUnit tests can be ran with `pytest` or `make test-unit`.\n\n> Since the end-to-end (e2e) tests are slow, they are not ran when running `make test`.\n> You will need to run `make test-e2e` to run them.\n\n## Why does this exist?\n\nI love doing code reviews: I like taking something and making it better, faster, more\nelegant, and so on. Lots of static analysis tools already exist, but none of them seem\nto be focused on making code more elegant, more readable, more modern. That is what\nRefurb tries to do.\n\n## What Refurb IS NOT\n\nRefurb is not a linter or a type checker. It is not meant as a first-line of defense for\nfinding bugs, it is meant for making nice code look even better.\n',
    'author': 'dosisod',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dosisod/refurb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
