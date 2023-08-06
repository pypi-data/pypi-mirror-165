# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chlore', 'chlore.testing']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'SQLAlchemy',
 'WTForms>=3.0.1,<4.0.0',
 'fastapi>=0.79.0,<0.80.0',
 'pika>=1.3.0,<2.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'pyopenssl>=22.0.0,<23.0.0',
 'requests>=2.28.1,<3.0.0',
 'structlog>=21.5.0,<22.0.0']

setup_kwargs = {
    'name': 'chlore',
    'version': '0.12.7',
    'description': 'Web utilities with a good smell',
    'long_description': None,
    'author': 'Clément "Doom" Doumergue',
    'author_email': 'clement.doumergue@etna.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
