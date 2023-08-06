# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['file_storehouse',
 'file_storehouse.engine',
 'file_storehouse.file_manager',
 'file_storehouse.key_mapping',
 'file_storehouse.transformation']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.24.36,<2.0.0']

setup_kwargs = {
    'name': 'file-storehouse',
    'version': '0.5.0',
    'description': 'Manage files in bulk quantity using a friendly dict-like interface',
    'long_description': "# File-Storehouse\n\n[![Test and build](https://github.com/fschuch/file_storehouse/actions/workflows/ci.yml/badge.svg)](https://github.com/fschuch/file_storehouse/actions/workflows/ci.yml)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![python](https://img.shields.io/badge/Python-3.8%2B-brightgreen)\n[![PyPI Version](https://img.shields.io/pypi/v/file_storehouse.svg)](https://pypi.org/project/file_storehouse/)\n\n## Main Features\n\nFile-Storehouse is a lightweight Python package that aims to facilitate the management of files in bulk quantity.\n\nThere are four key points that are combined to achieving such a goal:\n\n* Mapping Interface - The file managers are leveraged by the Mapping and MutableMapping interfaces, which means that everything can be done using a friendly dict-like interface. For instance:\n\n  ```python\n  # Store data to a file:\n  file_manager[id] = file_content\n  # Retrine data from a file\n  file_content = file_manager[id]\n  # Delete a file\n  del file_manager[id]\n  # Loop through all files\n  for id, content in file_manager.items():\n      pass\n  # and many more...\n  ```\n\n* Engine - Choose the engine (or back-end) your file managers are connected to:\n\n  * S3 buckets, powered by [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html);\n  * Local filesystem and more are planned.\n\n* Key Mapping - Customize a two-way key mapping between the dict-like keys and the files' location at the engines according to the business rules of your application.\n\n* Transformations - Configure a chained operation to convert the files back and forward between your Python code and the storage. The supported operations are:\n\n  * Encode/decode bytes and strings;\n  * Dump/load Json files;\n  * Compress/decompress tarballs and more transformations are planned.\n\n## Example\n\nPlease, take a look at the [user story](tests/test_user_story.py) used for testing.\n\n## Copyright and License\n\n© 2022 Felipe N. Schuch. All content is under [MIT License](https://github.com/fschuch/file_storehouse/blob/master/LICENSE).\n",
    'author': 'Felipe N. Schuch',
    'author_email': 'me@fschuch.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fschuch/file_storehouse',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
