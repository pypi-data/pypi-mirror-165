from typing import TypedDict


class LinkInfoBridge(TypedDict):
    kind: str
    forward_delay: int
    hello_time: int
    hello_timer: int

    max_age: int
    ageing_time: int

    stp_state: int
    priority: int
    bridge_id: str
    root_id: str
    root_port: int
    root_path_cost: int
    tcn_timer: int
    topology_change: int
    topology_change_detected: int
    topology_change_timer: int
    gc_timer: float

    vlan_protocol: str
    vlan_filtering: int
    vlan_default_pvid: int
    vlan_stats_enabled: int
    vlan_stats_per_port: int

    group_fwd_mask: int
    group_addr: str

    mcast_snooping: int
    mcast_router: int
    mcast_query_use_ifaddr: int
    mcast_querier: int
    mcast_hash_elasticity: int
    mcast_hash_max: int
    mcast_last_member_cnt: int
    mcast_startup_query_cnt: int
    mcast_last_member_intvl: int
    mcast_membership_intvl: int
    mcast_querier_intvl: int
    mcast_query_intvl: int
    mcast_query_response_intvl: int
    mcast_startup_query_intvl: int
    mcast_stats_enabled: int
    mcast_igmp_version: int
    mcast_mld_version: int

    nf_call_iptables: int
    nf_call_ip6tables: int
    nf_call_arptables: int
