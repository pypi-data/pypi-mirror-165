from netviewer.model.link_info_bridge import LinkInfoBridge
from netviewer.view.console import print_key_oneline, print_key_value_oneline

from .utils import enabled_str, mcast_router_str


def vlan_info_render(info: LinkInfoBridge, indent: int = 0) -> None:
    print_key_oneline("vlan:", indent=indent)
    print_key_value_oneline("protocol:", info["vlan_protocol"], indent=indent + 1)
    print_key_value_oneline(
        "default PVID:", info["vlan_default_pvid"], indent=indent + 1
    )
    print_key_value_oneline(
        "filtering:", f'{enabled_str(info["vlan_filtering"])}', indent=indent + 1
    )
    print_key_value_oneline(
        "stats:",
        f'{enabled_str(info["vlan_stats_enabled"])}',
        indent=indent + 1,
    )


def stp_info_render(info: LinkInfoBridge, indent: int = 0) -> None:
    print_key_oneline("stp:", indent=indent)
    print_key_value_oneline(
        "state:",
        f'{enabled_str(info["stp_state"])}',
        indent=indent + 1,
    )
    print_key_value_oneline("priority:", info["priority"], indent=indent + 1)
    print_key_value_oneline(
        "hello timer:",
        f'{enabled_str(info["hello_timer"])}',
        indent=indent + 1,
    )
    print_key_value_oneline("hello time:", f'{info["hello_time"]}s', indent=indent + 1)
    print_key_value_oneline("maximum age:", f'{info["max_age"]}s', indent=indent + 1)
    print_key_value_oneline(
        "forward delay:", f'{info["forward_delay"]}s', indent=indent + 1
    )
    print_key_value_oneline(
        "ageing time:", f'{info["ageing_time"]}s', indent=indent + 1
    )


def hooks_info_render(info: LinkInfoBridge, indent: int = 0) -> None:
    print_key_oneline("hooks:", indent=indent)
    print_key_value_oneline(
        "iptables:", f'{enabled_str(info["nf_call_iptables"])}', indent=indent + 1
    )
    print_key_value_oneline(
        "ip6tables:", f'{enabled_str(info["nf_call_ip6tables"])}', indent=indent + 1
    )
    print_key_value_oneline(
        "arptables:", f'{enabled_str(info["nf_call_arptables"])}', indent=indent + 1
    )


def root_info_render(info: LinkInfoBridge, indent: int = 0) -> None:
    print_key_value_oneline("root id:", info["root_id"], indent=indent)
    print_key_value_oneline("root port:", info["root_port"], indent=indent)
    print_key_value_oneline("root path cost:", info["root_path_cost"], indent=indent)


def multicast_info_render(info: LinkInfoBridge, indent: int = 0) -> None:
    print_key_oneline("multicast:", indent=indent)
    print_key_value_oneline(
        "router:", f'{mcast_router_str(info["mcast_router"])}', indent=indent + 1
    )
    print_key_value_oneline(
        "snooping:", f'{enabled_str(info["mcast_snooping"])}', indent=indent + 1
    )
    print_key_value_oneline(
        "IGMP query use interface address:",
        f'{enabled_str(info["mcast_query_use_ifaddr"])}',
        indent=indent + 1,
    )
    print_key_value_oneline(
        "querier:", f'{enabled_str(info["mcast_querier"])}', indent=indent + 1
    )
    print_key_value_oneline(
        "querier interval:", f'{info["mcast_querier_intvl"]}s', indent=indent + 1
    )
    print_key_value_oneline(
        "hash elasticity:",
        info["mcast_hash_elasticity"],
        indent=indent + 1,
    )
    print_key_value_oneline("hash max:", info["mcast_hash_max"], indent=indent + 1)
    print_key_value_oneline(
        "last member count:",
        info["mcast_last_member_cnt"],
        indent=indent + 1,
    )
    print_key_value_oneline(
        "last member interval:",
        f'{info["mcast_last_member_intvl"]}s',
        indent=indent + 1,
    )
    print_key_value_oneline(
        "startup query count:",
        info["mcast_startup_query_cnt"],
        indent=indent + 1,
    )
    print_key_value_oneline(
        "startup query interval:",
        f'{info["mcast_startup_query_intvl"]}s',
        indent=indent + 1,
    )
    print_key_value_oneline(
        "query interval:",
        info["mcast_query_intvl"],
        indent=indent + 1,
    )
    print_key_value_oneline(
        "query response interval:",
        f'{info["mcast_query_response_intvl"]}s',
        indent=indent + 1,
    )
    print_key_value_oneline(
        "membership interval:",
        f'{info["mcast_membership_intvl"]}s',
        indent=indent + 1,
    )
    print_key_value_oneline(
        "statistics:",
        f'{enabled_str(info["mcast_stats_enabled"])}',
        indent=indent + 1,
    )
    print_key_value_oneline(
        "IGMP Version:",
        info["mcast_igmp_version"],
        indent=indent + 1,
    )
    print_key_value_oneline(
        "MLD Version:",
        info["mcast_mld_version"],
        indent=indent + 1,
    )


def bridge_link_info_render(
    info: LinkInfoBridge, detail: bool = False, indent: int = 0
) -> None:
    print_key_value_oneline("bridge id:", info["bridge_id"], indent=indent)
    root_info_render(info, indent=indent)
    vlan_info_render(info, indent=indent)
    stp_info_render(info, indent=indent)
    multicast_info_render(info, indent=indent)
    hooks_info_render(info, indent=indent)
