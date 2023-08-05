"""Hot reload and restart functionality."""


import atexit
from functools import partial
from importlib import util
from pathlib import Path

import flet
from loguru import logger
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


class Handler(PatternMatchingEventHandler):
    """Filesystem events handler."""

    def __init__(self, module, target_name):
        self._module = module
        self._target_name = target_name
        self._page = None
        super().__init__(patterns=["*.py"], ignore_directories=True)
        return

    def on_any_event(self, event):
        """Perform a `restart` if the event is relevant."""
        if event.event_type in [
                "created",
                "modified",
                "deleted",
        ]:
            logger.info(f"{event.event_type.title()}: {event.src_path}")
            module_name = self._module.__name__
            # TODO: construct the module name from the file path and base name
            # TODO: reload ALL modules at the path!
            spec = util.spec_from_file_location(
                module_name, event.src_path)
            module = util.module_from_spec(spec)
            spec.loader.exec_module(module)
            target = getattr(module, self._target_name)
            assert callable(target), f'"{self._target_name}" is not a function'
            page = self._page
            page.controls.clear()
            page.update()
            target(page)
            page.update()
        return

    def set_page(self, page: flet.Page):
        """Save the default page.

        This method is called by a decorator which wraps the target
        function.
        """
        if not self._page:
            self._page = page
        return


def cleanup(observer):
    """Gracefully terminate the watcher upon exit."""
    logger.info("Terminating watcher...")
    observer.stop()
    observer.join()
    return


def get_page(handler, target):
    """Collect the original page with which the app's target is called."""

    def _get(page):
        handler.set_page(page)
        return target(page)
    return _get


def watch_and_restart(module, target_name):
    """Create a watcher for the project."""
    handler = Handler(module, target_name)
    observer = Observer()
    path = Path(module.__file__).parent
    observer.schedule(handler, str(path), recursive=True)
    atexit.register(cleanup, observer)
    observer.start()
    logger.info(f"Watching for changes in {path}")
    return partial(get_page, handler)
