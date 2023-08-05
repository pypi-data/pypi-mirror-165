from netviewer.model.bridge import Bridge
from netviewer.model.interface import Interface


def parse(addresses: dict[str, Interface]) -> dict[str, Bridge]:
    bridges: dict[str, Bridge] = {}
    if len(addresses) != 0:
        for item in addresses.values():
            if item["master"] is not None:
                if item["master"] not in bridges:
                    br: Bridge = {
                        "name": item["master"],
                        "devices": [item["name"]],
                        "interface": addresses[item["master"]],
                    }
                    bridges[item["master"]] = br
                else:
                    bridges[item["master"]]["devices"].append(item["name"])

    return bridges
