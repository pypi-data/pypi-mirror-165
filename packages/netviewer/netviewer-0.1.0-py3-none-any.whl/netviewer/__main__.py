import json
import os
from typing import Any

import click

import netviewer.ip
from netviewer.config import config_load, maybe, _config  # type: ignore
from netviewer.context import _console  # type: ignore
from netviewer.view import console, rich_init
from netviewer.view.render.bridge import (
    bridge_list_render,
    bridge_render,
    bridges_render,
)
from netviewer.view.render.interface import (
    interface_list_render,
    interface_render,
    interfaces_render,
)
from netviewer.view.render.link import link_list_render, link_render, links_render
from netviewer.view.render.route import route_list_render, route_render, routes_render


@click.group()
@click.pass_context
@click.option(
    "-d", "--detail", is_flag=True, default=False, help="Show detailed information"
)
@click.option(
    "-i",
    "--input",
    type=click.File(),
    help="A json format file containing network information",
)
@click.option(
    "--save-html",
    type=click.Path(),
    help="Filename to save HTML to.",
    metavar="HTMLFILE",
)
@click.option(
    "--save-svg", type=click.Path(), help="Filename to save SVG to.", metavar="SVGFILE"
)
@click.option(
    "--width",
    default=100,
    help="Number of columns to use when saving HTML/SVG",
    show_default=True,
)
def run(
    ctx: click.core.Context,
    detail: bool,
    input: click.File,
    save_html: click.Path | None,
    save_svg: click.Path | None,
    width: int,
):
    cfg = config_load("netviewer.toml")
    cfg["detail"] = detail

    if save_svg is None:
        output_svg = maybe(cfg, "output.svg", "")  # type: ignore
    else:
        output_svg = str(save_svg)

    if save_html is None:
        output_html = maybe(cfg, "output.html", "")  # type: ignore
    else:
        output_html = str(save_html)

    cfg["output_svg"] = str(output_svg)
    cfg["output_html"] = str(output_html)
    _config.set(cfg)

    # Initialize rich
    if output_html or output_svg:
        record = True
        rich_init(
            record=record,
            file=open(os.devnull, "wt", encoding="utf-8"),
            color_system="truecolor",
            width=width,
        )
    else:
        record = False
        rich_init(record=False)

    ctx.ensure_object(dict)
    if not input:
        netdata = netviewer.ip.load()
    else:
        netdata = json.load(input)  # type: ignore
    ctx.obj["netinfo"] = netviewer.ip.parse(netdata)


@run.command(short_help="Print information about a specific interfaces")
@click.pass_context
@click.argument("interfaces", required=False, nargs=-1)
def interface(ctx: click.core.Context, interfaces: tuple[str, ...]):
    """Print information about a specific interfaces or all interfaces if none specified.

    e.g. 'netviewer interface eth0' prints information about the eth0 interface
    and 'netviewer interface' prints information about all interfaces
    """
    d = _config.get()["detail"]
    if len(interfaces) == 0:
        interfaces_render(ctx.obj["netinfo"]["address"], detail=d)
    else:
        for i in interfaces:
            if i in ctx.obj["netinfo"]["address"]:
                interface_render(ctx.obj["netinfo"]["address"][i], detail=d)
            else:
                console.print(f"Interface {i} not defined", color="warning")


@run.command()
@click.pass_context
def interfaces(ctx: click.core.Context):
    """Print a list of available interfaces"""
    if len(ctx.obj["netinfo"]["address"]) == 0:
        console.print("No interfaces defined", color="warning")
    else:
        interface_list_render(ctx.obj["netinfo"]["address"])


@run.command()
@click.pass_context
@click.argument("bridges", required=False, nargs=-1)
def bridge(ctx: click.core.Context, bridges: tuple[str, ...]):
    """Print information about network bridges"""
    d = _config.get()["detail"]
    if len(ctx.obj["netinfo"]["bridge"]) > 0:
        if len(bridges) == 0:
            bridges_render(ctx.obj["netinfo"]["bridge"], detail=d)
        else:
            for b in bridges:
                if b in ctx.obj["netinfo"]["bridge"]:
                    bridge_render(ctx.obj["netinfo"]["bridge"][b], detail=d)
                else:
                    console.print(f"Bridge {b} not defined", color="warning")
    else:
        console.print("No bridges defined", color="warning")


@run.command()
@click.pass_context
def bridges(ctx: click.core.Context):
    """Print a list of available interfaces"""
    if len(ctx.obj["netinfo"]["bridge"]) == 0:
        console.print("No bridges defined", color="warning")
    else:
        bridge_list_render(ctx.obj["netinfo"]["bridge"])


@run.command()
@click.pass_context
@click.argument("routes", required=False, nargs=-1)
def route(ctx: click.core.Context, routes: tuple[str, ...]):
    """Print information about network routes"""
    d = _config.get()["detail"]
    if len(ctx.obj["netinfo"]["route"]) > 0:
        if len(routes) == 0:
            routes_render(ctx.obj["netinfo"]["route"], detail=d)
        else:
            for r in routes:
                if r in ctx.obj["netinfo"]["route"].keys():
                    route_render(ctx.obj["netinfo"]["route"][r], detail=d)
                else:
                    console.print(f"Route {r} not defined", color="warning")


@run.command()
@click.pass_context
def routes(ctx: click.core.Context):
    """Print a list of available routes"""
    if len(ctx.obj["netinfo"]["route"]) == 0:
        console.print("No routes defined", color="warning")
    else:
        route_list_render(ctx.obj["netinfo"]["route"])


@run.command()
@click.pass_context
@click.argument("link", required=False)
def link(ctx: click.core.Context, link: str | None):
    """Print information about network links"""
    d = _config.get()["detail"]
    if link is None:
        links_render(ctx.obj["netinfo"]["link"], detail=d)
    else:
        if link in ctx.obj["netinfo"]["link"]:
            link_render(ctx.obj["netinfo"]["link"][link], detail=d)
        else:
            console.print(f"Link {link} not defined", color="warning")


@run.command()
@click.pass_context
def links(ctx: click.core.Context):
    """Print a list of available links"""
    if len(ctx.obj["netinfo"]["link"]) == 0:
        console.print("No links defined", color="warning")
    else:
        link_list_render(ctx.obj["netinfo"]["link"])


@run.command()
@click.argument("filename", type=click.Path())
def dump(filename: click.Path):
    """Dumps the network information as a json file"""
    with open(str(filename), "w") as fp:
        netinfo = netviewer.ip.load()
        json.dump(netinfo, fp)


@run.result_callback()
def teardown(result: Any, **kwargs: dict[str, Any]):
    """Output to SVG/HTML after commands run"""
    cfg = _config.get()
    output_svg = cfg["output_svg"]
    output_html = cfg["output_html"]

    con = _console.get()
    if con.record:
        clear = output_svg == ""
        con = _console.get()
        if output_svg:
            con.save_svg(output_svg, clear=clear)
        if output_html:
            con.save_html(output_html)


run()
