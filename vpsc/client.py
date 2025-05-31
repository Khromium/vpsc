from types import MappingProxyType
from typing import Optional, Iterable, List

from pydantic_settings import BaseSettings, SettingsConfigDict

from .models.custom import (
    server_sort_query,
    UpdateServer,
    ShutdownServer,
    UpdateHost,
    UpdateNfsServer,
    UpdateNfsServerIpv4,
    CreateSwitch,
    UpdateSwitch,
    Ptr,
    UpdateApiKey,
    CreateRole,
    UpdateRole,
    CreateApiKey,
    CreateServerMonitoring,
    UpdateServerMonitoring,
    UpdateKeymap,
    MountDisc,
)
from .models.generated import (
    Server,
    ServerPowerStatus,
    NfsServer,
    NfsServerPowerStatus,
    Switch,
    Limitation,
    ApiKey,
    Role,
    Permission,
    ServerMonitoring,
    ServerMonitoringHealth,
    Disc,
    NfsStorageInfo,
    Keymap,
    Zone3,
)
from .api_request import APIRequest


class APIConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file="~/.vpsc", env_file_encoding="utf-8", env_prefix="vps_")
    host: str = "https://secure.sakura.ad.jp/vps/api/v7"
    api_key: str


class Client:
    def __init__(self, config: APIConfig):
        self.config = config
        self.header = MappingProxyType({"Authorization": f"Bearer {self.config.api_key}"})
        self.client = APIRequest(config=self.config, header=self.header)

    def get_servers(self, sort: Optional[server_sort_query] = None) -> Iterable[Server]:
        """
        サーバー一覧を取得する

        :param sort: ソート情報
        :return:
        """
        return self.client.request(
            endpoint="/servers",
            method="get",
            response_obj=Server,
        )

    def get_server(self, server_id: int) -> Server:
        """
        サーバー情報を取得する

        :param server_id: サーバーID
        :return:
        """
        return self.client.request(
            endpoint=f"/servers/{server_id}",
            method="get",
            response_obj=Server,
        )

    def update_server(self, server_id: int, data: UpdateServer) -> Server:
        """
        サーバー情報を更新する

        :param server_id: サーバーID
        :param data: 更新データ
        :return:
        """
        return self.client.request(
            endpoint=f"/servers/{server_id}",
            method="put",
            data=data,
            response_obj=Server,
        )

    def get_server_power_status(self, server_id: int) -> ServerPowerStatus:
        """
        サーバーの電源状態を取得する

        :param server_id:　サーバーID
        :return:
        """
        return self.client.request(
            endpoint=f"/servers/{server_id}/power-status",
            method="get",
            response_obj=ServerPowerStatus,
        )

    def power_on_server(self, server_id: int):
        """
        サーバーを起動する

        :param server_id: サーバーID
        :return:
        """
        return self.client.request(
            endpoint=f"/servers/{server_id}/power-on",
            method="post",
        )

    def shutdown_server(self, server_id: int, force: bool = False):
        """
        サーバーをシャットダウンする

        :param force: 強制停止を行うか
        :param server_id: サーバーID
        :return:
        """
        data = ShutdownServer(force=force)
        return self.client.request(
            endpoint=f"/servers/{server_id}/shutdown",
            method="post",
            data=data,
        )

    def force_force_reboot_server(self, server_id: int):
        """
        サーバーを強制再起動する

        :param server_id: サーバーID
        :return:
        """
        return self.client.request(
            endpoint=f"/servers/{server_id}/force-reboot",
            method="post",
        )

    def update_server_ipv4_ptr(self, server_id: int, data: UpdateHost):
        """
        サーバーのipv4の逆引きホスト名を設定する

        :param server_id: サーバーID
        :param data: 設定データ
        :return:
        """
        return self.client.request(
            endpoint=f"/servers/{server_id}/ipv4-ptr",
            method="put",
            data=data,
            response_obj=Ptr,
        )

    def update_server_ipv6_ptr(self, server_id: int, data: UpdateHost):
        """
        サーバーのipv6の逆引きホスト名を設定する

        :param server_id: サーバーID
        :param data: 設定データ
        :return:
        """
        return self.client.request(
            endpoint=f"/servers/{server_id}/ipv6-ptr",
            method="put",
            data=data,
            response_obj=Ptr,
        )

    def get_server_limitation(self, server_id: int) -> Limitation:
        """
        サーバーの制限情報を取得する

        :param server_id: サーバーID
        :return:
        """
        return self.client.request(
            endpoint=f"/servers/{server_id}/limitation",
            method="get",
            response_obj=Limitation,
        )

    def get_nfs_servers(self) -> Iterable[NfsServer]:
        """
        NFSサーバー情報一覧を取得する

        :return:
        """
        return self.client.request(
            endpoint=f"/nfs-servers",
            method="get",
            response_obj=NfsServer,
        )

    def get_nfs_server(self, nfs_server_id: int) -> NfsServer:
        """
        NFSサーバー情報を取得する


        :param nfs_server_id: NFSサーバーID
        :return:
        """
        return self.client.request(
            endpoint=f"/nfs-servers/{nfs_server_id}",
            method="get",
            response_obj=NfsServer,
        )

    def update_nfs_server(self, nfs_server_id: int, data: UpdateNfsServer):
        """
        NFSサーバー情報を更新する
        :param nfs_server_id:  NFSサーバーID
        :param data: 更新データ
        :return:
        """
        return self.client.request(
            endpoint=f"/nfs-servers/{nfs_server_id}",
            method="put",
            data=data,
            response_obj=NfsServer,
        )

    def update_nfs_server_ipv4(self, nfs_server_id: int, data: UpdateNfsServerIpv4):
        """
        NFSサーバーのipv4を設定する

        :param nfs_server_id: NFSサーバーID
        :param data: 設定情報
        :return:
        """
        return self.client.request(
            endpoint=f"/nfs-servers/{nfs_server_id}/ipv4",
            method="put",
            data=data,
        )

    def get_nfs_server_power_status(self, nfs_server_id: int) -> NfsServerPowerStatus:
        """
        NFSサーバーの電源状態を取得する

        :param nfs_server_id:
        :return:
        """
        return self.client.request(
            endpoint=f"/nfs-servers/{nfs_server_id}/power-status", method="get", response_obj=NfsServerPowerStatus
        )

    def create_switch(self, data: CreateSwitch) -> Switch:
        """
        スイッチを作成する

        :param data: 作成データ
        :return:
        """
        return self.client.request(
            endpoint=f"/switches",
            method="post",
            data=data,
            response_obj=Switch,
        )

    def get_switches(self) -> Iterable[Switch]:
        """
        スイッチ情報一覧を取得する

        :return:
        """
        return self.client.request(
            endpoint=f"/switches",
            method="get",
            response_obj=Switch,
        )

    def get_switch(self, switch_id: int) -> Switch:
        """
        スイッチ情報を取得する

        :param switch_id: スイッチID
        :return:
        """
        return self.client.request(
            endpoint=f"/switches/{switch_id}",
            method="get",
            response_obj=Switch,
        )

    def update_switch(self, switch_id: int, data: UpdateSwitch) -> Switch:
        """
        スイッチ情報を更新する

        :param switch_id: スイッチID
        :param data: 更新データ
        :return:
        """
        return self.client.request(
            endpoint=f"/switches/{switch_id}",
            method="put",
            data=data,
            response_obj=Switch,
        )

    def delete_switch(self, switch_id: int):
        """
        スイッチを削除する

        :param switch_id: スイッチID
        :return:
        """
        return self.client.request(
            endpoint=f"/switches/{switch_id}",
            method="delete",
        )

    def get_api_keys(self) -> Iterable[ApiKey]:
        """
        APIキーの一覧を取得する

        :return:
        """
        return self.client.request(
            endpoint=f"/api-keys",
            method="get",
            response_obj=ApiKey,
        )

    def get_api_key(self, key_id: int) -> ApiKey:
        """
        APIキーを取得する

        :param key_id:
        :return:
        """
        return self.client.request(
            endpoint=f"/api-keys/{key_id}",
            method="get",
            response_obj=ApiKey,
        )

    def create_api_key(self, data: CreateApiKey) -> ApiKey:
        """
        APIキーを作成する

        :param data:
        :return:
        """
        return self.client.request(
            endpoint=f"/api-keys",
            method="post",
            data=data,
            response_obj=ApiKey,
        )

    def update_api_key(self, key_id: int, data: UpdateApiKey) -> ApiKey:
        """
        APIキーを更新する

        :param key_id:
        :return:
        """
        return self.client.request(
            endpoint=f"/api-keys/{key_id}",
            method="put",
            data=data,
            response_obj=ApiKey,
        )

    def delete_api_key(self, key_id: int) -> ApiKey:
        """
        APIキーを削除する

        :param key_id:
        :return:
        """
        return self.client.request(
            endpoint=f"/api-keys/{key_id}",
            method="delete",
        )

    def rotate_api_key(self, key_id: int) -> ApiKey:
        """
        APIキーのトークンのローテーションを行う

        :param key_id:
        :return:
        """
        return self.client.request(
            endpoint=f"/api-keys/{key_id}",
            method="put",
            response_obj=ApiKey,
        )

    def create_role(self, data: CreateRole) -> Role:
        """
        ロールを作成する

        :return:
        """
        return self.client.request(
            endpoint=f"/roles",
            method="post",
            data=data,
            response_obj=Role,
        )

    def get_role(self, role_id: int) -> Role:
        """
        ロールを取得する

        :param role_id:
        :return:
        """
        return self.client.request(
            endpoint=f"/roles/{role_id}",
            method="get",
            response_obj=Role,
        )

    def update_role(self, role_id: int, data: UpdateRole) -> Role:
        """
        ロールを更新する

        :param role_id:
        :param data:
        :return:
        """
        return self.client.request(
            endpoint=f"/roles/{role_id}",
            method="put",
            data=data,
            response_obj=Role,
        )

    def delete_role(self, role_id: int) -> Role:
        """
        ロールを削除する

        :param role_id:
        :return:
        """
        return self.client.request(
            endpoint=f"/roles/{role_id}",
            method="delete",
        )

    def get_permissions(self) -> Iterable[Permission]:
        """
        権限の一覧を取得する

        :return:
        """
        return self.client.request(
            endpoint=f"/permissions",
            method="get",
            response_obj=Permission,
        )

    def get_server_monitorings(self, server_id: int) -> Iterable[ServerMonitoring]:
        """
        サーバー監視の一覧を取得する

        :return:
        """
        return self.client.request(
            endpoint=f"/servers/{server_id}/monitorings",
            method="get",
            response_obj=ServerMonitoring,
        )

    def get_server_monitoring(self, server_id: int, monitoring_id: int) -> ServerMonitoring:
        """
        サーバー監視を取得する

        :param monitoring_id: 監視ID
        :return:
        """
        return self.client.request(
            endpoint=f"/servers/{server_id}/monitorings/{monitoring_id}",
            method="get",
            response_obj=ServerMonitoring,
        )

    def create_server_monitoring(self, server_id: int, data: CreateServerMonitoring) -> ServerMonitoring:
        """
        サーバー監視を作成する

        :param data: 作成データ
        :return:
        """
        return self.client.request(
            endpoint=f"/servers/{server_id}/monitorings",
            method="post",
            data=data,
            response_obj=ServerMonitoring,
        )

    def update_server_monitoring(
        self, server_id: int, monitoring_id: int, data: UpdateServerMonitoring
    ) -> ServerMonitoring:
        """
        サーバー監視を更新する

        :param monitoring_id: 監視ID
        :param data: 更新データ
        :return:
        """
        return self.client.request(
            endpoint=f"/servers/{server_id}/monitorings/{monitoring_id}",
            method="put",
            data=data,
            response_obj=ServerMonitoring,
        )

    def delete_server_monitoring(self, server_id: int, monitoring_id: int):
        """
        サーバー監視を削除する

        :param monitoring_id: 監視ID
        :return:
        """
        return self.client.request(
            endpoint=f"/servers/{server_id}/monitorings/{monitoring_id}",
            method="delete",
        )

    def get_server_monitoring_health(self, server_id: int, monitoring_id: int) -> ServerMonitoringHealth:
        """
        サーバー監視の健全性を取得する

        :param monitoring_id: 監視ID
        :return:
        """
        return self.client.request(
            endpoint=f"/servers/{server_id}/monitorings/{monitoring_id}/health",
            method="get",
            response_obj=ServerMonitoringHealth,
        )

    def get_discs(self) -> Iterable[Disc]:
        """
        ディスク一覧を取得する

        :return:
        """
        return self.client.request(
            endpoint="/discs",
            method="get",
            response_obj=Disc,
        )

    def mount_disc(self, server_id: int, data: MountDisc):
        """
        サーバーにディスクをマウントする

        :param server_id: サーバーID
        :param data: マウントデータ
        :return:
        """
        return self.client.request(
            endpoint=f"/servers/{server_id}/mount-disc",
            method="post",
            data=data,
        )

    def get_nfs_storage_info(self, nfs_server_id: int) -> NfsStorageInfo:
        """
        NFSサーバーのストレージ情報を取得する

        :param nfs_server_id: NFSサーバーID
        :return:
        """
        return self.client.request(
            endpoint=f"/nfs-servers/{nfs_server_id}/storage-info",
            method="get",
            response_obj=NfsStorageInfo,
        )

    def get_server_vnc_console_keymap(self, server_id: int) -> Keymap:
        """
        サーバーのVNCコンソールのキーマップを取得する

        :param server_id: サーバーID
        :return:
        """
        return self.client.request(
            endpoint=f"/servers/{server_id}/vnc-console-keymap",
            method="get",
            response_obj=Keymap,
        )

    def update_server_vnc_console_keymap(self, server_id: int, data: UpdateKeymap) -> Keymap:
        """
        サーバーのVNCコンソールのキーマップを更新する

        :param server_id: サーバーID
        :param data: 更新データ
        :return:
        """
        return self.client.request(
            endpoint=f"/servers/{server_id}/vnc-console-keymap",
            method="put",
            data=data,
            response_obj=Keymap,
        )

    def get_zones(self) -> Iterable[Zone3]:
        """
        ゾーン一覧を取得する

        :return:
        """
        return self.client.request(
            endpoint="/zones",
            method="get",
            response_obj=Zone3,
        )
