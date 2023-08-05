# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pygmentize_faster']
install_requires = \
['pygments-cache>=0.1.3,<0.2.0']

entry_points = \
{'console_scripts': ['pygmentize = pygmentize_faster:main']}

setup_kwargs = {
    'name': 'pygmentize-faster',
    'version': '1.0.0',
    'description': 'Provides a faster version of pygmentize',
    'long_description': "# Pygmentize Faster\n\nThis package uses [pygments-cache](https://github.com/xonsh/pygments-cache) to run `pygmentize` just a little bit faster.\n\nIt overrides the `pygmentize` script provided by `pygments`.\n\n## Benkmarks\n\n`pygmentize-faster` runs about twice as fast as `pygmentize`:\n\n```bash\n\n$ time fd -d1 -j1 '.py$' -x python -m pygmentize {} > /dev/null ';' /usr/lib/python3.10\nuser=65.25s system=7.81s cpu=98% total=1:14.45\n\n$ time fd -d1 -j1 '.py$' -x python -m pygmentize_faster {} > /dev/null ';' /usr/lib/python3.10\nuser=33.61s system=4.96s cpu=99% total=38.663\n\n```\n",
    'author': 'Josiah Outram Halstead',
    'author_email': 'josiah@halstead.email',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joouha/pygmentize_faster',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
