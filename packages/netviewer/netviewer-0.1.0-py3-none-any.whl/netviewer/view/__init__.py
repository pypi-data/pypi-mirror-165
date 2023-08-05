import rich.console
import rich.theme

from netviewer.config import _config  # type: ignore
from netviewer.context import _console, _err_console, _theme  # type: ignore


def rich_init(**kwargs: object):
    theme = None
    config = _config.get()
    if config is not None:
        theme = config.get("theme", None)

    console_args = kwargs.copy()
    if theme is not None:
        _theme.set(rich.theme.Theme(theme))
        console_args["theme"] = _theme.get()

    console = rich.console.Console(**console_args)
    _console.set(console)

    err_console_args = kwargs.copy()
    err_console_args["stderr"] = True
    err_console = rich.console.Console(**err_console_args)
    _err_console.set(err_console)
