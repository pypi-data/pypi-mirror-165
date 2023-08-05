from typing import Any

from netviewer.model.route import Route


def parse(info: list[dict[str, Any]]) -> dict[str, Route]:
    routes: dict[str, Route] = {}
    for item in info:
        ri: Route = {
            "destination": item["dst"],
            "device": item["dev"],
            "protocol": item.get("protocol", None),
            "scope": item.get("scope", "global"),
            "source": item.get("prefsrc", None),
            "flags": item["flags"],
            "gateway": item.get("gateway", None),
            "metric": item.get("metric", -1),
            "type": item.get("type", None),
        }
        routes[item["dst"]] = ri

    return routes
