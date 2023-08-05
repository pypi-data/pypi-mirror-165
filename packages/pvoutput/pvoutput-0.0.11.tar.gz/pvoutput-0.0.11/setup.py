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
    'version': '0.0.11',
    'description': 'Interface to the PVOutput API',
    'long_description': '# pvoutput\n\nPVOutput.org python API module. Works with the R2 [API version spec here](https://pvoutput.org/help.html#api-spec).\n\nGet your API key from [the account page on PVOutput](https://pvoutput.org/account.jsp)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n# Example usage\n\nHere\'s a quick code example:\n\n```python\n    from pvoutput import PVOutput\n    import json\n    apikey = \'aaaaaabbbbbbccccccddddddeeeeeeffffffgggg\'\n    systemid = 12345\n    pvo = PVOutput(apikey=apikey, systemid=systemid)\n    print(json.dumps(pvo.check_rate_limit(), indent=2))\n```\nWill give you output like this:\n```\n    {\n        "X-Rate-Limit-Remaining": "271",\n        "X-Rate-Limit-Limit": "300",\n        "X-Rate-Limit-Reset": "1570597200"\n    }\n```\n\nThere are more example code snippets in the [examples](examples/) directory.\n\n# Installing\n\n## Prod-ish usage\n\n`python -m pip install pvoutput` to install from pypi\n\n## Dev Install Things\n\n```shell\npython -m venv venv\nsource venv/bin/activate\npython -m pip install --upgrade pip flit\npython -m flit install\n```\n\n# Input validation\n\nThis is handled by the `pvoutput.base.PVOutputBase.validate_data` function.\n\nIt expects the input data and a dict of configuration parameters, which are described in the table below:\n\n| Field name | Required | Valid Types | Description |\n| --- |  --- | --- | --- |\n| `type` | Yes | `Any` | This is a python type object to match against the field type. |\n| `required` | No | `bool` | This defines if the field is required. |\n| `description` | No | `Any` | This is currently unused, but typically holds the description from the PVOutput API Docs |\n| `donation_required` | No | `bool` | If set to true, and the user\'s not donated, it\'ll throw a `DonationRequired` exception if the user tries to use functionality that requires them to have donated. It\'s a whole thing. |\n| `maxlen` | No | `int` | Maximum length of the field. ie. `if len(field) > maxlen: raise ValueError` |\n| `maxval` | No | `int` | Maximum value of the field. |\n| `minval` | No | `int` | Minimum value of the field. |\n| `additional_validators` | No | `List[function]` | A list of functions to run against the field, which should throw exceptions if something\'s wrong. |\n\nAn example configuration\n\n```\n"date_val": {\n    "required": True,\n    "description": "Date",\n    "type": date,\n    "donation_required": False,\n    "additional_validators" : [\n        validate_delete_status_date\n    ]\n}\n```\n\n# Contributing / Testing\n\n`pylint`, `black` and `mypy` should all pass before submitting a PR.\n\n# License\n\nMIT License (see `LICENSE`), don\'t use this for anything you care about - I don\'t provide a warranty at all, and it\'ll likely steal your socks and underfeed your dog.\n\n# Changelog\n\n* 0.0.1 Initial version\n* 0.0.2 2019-10-12 Fixed some bugs\n* 0.0.3 2019-10-13 Added PVOutput.getstatus() which returns the current status as a dict\n* 0.0.4 2019-11-05 Code cleanup using sonarqube, added an error check for registernotification\n* 0.0.5 Asyncio things\n* 0.0.6 I broke the build when uploading to pypi, fixed in 0.0.7.\n* 0.0.7 2021-12-27 [#117](https://github.com/yaleman/pvoutput/issues/117) fix for getstatus issues\n* 0.0.8 2022-01-02 @cheops did great work cleaning up a lot of my mess, and testing is much better.\n* 0.0.10 2022-08-27 Added explicit timeouts to HTTP connections in the synchronous client.\n* 0.0.11 2022-08-27 Added explicit timeouts to HTTP connections in the aiohttp client.',
    'author': 'James Hodgkinson',
    'author_email': 'james@terminaloutcomes.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://yaleman.github.io/pvoutput/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
