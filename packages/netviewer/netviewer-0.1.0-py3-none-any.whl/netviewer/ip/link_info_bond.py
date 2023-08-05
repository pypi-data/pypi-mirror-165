from typing import Any

from netviewer.model.link_info_bond import LinkInfoBond


def parse_bond_info(link_info: dict[str, Any]) -> LinkInfoBond:
    data = link_info["info_data"]

    bi: LinkInfoBond = {
        "kind": "bond",
        "mode": data["mode"],
        "miimon": data["miimon"],
        "updelay": data["updelay"],
        "downdelay": data["downdelay"],
        "peer_notify_delay": data["peer_notify_delay"],
        "use_carrier": data["use_carrier"],
        "arp_interval": data["arp_interval"],
        "arp_validate": data["arp_validate"] or 1,
        "arp_all_targets": data["arp_all_targets"],
        "primary_reselect": data["primary_reselect"],
        "fail_over_mac": data["fail_over_mac"],
        "xmit_hash_policy": data["xmit_hash_policy"],
        "resend_igmp": data["resend_igmp"],
        "num_peer_notif": data["num_peer_notif"],
        "all_slaves_active": data["all_slaves_active"],
        "min_links": data["min_links"],
        "lp_interval": data["lp_interval"],
        "packets_per_slave": data["packets_per_slave"],
        "ad_lacp_rate": data["ad_lacp_rate"],
        "ad_select": data["ad_select"],
        "tlb_dynamic_lb": data["tlb_dynamic_lb"],
    }

    return bi
