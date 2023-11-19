from pprint import pprint

import click

from .client import APIConfig, Client


@click.group()
def entrypoint():
    pass


@click.command
@click.option("--server_id", "-sid", required=False, type=int)
def get_servers(server_id):
    client = Client(config=APIConfig())
    if server_id is not None:
        client.get_server(server_id)
    for item in client.get_servers():
        pprint(item.model_dump())


entrypoint.add_command(get_servers, name="servers")
