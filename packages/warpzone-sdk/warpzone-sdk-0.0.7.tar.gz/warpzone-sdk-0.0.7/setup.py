# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['warpzone', 'warpzone.servicebus', 'warpzone.tablestorage']

package_data = \
{'': ['*']}

install_requires = \
['azure-data-tables>=12.4.0,<13.0.0',
 'azure-servicebus>=7.8.0,<8.0.0',
 'pandas>=1.4.3,<2.0.0',
 'pyarrow>=9.0.0,<10.0.0']

setup_kwargs = {
    'name': 'warpzone-sdk',
    'version': '0.0.7',
    'description': 'The main objective of this package is to centralize logic used to interact with Azure Functions, Azure Service Bus and Azure Table Storage',
    'long_description': 'None',
    'author': 'Anders Launer Baek-Petersen',
    'author_email': 'alp@energinet.dk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
