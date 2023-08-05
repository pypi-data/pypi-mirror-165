from netviewer.model.link_info_veth import LinkInfoVeth
from netviewer.view.console import print_key_oneline
from netviewer.view.render.link_info_bridge_slave import bridge_slave_link_info_render


def veth_link_info_render(
    info: LinkInfoVeth, detail: bool = False, indent: int = 0
) -> None:
    print_key_oneline("veth:", indent=indent)
    bridge_slave_link_info_render(info["slave"], indent=indent + 1)
