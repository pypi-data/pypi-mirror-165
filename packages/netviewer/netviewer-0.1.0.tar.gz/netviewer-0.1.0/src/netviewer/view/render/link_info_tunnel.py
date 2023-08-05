from netviewer.model.link_info_tunnel import LinkInfoTunnel
from netviewer.view.console import print_key_value_oneline


def tunnel_link_info_render(
    info: LinkInfoTunnel, detail: bool = False, indent: int = 0
) -> None:
    print_key_value_oneline("type:", info["kind"], indent=indent)
    print_key_value_oneline("protocol:", info["proto"], indent=indent)
    print_key_value_oneline("remote:", info["remote"], indent=indent)
    print_key_value_oneline("local:", info["local"], indent=indent)
    print_key_value_oneline("TTL:", info["ttl"], indent=indent)
    print_key_value_oneline("Path MTU Discovery:", info["pmtudisc"], indent=indent)
