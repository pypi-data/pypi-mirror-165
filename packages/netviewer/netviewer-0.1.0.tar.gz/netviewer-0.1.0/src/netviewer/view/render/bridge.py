from netviewer.model.bridge import Bridge
from netviewer.model.interface import Interface
from netviewer.view.console import print_info, print_key_value_oneline
from netviewer.view.render.interface import inet_info_render, interface_render
from netviewer.view.render.utils import link_type_order, state_order


def bridge_sort_key(bridge: Bridge) -> tuple[int, int, str]:
    updown_order = state_order[bridge["interface"]["state"].lower()]
    lt_order = link_type_order.get(bridge["interface"]["link_type"], 999)
    order = updown_order, lt_order, bridge["name"]
    return order


def bridge_address_render(address: Interface, indent: int = 0) -> None:
    inet_info_render(address["info"], indent=indent)


def bridge_render(bridge: Bridge, detail: bool = False, indent: int = 0) -> None:
    print_info(f'{bridge["name"]}:')
    devices = ", ".join(bridge["devices"])
    print_key_value_oneline("devices:", devices, indent=indent + 1)

    bridge_address = bridge["interface"]
    interface_render(bridge_address, detail, indent=indent, show_name=False)


def bridges_render(
    bridges: dict[str, Bridge], detail: bool = False, indent: int = 0
) -> None:
    for bridge in bridges.values():
        bridge_render(bridge, detail, indent)


def bridge_list_render(bridges: dict[str, Bridge]) -> None:
    for bridge in sorted(bridges.values(), key=bridge_sort_key):
        name = bridge["name"]
        if bridge["interface"]["state"].lower() in ["up", "unknown"]:
            print_info(f"{name}")
        else:
            print_info(f"[dim]{name}[/]")
