"""
VPSC のコマンド一覧です
"""

from time import sleep

import click
from pydantic import BaseModel

from .exceptions import exception_handler, APIException
from .models import UpdateServer, UpdateHost, UpdateNfsServer, UpdateNfsServerIpv4
from .client import APIConfig, Client


def _print(data: BaseModel):
    click.echo(data.model_dump_json(exclude_unset=True, indent=2))


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
@click.option("--server-id", "-id", help="サーバーID", required=False, type=int)
def get_servers(server_id):
    """サーバー情報の取得"""
    if server_id is not None:
        _print(client.get_server(server_id=server_id))
    else:
        for item in client.get_servers():
            _print(item)


@click.command(name="update")
@click.option("--server-id", "-id", help="サーバーID", required=True, type=int)
@click.option("--name", "-n", help="名前", required=False, type=str, default="")
@click.option("--description", "-d", help="説明", required=False, type=str, default="")
def update_server(server_id, name, description):
    """サーバー情報更新"""
    data = UpdateServer(name=name, description=description)
    res = client.update_server(server_id=server_id, data=data)
    _print(res)


@click.command(name="power-status")
@click.option("--server-id", "-id", help="サーバーID", required=True, type=int)
def get_server_power_status(server_id):
    """サーバーの電源状態を取得"""
    _print(client.get_server_power_status(server_id=server_id))


@click.command(name="power-on")
@click.option("--server-id", "-id", help="サーバーID", required=True, type=int)
def power_on_server(server_id):
    """サーバーを起動"""
    client.power_on_server(server_id=server_id)
    sleep(5)
    _print(client.get_server_power_status(server_id=server_id))


@click.command(name="shutdown")
@click.option("--server-id", "-id", help="サーバーID", required=True, type=int)
@click.option("--force", "-f", help="強制的にシャットダウン", required=False, type=bool, default=False, is_flag=True)
def shutdown_server(server_id, force):
    """サーバーをシャットダウン"""
    client.shutdown_server(server_id=server_id, force=force)
    sleep(5)
    _print(client.get_server_power_status(server_id=server_id))


@click.command(name="ptr-record")
@click.option("--server-id", "-id", help="サーバーID", required=True, type=int)
@click.option("--type", "-t", help="設定タイプ", required=True, type=click.Choice(["ipv4", "ipv6"], case_sensitive=True))
@click.option("--hostname", "-h", help="ホスト名", required=True, type=str)
def update_server_ptr_record(server_id, _type, hostname):
    """サーバーの逆引きホスト名を設定"""
    data = UpdateHost(hostname=hostname)
    if _type == "ipv4":
        client.update_server_ipv4_ptr(server_id=server_id, data=data)
    elif _type == "ipv6":
        client.update_server_ipv6_ptr(server_id=server_id, data=data)
    _print(client.get_server(server_id=server_id))


@click.command(name="list")
@click.option("--nfs-server-id", "-id", help="NFSサーバーID", required=False, type=int)
def get_nfs_servers(server_id):
    """NFSサーバー情報の取得"""
    if server_id is not None:
        _print(client.get_nfs_server(nfs_server_id=server_id))
    else:
        for item in client.get_nfs_servers():
            _print(item)


@click.command(name="update")
@click.option("--nfs-server-id", "-id", help="NFSサーバーID", required=False, type=int)
@click.option("--name", "-n", help="名前", required=False, type=str, default="")
@click.option("--description", "-d", help="説明", required=False, type=str, default="")
def update_nfs_server(nfs_server_id, name, description):
    """サーバー情報更新"""
    data = UpdateNfsServer(name=name, description=description)
    res = client.update_nfs_server(nfs_server_id=nfs_server_id, data=data)
    _print(res)


@click.command(name="update-ipv4")
@click.option("--nfs-server-id", "-id", help="NFSサーバーID", required=False, type=int)
@click.option("--hostname", "-h", help="ホスト名", required=True, type=str)
def update_nfs_server_ipv4(nfs_server_id, address, netmask):
    """NFSサーバーのipv4を設定"""
    data = UpdateNfsServerIpv4(address=address, netmask=netmask)
    client.update_nfs_server_ipv4(nfs_server_id=nfs_server_id, data=data)
    _print(client.get_nfs_server(nfs_server_id=nfs_server_id))


@click.command(name="power-status")
@click.option("--nfs-server-id", "-id", help="サーバーID", required=True, type=int)
def get_nfs_server_power_status(nfs_server_id):
    """NFSサーバーの電源状態を取得"""
    _print(client.get_nfs_server_power_status(nfs_server_id=nfs_server_id))


# server commands
server.add_command(get_servers)
server.add_command(update_server)
server.add_command(get_server_power_status)
server.add_command(power_on_server)
server.add_command(shutdown_server)
server.add_command(update_server_ptr_record)

# nfs server commands
nfs_server.add_command(get_nfs_servers)
nfs_server.add_command(update_nfs_server)
nfs_server.add_command(update_nfs_server_ipv4)
nfs_server.add_command(get_nfs_server_power_status)


def entry_point():
    try:
        vpsc()
    except APIException as e:
        exception_handler(e)
    except Exception as e:
        click.echo(e)
