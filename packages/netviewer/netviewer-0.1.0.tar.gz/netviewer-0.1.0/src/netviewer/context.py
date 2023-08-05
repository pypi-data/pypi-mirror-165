from contextvars import ContextVar

import rich.console
import rich.theme

_console: ContextVar[rich.console.Console] = ContextVar("console")
_theme: ContextVar[rich.theme.Theme] = ContextVar("theme")
_err_console: ContextVar[rich.console.Console] = ContextVar("error_console")
