# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['valtools',
 'valtools.forecasttools',
 'valtools.histtools',
 'valtools.risktools',
 'valtools.utils']

package_data = \
{'': ['*']}

install_requires = \
['cytoolz>=0.12.0,<0.13.0',
 'numpy>=1.23.2,<2.0.0',
 'pandas-datareader>=0.10.0,<0.11.0',
 'pandas>=1.4.3,<2.0.0',
 'yfinance>=0.1.74,<0.2.0']

setup_kwargs = {
    'name': 'valtools',
    'version': '0.0.1',
    'description': 'Various tools to help in valuation and fundamental analysis',
    'long_description': '',
    'author': '_fiz_',
    'author_email': 'crxz.fiz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
