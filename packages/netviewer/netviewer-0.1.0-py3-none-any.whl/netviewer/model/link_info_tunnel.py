from typing import TypedDict


class LinkInfoTunnel(TypedDict):
    kind: str
    proto: str
    remote: str
    local: str
    ttl: int
    pmtudisc: bool
