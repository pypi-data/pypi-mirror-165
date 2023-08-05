def bool_str(value: bool) -> str:
    return "true" if value else "false"


def true_false_str(value: int) -> str:
    return "true (1)" if value else "false (0)"


def on_off_str(value: int) -> str:
    return "on" if value else "off"


def enabled_str(value: int) -> str:
    return "enabled" if value else "disabled"


def mcast_router_str(value: int) -> str:
    router = {
        0: "disabled",
        1: "automatic (queried)",
        2: "permanently enabled",
        3: "temporarily enabled",
    }
    return router[value]


state_order = {"unknown": 1, "up": 2, "down": 3}
link_type_order = {
    "loopback": 1,
    "ether": 2,
    "bridge": 3,
    "veth": 4,
    "ipip": 5,
    "sit": 5,
}
