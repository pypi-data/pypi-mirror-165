from typing import TypedDict

from netviewer.ip.link_info_bond import LinkInfoBond
from netviewer.ip.link_info_bridge import LinkInfoBridge
from netviewer.ip.link_info_tunnel import LinkInfoTunnel
from netviewer.ip.link_info_veth import LinkInfoVeth


class LinkInfo(TypedDict):
    kind: str
    info: LinkInfoBond | LinkInfoBridge | LinkInfoTunnel | LinkInfoVeth | None
