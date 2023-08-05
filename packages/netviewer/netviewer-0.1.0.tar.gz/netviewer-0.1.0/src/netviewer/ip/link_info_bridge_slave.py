from typing import Any

from netviewer.model.link_info_bridge_slave import LinkInfoBridgeSlave


def parse_bridge_slave_info(slave_info: dict[str, Any]) -> LinkInfoBridgeSlave:
    vi: LinkInfoBridgeSlave = {
        "slave_kind": "bridge",
        "state": slave_info["state"],
        "priority": slave_info["priority"],
        "cost": slave_info["cost"],
        "hairpin": slave_info["hairpin"],
        "guard": slave_info["guard"],
        "root_block": slave_info["root_block"],
        "fastleave": slave_info["fastleave"],
        "learning": slave_info["learning"],
        "flood": slave_info["flood"],
        "id": slave_info["id"],
        "no": slave_info["no"],
        "designated_port": slave_info["designated_port"],
        "designated_cost": slave_info["designated_cost"],
        "bridge_id": slave_info["bridge_id"],
        "root_id": slave_info["root_id"],
        "hold_timer": slave_info["hold_timer"],
        "message_age_timer": slave_info["message_age_timer"],
        "forward_delay_timer": slave_info["forward_delay_timer"],
        "topology_change_ack": slave_info["topology_change_ack"],
        "config_pending": slave_info["config_pending"],
        "proxy_arp": slave_info["proxy_arp"],
        "proxy_arp_wifi": slave_info["proxy_arp_wifi"],
        "multicast_router": slave_info["multicast_router"],
        "mcast_flood": slave_info["mcast_flood"],
        "mcast_to_unicast": slave_info["mcast_to_unicast"],
        "neigh_suppress": slave_info["neigh_suppress"],
        "group_fwd_mask": slave_info["group_fwd_mask"],
        "group_fwd_mask_str": slave_info["group_fwd_mask_str"],
        "vlan_tunnel": slave_info["vlan_tunnel"],
        "isolated": slave_info["isolated"],
    }

    return vi
