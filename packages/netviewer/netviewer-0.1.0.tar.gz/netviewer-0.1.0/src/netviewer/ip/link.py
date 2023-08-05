from typing import Any

from netviewer.ip.link_info import link_info_parse
from netviewer.model.link import Link


def parse(info: list[dict[str, Any]]) -> dict[str, Link]:
    links: dict[str, Link] = {}
    for item in info:
        li: Link = {
            "index": item["ifindex"],
            "name": item["ifname"],
            "link_index": item.get("link_index", None),
            "flags": item["flags"],
            "mtu": item["mtu"],
            "qdisc": item["qdisc"],
            "master": item.get("master", None),
            "state": item["operstate"],
            "link_mode": item.get("link_mode", None),
            "group": item["group"],
            "link_type": item["link_type"],
            "address": item["address"],
            "broadcast": item["broadcast"],
            "link_netnsid": int(item.get("link_netnsid", 0)),
            "link_info_type": "",
            "link_info": None,
        }

        if "linkinfo" in item:
            li["link_info_type"] = item["linkinfo"]["info_kind"]
            li["link_info"] = link_info_parse(item["linkinfo"])

        links[item["ifname"]] = li

    return links
