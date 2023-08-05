# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dep_postgres', 'tests']

package_data = \
{'': ['*']}

modules = \
['pyproject']
install_requires = \
['SQLAlchemy>=1.4.40,<2.0.0',
 'asyncpg>=0.26.0,<0.27.0',
 'dep-spec>=1.2.14,<2.0.0']

setup_kwargs = {
    'name': 'dep-module-postgres',
    'version': '0.3.14',
    'description': '',
    'long_description': None,
    'author': 'everhide',
    'author_email': 'i.tolkachnikov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
