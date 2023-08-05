# Fletil
A CLI for the Flet framework.

## Features
- Exposes the standard run options for a Flet app.
- Implements basic "restart" functionality: reloads the targeted source file whenever changes are saved, but makes no attempt to preserve running state.

## Installing
- From PyPI: `$ pip install fletil`. Note this also installs `Flet` if it isn't present.
- From GitLab (NOTE: development is managed by Poetry):
  + git clone https://gitlab.com/skeledrew/fletil.git
  + cd fletil
  + poetry install

## Usage
Help is available via `$ fletil --help`.

## Known Limitations
- The `restart` option currently only works with a single source file. Doing filesystem operations on another source file in the folder being watched (or a subfolder) will likely lead to undefined behavior.

## License
MIT.
