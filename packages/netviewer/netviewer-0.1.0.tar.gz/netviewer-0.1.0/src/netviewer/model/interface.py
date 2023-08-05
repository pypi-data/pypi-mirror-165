from typing import TypedDict

from netviewer.model import MAC, inet
from netviewer.model.link_info import LinkInfo


class Interface(TypedDict):
    index: int
    name: str
    flags: list[str]
    mtu: int
    metric: int
    qdisc: str
    state: str
    group: str
    qlen: int | None
    link_type: str
    info: list[inet.INetInfo]
    address: MAC
    broadcast: MAC
    master: str | None

    # detail information
    dynamic: bool
    promiscuity: int
    min_mtu: int
    max_mtu: int
    num_tx_queues: int
    num_rx_queues: int
    gso_max_size: int
    gso_max_segs: int
    parentbus: str | None
    parentdev: str | None
    inet6_addr_gen_mode: str | None

    # link_info
    link_info_type: str
    link_info: LinkInfo | None
