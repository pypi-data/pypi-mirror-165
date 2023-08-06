# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djib']

package_data = \
{'': ['*']}

install_requires = \
['PyNaCl>=1.5.0,<2.0.0',
 'base58>=2.1.1,<3.0.0',
 'jsonrpcserver>=5.0.8,<6.0.0',
 'python-magic>=0.4.27,<0.5.0',
 'solana>=0.25.1,<0.26.0']

setup_kwargs = {
    'name': 'djib',
    'version': '0.1.2',
    'description': 'Djib Python API',
    'long_description': '<div align="center">\n    <img src="https://4289938616-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F6MrZ6BqPMP2mmJKSKsG8%2Ficon%2F5q4QZZ6hqugOY1FCi0Mw%2Flogo.svg?alt=media&token=114140fd-3e6b-4ba9-8925-07c50a835eb5" width="25%" height="25%">\n</div>\n\n---\n\n# Djib Python SDK\n\nIt\'s the base Python library for interacting with Djib network.\nYou can use it interact\nwith the Djib network. \n\n## Quickstart\n\n### Installation\n\n```sh\npip install djib\n```\n\n### General RPC Usage\n\n```py\nfrom djib.rpc import DjibRpc\n\nWALLET_PRIVATE_KEY = \'<Base58 encoded string>\'\n\ntry:\n    rpc = DjibRpc(WALLET_PRIVATE_KEY, is_devnet=True)\n\n    # status of drive\n    response = rpc.status()\n\n    if response.error:\n        print(f"Error: {response.error[\'message\']}, Code: {response.error[\'code\']}, Data: {response.error[\'data\']}")\n    else:\n        print(response.data)\nexcept Exception as e:\n    print(f"Error: {str(e)}")\n```\n\n### KMS Usage\n\n```py\nfrom djib.rpc import KmsClient\n\nWALLET_PRIVATE_KEY = \'<Base58 encoded string>\'\n\ntry:\n    kms = KmsClient(WALLET_PRIVATE_KEY, is_devnet=True)\n    a = \'Hello, World!\'\n    a_enc = kms.encrypt(a)\n    a_dec = kms.decrypt(a_enc)\n    assert a_dec == a\nexcept Exception as e:\n    print(f"Error: {str(e)}")\n```\n\n\n## Development\n\n### Setup\n\n1. Install [poetry](https://python-poetry.org/docs/#installation)\n2. Install dev dependencies:\n\n```sh\npoetry install\n```\n\n3. Activate the poetry shell.\n\n```sh\npoetry shell\n```\n',
    'author': 'Djib tech team',
    'author_email': 'tech@djib.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://djib.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
