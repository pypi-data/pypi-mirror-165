from typing import Any

from netviewer.ip.link_info_bridge_slave import parse_bridge_slave_info
from netviewer.model.link_info_veth import LinkInfoVeth


def parse_veth_link_info(link_info: dict[str, Any]) -> LinkInfoVeth:
    vi: LinkInfoVeth = {
        "kind": "veth",
        "slave": parse_bridge_slave_info(link_info["info_slave_data"]),
    }

    return vi
