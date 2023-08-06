# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tiny_blocks',
 'tiny_blocks.extract',
 'tiny_blocks.load',
 'tiny_blocks.transform']

package_data = \
{'': ['*']}

install_requires = \
['PyMySQL>=1.0.2,<2.0.0',
 'SQLAlchemy>=1.4.39,<2.0.0',
 'boto3>=1.24.43,<2.0.0',
 'cryptography>=37.0.4,<38.0.0',
 'cx-Oracle>=8.3.0,<9.0.0',
 'kafka-python>=2.0.2,<3.0.0',
 'minio>=7.1.11,<8.0.0',
 'pandas>=1.4.3,<2.0.0',
 'psycopg2>=2.9.3,<3.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'types-requests>=2.28.9,<3.0.0']

setup_kwargs = {
    'name': 'tiny-blocks',
    'version': '0.1.14',
    'description': 'Tiny Block Operations for Data Pipelines',
    'long_description': ' tiny-blocks\n=============\n\n[![Documentation Status](https://readthedocs.org/projects/tiny-blocks/badge/?version=latest)](https://tiny-blocks.readthedocs.io/en/latest/?badge=latest)\n[![License-MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/pyprogrammerblog/tiny-blocks/blob/master/LICENSE)\n[![GitHub Actions](https://github.com/pyprogrammerblog/tiny-blocks/workflows/CI/badge.svg/)](https://github.com/pyprogrammerblog/tiny-blocks/workflows/CI/badge.svg/)\n[![PyPI version](https://badge.fury.io/py/tiny-blocks.svg)](https://badge.fury.io/py/tiny-blocks)\n\nTiny Blocks to build large and complex ETL data pipelines!\n\nTiny-Blocks is a library for **data engineering** operations. \nEach **pipeline** is made out of **tiny-blocks** glued with the `>>` operator.\nThis library relies on a fundamental streaming abstraction consisting of three\nparts: **extract**, **transform**, and **load**. You can view a pipeline \nas an extraction, followed by zero or more transformations, followed by a sink. \nVisually, this looks like:\n\n```\nextract -> transform1 -> transform2 -> ... -> transformN -> load\n```\n\nYou can also `fan-in`, `fan-out` for more complex operations.\n\n```\nextract1 -> transform1 -> |-> transform2 -> ... -> | -> transformN -> load1\nextract2 ---------------> |                        | -> load2\n```\n\nTiny-Blocks use **generators** to stream data. Each **chunk** is a **Pandas DataFrame**. \nThe `chunksize` or buffer size is adjustable per pipeline.\n\nInstallation\n-------------\n\nInstall it using ``pip``\n\n```shell\npip install tiny-blocks\n```\n\nBasic usage\n---------------\n\n```python\nfrom tiny_blocks.extract import FromCSV\nfrom tiny_blocks.transform import Fillna\nfrom tiny_blocks.load import ToSQL\n\n# ETL Blocks\nfrom_csv = FromCSV(path=\'/path/to/source.csv\')\nfill_na = Fillna(value="Hola Mundo")\nto_sql = ToSQL(dsn_conn=\'psycopg2+postgres://...\', table_name="sink")\n\n# Pipeline\nfrom_csv >> fill_na >> to_sql\n```\n\nExamples\n----------------------\n\nFor more complex examples please visit \nthe [notebooks\' folder](https://github.com/pyprogrammerblog/tiny-blocks/blob/master/notebooks/Examples.ipynb).\n\n\nDocumentation\n--------------\n\nPlease visit this [link](https://tiny-blocks.readthedocs.io/en/latest/) for documentation.\n',
    'author': 'Jose Vazquez',
    'author_email': 'josevazjim88@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyprogrammerblog/tiny-blocks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
