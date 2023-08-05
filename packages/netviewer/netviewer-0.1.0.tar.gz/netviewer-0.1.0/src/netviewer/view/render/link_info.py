from netviewer.model.link_info import LinkInfo
from netviewer.model.link_info_bond import LinkInfoBond
from netviewer.model.link_info_bridge import LinkInfoBridge
from netviewer.model.link_info_tunnel import LinkInfoTunnel
from netviewer.model.link_info_veth import LinkInfoVeth
from netviewer.view.console import print_key_oneline
from netviewer.view.render.link_info_bond import bond_link_info_render
from netviewer.view.render.link_info_bridge import bridge_link_info_render
from netviewer.view.render.link_info_tunnel import tunnel_link_info_render
from netviewer.view.render.link_info_veth import veth_link_info_render


def link_info_render(link_info: LinkInfo, indent: int = 0):
    link_info_type: str = link_info["kind"]
    print_key_oneline("link info:", indent=indent + 1)
    if link_info_type == "bridge":
        bridge_link_info: LinkInfoBridge = link_info.get("info", None)  # type: ignore
        bridge_link_info_render(bridge_link_info, indent=indent + 2)
    elif link_info_type == "veth":
        veth_link_info: LinkInfoVeth = link_info.get("info", None)  # type: ignore
        veth_link_info_render(veth_link_info, indent=indent + 2)
    elif link_info_type == "bond":
        bond_link_info: LinkInfoBond = link_info.get("info", None)  # type: ignore
        bond_link_info_render(bond_link_info, indent=indent + 2)
    elif link_info_type in ["sit", "ipip"]:
        tunnel_link_info: LinkInfoTunnel = link_info.get("info", None)  # type: ignore
        tunnel_link_info_render(tunnel_link_info, indent=indent + 2)
