# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sec_client',
 'sec_client.tables',
 'sec_client.tables.query',
 'sec_client.utils']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.40,<2.0.0',
 'fake-useragent>=0.1.11,<0.2.0',
 'sec-edgar-api>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'sec-client',
    'version': '0.0.2a0',
    'description': 'Client for retrieving and storing company data from SEC EDGAR RESTful API',
    'long_description': None,
    'author': '_fiz_',
    'author_email': 'crxz.fiz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
