from typing import TypedDict

from netviewer.model.interface import Interface


class Bridge(TypedDict):
    name: str
    devices: list[str]
    interface: Interface
