# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['onx']

package_data = \
{'': ['*']}

modules = \
['run']
install_requires = \
['aiohttp[speedups]==3.8.1',
 'click==8.1.3',
 'pydantic==1.9.2',
 'pyfiglet==0.8.post1',
 'schema==0.7.5',
 'textual==0.1.18']

entry_points = \
{'console_scripts': ['onx = run:main']}

setup_kwargs = {
    'name': 'onx',
    'version': '0.1.1',
    'description': 'Client-server Tic Tac Toe (Noughts & Crosses) terminal based, online game through websockets.',
    'long_description': '# Tic Tac Toe (Noughts & Crosses)\n\n[![RunTests](https://github.com/vyalovvldmr/onx/actions/workflows/run_tests.yml/badge.svg)](https://github.com/vyalovvldmr/onx/actions/workflows/run_tests.yml)\n\nClient-server Tic Tac Toe (Noughts & Crosses) terminal based, online game through websockets.\n\n## Requires\n\nPython 3.10\n\n## Install\n\n```\n$ pip install onx\n```\n\n## Play Game\n\n```\n$ onx\n```\n\n![TUI screenshot 1](https://github.com/vyalovvldmr/onx/blob/master/static/screen1.png?raw=true)\n\nCommand line option `-g` or `--grid-size` changes grid size.\nOption `-w` or `--wining-length` changes winning sequence length.\nOption `-h` or `--help` prints help.\n\n```\n$ onx -g14 -w3\n```\n\n![TUI screenshot 1](https://github.com/vyalovvldmr/onx/blob/master/static/screen2.png?raw=true)\n\n## Run Server and Client Locally\n\nSet up env variables.\n\n```\n$ export LOCALHOST="0.0.0.0"\n$ export PORT=8888\n```\n\nRun server.\n\n```\n$ onx -d\n```\n\nRun client.\n\n```\n$ onx\n```\n\n## Run Tests\n\n```\n$ git clone git@github.com:vyalow/onx.git\n$ cd onx\n$ pip install -r requirements.txt -r requirements-dev.txt\n$ pytest --cov\n```\n\n## TODO\n\n- [x] Bump up Python version from 3.5 to 3.10\n- [x] Fix tests stability after bumping aiohttp from 1.3 to 3.8\n- [x] Set up code linting\n- [x] Set up mypy\n- [ ] Fix aiohttp deprecations\n- [x] Better client\n- [x] Add to PyPI\n- [x] Heroku deployment\n- [ ] Migrate from aiohttp to starlette or migrate from websockets to gRPC\n- [x] Expand play board\n- [ ] Add gameplay with a computer\n',
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
