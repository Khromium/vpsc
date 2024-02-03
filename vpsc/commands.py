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
    VPSC コマンドです。

    操作するリソースを指定して実行してください
    """
    global client
    client = Client(config=APIConfig())


@vpsc.group()
def server():
    """
    サーバーリソースに対する操作
    """
    pass


@vpsc.group()
def nfs_server():
    """
    NFSサーバーのリソースに対する操作
    """


@click.command(name="list")
@click.option("--server_id", "-id", help="サーバーID", required=False, type=int)
def get_servers(server_id):
    """サーバー情報の取得"""
    if server_id is not None:
        pprint(client.get_server(server_id=server_id).model_dump())
    else:
        for item in client.get_servers():
            pprint(item.model_dump())


@click.command(name="update")
@click.option("--server_id", "-id", help="サーバーID", required=True, type=int)
@click.option("--name", "-n", help="名前", required=False, type=str, default="")
@click.option("--description", "-d", help="説明", required=False, type=str, default="")
def update_server(server_id, name, description):
    """サーバー情報更新"""
    data = UpdateServer(name=name, description=description)
    res = client.update_server(server_id=server_id, data=data)
    pprint(res.model_dump())


@click.command(name="power_status")
@click.option("--server_id", "-id", help="サーバーID", required=True, type=int)
def get_server_power_status(server_id):
    """サーバーの電源状態を取得"""
    pprint(client.get_server_power_status(server_id=server_id).model_dump())


@click.command(name="power_on")
@click.option("--server_id", "-id", help="サーバーID", required=True, type=int)
def power_on_server(server_id):
    """サーバーを起動"""
    client.power_on_server(server_id=server_id)
    sleep(5)
    pprint(client.get_server_power_status(server_id=server_id).model_dump())


@click.command(name="shutdown")
@click.option("--server_id", "-id", help="サーバーID", required=True, type=int)
@click.option("--force", "-f", help="強制的にシャットダウン", required=False, type=bool, default=False, is_flag=True)
def shutdown_server(server_id, force):
    """サーバーをシャットダウン"""
    client.shutdown_server(server_id=server_id, force=force)
    sleep(5)
    pprint(client.get_server_power_status(server_id=server_id).model_dump())


vpsc.add_command(servers, name="servers")
vpsc.add_command(server_update, name="server-update")
vpsc.add_command(server_power_status, name="server-power-status")
vpsc.add_command(server_power_on, name="server-power-on")
vpsc.add_command(server_shutdown, name="server-shutdown")
vpsc.add_command(update_server, name="update-server")
vpsc.add_command(power_status_server, name="power-status-server")
vpsc.add_command(power_on_server, name="power-on-server")
vpsc.add_command(shutdown_server, name="shutdown-server")
vpsc.add_command(update_server_ptr_record, name="update-server-ptr-record")
# server commands
server.add_command(get_servers)
server.add_command(update_server)
server.add_command(get_server_power_status)
server.add_command(power_on_server)
server.add_command(shutdown_server)

