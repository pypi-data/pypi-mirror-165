from typing import TypedDict

from netviewer.model import MAC
from netviewer.model.link_info import LinkInfo


class Link(TypedDict):
    index: int
    name: str
    link_index: int | None
    flags: list[str]
    mtu: int
    qdisc: str
    master: str | None
    state: str
    link_mode: str | None
    group: str
    link_type: str
    address: MAC
    broadcast: MAC
    link_netnsid: int

    # link_info
    link_info_type: str
    link_info: LinkInfo | None
