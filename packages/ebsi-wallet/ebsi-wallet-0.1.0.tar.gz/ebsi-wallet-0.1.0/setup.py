# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ebsi_wallet',
 'ebsi_wallet.did_jwt',
 'ebsi_wallet.did_jwt.util',
 'ebsi_wallet.did_jwt.util.json_canonicalize',
 'ebsi_wallet.ebsi_client',
 'ebsi_wallet.ebsi_did',
 'ebsi_wallet.ebsi_did_resolver',
 'ebsi_wallet.ebsi_did_resolver.constants',
 'ebsi_wallet.ebsi_did_resolver.validators',
 'ebsi_wallet.ethereum',
 'ebsi_wallet.siop_auth',
 'ebsi_wallet.util',
 'ebsi_wallet.validators',
 'ebsi_wallet.verifiable_credential',
 'ebsi_wallet.verifiable_credential.validators',
 'ebsi_wallet.verifiable_presentation',
 'ebsi_wallet.verifiable_presentation.v2']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.4.0,<3.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'base58==1.0.3',
 'coincurve>=17.0.0,<18.0.0',
 'eth-keys>=0.4.0,<0.5.0',
 'jsonschema>=4.14.0,<5.0.0',
 'jwcrypto>=1.3.1,<2.0.0',
 'py-multibase>=1.0.3,<2.0.0',
 'pysha3>=1.0.2,<2.0.0',
 'rich>=12.5.1,<13.0.0',
 'sslcrypto>=5.3,<6.0']

setup_kwargs = {
    'name': 'ebsi-wallet',
    'version': '0.1.0',
    'description': 'EBSI Python SDK',
    'long_description': None,
    'author': 'George J Padayatti',
    'author_email': 'george.padayatti@igrant.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
