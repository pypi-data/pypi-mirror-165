# Fletil
A CLI for the [Flet](https://flet.dev/) framework.

## Features
- Exposes the standard run options for a Flet app.
- Implements "hot reload": reloads the targeted source file whenever changes are saved, attempting to preserve the running state of controls.
  + State to preserve must be specified by passing a unique ID and list of attribute names as `data` to the controls, eg. `TextField(value="hello world", data={"_cid": "greet_text", "_state_attrs": ["value"]})`.
  + If a Syntax error is detected during a reload, it is aborted.

## Installing
NOTE: this also installs `Flet` if it isn't present.
- From PyPI:
  + `$ pip install fletil`.
- From GitLab (NOTE: development is managed by Poetry):
  + `$ git clone https://gitlab.com/skeledrew/fletil`
  + `$ cd fletil`
  + `$ poetry install`

## Usage
- Ensure script is import-friendly, ie. invoke runner with ([doc](https://docs.python.org/3/library/__main__.html)):
```python
if __name__ == "__main__":
    flet.app(target=main)
```
and not:

``` python
flet.app(target=main)
```
- Further help is available via `$ fletil --help`.

## License
MIT.
