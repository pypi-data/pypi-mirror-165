from typing import Any

import netviewer.ip.link_info_bond
import netviewer.ip.link_info_bridge
import netviewer.ip.link_info_tunnel
import netviewer.ip.link_info_veth
from netviewer.model.link_info import LinkInfo


def link_info_parse(link_info: dict[str, Any]):
    item_kind = link_info["info_kind"]

    li: LinkInfo = {"kind": item_kind, "info": None}

    if item_kind == "bridge":
        li["info"] = netviewer.ip.link_info_bridge.parse_bridge_link_info(link_info)
    elif item_kind == "veth":
        li["info"] = netviewer.ip.link_info_veth.parse_veth_link_info(link_info)
    elif item_kind == "bond":
        li["info"] = netviewer.ip.link_info_bond.parse_bond_info(link_info)
    elif item_kind == "sit" or item_kind == "ipip":
        li["info"] = netviewer.ip.link_info_tunnel.parse_tunnel_info(link_info)

    return li
