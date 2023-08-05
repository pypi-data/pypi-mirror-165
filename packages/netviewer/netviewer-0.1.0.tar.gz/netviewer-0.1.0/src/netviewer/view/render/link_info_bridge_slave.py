from netviewer.model.link_info_bridge_slave import LinkInfoBridgeSlave
from netviewer.view.console import print_key_oneline, print_key_value_oneline

from .utils import bool_str, mcast_router_str, on_off_str


def bridge_slave_link_info_render(
    info: LinkInfoBridgeSlave, detail: bool = False, indent: int = 0
) -> None:
    print_key_oneline("bridge slave:", indent=indent)
    print_key_value_oneline("bridge id:", info["bridge_id"], indent=indent + 1)
    print_key_value_oneline("root id:", info["root_id"], indent=indent + 1)
    print_key_value_oneline("state:", info["state"], indent=indent + 1)
    print_key_value_oneline("priority:", info["priority"], indent=indent + 1)
    print_key_value_oneline("cost:", info["cost"], indent=indent + 1)
    print_key_value_oneline("guard:", on_off_str(info["guard"]), indent=indent + 1)
    print_key_value_oneline("hairpin:", on_off_str(info["hairpin"]), indent=indent + 1)
    print_key_value_oneline(
        "fast leave:", on_off_str(info["fastleave"]), indent=indent + 1
    )
    print_key_value_oneline(
        "root block:", on_off_str(info["root_block"]), indent=indent + 1
    )
    print_key_value_oneline(
        "learning:", on_off_str(info["learning"]), indent=indent + 1
    )
    print_key_value_oneline("flood:", on_off_str(info["flood"]), indent=indent + 1)
    print_key_value_oneline(
        "proxy arp:", on_off_str(info["proxy_arp"]), indent=indent + 1
    )
    print_key_value_oneline(
        "proxy arp wifi:", on_off_str(info["proxy_arp_wifi"]), indent=indent + 1
    )
    print_key_value_oneline(
        "neighbor discovery suppression:",
        on_off_str(info["neigh_suppress"]),
        indent=indent + 1,
    )
    print_key_value_oneline(
        "vlan tunnel:",
        on_off_str(info["vlan_tunnel"]),
        indent=indent + 1,
    )
    print_key_value_oneline(
        "multicast router:",
        mcast_router_str(info["multicast_router"]),
        indent=indent + 1,
    )
    print_key_value_oneline(
        "multicast flood:", on_off_str(info["mcast_flood"]), indent=indent + 1
    )
    print_key_value_oneline(
        "multicast to unicast:", on_off_str(info["mcast_to_unicast"]), indent=indent + 1
    )
    print_key_value_oneline(
        "group forward mask:", hex(info["mcast_to_unicast"]), indent=indent + 1
    )
    print_key_value_oneline(
        "isolated:",
        bool_str(info["isolated"]),
        indent=indent + 1,
    )
