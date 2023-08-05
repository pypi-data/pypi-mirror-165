from typing import Any

from netviewer.model.link_info_tunnel import LinkInfoTunnel


def parse_tunnel_info(link_info: dict[str, Any]) -> LinkInfoTunnel:
    data = link_info["info_data"]

    ti: LinkInfoTunnel = {
        "kind": link_info["info_kind"],
        "proto": data["proto"],
        "remote": data["remote"],
        "local": data["local"],
        "ttl": data["ttl"],
        "pmtudisc": data["pmtudisc"],
    }

    return ti
