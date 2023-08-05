# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alto_exp_bot']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.1,<5.0',
 'Pyrebase4>=4.5.0,<5.0.0',
 'azure-cosmos>=4.3.0,<5.0.0',
 'azure-iot-hub>=2.6.0,<3.0.0',
 'azure-servicebus>=7.8.0,<8.0.0',
 'boto3>=1.24.60,<2.0.0',
 'chart-studio>=1.1.0,<2.0.0',
 'djangorestframework>=3.13.1,<4.0.0',
 'line_notify>=0.1.4,<0.2.0',
 'opencv-python>=4.6.0,<5.0.0',
 'pandas>=1.4.3,<2.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'plotly>=5.10.0,<6.0.0',
 'psycopg2-binary>=2.9.3,<3.0.0',
 'vincenty>=0.1.4,<0.2.0']

setup_kwargs = {
    'name': 'alto-exp-bot',
    'version': '0.1.0',
    'description': 'Alto experience package LINE bot',
    'long_description': None,
    'author': 'Mixchanawee',
    'author_email': 'chanawee.janyakhantikul@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
