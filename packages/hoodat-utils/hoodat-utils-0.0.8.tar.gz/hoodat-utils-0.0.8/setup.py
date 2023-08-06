# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hoodat_utils', 'hoodat_utils.alembic', 'hoodat_utils.alembic.versions']

package_data = \
{'': ['*']}

install_requires = \
['Flask-Login>=0.6.0,<0.7.0',
 'Flask-SQLAlchemy>=2.5.1,<3.0.0',
 'PyMySQL>=1.0.2,<2.0.0',
 'SQLAlchemy>=1.4.35,<2.0.0',
 'alembic>=1.8.1,<2.0.0',
 'google-cloud-storage>=1.20.0,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pytest>=7.1.1,<8.0.0']

setup_kwargs = {
    'name': 'hoodat-utils',
    'version': '0.0.8',
    'description': '',
    'long_description': None,
    'author': 'Eugene Brown',
    'author_email': 'efbbrown@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
