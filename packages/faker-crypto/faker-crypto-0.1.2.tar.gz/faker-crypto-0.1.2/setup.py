# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['faker_crypto']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=14.2.0,<15.0.0']

setup_kwargs = {
    'name': 'faker-crypto',
    'version': '0.1.2',
    'description': 'faker_crypto is a Faker provider for crytoaddreses.',
    'long_description': "# faker_crypto\n\n__Version:__ 0.1.2\n\nfaker_crypto is a Faker provider for crytoaddreses.\n\nFollowing crypto addresses are supported:\n\n- Bitcoin\n- Litecoin\n- Ethereum\n\n## Installation\n\nInstall with pip:\n\n```bash\npip install faker-cypto\n```\n\n## Usage\n\nAdd `CryptoAddress` provider to Faker instance:\n\n```python\nfrom faker import Faker\nfrom faker_crypto import CryptoAddress\n\nfake = Faker()\nfake.add_provider(CryptoAddress)\n\nfake.bitcoin_address()\n# '13XTsE8TKEHW5zAmCWmBvNk5KvEcEjVQu'\nfake.litecoin_address()\n# 'LM3HgLcPemiBb5MJ3vqRRPrPqBdtf7pL'\nfake.ethereum_address()\n# '0x7ea8abae70ce7e9ce09155ee9169d5f18fc96b'\n```\n\n\n## Testing\n\nRun unit tests with code coverage with:\n\n```\npytest --cov -v \n```\n",
    'author': 'Karambir Singh Nain',
    'author_email': 'me@karambir.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
