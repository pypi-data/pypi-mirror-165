from typing import TypedDict

from netviewer.model.link_info_bridge_slave import LinkInfoBridgeSlave


class LinkInfoVeth(TypedDict):
    kind: str
    slave: LinkInfoBridgeSlave
