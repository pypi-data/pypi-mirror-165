#!/usr/bin/env python3

"""
CLI for fletil (Flet utility).

Type `fletil --help` for usage.
"""


import sys
from importlib import import_module

import fire
import flet

from fletil.hot_reload_and_restart import watch_and_restart


class Commands:
    """Available commands/groups."""

    def run(
            self,
            app: str,
            host: str = None,
            port: int = 0,
            browser: bool = False,
            assets_dir: str = None,
            web_renderer: flet.WebRenderer = "canvaskit",
            restart: bool = False,
    ):
        """Run the specified app (`module.path:main_func`)."""
        sys.path.append(".")
        module_path, _, target_name = app.rpartition(":")
        module = import_module(module_path)
        target = getattr(module, target_name)
        assert callable(target), f'"{target_name}" is not a function'

        if restart:
            get_page = watch_and_restart(module, target_name)
            target = get_page(target)
        return flet.app(
            host=host,
            port=port,
            target=target,
            view=flet.FLET_APP if not browser else flet.WEB_BROWSER,
            assets_dir=assets_dir,
            web_renderer=web_renderer,
        )


def run():
    """Run the CLI."""
    return fire.Fire(Commands())


if __name__ == "__main__":
    run()
