# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pvoutput', 'pvoutput.asyncio']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'mkdocs-material[docs]>=8.2.9,<9.0.0',
 'mkdocs[docs]>=1.3.0,<2.0.0',
 'mkdocstrings[docs]>=0.18.1,<0.20.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'pvoutput',
    'version': '0.0.10',
    'description': 'Interface to the PVOutput API',
    'long_description': None,
    'author': 'yaleman',
    'author_email': 'james@terminaloutcomes.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
