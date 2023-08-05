from netviewer.config import _config  # type: ignore
from netviewer.model.link import Link
from netviewer.view.console import print_info, print_key_value_oneline
from netviewer.view.render.link_info import link_info_render
from netviewer.view.render.utils import link_type_order, state_order


def link_sort_key(link: Link) -> tuple[int, int, str]:
    updown_order = state_order[link["state"].lower()]
    lt_order = link_type_order.get(link["link_type"], 999)
    order = updown_order, lt_order, link["name"]
    return order


def link_render(link: Link, detail: bool = False, indent: int = 0) -> None:
    name = link["name"]
    if link["state"].lower() in ["up", "unknown"]:
        print_info(f"{name}:")
    else:
        print_info(f"[dim]{name}:[/]")

    print_key_value_oneline("index:", link["index"], indent=1)
    print_key_value_oneline("state:", link["state"].lower(), indent=1)
    print_key_value_oneline("type:", link["link_type"], indent=1)
    print_key_value_oneline("address:", link["address"], indent=1)
    print_key_value_oneline("broadcast:", link["broadcast"], indent=1)

    flags = ", ".join(link["flags"])
    print_key_value_oneline("flags:", flags, indent=1)
    print_key_value_oneline("mtu:", link["mtu"], indent=1)
    if link["master"] is not None:
        print_key_value_oneline("master:", link["master"], indent=1)
    if link["link_index"] is not None:
        print_key_value_oneline("index:", link["link_index"], indent=1)
    if link["link_mode"] is not None:
        print_key_value_oneline("mode:", link["link_mode"], indent=1)
    print_key_value_oneline("namespace id:", link["link_netnsid"], indent=1)
    print_key_value_oneline("group:", link["group"], indent=1)
    print_key_value_oneline("queue type:", f"{link['qdisc']}", indent=1)

    cfg = _config.get()
    link_info = link.get("link_info", None)
    if cfg["detail"] and link_info is not None:
        link_info_render(link_info)


def links_render(links: dict[str, Link], detail: bool = False, indent: int = 0) -> None:
    for link in sorted(links.values(), key=link_sort_key):
        link_render(link, detail, indent)


def link_list_render(links: dict[str, Link]) -> None:
    for link in sorted(links.values(), key=link_sort_key):
        name = link["name"]
        if link["state"].lower() in ["up", "unknown"]:
            print_info(f"{name}")
        else:
            print_info(f"[dim]{name}[/]")
