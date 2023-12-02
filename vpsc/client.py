from types import MappingProxyType
from typing import Optional, Iterable

from pydantic_settings import BaseSettings, SettingsConfigDict

from .api_request import APIRequest
from .models import server_sort_query, Server


class APIConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file="~/.vpsc", env_file_encoding="utf-8", env_prefix="vps_")
    host: str = "https://secure.sakura.ad.jp/vps/api/v7"
    api_key: str


class Client:
    def __init__(self, config: APIConfig):
        self.config = config
        self.header = MappingProxyType({"Authorization": f"Bearer {self.config.api_key}"})

    def get_servers(self, sort: Optional[server_sort_query] = None) -> Iterable[Server]:
        """
        サーバー一覧を取得する
        :param sort: ソート情報
        :return:
        """
        return APIRequest(config=self.config, header=self.header).request(
            endpoint="/servers",
            method="get",
            response_obj=Server,
        )

    def get_server(self, server_id: int) -> Server:
        """
        個別のサーバー情報を取得する
        :param server_id: サーバーid
        :return:
        """
        return APIRequest(config=self.config, header=self.header).request(
            endpoint=f"/servers/{server_id}",
            method="get",
            response_obj=Server,
        )
