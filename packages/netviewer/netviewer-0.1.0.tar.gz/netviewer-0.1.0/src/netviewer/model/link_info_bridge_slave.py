from typing import TypedDict


class LinkInfoBridgeSlave(TypedDict):
    slave_kind: str
    state: str
    priority: int
    cost: int
    hairpin: bool
    guard: bool
    root_block: bool
    fastleave: bool
    learning: bool
    flood: bool
    id: int
    no: int
    designated_port: int
    designated_cost: int
    bridge_id: str
    root_id: str
    hold_timer: int
    message_age_timer: int
    forward_delay_timer: int
    topology_change_ack: int
    config_pending: int
    proxy_arp: bool
    proxy_arp_wifi: bool
    multicast_router: int
    mcast_flood: bool
    mcast_to_unicast: bool
    neigh_suppress: bool
    group_fwd_mask: int
    group_fwd_mask_str: int
    vlan_tunnel: bool
    isolated: bool
