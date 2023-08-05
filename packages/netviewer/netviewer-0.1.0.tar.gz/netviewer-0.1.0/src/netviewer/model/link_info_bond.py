from typing import TypedDict


class LinkInfoBond(TypedDict):
    kind: str
    mode: str
    miimon: int
    updelay: int
    downdelay: int
    peer_notify_delay: int
    use_carrier: int
    arp_interval: int
    arp_validate: int
    arp_all_targets: str
    primary_reselect: str
    fail_over_mac: str
    xmit_hash_policy: str
    resend_igmp: int
    num_peer_notif: int
    all_slaves_active: int
    min_links: int
    lp_interval: int
    packets_per_slave: int
    ad_lacp_rate: str
    ad_select: str
    tlb_dynamic_lb: int
