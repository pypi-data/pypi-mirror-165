# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fletil']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.4.0,<0.5.0',
 'flet>=0.1.52,<0.2.0',
 'loguru>=0.6.0,<0.7.0',
 'watchdog>=2.1.9,<3.0.0']

entry_points = \
{'console_scripts': ['fletil = fletil.cli:run']}

setup_kwargs = {
    'name': 'fletil',
    'version': '0.1.0',
    'description': 'A CLI for the Flet framework.',
    'long_description': '# Fletil\nA CLI for the Flet framework.\n\n## Features\n- Exposes the standard run options for a Flet app.\n- Implements basic "restart" functionality: reloads the targeted source file whenever changes are saved, but makes no attempt to preserve running state.\n\n## Installing\n- From PyPI: `$ pip install fletil`. Note this also installs `Flet` if it isn\'t present.\n- From GitLab (NOTE: development is managed by Poetry):\n  + git clone https://gitlab.com/skeledrew/fletil.git\n  + cd fletil\n  + poetry install\n\n## Usage\nHelp is available via `$ fletil --help`.\n\n## Known Limitations\n- The `restart` option currently only works with a single source file. Doing filesystem operations on another source file in the folder being watched (or a subfolder) will likely lead to undefined behavior.\n\n## License\nMIT.\n',
    'author': 'Andrew Phillips',
    'author_email': 'skeledrew@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/skeledrew/fletil',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
