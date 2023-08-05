import textwrap
from typing import Any

import rich.console
import rich.style
import rich.theme

from netviewer.context import _console  # type: ignore
from netviewer.types import Error, Warning
from netviewer.view.theme import INDENT_PER_LEVEL, get_style, indents

MAX_STRIDE = 24


def print(text: str, color: str = "normal", indent: int = 0) -> None:
    c = _console.get()
    c.print(f"{indents[indent]}[{color}]{text}[/]", emoji=False, highlight=False)


def print_info(text: str, indent: int = 0) -> None:
    c = _console.get()
    c.print(f"{indents[indent]}[info]{text}[/]", emoji=False, highlight=False)


def print_key_oneline(
    key: str,
    indent: int = 0,
    key_style: rich.style.Style | None = None,
    c: rich.console.Console | None = None,
) -> None:
    if c is None:
        c = _console.get()
    if key_style is None:
        key_style = get_style("key")
    c.print(f"{indents[indent]}[{key_style}]{key}[/]", emoji=False, highlight=False)


def print_value_oneline(
    value: str,
    indent: int = 0,
    value_style: rich.style.Style | None = None,
    c: rich.console.Console | None = None,
) -> None:
    if c is None:
        c = _console.get()
    if value_style is None:
        value_style = get_style("value")
    c.print(f"{indents[indent]}[{value_style}]{value}[/]", emoji=False, highlight=False)


def print_value_multiline(
    value: str,
    indent: int = 0,
    value_style: rich.style.Style | None = None,
    c: rich.console.Console | None = None,
) -> None:
    if c is None:
        c = _console.get()

    if value_style is None:
        value_style = get_style("value")

    space_left = c.width - indent * INDENT_PER_LEVEL
    if space_left < len(value):
        text = textwrap.fill(
            value,
            width=c.width,
            initial_indent=indents[indent],
            subsequent_indent=indents[indent],
        )
        c.print(f"[{value_style}]{text}[/]", emoji=False, highlight=False)
    else:
        print_value_oneline(f"[{value_style}]{value}[/]", indent=indent)


def print_multivalue_multiline(
    value: list[str],
    indent: int = 0,
    value_style: rich.style.Style | None = None,
    c: rich.console.Console | None = None,
) -> None:
    if c is None:
        c = _console.get()
    for item in value:
        print_value_multiline(item, indent=indent, value_style=value_style, c=c)


def print_key_value_oneline(
    key: str,
    value: Any,
    indent: int = 0,
    key_style: rich.style.Style | None = None,
    value_style: rich.style.Style | None = None,
    c: rich.console.Console | None = None,
) -> None:
    if c is None:
        c = _console.get()
    if key_style is None or value_style is None:
        if key_style is None:
            key_style = get_style("key")
        if value_style is None:
            value_style = get_style("value")

    c.print(
        f"{indents[indent]}[{key_style}]{key}[/] [{value_style}]{value}[/]",
        emoji=False,
        highlight=False,
    )


def print_key_value_multiline(
    key: str,
    value: Any,
    indent: int = 0,
    key_style: rich.style.Style | None = None,
    value_style: rich.style.Style | None = None,
    c: rich.console.Console | None = None,
) -> None:
    if c is None:
        c = _console.get()
    if key_style is None or value_style is None:
        if key_style is None:
            key_style = get_style("key")
        if value_style is None:
            value_style = get_style("value")

    print_key_oneline(key, indent, key_style, c=c)
    print_value_multiline(value, indent + 1, value_style, c=c)


def print_error(
    error: Error,
    filename: str = "",
    indent: int = 0,
    c: rich.console.Console | None = None,
) -> None:
    if c is None:
        c = _console.get()
    if filename:
        c.print(f"{indents[indent]}[error]{filename}[/]", highlight=False)

    text = f"{error['module']}: {error['text']}"
    text = textwrap.fill(
        text,
        width=c.width,
        initial_indent=indents[indent + 1],
        subsequent_indent=indents[indent + 1],
    )
    c.print(f"[error]{text}[/]", highlight=False)


def print_warning(
    warning: Warning,
    filename: str = "",
    indent: int = 0,
    c: rich.console.Console | None = None,
) -> None:
    if c is None:
        c = _console.get()
    if filename:
        c.print(f"{indents[indent]}[warning]{filename}[/]", highlight=False)

    text = f"{warning['module']}: {warning['text']}"
    text = textwrap.fill(
        text,
        width=c.width,
        initial_indent=indents[indent + 1],
        subsequent_indent=indents[indent + 1],
    )
    c.print(f"[warning]{text}[/]", highlight=False)
