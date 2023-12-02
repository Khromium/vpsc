from typing import Literal, List, Optional

from pydantic import BaseModel, IPvAnyAddress


class Storage(BaseModel):
    port: int
    type: Literal["ssd", "hdd"]
    size_gibibytes: int


class Zone(BaseModel):
    code: Literal["tk1", "tk2", "tk3", "os1", "os2", "os3", "is1"]
    name: str


class IPv6Address(BaseModel):
    address: IPvAnyAddress
    gateway: IPvAnyAddress
    nameservers: List[IPvAnyAddress]
    hostname: str
    ptr: str


class IPv4Address(BaseModel):
    address: IPvAnyAddress
    netmask: IPvAnyAddress
    gateway: IPvAnyAddress
    nameservers: List[IPvAnyAddress]
    hostname: str
    ptr: str


class Contract(BaseModel):
    plan_code: int
    plan_name: str
    service_code: str


class PowerStatus(BaseModel):
    status: Literal["power_on", "in_shutdown", "power_off", "installing", "in_scaleup", "migration", "unknown"]


class Server(BaseModel):
    id: int
    name: str
    description: str
    service_type: Literal["linux", "windows"]
    service_status: Literal["on_trial", "link_down_on_trial", "in_use", "link_down"]
    cpu_cores: int
    memory_mebibytes: int
    storage: List[Storage]
    zone: Zone
    options: List[str]
    version: Literal["v1", "v2", "v3", "v4", "v5"]
    ipv4: IPv4Address
    ipv6: Optional[IPv6Address]
    power_status: Literal["power_on", "in_shutdown", "power_off", "installing", "in_scaleup", "migration", "unknown"]


class UpdateServer(BaseModel):
    name: str
    description: str


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
