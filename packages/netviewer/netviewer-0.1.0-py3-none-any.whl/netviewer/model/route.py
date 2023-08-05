from typing import TypedDict


class Route(TypedDict):
    destination: str
    device: str
    protocol: str | None
    scope: str
    source: str | None
    flags: list[str]
    gateway: str | None
    type: str | None
    metric: int | None
