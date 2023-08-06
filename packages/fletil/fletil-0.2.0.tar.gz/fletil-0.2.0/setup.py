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
    'version': '0.2.0',
    'description': 'A CLI for the Flet framework.',
    'long_description': '# Fletil\nA CLI for the [Flet](https://flet.dev/) framework.\n\n## Features\n- Exposes the standard run options for a Flet app.\n- Implements "hot reload": reloads the targeted source file whenever changes are saved, attempting to preserve the running state of controls.\n  + State to preserve must be specified by passing a unique ID and list of attribute names as `data` to the controls, eg. `TextField(value="hello world", data={"_cid": "greet_text", "_state_attrs": ["value"]})`.\n  + If a Syntax error is detected during a reload, it is aborted.\n\n## Installing\nNOTE: this also installs `Flet` if it isn\'t present.\n- From PyPI:\n  + `$ pip install fletil`.\n- From GitLab (NOTE: development is managed by Poetry):\n  + `$ git clone https://gitlab.com/skeledrew/fletil`\n  + `$ cd fletil`\n  + `$ poetry install`\n\n## Usage\n- Ensure script is import-friendly, ie. invoke runner with ([doc](https://docs.python.org/3/library/__main__.html)):\n```python\nif __name__ == "__main__":\n    flet.app(target=main)\n```\nand not:\n\n``` python\nflet.app(target=main)\n```\n- Further help is available via `$ fletil --help`.\n\n## License\nMIT.\n',
    'author': 'Andrew Phillips',
    'author_email': 'skeledrew@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/skeledrew/fletil',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
