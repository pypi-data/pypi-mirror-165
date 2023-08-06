# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiomcrcon']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aio-mc-rcon',
    'version': '3.2.0',
    'description': 'An async library for utilizing remote console on Minecraft Java Edition servers',
    'long_description': "# Aio-MC-RCON ![Code Quality](https://www.codefactor.io/repository/github/iapetus-11/aio-mc-rcon/badge) ![PYPI Version](https://img.shields.io/pypi/v/aio-mc-rcon.svg) ![PYPI Downloads](https://img.shields.io/pypi/dw/aio-mc-rcon?color=0FAE6E)\nAn asynchronous RCON client/wrapper written in Python for Minecraft Java Edition servers!\n\n## Installation\n```\npip install -U aio-mc-rcon\n```\n\n## Example Usage\n- See the [examples folder](https://github.com/Iapetus-11/aio-mc-rcon/tree/main/examples).\n\n## Documentation\n#### *class* aiomcrcon.**Client**(host: *str*, port: *int*, password: *str*):\n- Arguments:\n  - `host: str` - *The hostname / ip of the server to connect to.*\n  - `port: int` - *The port of the server to connect to.*\n  - `password: str` - *The password to connect, can be found as the value under `rcon.password` in the `server.properties` file.*\n- Methods:\n  - `connect(timeout: int = 2)` - *where `timeout` has a default value of 2 seconds.*\n  - `send_cmd(cmd: str, timeout: int = 2)` - *where `cmd` is the command to be executed on the server and timeout has a default value of 2 seconds.*\n  - `close()` - *closes the connection between the client and server.*\n\n#### *exception* aiomcrcon.**RCONConnectionError**\n- *Raised when the connection to the server fails.*\n\n#### *exception* aiomcrcon.**IncorrectPasswordError**\n- *Raised when the provided password/authentication is invalid.*\n\n#### *exception* aiomcrcon.**ClientNotConnectedError**\n- *Raised when the connect() method hasn't been called yet, and commands cannot be sent.*\n",
    'author': 'Milo Weinberg',
    'author_email': 'iapetus011@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Iapetus-11/aio-mc-rcon',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
