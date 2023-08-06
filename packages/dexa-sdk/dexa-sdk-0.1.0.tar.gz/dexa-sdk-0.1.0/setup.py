# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dexa_sdk',
 'dexa_sdk.agreements',
 'dexa_sdk.agreements.dda',
 'dexa_sdk.agreements.dda.v1',
 'dexa_sdk.agreements.dda.v1.instances',
 'dexa_sdk.agreements.dda.v1.instances.tests',
 'dexa_sdk.agreements.dda.v1.models',
 'dexa_sdk.agreements.dda.v1.models.fields',
 'dexa_sdk.agreements.dda.v1.models.tests',
 'dexa_sdk.agreements.dda.v1.templates',
 'dexa_sdk.agreements.dda.v1.version_tree',
 'dexa_sdk.agreements.dda.v1.version_tree.tests',
 'dexa_sdk.aries',
 'dexa_sdk.aries.admin',
 'dexa_sdk.aries.admin.aiohttp_apispec',
 'dexa_sdk.aries.commands',
 'dexa_sdk.aries.config',
 'dexa_sdk.aries.core',
 'dexa_sdk.did_mydata',
 'dexa_sdk.jsonld',
 'dexa_sdk.logs',
 'dexa_sdk.proofs',
 'dexa_sdk.signatures',
 'dexa_sdk.storage',
 'dexa_sdk.storage.utils']

package_data = \
{'': ['*'], 'dexa_sdk.aries.admin.aiohttp_apispec': ['static/*']}

install_requires = \
['MarkupSafe==2.0.1',
 'PyLD==2.0.1',
 'aries-cloudagent==0.5.6',
 'asynctest>=0.13.0,<0.14.0',
 'green>=3.4.2,<4.0.0',
 'ipykernel>=6.15.1,<7.0.0',
 'jcs>=0.2.1,<0.3.0',
 'loguru>=0.6.0,<0.7.0',
 'marshmallow==3.5.1',
 'merklelib>=1.0,<2.0',
 'merkletools>=1.0.3,<2.0.0',
 'py-multibase>=1.0.3,<2.0.0',
 'py-multicodec>=0.2.1,<0.3.0',
 'pydantic>=1.9.1,<2.0.0',
 'pytest>=7.1.2,<8.0.0',
 'python3-indy>=1.16.0,<2.0.0',
 'rdflib>=6.2.0,<7.0.0',
 'requests>=2.23.0,<2.24.0',
 'rich>=12.5.1,<13.0.0',
 'semver>=2.13.0,<3.0.0',
 'uvloop>=0.16.0,<0.17.0']

setup_kwargs = {
    'name': 'dexa-sdk',
    'version': '0.1.0',
    'description': 'Store and manage Data Exchange Agreements (DEXA)',
    'long_description': None,
    'author': 'George J Padayatti',
    'author_email': 'george.padayatti@igrant.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
