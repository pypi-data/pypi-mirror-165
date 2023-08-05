from netviewer.model.route import Route
from netviewer.view.console import print_info, print_key_value_oneline


def route_render(route: Route, detail: bool = False, indent: int = 0) -> None:
    dst = route["destination"]
    print_info(f"[info]{dst}:[/]", indent=indent)
    print_key_value_oneline("device:", route["device"], indent=indent + 1)
    print_key_value_oneline("scope:", route["scope"], indent=indent + 1)
    if route["source"] is not None:
        print_key_value_oneline("source:", route["source"], indent=indent + 1)
    if route["gateway"] is not None:
        print_key_value_oneline("via:", route["gateway"], indent=indent + 1)
    if route["protocol"] is not None:
        print_key_value_oneline("protocol:", route["protocol"], indent=indent + 1)

    if detail:
        if route["metric"] != -1:
            print_key_value_oneline("metric:", route["metric"], indent=indent + 1)
        if route["type"] is not None:
            print_key_value_oneline("type:", route["type"], indent=indent + 1)


def routes_render(
    routes: dict[str, Route], detail: bool = False, indent: int = 0
) -> None:
    for item in routes.values():
        route_render(item, detail, indent)


def route_list_render(routes: dict[str, Route]) -> None:
    for item in routes.values():
        print_info(item["destination"])
