#!/usr/bin/env python3

import os, sys
import requests
from dotenv import load_dotenv
from rich import print
from rich.table import Table
import urllib3
import typer
from typing import Literal, List, Union, Optional
from types import SimpleNamespace
from typing_extensions import Annotated

load_dotenv()

__version__ = "1.0.0"

app = typer.Typer(no_args_is_help=True)
host_app = typer.Typer()
app.add_typer(host_app, name="host", help="Configure host objects", no_args_is_help=True)
group_app = typer.Typer()
app.add_typer(group_app, name="group", help="Configure host group objects", no_args_is_help=True)
group_update_app = typer.Typer()
group_app.add_typer(group_update_app, name="update", help="Update a host group", no_args_is_help=True)


def do_http(ctx: typer.Context, path: str, method: Literal["get", "post", "put", "delete"]="get", data=None):

    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer " + ctx.obj.apikey
    }

    try:
        if method == "get":
            r = requests.get(ctx.obj.smcurl + path, verify=ctx.obj.verify, headers=headers)
        elif method == "post" or method == "put":
            headers["Content-Type"] = "application/json"

            r = requests.request(method=method, url=ctx.obj.smcurl + path, verify=ctx.obj.verify, headers=headers, json=data)
        elif method == "delete":
            r = requests.delete(ctx.obj.smcurl + path, verify=ctx.obj.verify, headers=headers)
    except requests.exceptions.SSLError as e:
        print("[red]Error: SSL connection failed[/red]")
        print(str(e))
        print("Try --unsecure or --cacert options.")
        sys.exit(1)

    if r.status_code != 200:
        print("[red]Error: api call failed[/red] ")
        print(f"{method.upper()} {path}")
        print(f"status code: {r.status_code}")
        print(r.text)
        sys.exit(1)

    return r.json()

def version_callback(version: bool):
    if version:
        print(f"SMC object CLI version: {__version__}")
        raise typer.Exit()


@app.callback()
def context(ctx: typer.Context,
            apikey: Annotated[str, typer.Option(envvar="API_KEY", help="SMC api key")],
            smcurl: Annotated[str, typer.Option(envvar="SMC_URL", help="SMC url")],
            version: Annotated[Optional[bool], typer.Option("--version", is_eager=True, help="Show version", callback=version_callback)]=False,
            unsecure: Annotated[bool, typer.Option(envvar="UNSECURE", help="Disable TLS check")]=False,
            cacert: Annotated[Union[str,None], typer.Option(envvar="CACERT", help="Path to the TLS authority file")]=None):

    if cacert:
        ctx.obj = SimpleNamespace(apikey=apikey, smcurl=smcurl, verify=cacert)
    else:
        ctx.obj = SimpleNamespace(apikey=apikey, smcurl=smcurl, verify=not unsecure)

    if unsecure:
        urllib3.disable_warnings()


@host_app.command("list", help="List host objects")
def host_list(ctx: typer.Context):

    data = do_http(ctx, "/papi/v1/objects")

    table = Table()
    table.add_column("name")
    table.add_column("ip")
    table.add_column("comment")

    for entry in data["result"]["hosts"]:
        ip = ""
        if "ip" in entry:
            ip = entry["ip"]
        comment = ""
        if "comment" in entry:
            comment = entry["comment"]
        table.add_row(entry["name"], ip, comment)

    print(table)


@group_app.command("list", help="List host groups")
def group_list(ctx: typer.Context, members: Annotated[bool, typer.Option(help="List group members")]=False):

    data = do_http(ctx, "/papi/v1/objects")

    table = Table()
    table.add_column("name")
    if members:
        table.add_column("members")
    else:
        table.add_column("members count")
    table.add_column("Comment")

    for entry in data["result"]["groups"]:
        if members:
            members_list = []
            for e in entry["elements"]:
                members_list.append(e["name"])
            members_str = ", ".join(members_list)
        else:
            members_str = str(len(entry["elements"]))
        comment = ""
        if "comment" in entry:
            comment = entry["comment"]
        table.add_row(entry["name"], members_str, comment)

    print(table)


@host_app.command("create", help="Create a new host object")
def host_create(ctx: typer.Context, name: str, ip: str, comment: str="", resolve: Literal["dynamic", "static"]="static"):

    do_http(ctx, method="post", path="/papi/v1/objects/hosts",
            data= {
                "name": name,
                "ip": ip,
                "resolve": resolve,
                "comment": comment
            }
    )

    print(f"[green]Host {name} created[/green]")


@group_app.command("create", help="Create a new host group")
def create_group(ctx: typer.Context, name: str, elements: List[str], comment: str=""):

    element_list = []
    for element in elements:
        element_list.append({"name": element})

    do_http(ctx, method="post", path="/papi/v1/objects/groups",
            data= {
                "name": name,
                "elements": element_list,
                "comment": comment
            }
    )

    print(f"[green]Group {name} created[/green]")


@group_update_app.command("add", help="Add host(s) to an host group")
def group_add(ctx: typer.Context, group: str, elements: List[str]):
    # get group members

    data = do_http(ctx, "/papi/v1/objects")
    g = next((item for item in data["result"]["groups"] if item["name"] == group), None)

    if not g:
        print(f"[red]Error:[/red] group {group} not found")
        sys.exit(1)

    content = []
    for m in g["elements"]:
        content.append({"name": m["name"]})

    # add new members
    for m in elements:
        if m not in content:
            content.append({"name": m})

    do_http(ctx, method="put", path=f"/papi/v1/objects/groups/{group}",
            data={
                "name": g["name"],
                "comment": g["comment"] if "comment" in g else "",
                "elements": content
            }
    )

    print(f"[green]Host {', '.join(elements)} added to group {group}[/green]")


@group_update_app.command("remove", help="Remove host(s) from an host group")
def group_remove(ctx: typer.Context, group: str, elements: List[str]):
    # get group members

    data = do_http(ctx, "/papi/v1/objects")
    g = next((item for item in data["result"]["groups"] if item["name"] == group), None)

    if not g:
        print(f"[red]Error:[/red] group {group} not found")
        sys.exit(1)

    # remove elements
    found = False
    content = []
    for e in g["elements"]:
        if e["name"] not in elements:
            content.append({"name": e["name"]})
        else:
            found = True

    if not found:
        print(f"[green]Host(s) {', '.join(elements)} not found in the group {group}, nothing to do.[/green]")
        sys.exit(0)

    do_http(ctx, method="put", path=f"/papi/v1/objects/groups/{group}",
            data={
                "name": g["name"],
                "comment": g["comment"] if "comment" in g else "",
                "elements": content
            }
    )

    print(f"[green]Host {', '.join(elements)} removed from group {group}[/green]")


@host_app.command("delete", help="Delete a host object")
def host_delete(ctx: typer.Context, name: str):

    do_http(ctx, method="delete", path=f"/papi/v1/objects/hosts/{name}")

    print(f"[green]Host {name} deleted[/green]")


@group_app.command("delete", help="Delete a host group")
def group_delete(ctx: typer.Context, name: str):

    do_http(ctx, method="delete", path=f"/papi/v1/objects/groups/{name}")

    print(f"[green]Group {name} deleted[/green]")


if __name__ == "__main__":
    app()
