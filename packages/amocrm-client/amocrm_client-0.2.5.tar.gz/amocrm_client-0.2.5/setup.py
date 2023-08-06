# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amocrm_client',
 'amocrm_client.internal',
 'amocrm_client.internal.amo',
 'amocrm_client.internal.amo.internal',
 'amocrm_client.internal.amo.internal.entities',
 'amocrm_client.internal.entities']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp==3.7.4', 'httpx>=0.21,<0.22']

setup_kwargs = {
    'name': 'amocrm-client',
    'version': '0.2.5',
    'description': '',
    'long_description': 'None',
    'author': 'BB Team',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
