# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tree_to_table',
 'tree_to_table.mappers',
 'tree_to_table.sqlalchemy',
 'tree_to_table.table',
 'tree_to_table.transforms']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.40,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'mypy>=0.971,<0.972',
 'pytest>=7.1.2,<8.0.0',
 'sqlalchemy-stubs>=0.4,<0.5']

setup_kwargs = {
    'name': 'tree-to-table',
    'version': '0.1.0',
    'description': 'A lightweight SQLAlchemy extension which flattens nested JSON into a tabular format',
    'long_description': None,
    'author': 'James Seymour',
    'author_email': 'james.seymour@cubiko.com.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
