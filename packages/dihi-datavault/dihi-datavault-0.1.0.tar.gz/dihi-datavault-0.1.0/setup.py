# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dihi_datavault']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'colorama>=0.4.5,<0.5.0',
 'cryptography>=37.0.4,<38.0.0']

entry_points = \
{'console_scripts': ['datavault = dihi_datavault.cli:main']}

setup_kwargs = {
    'name': 'dihi-datavault',
    'version': '0.1.0',
    'description': 'Store and encrypt sensitive data in your git repo',
    'long_description': '# Data Vault 🔒\n\n[![PyPI version](https://badge.fury.io/py/dihi-datavault.svg)](https://badge.fury.io/py/dihi-datavault)\n[![Test](https://github.com/dihi/datavault/actions/workflows/test.yml/badge.svg)](https://github.com/dihi/datavault/actions/workflows/test.yml)\n\nStore and encrypt sensitive data in your git repo.\n\n## Installation\n\nPick your poison:\n\n - `pip install dihi-datavault` then `datavault`\n - `poetry add dihi-datavault` then `poetry run datavault`\n - `pipx install dihi-datavault` then `pipx run datavault`\n\n## Usage\n\nFirst, create a new vault.\n\n```bash\ndatavault new path/to/vault\n```\n\nThis command will...\n\n  - Provide you with a secret to use when encrypting your files\n  - Create a folder at `path/to/vault` where you place files you wish to be encrypted\n  - Create a `path/to/vault/.encrypted` directory to store the encrypted files along with a manifest which tracks the state of files in the vault\n  - Create a `path/to/vault/.gitignore` file which will ignore the unencrypted files\n\nYou\'re now free to add files to your new vault and encrypt them:\n\n```bash\necho "apple" > path/to/vault/apple.txt\necho "banana" > path/to/vault/banana.txt\ndatavault inspect\ndatavault encrypt\n```\n\nYou can also clear out the contents of the vault as needed...\n\n```bash\ndatavault clear-decrypted\ndatavault clear-encrypted\n```\n\nNow lets say you\'ve just pulled the repo and have none of the original files...\n\n```bash\ndatavault decrypt\n```\n\n## Development\n\nUseful commands:\n\n - `poetry run pytest` to run the tests\n - `poetry publish -r testpypi` and `poetry publish -r testpypi` to test the deployment\n - `poetry version X.Y.Z` to bump the version, then `git tag vX.Y.Z` and `git push --tags`\n - `poetry publish` to release\n',
    'author': 'Faraz Yashar',
    'author_email': 'fny@duke.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dihi/datavault',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2',
}


setup(**setup_kwargs)
