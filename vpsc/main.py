from pprint import pprint

import click

from .client import APIConfig, Client


@click.group()
def entrypoint():
    pass


@click.command
@click.option("--server_id", "-id", required=False, type=int)
def servers(server_id):
    client = Client(config=APIConfig())
    if server_id is not None:
        pprint(client.get_server(server_id=server_id).model_dump())
    else:
        for item in client.get_servers():
            pprint(item.model_dump())


entrypoint.add_command(servers, name="servers")
