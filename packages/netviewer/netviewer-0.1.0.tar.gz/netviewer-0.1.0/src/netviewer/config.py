from contextvars import ContextVar

from typing import Any, TypedDict, cast

import tomli

from netviewer.types import Visibility

VisibilityMapping = {
    "normal": Visibility.NORMAL,
    "hidden": Visibility.HIDDEN,
    "lowlight": Visibility.LOWLIGHT,
    "highlight": Visibility.HIGHLIGHT,
}

ConfigSection = dict[str, Any]


class Configuration(TypedDict):
    theme: ConfigSection
    visibility: ConfigSection
    output: ConfigSection
    verbose: bool
    detail: bool
    state: str
    output_svg: str | None
    output_html: str | None


default_theme: dict[str, str] = {
    "default": "white",
    "error": "red",
    "warning": "yellow",
    "info": "green",
    "key": "blue",
    "value": "white",
}


default_x509_element_visibility: dict[str, str] = {
    ".Header": "normal",
}


_base_configuration: Configuration = {
    "theme": default_theme,
    "visibility": default_x509_element_visibility,
    "output": {"svg": "", "html": "", "options": {"width": "100"}},
    "verbose": False,
    "detail": False,
    "state": "",
    "output_svg": None,
    "output_html": None,
}

_config: ContextVar[Configuration] = ContextVar("config")
config_file = "netviewer.toml"


def config_from_file(filename: str) -> Configuration:
    config_file_config = {}
    try:
        with open(filename, "rb") as fp:
            config_file_config = tomli.load(fp)
    except FileNotFoundError:
        pass

    return cast(Configuration, config_file_config)


value_types = (int, float, str)


class MergeError(Exception):
    ...


def merge(base: ConfigSection, file: ConfigSection) -> ConfigSection:
    if len(file) == 0:
        return base

    result = base.copy()
    for key, value in file.items():
        if key in result:
            if isinstance(result[key], value_types):
                if isinstance(value, value_types):
                    result[key] = value
                else:
                    raise MergeError()
            elif isinstance(result[key], list):
                if isinstance(value, value_types):
                    result[key].append(value)
                elif isinstance(value, list):
                    result[key].extend(value)
                elif isinstance(value, dict):
                    raise MergeError()
            elif isinstance(result[key], dict):
                if isinstance(value, value_types):
                    raise MergeError()
                elif isinstance(value, list):
                    raise MergeError()
                elif isinstance(value, dict):
                    result[key] = merge(result[key], cast(ConfigSection, value))
        else:
            result[key] = value

    return result


def config_load(filename: str = config_file) -> Configuration:
    config: Configuration = _base_configuration.copy()
    _file: Configuration = config_from_file(filename)
    if len(_file) > 0:
        for section in config.keys():
            if section in _file:
                config[section] = merge(config[section], _file[section])  # type: ignore

    config["visibility"] = {
        key: VisibilityMapping[value] for key, value in config["visibility"].items()
    }
    _config.set(config)
    return config


def has_key(key_path: str, config: Configuration):
    section = config
    elems = list(reversed(key_path.split(".")))
    try:
        while elem := elems.pop():
            if not isinstance(section, dict) and len(elems) == 0:
                return False
            if elem not in section:
                return False

            section: Any = section[elem]
    except IndexError:
        return True


def maybe(
    data: dict[str, Any], path: str = "", default: Any | None = None
) -> Any | None:
    elems = list(reversed(path.split(".")))
    try:
        while elem := elems.pop():
            if elem not in data:
                return default
            elif len(elems) == 0:
                return data[elem]
            else:
                data = data[elem]
    except IndexError:
        return None
