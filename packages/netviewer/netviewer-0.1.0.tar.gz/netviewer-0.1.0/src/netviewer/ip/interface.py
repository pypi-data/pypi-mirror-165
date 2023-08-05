from typing import Any

from netviewer.ip.inet import parse_inet
from netviewer.ip.link_info import link_info_parse
from netviewer.model.interface import Interface


def parse(info: list[dict[str, Any]]) -> dict[str, Interface]:
    interfaces: dict[str, Interface] = {}
    for item in info:
        name = item["ifname"]
        ai: Interface = {
            "name": name,
            "index": item["ifindex"],
            "flags": item["flags"],
            "mtu": item["mtu"],
            "metric": item.get("mtu", -1),
            "qdisc": item["qdisc"],
            "state": item["operstate"],
            "group": item["group"],
            "qlen": item.get("txqlen", None),
            "link_type": item["link_type"],
            "info": parse_inet(item["addr_info"]),
            "address": item["address"],
            "broadcast": item["broadcast"],
            "master": item.get("master", None),
            # detail information
            "dynamic": item.get("dynamic", False),
            "promiscuity": item.get("promiscuity", -1),
            "min_mtu": item.get("min_mtu", -1),
            "max_mtu": item.get("max_mtu", -1),
            "num_tx_queues": item.get("num_tx_queues", -1),
            "num_rx_queues": item.get("num_rx_queues", -1),
            "gso_max_size": item.get("gso_max_size", -1),
            "gso_max_segs": item.get("gso_max_segs", -1),
            "parentbus": item.get("parentbus", None),
            "parentdev": item.get("parentdev", None),
            "link_info_type": "",
            "inet6_addr_gen_mode": item.get("inet6_addr_gen_mode", None),
        }

        if "linkinfo" in item:
            ai["link_info"] = link_info_parse(item["linkinfo"])

        interfaces[name] = ai

    return interfaces
