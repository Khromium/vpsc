from __future__ import annotations

from typing import Literal, List, Optional

from pydantic import BaseModel, Field, constr

from models.generated import Settings


class UpdateServer(BaseModel):
    name: str = Field(..., description="""名前""")
    description: str = Field(..., description="""説明""")


class ShutdownServer(BaseModel):
    force: bool = Field(False, description="""強制停止を行うか""")


class ShutdownNfsServer(BaseModel):
    force: bool = Field(False, description="""強制停止を行うか""")


class UpdateNfsServer(BaseModel):
    name: str = Field(..., description="""名前""")
    description: str = Field(..., description="""説明""")


class UpdateHost(BaseModel):
    hostname: str = Field(..., description="""ホスト名""", examples=["example.jp"])


class CreateSwitch(BaseModel):
    name: str = Field(..., description="""名前""")
    description: str = Field(..., description="""説明""")
    zone_code: Literal["tk2", "tk3", "os3", "is1"] = Field(..., description="""ゾーンコード""")


class UpdateSwitch(BaseModel):
    name: str = Field(..., description="""名前""")
    description: str = Field(..., description="""説明""")


class UpdateNfsServerIpv4(BaseModel):
    address: str = Field(..., description="""アドレス""", examples=["198.51.100.2"])
    netmask: str = Field(..., description="""サブネットマスク""", examples=["255.255.254.0"])


class Ptr(BaseModel):
    ptr: str = Field(..., description="""逆引きホスト名""", examples=["example.jp"])


class CreateApiKey(BaseModel):
    name: constr(max_length=100) = Field(..., description="""名前""")
    role: int = Field(..., description="""ロールID""")


class UpdateApiKey(BaseModel):
    name: constr(max_length=100) = Field(..., description="""名前""")
    role: int = Field(..., description="""ロールID""")


class CreateAllowedResources(BaseModel):
    servers: Optional[List[int]] = Field(None, description="""利用できるサーバーのid""", examples=[[1, 2, 3]])
    switches: Optional[List[int]] = Field(None, description="""利用できるスイッチのid""", examples=[[1, 2, 3]])
    nfs_servers: Optional[List[int]] = Field(None, description="""利用できるNFSのid""", examples=[[1, 2, 3]])


class CreateRole(BaseModel):
    name: constr(max_length=100) = Field(..., description="""名前""")
    description: constr(max_length=512) = Field(..., description="""説明""")
    permission_filtering: Literal["enabled", "disabled"] = Field(..., description="""利用できる権限を制限するか""")
    allowed_permissions: List[str] = Field(
        ...,
        description="""利用できる権限。permission_filteringがenabledの場合のみ指定可能。**権限の一覧を取得する**`/permissions`のcode値を指定します。""",
        examples=[["get-server-list", "get-server", "put-server"]],
    )
    resource_filtering: Literal["enabled", "disabled"] = Field(..., description="""利用できるリソースを制限するか""")
    allowed_resources: Optional[CreateAllowedResources] = Field(
        ..., description="""利用できるリソース。resource_filteringがenabledの場合のみ指定可能。"""
    )


class UpdateRole(BaseModel):
    name: constr(max_length=100) = Field(..., description="""名前""")
    description: constr(max_length=512) = Field(..., description="""説明""")
    permission_filtering: Literal["enabled", "disabled"] = Field(..., description="""利用できる権限を制限するか""")
    allowed_permissions: List[str] = Field(
        ...,
        description="""利用できる権限。permission_filteringがenabledの場合のみ指定可能。**権限の一覧を取得する**`/permissions`のcode値を指定します。""",
        examples=[["get-server-list", "get-server", "put-server"]],
    )
    resource_filtering: Literal["enabled", "disabled"] = Field(..., description="""利用できるリソースを制限するか""")
    allowed_resources: Optional[CreateAllowedResources] = Field(
        ..., description="""利用できるリソース。resource_filteringがenabledの場合のみ指定可能。"""
    )


server_sort_query = Literal[
    "service_code",
    "-service_code",
    "name",
    "-name",
    "storage_size_gibibytes",
    "-storage_size_gibibytes",
    "memory_mebibytes",
    "-memory_mebibytes",
    "cpu_cores",
    "-cpu_cores",
    "hostname",
    "-hostname",
    "ipv6_hostname",
    "-ipv6_hostname",
    "ipv4_address",
    "-ipv4_address",
    "ipv6_address",
    "-ipv6_address",
    "zone_code",
    "-zone_code",
    "ipv4_ptr",
    "-ipv4_ptr",
    "ipv6_ptr",
    "-ipv6_ptr",
]


class CreateServerMonitoring(BaseModel):
    name: constr(max_length=255) = Field(..., description="""名前""")
    description: constr(max_length=10000) = Field(..., description="""説明""")
    monitoring_resource_id: str = Field(..., description="""監視リソースID""")
    settings: Settings


class UpdateServerMonitoring(BaseModel):
    name: constr(max_length=255) = Field(..., description="""名前""")
    description: constr(max_length=10000) = Field(..., description="""説明""")
    settings: Settings


class UpdateKeymap(BaseModel):
    layout: Literal["ja", "en-us"] = Field(..., description="""指定したいキー配列の名称""")


class MountDisc(BaseModel):
    disc_id: int = Field(..., description="""ディスクID""")


class UpdateNfsServerInterface(BaseModel):
    switch_id: int = Field(..., description="""スイッチID""", examples=[1])
