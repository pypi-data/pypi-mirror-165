from ipaddress import AddressValueError, IPv4Address, IPv6Address
from typing import Any

from netviewer.model.inet import INetInfo
from netviewer.utils import is_mac


def parse_mac_or_ip(item: str) -> Any:
    if is_mac(item):
        return item
    else:
        try:
            if "." in item:
                return IPv4Address(item)
            else:
                return IPv6Address(item)
        except AddressValueError:
            return IPv4Address("0.0.0.0")


def parse_inet(info: list[dict[str, Any]]) -> list[INetInfo]:
    inet: list[INetInfo] = []
    for item in info:
        local = parse_mac_or_ip(item["local"])
        if "broadcast" in item:
            broadcast = parse_mac_or_ip(item["broadcast"])
        else:
            broadcast = None

        inetinfo: INetInfo = {
            "family": item["family"],
            "label": item.get("label", ""),
            "local": local,
            "broadcast": broadcast,
            "valid_lifetime": item.get("valid_life_time", -1),
            "preferred_lifetime": item.get("preferred_life_time", -1),
            "prefix_length": int(item["prefixlen"]),
            "scope": item["scope"],
            "metric": item.get("metric", 0),
            "dynamic": item.get("dynamic", False),
            "noprefixroute": item.get("noprefixroute", False),
        }

        inet.append(inetinfo)

    return inet
