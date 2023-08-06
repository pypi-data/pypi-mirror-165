# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mitzu',
 'mitzu.adapters',
 'mitzu.adapters.sqlalchemy',
 'mitzu.adapters.sqlalchemy.athena',
 'mitzu.adapters.sqlalchemy.athena.sqlalchemy',
 'mitzu.adapters.sqlalchemy.databricks',
 'mitzu.adapters.sqlalchemy.databricks.sqlalchemy',
 'mitzu.notebook',
 'mitzu.webapp',
 'mitzu.webapp.navbar']

package_data = \
{'': ['*']}

install_requires = \
['dash-bootstrap-components>=1.2.0,<2.0.0',
 'dash>=2.5.0,<3.0.0',
 'fastparquet>=0.8.0,<0.9.0',
 'pandas>=1.3.5,<1.4.0',
 'plotly>=5.5.0,<5.6.0',
 'pyarrow>=7.0.0,<7.1.0',
 'retry>=0.9.2,<0.10.0',
 'sqlalchemy>=1.4.31,<1.5.0',
 'sqlparse>=0.4.2,<0.5.0']

extras_require = \
{'athena': ['PyAthena>=2.13.0,<3.0.0'],
 'databricks': ['databricks-sql-connector>=2.0.2,<3.0.0'],
 'mysql': ['mysql-connector-python>=8.0.28,<8.1.0'],
 'postgres': ['psycopg2>=2.9.3,<2.10.0'],
 'trinodwh': ['trino[sqlalchemy]>=0.313.0,<0.314.0'],
 'webapp': ['serverless-wsgi>=3.0.1,<4.0.0',
            'orjson>=3.7.11,<4.0.0',
            's3fs>=2022.7.1,<2023.0.0',
            'PyJWT[crypto]>=2.4.0,<3.0.0']}

setup_kwargs = {
    'name': 'mitzu',
    'version': '0.2.24',
    'description': 'Product analytics over your data warehouse',
    'long_description': None,
    'author': 'Istvan Meszaros',
    'author_email': 'istvan.meszaros.88@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
