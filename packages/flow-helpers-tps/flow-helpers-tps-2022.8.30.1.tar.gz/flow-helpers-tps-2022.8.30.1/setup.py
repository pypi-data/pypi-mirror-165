# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flow_helpers_tps']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy',
 'boto3',
 'botocore',
 'cryptography',
 'facebook-business',
 'flatdict',
 'google',
 'google-api-python-client',
 'httplib2',
 'office365',
 'pandas',
 'pendulum',
 'poetry>=1.1.15,<2.0.0',
 'pysftp',
 'uuid']

setup_kwargs = {
    'name': 'flow-helpers-tps',
    'version': '2022.8.30.1',
    'description': 'Handy helpers for ETL and API interfacing.',
    'long_description': '# flow-helpers\n\nHandy helpers for ETLs and API interfacing.\n\n## APIs & Transformations\n* Bing Webmaster Tools\n* Firebase\n* Google Analytics (Universal Analytics)\n* Google BigQuery\n* Google Cloud Storage\n* Google Drive\n* Google Sheets\n* Google SearchAds 360\n* Impact\n* Journera\n* Listen360\n* ScrapingHub\n* Sharepoint\n\n## Data Transfers\n* SFTP\n* AWS S3\n* MSSQL\n* Snowflake\n\n## Other\n* Time\n* Files\n',
    'author': 'joshliu3',
    'author_email': 'jliu@theparkingspot.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
