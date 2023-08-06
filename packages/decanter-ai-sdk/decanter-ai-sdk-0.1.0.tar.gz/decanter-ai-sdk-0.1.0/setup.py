# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['decanter_ai_sdk', 'decanter_ai_sdk.enums', 'decanter_ai_sdk.web_api']

package_data = \
{'': ['*'], 'decanter_ai_sdk.web_api': ['data/*']}

install_requires = \
['black>=22.6.0,<23.0.0',
 'pandas>=1.4.3,<2.0.0',
 'poethepoet>=0.16.0,<0.17.0',
 'pydantic>=1.9.2,<2.0.0',
 'pytest>=7.1.2,<8.0.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'decanter-ai-sdk',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'senchao',
    'author_email': 'senchao@mobagel.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
