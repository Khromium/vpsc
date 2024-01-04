"""
VPSC のコマンド一覧です
"""

from pprint import pprint
from time import sleep

import click

from .models import UpdateServer
from .client import APIConfig, Client


@click.group()
def vpsc():
    """
    VPSC コマンドグループです。

    vpsc 以下にservers 等のコマンドで更新取得を行います。
    """
    global client
    client = Client(config=APIConfig())


@click.command()
@click.option("--server_id", "-id", help="サーバーID", required=False, type=int)
def servers(server_id):
    """サーバー情報の取得"""
    if server_id is not None:
        pprint(client.get_server(server_id=server_id).model_dump())
    else:
        for item in client.get_servers():
            pprint(item.model_dump())


@click.command()
@click.option("--server_id", "-id", help="サーバーID", required=True, type=int)
@click.option("--name", "-n", help="名前", required=False, type=str, default="")
@click.option("--description", "-d", help="説明", required=False, type=str, default="")
def server_update(server_id, name, description):
    """サーバー情報更新"""
    data = UpdateServer(name=name, description=description)
    client.update_server(server_id=server_id, data=data)
    pprint(client.get_server(server_id=server_id).model_dump())


@click.command()
@click.option("--server_id", "-id", help="サーバーID", required=True, type=int)
def server_power_status(server_id):
    """サーバーの電源状態を取得"""
    pprint(client.get_server_power_status(server_id=server_id).model_dump())


@click.command()
@click.option("--server_id", "-id", help="サーバーID", required=True, type=int)
def server_power_on(server_id):
    """サーバーを起動"""
    client.power_on_server(server_id=server_id)
    sleep(5)
    pprint(client.get_server_power_status(server_id=server_id).model_dump())


@click.command()
@click.option("--server_id", "-id", help="サーバーID", required=True, type=int)
@click.option("--force", "-f", help="強制的にシャットダウン", required=False, type=bool, default=False, is_flag=True)
def server_shutdown(server_id, force):
    """サーバーをシャットダウン"""
    client.shutdown_server(server_id=server_id, force=force)
    sleep(5)
    pprint(client.get_server_power_status(server_id=server_id).model_dump())


vpsc.add_command(servers, name="servers")
vpsc.add_command(server_update, name="server-update")
vpsc.add_command(server_power_status, name="server-power-status")
vpsc.add_command(server_power_on, name="server-power-on")
vpsc.add_command(server_shutdown, name="server-shutdown")
