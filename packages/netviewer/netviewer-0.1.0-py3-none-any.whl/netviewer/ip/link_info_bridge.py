from typing import Any

from netviewer.model.link_info_bridge import LinkInfoBridge


def parse_bridge_link_info(link_info: dict[str, Any]) -> LinkInfoBridge:
    data = link_info["info_data"]

    bi: LinkInfoBridge = {
        "kind": "bridge",
        "forward_delay": data["forward_delay"],
        "hello_time": data["hello_time"],
        "max_age": data["max_age"],
        "ageing_time": data["ageing_time"],
        "stp_state": data["stp_state"],
        "priority": data["priority"],
        "bridge_id": data["bridge_id"],
        "root_id": data["root_id"],
        "root_port": data["root_port"],
        "root_path_cost": data["root_path_cost"],
        "hello_timer": data["hello_timer"],
        "gc_timer": data["gc_timer"],
        "group_fwd_mask": data["group_fwd_mask"],
        "group_addr": data["group_addr"],
        # topology changes
        "topology_change": data["topology_change"],
        "topology_change_detected": data["topology_change_detected"],
        "tcn_timer": data["tcn_timer"],
        "topology_change_timer": data["topology_change_timer"],
        # Vlan
        "vlan_filtering": data["vlan_filtering"],
        "vlan_protocol": data["vlan_protocol"],
        "vlan_default_pvid": data["vlan_default_pvid"],
        "vlan_stats_enabled": data["vlan_stats_enabled"],
        "vlan_stats_per_port": data["vlan_stats_per_port"],
        # Multicast
        "mcast_snooping": data["mcast_snooping"],
        "mcast_router": data["mcast_router"],
        "mcast_query_use_ifaddr": data["mcast_query_use_ifaddr"],
        "mcast_querier": data["mcast_querier"],
        "mcast_hash_elasticity": data["mcast_hash_elasticity"],
        "mcast_hash_max": data["mcast_hash_max"],
        "mcast_last_member_cnt": data["mcast_last_member_cnt"],
        "mcast_startup_query_cnt": data["mcast_startup_query_cnt"],
        "mcast_last_member_intvl": data["mcast_last_member_intvl"],
        "mcast_membership_intvl": data["mcast_membership_intvl"],
        "mcast_querier_intvl": data["mcast_querier_intvl"],
        "mcast_query_intvl": data["mcast_query_intvl"],
        "mcast_query_response_intvl": data["mcast_query_response_intvl"],
        "mcast_startup_query_intvl": data["mcast_startup_query_intvl"],
        "mcast_stats_enabled": data["mcast_stats_enabled"],
        "mcast_igmp_version": data["mcast_igmp_version"],
        "mcast_mld_version": data["mcast_mld_version"],
        # iptable hooks
        "nf_call_iptables": data["nf_call_iptables"],
        "nf_call_ip6tables": data["nf_call_ip6tables"],
        "nf_call_arptables": data["nf_call_arptables"],
    }

    return bi
