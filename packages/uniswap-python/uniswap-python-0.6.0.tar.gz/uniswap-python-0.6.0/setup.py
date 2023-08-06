# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uniswap']

package_data = \
{'': ['*'],
 'uniswap': ['assets/*',
             'assets/uniswap-v1/*',
             'assets/uniswap-v2/*',
             'assets/uniswap-v3/*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'python-dotenv',
 'typing-extensions',
 'web3>=5.23.0,<6.0.0']

entry_points = \
{'console_scripts': ['unipy = uniswap:main']}

setup_kwargs = {
    'name': 'uniswap-python',
    'version': '0.6.0',
    'description': 'An unofficial Python wrapper for the decentralized exchange Uniswap',
    'long_description': '<p align="center">\n  <img width="350" height="350" src="https://user-images.githubusercontent.com/9441295/107376524-d96b5880-6a9e-11eb-9eba-094c439cfb07.png">\n</p>\n\n# uniswap-python\n\n[![GitHub Actions](https://github.com/shanefontaine/uniswap-python/workflows/Test/badge.svg)](https://github.com/shanefontaine/uniswap-python/actions)\n[![codecov](https://codecov.io/gh/uniswap-python/uniswap-python/branch/master/graph/badge.svg?token=VHAZHHLFX8)](https://codecov.io/gh/uniswap-python/uniswap-python)\n[![Downloads](https://pepy.tech/badge/uniswap-python)](https://pepy.tech/project/uniswap-python)\n[![License](http://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/shanefontaine/uniswap-python/master/LICENSE)\n[![PyPI](https://img.shields.io/pypi/v/uniswap-python)](https://pypi.org/project/uniswap-python/)\n[![Typechecking: Mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n[![GitHub Repo stars](https://img.shields.io/github/stars/uniswap-python/uniswap-python?style=social)](https://github.com/uniswap-python/uniswap-python/stargazers)\n[![Twitter Follow](https://img.shields.io/twitter/follow/UniswapPython?label=Follow&style=social)](https://twitter.com/UniswapPython)\n\nThe unofficial Python client for [Uniswap](https://uniswap.io/).\n\nDocumentation is available at https://uniswap-python.com/\n\n## Functionality\n\n*  A simple to use Python wrapper for all available contract functions and variables\n*  A basic CLI to get prices and token metadata\n*  Simple parsing of data returned from the Uniswap contract\n\n### Supports\n\n - Uniswap v3 (as of v0.5.0)\n    - Including beta support for Arbitrum & Optimism deployments (as of v0.5.4)\n - Uniswap v2 (as of v0.4.0)\n - Uniswap v1 (deprecated)\n - Various forks (untested, but should work)\n   - Honeyswap (xDai)\n   - Pancakeswap (BSC)\n   - Sushiswap (mainnet)\n\n## Getting Started\n\nSee our [Getting started guide](https://uniswap-python.com/getting-started.html) in the documentation.\n\n## Testing\n\nUnit tests are under development using the pytest framework. Contributions are welcome!\n\nTest are run on a fork of the main net using ganache-cli. You need to install it with `npm install -g ganache-cli` before running tests.\n\nTo run the full test suite, in the project directory set the `PROVIDER` env variable to a mainnet provider, and run:\n\n```sh\npoetry install\nexport PROVIDER= # URL of provider, e.g. https://mainnet.infura.io/v3/...\nmake test\n# or...\npoetry run pytest --capture=no  # doesn\'t capture output (verbose)\n```\n\n## Support our continued work!\n\nYou can support us on [Gitcoin Grants](https://gitcoin.co/grants/2631/uniswap-python).\n\n## Authors\n\n* [Shane Fontaine](https://twitter.com/shanecoin)\n* [Erik Bjäreholt](https://twitter.com/ErikBjare)\n* [@liquid-8](https://github.com/liquid-8)\n* ...and [others](https://github.com/uniswap-python/uniswap-python/graphs/contributors)\n\n*Want to help out with development? We have funding to those that do! See [#181](https://github.com/uniswap-python/uniswap-python/discussions/181)*\n\n## Changelog\n\n_0.5.4_\n\n* added use of gas estimation instead of a fixed gas limit (to support Arbitrum)\n* added `use_estimate_gas` constructor argument (used in testing)\n* added constants/basic support for Arbitrum, Optimism, Polygon, and Fantom. (untested)\n* incomplete changelog\n\n_0.5.3_\n\n* incomplete changelog\n\n_0.5.2_\n\n* incomplete changelog\n\n_0.5.1_\n\n* Updated dependencies\n* Fixed minor typing issues\n\n_0.5.0_\n\n* Basic support for Uniswap V3\n* Added new methods `get_price_input` and `get_price_output`\n* Made a lot of previously public methods private\n* Added documentation site\n* Removed ENS support (which was probably broken to begin with)\n\n_0.4.6_\n\n* Bug fix: Update bleach package from 3.1.4 to 3.3.0\n\n_0.4.5_\n* Bug fix: Use .eth instead of .ens\n\n_0.4.4_\n\n* General: Add new logo for Uniswap V2\n* Bug fix: Invalid balance check (#25)\n* Bug fix: Fixed error when passing WETH as token\n\n_0.4.3_\n\n* Allow kwargs in `approved` decorator.\n\n_0.4.2_\n\n* Add note about Uniswap V2 support\n\n_0.4.1_\n\n* Update changelog for PyPi and clean up\n\n_0.4.0_\n\n_A huge thank you [Erik Bjäreholt](https://github.com/ErikBjare) for adding Uniswap V2 support, as well as all changes in this version!_\n\n* Added support for Uniswap v2\n* Handle arbitrary tokens (by address) using the factory contract\n* Switched from setup.py to pyproject.toml/poetry\n* Switched from Travis to GitHub Actions\n* For CI to work in your repo, you need to set the secret MAINNET_PROVIDER. I use Infura.\n* Running tests on a local fork of mainnet using ganache-cli (started as a fixture)\n* Fixed tests for make_trade and make_trade_output\n* Added type annotations to the entire codebase and check them with mypy in CI\n* Formatted entire codebase with black\n* Moved stuff around such that the basic import becomes from uniswap import Uniswap (instead of from uniswap.uniswap import UniswapWrapper)\n* Fixed misc bugs\n\n_0.3.3_\n*  Provide token inputs as addresses instead of names\n\n_0.3.2_\n*  Add ability to transfer tokens after a trade\n*  Add tests for this new functionality\n\n_0.3.1_\n*  Add tests for all types of trades\n\n_0.3.0_\n*  Add ability to make all types of trades\n*  Add example to README\n\n_0.2.1_\n*  Add liquidity tests\n\n_0.2.0_\n*  Add liquidity and ERC20 pool methods\n\n_0.1.1_\n*  Major README update\n\n_0.1.0_\n*  Add market endpoints\n*  Add tests for market endpoints\n',
    'author': 'Shane Fontaine',
    'author_email': 'shane6fontaine@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shanefontaine/uniswap-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
