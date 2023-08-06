# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openapi',
 'openapi.data',
 'openapi.db',
 'openapi.db.openapi',
 'openapi.pagination',
 'openapi.spec',
 'openapi.ws']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'SQLAlchemy-Utils>=0.38.2,<0.39.0',
 'SQLAlchemy>=1.4.27,<2.0.0',
 'aiohttp>=3.8.0,<4.0.0',
 'alembic',
 'asyncpg>=0.26.0,<0.27.0',
 'click>=8.0.3,<9.0.0',
 'email-validator>=1.2.1,<2.0.0',
 'httptools>=0.4.0,<0.5.0',
 'psycopg2-binary>=2.9.2,<3.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'simplejson>=3.17.2,<4.0.0']

extras_require = \
{':python_version < "3.9"': ['backports.zoneinfo>=0.2.1,<0.3.0'],
 'dev': ['aiodns>=3.0.0,<4.0.0',
         'PyJWT>=2.3.0,<3.0.0',
         'colorlog>=6.6.0,<7.0.0',
         'phonenumbers>=8.12.37,<9.0.0',
         'cchardet>=2.1.7,<3.0.0'],
 'docs': ['Sphinx>=5.0.2,<6.0.0',
          'sphinx-copybutton>=0.5.0,<0.6.0',
          'sphinx-autodoc-typehints>=1.12.0,<2.0.0',
          'aiohttp-theme>=0.1.6,<0.2.0',
          'recommonmark>=0.7.1,<0.8.0']}

setup_kwargs = {
    'name': 'aio-openapi',
    'version': '3.0.2',
    'description': 'Minimal OpenAPI asynchronous server application',
    'long_description': '# aio-openapi\n\n[![PyPI version](https://badge.fury.io/py/aio-openapi.svg)](https://badge.fury.io/py/aio-openapi)\n[![Python versions](https://img.shields.io/pypi/pyversions/aio-openapi.svg)](https://pypi.org/project/aio-openapi)\n[![Build](https://github.com/quantmind/aio-openapi/workflows/build/badge.svg)](https://github.com/quantmind/aio-openapi/actions?query=workflow%3Abuild)\n[![Coverage Status](https://coveralls.io/repos/github/quantmind/aio-openapi/badge.svg?branch=master)](https://coveralls.io/github/quantmind/aio-openapi?branch=master)\n[![Documentation Status](https://readthedocs.org/projects/aio-openapi/badge/?version=latest)](https://aio-openapi.readthedocs.io/en/latest/?badge=latest)\n[![Downloads](https://img.shields.io/pypi/dd/aio-openapi.svg)](https://pypi.org/project/aio-openapi/)\n\nAsynchronous web middleware for [aiohttp][] and serving Rest APIs with [OpenAPI][] v 3\nspecification and with optional [PostgreSql][] database bindings.\n\nSee the [tutorial](https://aio-openapi.readthedocs.io/en/latest/tutorial.html) for a quick introduction.\n\n\n[aiohttp]: https://aiohttp.readthedocs.io/en/stable/\n[openapi]: https://www.openapis.org/\n[postgresql]: https://www.postgresql.org/\n[sqlalchemy]: https://www.sqlalchemy.org/\n[click]: https://github.com/pallets/click\n[alembic]: http://alembic.zzzcomputing.com/en/latest/\n[asyncpg]: https://github.com/MagicStack/asyncpg\n',
    'author': 'Luca',
    'author_email': 'luca@quantmind.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/quantmind/aio-openapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
