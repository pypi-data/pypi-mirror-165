# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['borsodi_database_model',
 'borsodi_database_model.alembic',
 'borsodi_database_model.alembic.versions',
 'borsodi_database_model.tables']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy==1.3.18']

setup_kwargs = {
    'name': 'borsodi-database-model',
    'version': '0.1.0',
    'description': 'Database table models for the Borsodi project.',
    'long_description': None,
    'author': 'Pintér Tamás',
    'author_email': 'tamas.pinter@dyntell.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
