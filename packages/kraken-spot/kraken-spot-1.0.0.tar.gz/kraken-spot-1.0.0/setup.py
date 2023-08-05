# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kraken_spot']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'kraken-spot',
    'version': '1.0.0',
    'description': 'A library for interacting with the Kraken Spot API',
    'long_description': '# Kraken Spot\n\n[![Build Status](https://app.travis-ci.com/kevbradwick/kraken-spot.svg?branch=master)](https://app.travis-ci.com/kevbradwick/kraken-spot)\n\nA Python library for interacting with the [Kraken Spot REST API](https://docs.kraken.com/rest/).\n\n## Quick Start\n\nInstall from source of via `pip`\n\n    pip install kraken-spot\n\n```python\nfrom kraken_spot import DefaultClient\n\nclient = DefaultClient()\nclient.get_account_balance()\n```\n\nThe default client will attempt to configure the client with api keys from environment variables. Both `KRAKEN_API_KEY` and `KRAKEN_PRIVATE_KEY` needs to be set.\n\n## OTP Authentication\n\nIf the API key has 2FA enabled, you will need to provide a one time password with your call.\n\n```python\nclient.set_otp(123456)\nclient.get_account_balance()\n```\n\nThe OTP is reset after each request.\n\n## Features\n\nThe following endpoints are currently supported;\n\n| Endpoint Set | Supported |\n| ------ | ------- |\n| Market Data | ✅ |\n| User Data | ✅ |\n| User Trading | ✅ (except batch orders) |\n| User Funding | ✅ |\n| User staking | ✅ |\n| Websocket Authentication | ✅ |\n',
    'author': 'Kevin Bradwick',
    'author_email': 'kevinbradwick@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kevbradwick/kraken-spot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
