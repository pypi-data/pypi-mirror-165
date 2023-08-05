# flow-helpers

Handy helpers for ETLs and API interfacing.

## APIs & Transformations
* Bing Webmaster Tools
* Firebase
* Google Analytics (Universal Analytics)
* Google BigQuery
* Google Cloud Storage
* Google Drive
* Google Sheets
* Google SearchAds 360
* Impact
* Journera
* Listen360
* ScrapingHub
* Sharepoint

## Data Transfers
* SFTP
* AWS S3
* MSSQL
* Snowflake

## Other
* Time
* Files

## Handy Notes for working with Poetry & Test PyPI
* create test account on test.pypi.org and get token
* using poetry, run `poetry config repositories.test-pypi https://test.pypi.org/legacy/`
* then add token using `poetry config pypi-token.test-pypi <token>`
* use `poetry version patch` to autoincrement new release
  * can also use `poetry version minor` or `poetry version major` as appropriate
* use `poetry build` to build the dist files
* use `poetry publish --build -r test-pypi` to build dist files and publish to the Test PyPI repo

## Internal Reference for production pypi
* create account on pypi.org, get api token
* using poetry, run `poetry config pypi-token.pypi <token>` to add token
* use `poetry publish --build` to build dist files and publish to actual PyPI repo