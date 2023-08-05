from netviewer.config import _config  # type: ignore
from netviewer.model.inet import INetInfo
from netviewer.model.interface import Interface
from netviewer.view.console import (
    print_info,
    print_key_oneline,
    print_key_value_oneline,
)
from netviewer.view.render.link_info import link_info_render
from netviewer.view.render.utils import link_type_order, state_order
from netviewer.view.theme import get_style


def interface_sort_key(interface: Interface) -> tuple[int, int, str]:
    updown_order = state_order[interface["state"].lower()]
    lt_order = link_type_order.get(interface["link_type"], 999)
    order = updown_order, lt_order, interface["name"]
    return order


def ipv4_info_render(inet: INetInfo, indent: int = 0) -> None:
    print_key_oneline("ipv4:", indent=indent + 1)
    print_key_value_oneline("scope:", f"{inet['scope']}", indent=indent + 2)
    print_key_value_oneline(
        "ip:", f'{inet["local"]}/{inet["prefix_length"]}', indent=indent + 2
    )
    if inet["broadcast"]:
        print_key_value_oneline("broadcast:", f'{inet["broadcast"]}', indent=indent + 2)
    if inet["metric"]:
        print_key_value_oneline("metric:", inet["metric"], indent=indent + 2)
    if inet["dynamic"]:
        print_key_value_oneline(
            "dynamic:", str(inet["dynamic"]).lower(), indent=indent + 2
        )


def ipv6_info_render(inet: INetInfo, indent: int = 0) -> None:
    print_key_oneline("ipv6:", indent=indent + 1)
    print_key_value_oneline("scope:", inet["scope"], indent=indent + 2)
    print_key_value_oneline(
        "ip:", f'{inet["local"]}/{inet["prefix_length"]}', indent=indent + 2
    )


def inet_info_render(info: list[INetInfo], indent: int = 0):
    def inet_key(item: INetInfo) -> str:
        return item["family"]

    for inet in sorted(info, key=inet_key):
        if inet["family"] == "inet":
            ipv4_info_render(inet, indent)
        elif inet["family"] == "inet6":
            ipv6_info_render(inet, indent)

        if inet["preferred_lifetime"] == -1 or inet["preferred_lifetime"] == 0xFFFFFFFF:
            print_key_value_oneline("preferred lifetime:", "forever", indent=indent + 2)
        else:
            print_key_value_oneline(
                "preferred lifetime:",
                f'{inet["preferred_lifetime"]}s',
                indent=indent + 2,
            )

        if inet["valid_lifetime"] == -1 or inet["valid_lifetime"] == 0xFFFFFFFF:
            print_key_value_oneline("valid lifetime:", "forever", indent=indent + 2)
        else:
            print_key_value_oneline(
                "valid lifetime:",
                f'{inet["valid_lifetime"]}s',
                indent=indent + 2,
            )


def mac_info_render(info: Interface, indent: int = 0) -> None:
    print_key_oneline("mac:", indent=indent + 1)
    print_key_value_oneline("address:  ", f'{info["address"]}', indent=indent + 2)
    print_key_value_oneline("broadcast:", f'{info["broadcast"]}', indent=indent + 2)


def mtu_render(info: Interface, indent: int = 0) -> None:
    cfg = _config.get()
    print_key_oneline("mtu:", indent=indent + 1)
    print_key_value_oneline("size:", info["mtu"], indent=indent + 2)
    if cfg["detail"]:
        print_key_value_oneline("min: ", info["min_mtu"], indent=indent + 2)
        print_key_value_oneline("max: ", info["max_mtu"], indent=indent + 2)


def queue_info_render(info: Interface, indent: int = 0) -> None:
    print_key_oneline("queue:", indent=indent + 1)
    print_key_value_oneline("type:", info["qdisc"], indent=indent + 2)
    if info["qlen"] is not None:
        print_key_value_oneline("length:", info["qlen"], indent=indent + 2)

    if info["num_tx_queues"] != -1 or info["num_rx_queues"] != -1:
        print_key_oneline("count:", indent=indent + 2)
    if info["num_tx_queues"] != -1:
        print_key_value_oneline(
            "transmit:",
            info["num_tx_queues"],
            indent=indent + 3,
        )

    if info["num_rx_queues"] != -1:
        print_key_value_oneline("receive: ", info["num_rx_queues"], indent=indent + 3)


def interface_render(
    interface: Interface,
    detail: bool = False,
    indent: int = 0,
    show_name: bool = True,
) -> None:
    cfg = _config.get()

    state = interface["state"].lower()
    link_type = interface["link_type"].lower()
    if show_name:
        if state == "up" or link_type == "loopback" or cfg["state"] is not None:
            highlight = "info"
        else:
            highlight = "dim green"

        print_key_oneline(
            f'[{highlight}]{interface["name"]}[/]:',
            key_style=get_style(highlight),
        )
    print_key_value_oneline("index:", interface["index"], indent=indent + 1)
    print_key_value_oneline("type:", interface["link_type"], indent=indent + 1)
    print_key_value_oneline("state:", state, indent=indent + 1)
    if interface["info"]:
        inet_info_render(interface["info"], indent=indent)

    if cfg["detail"]:
        if interface["inet6_addr_gen_mode"] is not None:
            print_key_value_oneline(
                "ipv6 address generation mode:",
                interface["inet6_addr_gen_mode"],
                indent=indent + 1,
            )

    flags = ", ".join(interface["flags"])
    print_key_value_oneline("flags:", flags, indent=indent + 1)

    if interface["link_type"] == "ether":
        mac_info_render(interface, indent=indent)

    mtu_render(interface)

    if interface["master"]:
        print_key_value_oneline("master:", interface["master"], indent=indent + 1)

    if cfg["detail"]:
        if interface["promiscuity"] != -1:
            print_key_value_oneline(
                "promiscuity:", interface["promiscuity"], indent=indent + 1
            )

        queue_info_render(interface, indent=indent)

        if interface["gso_max_size"] != -1:
            print_key_value_oneline(
                "generic segment offload (gso) max packet size:",
                interface["gso_max_size"],
                indent=indent + 1,
            )

        if interface["gso_max_segs"] != -1:
            print_key_value_oneline(
                "generic segment offload (gso) max segments:",
                interface["gso_max_segs"],
                indent=indent + 1,
            )

        if interface["parentbus"] is not None or interface["parentdev"] is not None:
            print_key_oneline("parent:", indent=indent + 1)
        if interface["parentbus"] is not None:
            print_key_value_oneline(
                "bus:",
                interface["parentbus"],
                indent=indent + 2,
            )

        if interface["parentdev"] is not None:
            print_key_value_oneline(
                "device:",
                interface["parentdev"],
                indent=indent + 2,
            )

        link_info = interface.get("link_info", None)
        if link_info is not None:
            link_info_render(link_info)


def interfaces_render(
    interfaces: dict[str, Interface], detail: bool = False, indent: int = 0
) -> None:
    cfg = _config.get()
    for interface in interfaces.values():
        if not cfg["state"] or (
            cfg["state"] and interface["state"].lower() == cfg["state"]
        ):
            interface_render(interface, detail, indent)


def interface_list_render(interfaces: dict[str, Interface]) -> None:
    for interface in sorted(interfaces.values(), key=interface_sort_key):
        name = interface["name"]
        if interface["state"].lower() in ["up", "unknown"]:
            print_info(f"{name}")
        else:
            print_info(f"[dim]{name}[/]")
