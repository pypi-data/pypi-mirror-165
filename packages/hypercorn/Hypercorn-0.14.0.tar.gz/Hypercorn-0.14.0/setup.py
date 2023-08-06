# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hypercorn',
 'hypercorn.asyncio',
 'hypercorn.middleware',
 'hypercorn.protocol',
 'hypercorn.trio']

package_data = \
{'': ['*']}

install_requires = \
['h11', 'h2>=3.1.0', 'priority', 'toml', 'wsproto>=0.14.0']

extras_require = \
{':python_version < "3.8"': ['typing_extensions>=3.7.4'],
 'docs': ['pydata_sphinx_theme'],
 'h3': ['aioquic>=0.9.0,<1.0'],
 'trio': ['trio>=0.11.0'],
 'uvloop:platform_system != "Windows"': ['uvloop']}

entry_points = \
{'console_scripts': ['hypercorn = hypercorn.__main__:main']}

setup_kwargs = {
    'name': 'hypercorn',
    'version': '0.14.0',
    'description': 'A ASGI Server based on Hyper libraries and inspired by Gunicorn',
    'long_description': "Hypercorn\n=========\n\n.. image:: https://github.com/pgjones/hypercorn/raw/main/artwork/logo.png\n   :alt: Hypercorn logo\n\n|Build Status| |docs| |pypi| |http| |python| |license|\n\nHypercorn is an `ASGI\n<https://github.com/django/asgiref/blob/main/specs/asgi.rst>`_ web\nserver based on the sans-io hyper, `h11\n<https://github.com/python-hyper/h11>`_, `h2\n<https://github.com/python-hyper/hyper-h2>`_, and `wsproto\n<https://github.com/python-hyper/wsproto>`_ libraries and inspired by\nGunicorn. Hypercorn supports HTTP/1, HTTP/2, WebSockets (over HTTP/1\nand HTTP/2), ASGI/2, and ASGI/3 specifications. Hypercorn can utilise\nasyncio, uvloop, or trio worker types.\n\nHypercorn can optionally serve the current draft of the HTTP/3\nspecification using the `aioquic\n<https://github.com/aiortc/aioquic/>`_ library. To enable this install\nthe ``h3`` optional extra, ``pip install hypercorn[h3]`` and then\nchoose a quic binding e.g. ``hypercorn --quic-bind localhost:4433\n...``.\n\nHypercorn was initially part of `Quart\n<https://github.com/pgjones/quart>`_ before being separated out into a\nstandalone ASGI server. Hypercorn forked from version 0.5.0 of Quart.\n\nQuickstart\n----------\n\nHypercorn can be installed via `pip\n<https://docs.python.org/3/installing/index.html>`_,\n\n.. code-block:: console\n\n    $ pip install hypercorn\n\nand requires Python 3.7.0 or higher.\n\nWith hypercorn installed ASGI frameworks (or apps) can be served via\nHypercorn via the command line,\n\n.. code-block:: console\n\n    $ hypercorn module:app\n\nAlternatively Hypercorn can be used programatically,\n\n.. code-block:: python\n\n    import asyncio\n    from hypercorn.config import Config\n    from hypercorn.asyncio import serve\n\n    from module import app\n\n    asyncio.run(serve(app, Config()))\n\nlearn more (including a Trio example of the above) in the `API usage\n<https://hypercorn.readthedocs.io/en/latest/how_to_guides/api_usage.html>`_\ndocs.\n\nContributing\n------------\n\nHypercorn is developed on `Github\n<https://github.com/pgjones/hypercorn>`_. If you come across an issue,\nor have a feature request please open an `issue\n<https://github.com/pgjones/hypercorn/issues>`_.  If you want to\ncontribute a fix or the feature-implementation please do (typo fixes\nwelcome), by proposing a `pull request\n<https://github.com/pgjones/hypercorn/merge_requests>`_.\n\nTesting\n~~~~~~~\n\nThe best way to test Hypercorn is with `Tox\n<https://tox.readthedocs.io>`_,\n\n.. code-block:: console\n\n    $ pipenv install tox\n    $ tox\n\nthis will check the code style and run the tests.\n\nHelp\n----\n\nThe Hypercorn `documentation <https://hypercorn.readthedocs.io>`_ is\nthe best place to start, after that try searching stack overflow, if\nyou still can't find an answer please `open an issue\n<https://github.com/pgjones/hypercorn/issues>`_.\n\n\n.. |Build Status| image:: https://github.com/pgjones/hypercorn/actions/workflows/ci.yml/badge.svg\n   :target: https://github.com/pgjones/hypercorn/commits/main\n\n.. |docs| image:: https://img.shields.io/badge/docs-passing-brightgreen.svg\n   :target: https://hypercorn.readthedocs.io\n\n.. |pypi| image:: https://img.shields.io/pypi/v/hypercorn.svg\n   :target: https://pypi.python.org/pypi/Hypercorn/\n\n.. |http| image:: https://img.shields.io/badge/http-1.0,1.1,2-orange.svg\n   :target: https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol\n\n.. |python| image:: https://img.shields.io/pypi/pyversions/hypercorn.svg\n   :target: https://pypi.python.org/pypi/Hypercorn/\n\n.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg\n   :target: https://github.com/pgjones/hypercorn/blob/main/LICENSE\n",
    'author': 'pgjones',
    'author_email': 'philip.graham.jones@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pgjones/hypercorn/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
