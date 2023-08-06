# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['onx', 'onx.server', 'onx.tui', 'server', 'tui']

package_data = \
{'': ['*']}

modules = \
['run']
install_requires = \
['aiohttp[speedups]==3.8.1',
 'cachetools==5.2.0',
 'click==8.1.3',
 'pydantic==1.9.2',
 'pyfiglet==0.8.post1',
 'schema==0.7.5',
 'single-source==0.3.0',
 'textual==0.1.18']

entry_points = \
{'console_scripts': ['onx = run:main']}

setup_kwargs = {
    'name': 'onx',
    'version': '0.2.0',
    'description': 'Noughts & Crosses (Tic Tac Toe) terminal based, client-server online game with your partner through websockets.',
    'long_description': '# Noughts & Crosses (Tic Tac Toe)\n\n[![RunTests](https://github.com/vyalovvldmr/onx/actions/workflows/run_tests.yml/badge.svg)](https://github.com/vyalovvldmr/onx/actions/workflows/run_tests.yml)\n\nNoughts & Crosses (Tic Tac Toe) terminal based, client-server online game with your partner through websockets.\n\n## Requires\n\nPython 3.10\n\n## Install\n\n```\n$ pip install onx\n```\n\nor\n\n```\n$ poetry shell\n$ poetry add onx\n```\n\n## Play Game\n\nFor running your game board just type in a terminal:\n\n```\n$ onx\n```\n\nYou will see a game board in a waiting for your partner state.\n\nThen ask your partner to run the same cli command with **exactly** the same cli options.\nYou will be matched to your partner by cli options (size and winning sequence length) on a server side.\n\nIf you are running a game with a public server than I\'ll suggest you to make a shorter delay between running your game board and your partners board. Just for reducing the probability to be matched with somebody else.\n\n\n![TUI screenshot 1](https://github.com/vyalovvldmr/onx/blob/master/static/screen1.png?raw=true)\n\nThere are command line options for changing game board settings.\n`-g` or `--grid-size` changes grid size.\n`-w` or `--wining-length` changes winning sequence length.\n`-h` or `--help` prints help.\n\n```\n$ onx -g14 -w3\n```\n\n![TUI screenshot 1](https://github.com/vyalovvldmr/onx/blob/master/static/screen2.png?raw=true)\n\n## Run Server and Client Locally\n\nSet up env variables.\n\n```\n$ export LOCALHOST="0.0.0.0"\n$ export PORT=8888\n```\n\nRun server.\n\n```\n$ onx -d\n```\n\nRun client.\n\n```\n$ onx\n```\n\n## Run Tests\n\n```\n$ git clone git@github.com:vyalow/onx.git\n$ cd onx\n$ poetry shell\n$ poetry install --no-root\n$ pytest --cov\n```\n\n## Known Limitations\n\n- **onx** is currently based on [textual](https://github.com/Textualize/textual) TUI framework which is awesome\n  but is at an extremely early development stage. As a result you may be faced with some rendering problem like [711](https://github.com/Textualize/textual/issues/711), [710](https://github.com/Textualize/textual/issues/710).\n  I\'ll suggest you to run a game board in a fullscreen mode for now.\n- Public server is currently running on a free Heroku app. It means that a good enough SLA is not expected.\n',
    'author': 'Vladimir Vyalov',
    'author_email': 'vyalov.v@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vyalovvldmr/onx',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
