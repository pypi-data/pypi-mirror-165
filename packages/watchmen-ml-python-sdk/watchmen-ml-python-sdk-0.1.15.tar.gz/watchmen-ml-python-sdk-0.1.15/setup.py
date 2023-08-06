# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['client',
 'client.achievement',
 'client.ml',
 'client.ml.model',
 'client.ml.pd',
 'client.sdk',
 'client.sdk.watchmen']

package_data = \
{'': ['*']}

install_requires = \
['ipynbname>=2021.3.2,<2022.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'watchmen-ml-python-sdk',
    'version': '0.1.15',
    'description': '',
    'long_description': None,
    'author': 'luke0623',
    'author_email': 'luke0623@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
