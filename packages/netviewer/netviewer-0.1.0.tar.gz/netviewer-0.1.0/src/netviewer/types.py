from enum import Enum, auto
from typing import TypedDict


class Visibility(Enum):
    NORMAL = auto()
    HIDDEN = auto()
    HIGHLIGHT = auto()
    LOWLIGHT = auto()


class Error(TypedDict):
    module: str
    text: str


class Warning(TypedDict):
    module: str
    text: str
