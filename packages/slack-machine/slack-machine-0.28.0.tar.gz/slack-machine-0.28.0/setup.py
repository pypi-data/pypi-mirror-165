# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['machine',
 'machine.asyncio',
 'machine.asyncio.clients',
 'machine.asyncio.models',
 'machine.asyncio.plugins',
 'machine.asyncio.plugins.builtin',
 'machine.asyncio.plugins.builtin.fun',
 'machine.asyncio.storage',
 'machine.asyncio.storage.backends',
 'machine.asyncio.utils',
 'machine.bin',
 'machine.clients',
 'machine.clients.singletons',
 'machine.models',
 'machine.plugins',
 'machine.plugins.builtin',
 'machine.plugins.builtin.fun',
 'machine.storage',
 'machine.storage.backends',
 'machine.utils',
 'machine.vendor']

package_data = \
{'': ['*']}

install_requires = \
['APScheduler>=3.9.1,<4.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'blinker-alt>=1.5,<2.0',
 'clint>=0.5.1,<0.6.0',
 'dacite>=1.6.0,<2.0.0',
 'dill>=0.3.5.1,<0.4.0.0',
 'httpx>=0.23.0,<0.24.0',
 'pyee>=9.0.4,<10.0.0',
 'requests>=2.28.1,<3.0.0',
 'slack-sdk>=3.18.1,<4.0.0',
 'tzdata>=2022.2,<2023.0']

extras_require = \
{':python_version < "3.9"': ['backports.zoneinfo>=0.2.1,<0.3.0'],
 'dynamodb': ['aioboto3>=10.0.0,<11.0.0'],
 'redis': ['redis>=4.3.4,<5.0.0', 'hiredis>=2.0.0,<3.0.0']}

entry_points = \
{'console_scripts': ['slack-machine = machine.bin.run:main',
                     'slack-machine-async = machine.bin.run_async:main']}

setup_kwargs = {
    'name': 'slack-machine',
    'version': '0.28.0',
    'description': 'A wonderful, simple, yet powerful and extendable Slack bot framework',
    'long_description': "# Slack Machine\n\n[![Join the chat at https://gitter.im/slack-machine/lobby](https://badges.gitter.im/slack-machine/lobby.svg)](https://gitter.im/slack-machine/lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\n[![image](https://img.shields.io/pypi/v/slack-machine.svg)](https://pypi.python.org/pypi/slack-machine)\n[![image](https://img.shields.io/pypi/l/slack-machine.svg)](https://pypi.python.org/pypi/slack-machine)\n[![image](https://img.shields.io/pypi/pyversions/slack-machine.svg)](https://pypi.python.org/pypi/slack-machine)\n[![CI Status](https://github.com/DonDebonair/slack-machine/actions/workflows/ci.yml/badge.svg)](https://github.com/DonDebonair/slack-machine/actions/workflows/ci.yml)\n[![image](https://codecov.io/gh/DonDebonair/slack-machine/branch/main/graph/badge.svg)](https://codecov.io/gh/DonDebonair/slack-machine)\n\nSlack Machine is a wonderful, simple, yet powerful and extendable Slack bot framework.\nMore than just a bot, Slack Machine is a framework that helps you\ndevelop your Slack team into a ChatOps powerhouse.\n\n![image](extra/logo.png)\n\n## *Note*\n\nAs of v0.26.0 Slack Machine supports AsyncIO using the\n[Slack Events API](https://api.slack.com/apis/connections/events-api) and\n[Socket Mode](https://api.slack.com/apis/connections/socket). This is still experimental and should be thoroughly\ntested. The goal is to eventually stop supporting the old version that uses the Slack RTM API, as the Events API is\nrecommended by Slack for must use cases and asyncio has the potential to be much more performant.\n\nI encourage everyone to start testing the async mode and report any issues in this repository.\n\n## Features\n\n- Get started with mininal configuration\n- Built on top of the [Slack RTM API](https://api.slack.com/rtm) for smooth, real-time\n  interactions (or Slack Events API + Socket Mode for async mode)\n- Support for rich interactions using the [Slack Web API](https://api.slack.com/web)\n- High-level API for maximum convenience when building plugins\n- Low-level API for maximum flexibility\n- **(Experimental) Support for asyncio**\n\n### Plugin API features:\n\n- Listen and respond to any regular expression\n- Capture parts of messages to use as variables in your functions\n- Respond to messages in channels, groups and direct message conversations\n- Respond with reactions\n- Respond in threads\n- Respond with ephemeral messages\n- Send DMs to any user\n- Support for [message attachments](https://api.slack.com/docs/message-attachments)\n- Support for [blocks](https://api.slack.com/reference/block-kit/blocks)\n- Listen and respond to any [Slack event](https://api.slack.com/events) supported by the RTM API (or the Events API\n  with Socket Mode in the case of using async mode)\n- Store and retrieve any kind of data in persistent storage (currently Redis and in-memory storage are supported)\n- Schedule actions and messages (note: currently not supported in async mode)\n- Emit and listen for events\n- Help texts for Plugins\n- Built in web server for webhooks (note: currently not supported in async mode)\n\n### Coming Soon\n\n- Support for Interactive Buttons\n- ... and much more\n\n## Installation\n\nYou can install Slack Machine using pip:\n\n``` bash\n$ pip install slack-machine\n```\n\nIt is **strongly recommended** that you install `slack-machine` inside a\n[virtual environment](https://docs.python.org/3/tutorial/venv.html)!\n\n## Usage\n\n1. Create a directory for your Slack Machine bot:\n   `mkdir my-slack-bot && cd my-slack-bot`\n2. Add a `local_settings.py` file to your bot directory:\n   `touch local_settings.py`\n3. Create a Bot User for your Slack team:\n   https://my.slack.com/services/new/bot (take note of your API\n   token)\n4. Add the Slack API token to your `local_settings.py` like this:\n\n``` python\nSLACK_API_TOKEN = 'xox-my-slack-token'\n```\n\n5. Start the bot with `slack-machine`\n6. ...\n7. Profit!\n\n## Documentation\n\nYou can find the documentation for Slack Machine here: https://dondebonair.github.io/slack-machine/\n\nGo read it to learn how to properly configure Slack Machine, write plugins, and more!\n",
    'author': 'Daan Debie',
    'author_email': 'daan@dv.email',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DandyDev/slack-machine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
