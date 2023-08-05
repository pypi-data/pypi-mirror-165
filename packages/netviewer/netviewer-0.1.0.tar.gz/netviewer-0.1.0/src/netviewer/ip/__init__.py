import json
import subprocess
from typing import Any, Literal

from netviewer.ip import bridge, interface, link, route

IPSection = Literal["link", "address", "route"]
parse_funcs = {"address": interface.parse, "link": link.parse, "route": route.parse}


def exec_ip(cmd: str) -> dict[str, Any]:
    res = subprocess.run(["ip", "-json", "-detail", cmd, "show"], capture_output=True)
    r = json.loads(res.stdout.decode("utf-8"))
    return r


def load(section: IPSection | None = None) -> dict[str, Any]:
    netdata: dict[str, Any] = {}
    if section is None:
        sections = ["link", "address", "route"]
    else:
        sections = [section]

    for item in sections:
        output = exec_ip(item)
        netdata[item] = output

    return netdata


def parse(netdata: dict[str, Any], section: IPSection | None = None) -> dict[str, Any]:
    netinfo: dict[str, Any] = {}
    if section is None:
        sections = ["link", "address", "route"]
    else:
        sections = [section]

    for item in sections:
        netinfo[item] = parse_funcs[item](netdata[item])

    if "address" in netdata:
        netinfo["bridge"] = bridge.parse(netinfo["address"])
    else:
        netinfo["bridge"] = {}

    return netinfo
