# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['blockbax_sdk',
 'blockbax_sdk.client.http',
 'blockbax_sdk.client.http.api',
 'blockbax_sdk.models',
 'blockbax_sdk.util']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'python-dateutil==2.8.2',
 'pytz==2020.1',
 'requests>=2.26.0',
 'types-python-dateutil>=2.8.19,<3.0.0',
 'types-pytz>=2022.1.2,<2023.0.0',
 'types-requests>=2.28.8,<3.0.0',
 'typing-extensions==4.0.0',
 'urllib3>=1.26.6']

entry_points = \
{'console_scripts': ['bx = blockbax_sdk.console:main',
                     'user-agent = blockbax_sdk.console:user_agent']}

setup_kwargs = {
    'name': 'blockbax-sdk',
    'version': '0.0.7',
    'description': 'Blockbax Python SDK',
    'long_description': '# Blockbax Python SDK\n\nFor more information please refer to our [Python SDK documentation](https://blockbax.com/docs/integrations/python-sdk/).\n',
    'author': 'Blockbax',
    'author_email': 'development@blockbax.com',
    'maintainer': 'Blockbax',
    'maintainer_email': 'development@blockbax.com',
    'url': 'https://blockbax.com/docs/integrations/python-sdk/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
