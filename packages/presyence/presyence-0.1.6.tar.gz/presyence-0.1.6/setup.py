# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['presyence',
 'presyence.reporter',
 'presyence.reporter.www',
 'presyence.reporter.www.assets',
 'presyence.testrunner']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.80.0,<0.81.0',
 'pandas>=1.4.3,<2.0.0',
 'typer>=0.6.1,<0.7.0',
 'uvicorn>=0.18.3,<0.19.0']

entry_points = \
{'console_scripts': ['presyence = presyence.main:app']}

setup_kwargs = {
    'name': 'presyence',
    'version': '0.1.6',
    'description': '',
    'long_description': None,
    'author': 'Rémi Connesson',
    'author_email': 'remiconnesson@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
