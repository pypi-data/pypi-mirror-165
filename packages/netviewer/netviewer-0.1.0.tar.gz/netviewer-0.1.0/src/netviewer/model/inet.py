from ipaddress import IPv4Address, IPv6Address
from typing import Literal, TypedDict

from netviewer.model import MAC


class INetInfo(TypedDict):
    family: Literal["inet", "inet6"]
    label: str
    local: MAC | IPv4Address | IPv6Address
    broadcast: MAC | IPv4Address | IPv6Address | None
    valid_lifetime: int
    preferred_lifetime: int
    prefix_length: int
    scope: str
    metric: int
    dynamic: bool
    noprefixroute: bool
