# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['vaping', 'vaping.config', 'vaping.plugins']

package_data = \
{'': ['*']}

install_requires = \
['confu>=1.7.1,<2.0.0',
 'munge[yaml,tomlkit]>=1.2.0,<2.0.0',
 'pid>=3,<4',
 'pluginmgr>=1,<2',
 'python-daemon>=2,<3']

extras_require = \
{'all': ['requests>=2.19.1,<3.0.0',
         'graphyte>=1.4,<2.0',
         'rrdtool>=0.1.14,<1',
         'prometheus_client>=0.11.0,<0.12.0',
         'graphsrv>=2,<3',
         'vodka>=3.1,<4.0',
         'whisper>=0.9.15,<2',
         'pyzmq>=15.3.0'],
 'graphite': ['requests>=2.19.1,<3.0.0', 'graphyte>=1.4,<2.0'],
 'prometheus': ['prometheus_client>=0.11.0,<0.12.0'],
 'rrdtool': ['rrdtool>=0.1.14,<1'],
 'standalone': ['graphsrv>=2,<3', 'vodka>=3.1,<4.0'],
 'whisper': ['whisper>=0.9.15,<2'],
 'zeromq': ['pyzmq>=15.3.0']}

entry_points = \
{'console_scripts': ['vaping = vaping.cli:cli']}

setup_kwargs = {
    'name': 'vaping',
    'version': '1.5.3',
    'description': 'vaping is a healthy alternative to smokeping!',
    'long_description': '\n# Vaping\n\n[![PyPI](https://img.shields.io/pypi/v/vaping.svg?maxAge=60)](https://pypi.python.org/pypi/vaping)\n[![PyPI](https://img.shields.io/pypi/pyversions/vaping.svg?maxAge=600)](https://pypi.python.org/pypi/vaping)\n[![Tests](https://github.com/20c/vaping/workflows/tests/badge.svg)](https://github.com/20c/vaping)\n[![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/20c/vaping)](https://lgtm.com/projects/g/20c/vaping/alerts/)\n[![Codecov](https://img.shields.io/codecov/c/github/20c/vaping/master.svg)](https://codecov.io/github/20c/vaping)\n\n\nvaping is a healthy alternative to smokeping!*\n\n* (This statement has not been evaluated by the Food and Drug Administration)\n\n![Vaping](https://raw.githubusercontent.com/20c/vaping/master/docs/img/vaping.png)\n\n## Introduction\n\nVaping provides the following features:\n\n- Real-time latency graphing viewable in the browser\n- Line and smokestack graphs\n- Containerized and easy to setup and configure\n- Support for time-series databases\n- Plugin-based design to allow integration with other services\n- Supports distributed setups through message queue\n\nVaping is a Python daemon which polls for input and sends its output through plugins.\n\nIt has a standalone mode to directly serve realtime graphs in a browser, or can use ZeroMQ to distribute messages.\n\n## Installation\n\n```sh\npip install vaping\n```\n\nYou will need a compiler and Python development libraries for some components, which you can obtain with the `gcc` and `python-devel` packages for your operating system.\n\nAlternatively, you can use the [Docker image](Dockerfile), which includes all requirements.\n\n## Quick Start\n\nTo use Vaping, you need first a configuration file that defines which hosts to target and where to send the output. You can have a look at [the examples in this repository](examples/) and adapt them to your needs.\n\nThen, start the `vaping` program from the command line, specifying the path to the configuration file.\n\nA quick start example is [available here](https://vaping.readthedocs.io/en/stable/quickstart/). It shows you how to ping multiple hosts and display the resulting graphs using a local web server.\n\n## Usage\n\n\nVaping has a command-line interface with the following usage:\n\n```\nUsage: vaping [OPTIONS] COMMAND [ARGS]...\n\n  Vaping\n\nOptions:\n  --version    Show the version and exit.\n  --quiet      no output at all\n  --verbose    enable more verbose output\n  --home TEXT  specify the home directory, by default will check in order:\n               $VAPING_HOME, ./.vaping, ~/.config/vaping\n  --debug      enable extra debug output\n  --help       Show this message and exit.\n\nCommands:\n  start    start a vaping process\n  stop     stop a vaping process\n  restart  restart a vaping process\n```\n\n### start\n\nStarts a vaping process, by default will fork into the background unless\n`--debug` or `--no-fork` is passed.\n\nIt adds options:\n\n```\n  -d, --no-fork  do not fork into background\n```\n\n\n### stop\n\nStops a vaping process identified by `$VAPING_HOME/vaping.pid`\n\n\n## Documentation\n\nDocumentation is created with mkdocs and available here:\n\n**stable**: <http://vaping.readthedocs.io/en/stable/>\n\n**latest**: <http://vaping.readthedocs.io/en/latest/>\n\n\n## Changes\n\nThe current change log is available at <https://github.com/20c/vaping/blob/master/CHANGELOG.md>\n\n\n## License\n\nCopyright 2016-2021 20C, LLC\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this software except in compliance with the License.\nYou may obtain a copy of the License at\n\n   http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n\n',
    'author': '20C',
    'author_email': 'code@20c.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/20c/vaping',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
