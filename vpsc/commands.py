"""
VPSC のコマンド一覧です
"""

from time import sleep

import click
from pydantic import BaseModel

from .models.custom import (
    UpdateServer,
    UpdateHost,
    UpdateNfsServer,
    UpdateNfsServerIpv4,
    UpdateApiKey,
    CreateApiKey,
    CreateServerMonitoring,
    UpdateServerMonitoring,
    UpdateKeymap,
    MountDisc,
)
from .exceptions import exception_handler, APIException
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


@vpsc.group()
def apikey():
    """
    APIキーのリソースに対する操作
    """


@vpsc.group()
def monitoring():
    """
    サーバー監視リソースに対する操作
    """


@vpsc.group(
    [
        "disc",
    ]
)
def disc():
    """
    ディスクリソースに対する操作
    """


@vpsc.group()
def keymap():
    """
    キーマップリソースに対する操作
    """


@vpsc.group()
def zone():
    """
    ゾーンリソースに対する操作
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
@click.option(
    "--type", "-t", "type_", help="設定タイプ", required=True, type=click.Choice(["ipv4", "ipv6"], case_sensitive=False)
)
@click.option("--hostname", "-h", help="ホスト名", required=True, type=str)
def update_server_ptr_record(server_id, type_, hostname):
    """サーバーの逆引きホスト名を設定"""
    data = UpdateHost(hostname=hostname)
    if type_ == "ipv4":
        client.update_server_ipv4_ptr(server_id=server_id, data=data)
    elif type_ == "ipv6":
        client.update_server_ipv6_ptr(server_id=server_id, data=data)
    _print(client.get_server(server_id=server_id))


@click.command(name="limitation")
@click.option("--server-id", "-id", help="サーバーID", required=True, type=int)
def get_server_limitation(server_id):
    """サーバーの電源状態を取得"""
    _print(client.get_server_limitation(server_id=server_id))


@click.command(name="list")
@click.option("--nfs-server-id", "-id", help="NFSサーバーID", required=False, type=int)
def get_nfs_servers(nfs_server_id):
    """NFSサーバー情報の取得"""
    if nfs_server_id is not None:
        _print(client.get_nfs_server(nfs_server_id=nfs_server_id))
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


@click.command(name="list")
@click.option("--key-id", "-id", help="APIキーID", required=False, type=int)
def get_api_keys(key_id):
    """APIキー情報の取得"""
    if key_id is not None:
        _print(client.get_api_key(key_id=key_id))
    else:
        for item in client.get_api_keys():
            _print(item)


@click.command(name="create")
@click.option("--name", "-n", help="名前", required=False, type=str, default="")
@click.option("--role-id", "-rid", help="ロールID", required=True, type=int)
def create_api_key(name, role_id):
    data = CreateApiKey(name=name, role=role_id)
    res = client.create_api_key(data=data)
    _print(res)


@click.command(name="update")
@click.option("--key-id", "-id", help="APIキーID", required=True, type=int)
@click.option("--name", "-n", help="名前", required=False, type=str, default="")
@click.option("--role-id", "-rid", help="ロールID", required=True, type=int)
def update_api_key(key_id, name, role_id):
    data = UpdateApiKey(name=name, role=role_id)
    res = client.update_api_key(key_id=key_id, data=data)
    _print(res)


@click.command(name="delete")
@click.option("--key-id", "-id", help="APIキーID", required=True, type=int)
def delete_api_key(key_id):
    client.delete_api_key(key_id=key_id)


@click.command(name="list")
@click.option("--server-id", "-sid", help="サーバーID", required=True, type=int)
@click.option("--monitoring-id", "-id", help="監視ID", required=False, type=int)
def get_server_monitorings(server_id, monitoring_id):
    """サーバー監視情報の取得"""
    if monitoring_id is not None:
        _print(client.get_server_monitoring(monitoring_id=monitoring_id))
    else:
        for item in client.get_server_monitorings(server_id):
            _print(item)


@click.command(name="create")
@click.option("--server-id", "-sid", help="サーバーID", required=True, type=int)
@click.option("--name", "-n", help="名前", required=True, type=str)
@click.option("--description", "-d", help="説明", required=False, type=str, default="")
@click.option("--resource-id", "-rid", help="監視リソースID", required=True, type=str)
@click.option("--settings", "-s", help="設定情報(JSON形式)", required=True, type=str)
def create_server_monitoring(server_id, name, description, resource_id, settings):
    """サーバー監視の作成"""
    import json

    settings_data = json.loads(settings)
    data = CreateServerMonitoring(
        name=name,
        description=description,
        monitoring_resource_id=resource_id,
        settings=settings_data,
    )
    res = client.create_server_monitoring(server_id=server_id, data=data)
    _print(res)


@click.command(name="update")
@click.option("--server-id", "-sid", help="サーバーID", required=True, type=int)
@click.option("--monitoring-id", "-id", help="監視ID", required=True, type=int)
@click.option("--name", "-n", help="名前", required=True, type=str)
@click.option("--description", "-d", help="説明", required=False, type=str, default="")
@click.option("--settings", "-s", help="設定情報(JSON形式)", required=True, type=str)
def update_server_monitoring(server_id, monitoring_id, name, description, settings):
    """サーバー監視の更新"""
    import json

    settings_data = json.loads(settings)
    data = UpdateServerMonitoring(name=name, description=description, settings=settings_data)
    res = client.update_server_monitoring(server_id=server_id, monitoring_id=monitoring_id, data=data)
    _print(res)


@click.command(name="delete")
@click.option("--server-id", "-sid", help="サーバーID", required=True, type=int)
@click.option("--monitoring-id", "-id", help="監視ID", required=True, type=int)
def delete_server_monitoring(server_id, monitoring_id):
    """サーバー監視の削除"""
    client.delete_server_monitoring(server_id=server_id, monitoring_id=monitoring_id)


@click.command(name="health")
@click.option("--server-id", "-sid", help="サーバーID", required=True, type=int)
@click.option("--monitoring-id", "-id", help="監視ID", required=True, type=int)
def get_server_monitoring_health(server_id, monitoring_id):
    """サーバー監視の健全性を取得"""
    _print(client.get_server_monitoring_health(server_id=server_id, monitoring_id=monitoring_id))


@click.command(name="list")
def get_discs():
    """ディスク一覧の取得"""
    for item in client.get_discs():
        _print(item)


@click.command(name="mount")
@click.option("--server-id", "-sid", help="サーバーID", required=True, type=int)
@click.option("--disc-id", "-did", help="ディスクID", required=True, type=int)
def mount_disc(server_id, disc_id):
    """サーバーにディスクをマウント"""
    data = MountDisc(disc_id=disc_id)
    client.mount_disc(server_id=server_id, data=data)


@click.command(name="storage-info")
@click.option("--nfs-server-id", "-id", help="NFSサーバーID", required=True, type=int)
def get_nfs_storage_info(nfs_server_id):
    """NFSサーバーのストレージ情報を取得"""
    _print(client.get_nfs_storage_info(nfs_server_id=nfs_server_id))


@click.command(name="get")
@click.option("--server-id", "-id", help="サーバーID", required=True, type=int)
def get_server_vnc_console_keymap(server_id):
    """サーバーのVNCコンソールのキーマップを取得"""
    _print(client.get_server_vnc_console_keymap(server_id=server_id))


@click.command(name="update")
@click.option("--server-id", "-id", help="サーバーID", required=True, type=int)
@click.option("--layout", "-l", help="キー配列", required=True, type=click.Choice(["ja", "en-us"], case_sensitive=False))
def update_server_vnc_console_keymap(server_id, layout):
    """サーバーのVNCコンソールのキーマップを更新"""
    data = UpdateKeymap(layout=layout)
    res = client.update_server_vnc_console_keymap(server_id=server_id, data=data)
    _print(res)


@click.command(name="list")
def get_zones():
    """ゾーン一覧の取得"""
    for item in client.get_zones():
        _print(item)


# server commands
server.add_command(get_servers)
server.add_command(update_server)
server.add_command(get_server_power_status)
server.add_command(power_on_server)
server.add_command(shutdown_server)
server.add_command(update_server_ptr_record)
server.add_command(get_server_limitation)

# nfs server commands
nfs_server.add_command(get_nfs_servers)
nfs_server.add_command(update_nfs_server)
nfs_server.add_command(update_nfs_server_ipv4)
nfs_server.add_command(get_nfs_server_power_status)
nfs_server.add_command(get_nfs_storage_info)

# TODO: switch

# api key
apikey.add_command(get_api_keys)
apikey.add_command(create_api_key)
apikey.add_command(update_api_key)
apikey.add_command(delete_api_key)

# monitoring
monitoring.add_command(get_server_monitorings)
monitoring.add_command(create_server_monitoring)
monitoring.add_command(update_server_monitoring)
monitoring.add_command(delete_server_monitoring)
monitoring.add_command(get_server_monitoring_health)

# disc
disc.add_command(get_discs)
disc.add_command(mount_disc)

# keymap
keymap.add_command(get_server_vnc_console_keymap)
keymap.add_command(update_server_vnc_console_keymap)

# zone
zone.add_command(get_zones)


def entry_point():
    try:
        vpsc()
    except APIException as e:
        exception_handler(e)
    except Exception as e:
        click.echo(e)
