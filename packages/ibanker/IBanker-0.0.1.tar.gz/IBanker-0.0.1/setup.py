# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ibanker',
 'ibanker.sec_client',
 'ibanker.tables',
 'ibanker.tables.query',
 'ibanker.utils',
 'ibanker.utils.sec_client_utils',
 'ibanker.utils.valtools_utils',
 'ibanker.valtools',
 'ibanker.valtools.forecasttools',
 'ibanker.valtools.histtools',
 'ibanker.valtools.ratiotools',
 'ibanker.valtools.risktools',
 'ibanker.valtools.visualtools']

package_data = \
{'': ['*'], 'ibanker.tables': ['data/*']}

install_requires = \
['SQLAlchemy>=1.4.40,<2.0.0',
 'cytools>=0.4.1,<0.5.0',
 'fake-useragent>=0.1.11,<0.2.0',
 'numpy>=1.23.2,<2.0.0',
 'pandas-datareader>=0.10.0,<0.11.0',
 'pandas>=1.4.3,<2.0.0',
 'sec-edgar-api>=1.0.0,<2.0.0',
 'tinydb>=4.7.0,<5.0.0',
 'yfinance>=0.1.74,<0.2.0']

setup_kwargs = {
    'name': 'ibanker',
    'version': '0.0.1',
    'description': 'IBanker is a package intended for building typical financial models used in investment banking i.e DCFs, LBOs, etc.',
    'long_description': '# IBanker\n IBanker is a package intended for building typical financial models used in investment banking i.e DCFs, LBOs, etc.\n',
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
