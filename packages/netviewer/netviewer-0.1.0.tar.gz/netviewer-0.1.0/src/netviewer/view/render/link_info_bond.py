from netviewer.model.link_info_bond import LinkInfoBond
from netviewer.view.console import print_key_value_oneline
from netviewer.view.render.utils import true_false_str


def arp_validate_render(arp_validate: str | int | None, indent: int = 0) -> None:
    if arp_validate is None:
        return

    validate_int = {
        0: "none",
        1: "active",
        2: "backup",
        3: "all",
        4: "filter",
        5: "filter_active",
        6: "filter_backup",
    }
    if isinstance(arp_validate, str):
        validate = arp_validate
    else:
        validate = validate_int[arp_validate]

    print_key_value_oneline("ARP validate:", validate, indent=indent)


# https://www.kernel.org/doc/html/latest/networking/bonding.html
def bond_link_info_render(
    info: LinkInfoBond, detail: bool = False, indent: int = 0
) -> None:
    print_key_value_oneline("type:", "bond", indent=indent)
    print_key_value_oneline("mode:", info["mode"], indent=indent)
    print_key_value_oneline("miimon:", info["miimon"], indent=indent)
    print_key_value_oneline("up delay:", f'{info["updelay"]}ms', indent=indent)
    print_key_value_oneline("down delay:", f'{info["downdelay"]}ms', indent=indent)
    print_key_value_oneline(
        "peer notifier delay:", f'{info["peer_notify_delay"]}ms', indent=indent
    )
    print_key_value_oneline(
        "use carrier:", true_false_str(info["use_carrier"]), indent=indent
    )
    print_key_value_oneline("ARP interval:", f'{info["arp_interval"]}ms', indent=indent)
    if info["arp_validate"] is not None:
        arp_validate_render(info["arp_validate"], indent=indent)
    print_key_value_oneline("arp all targets:", info["arp_all_targets"], indent=indent)
    print_key_value_oneline(
        "primary reselect:", info["primary_reselect"], indent=indent
    )
    print_key_value_oneline("failover mac:", info["fail_over_mac"], indent=indent)
    print_key_value_oneline(
        "transmit hash policy:", info["xmit_hash_policy"], indent=indent
    )
    print_key_value_oneline("resend IGMP:", info["resend_igmp"], indent=indent)

    all_slaves = "dropped" if info["all_slaves_active"] == 0 else "delivered"
    print_key_value_oneline("all slaves active:", all_slaves, indent=indent)

    print_key_value_oneline("minimum links:", info["min_links"], indent=indent)
    print_key_value_oneline("lp interval:", f'{info["lp_interval"]}s', indent=indent)

    if info["mode"] == "balance-rr":
        print_key_value_oneline(
            "packets per slave:", info["packets_per_slave"], indent=indent
        )

    print_key_value_oneline("LACP rate:", info["ad_lacp_rate"], indent=indent)
    print_key_value_oneline(
        "LACP aggregation selection logic:", info["ad_select"], indent=indent
    )
    print_key_value_oneline(
        "tb mode dynamic shuffling:", info["tlb_dynamic_lb"], indent=indent
    )
