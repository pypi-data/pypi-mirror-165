def is_mac(address: str) -> bool:
    elems = address.split(":")
    if len(elems) != 6:
        return False

    try:
        for e in elems:
            if e == "":
                return False
            _ = int(e, 16)
    except ValueError:
        return False

    return True
