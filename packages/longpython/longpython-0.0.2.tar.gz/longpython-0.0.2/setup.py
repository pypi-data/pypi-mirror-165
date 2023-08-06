# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['longpython']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['longpython = longpython.main:main']}

setup_kwargs = {
    'name': 'longpython',
    'version': '0.0.2',
    'description': 'CLI tool to print long python',
    'long_description': '# longpython\n\n[![PyPI](https://img.shields.io/pypi/v/longpython?color=blue)](https://pypi.org/project/longpython/)\n\n_looooooooooooooooooooong python!_\n\n## Usage\n\n```shellsession\n$ longpython\n  _\n(" ヽ\n   \\ \\\n   / /\n   \\ \\ _ ,\n    \\___/\n\n$ longpython -h\nusage: longpython [-h] [-l INT]\n\nCLI tool to print long python\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -l INT, --length INT  length of python (default: 1)\n```\n\n## Installation\n\n### Via pipx (recommended)\n\nI recommend using [pipx](https://github.com/pypa/pipx) to install this project.\n\n```sh\npipx install longpython\n```\n\n### Via pip\n\n```sh\npip install longpython\n```\n\n### Download Single File\n\nThe project does not have any dependencies, you can download\n[this file](./longpython/main.py) and use as soon as.\n\n## Derived Projects\n\n- [syumai/longify](https://github.com/syumai/longify): A command to output\n  longified any ascii art\n- [arrow2nd/longdeno](https://github.com/arrow2nd/longdeno):\n  Looooooooooooooooooooooooooooooooooooooooooooooong [Deno](https://deno.land)\n- [ikanago/longferris](https://github.com/ikanago/longferris): Long\n  [Ferris](https://github.com/ciusji/ferris) written in Rust\n- [sheepla/longgopher](https://github.com/sheepla/longgopher): ʕ◉ϖ◉ʔ\n  loooooooooooooooooooooong gopher\n\n## License\n\nMIT\n',
    'author': 'Hibiki(4513ECHO)',
    'author_email': '4513echo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/4513ECHO/longpython',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
