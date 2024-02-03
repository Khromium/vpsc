import unittest

from vpsc.models import UpdateNfsServerIpv4, UpdateNfsServer
from vpsc.client import Client, APIConfig
from .patch_request import patch_request


class TestServers(unittest.TestCase):
    def setUp(self):
        self.client = Client(config=APIConfig(api_key="test"))

    @patch_request("nfs_servers_200")
    def test_nfs_servers(self, patched):
        servers = self.client.get_nfs_servers()
        assert 1 == len(servers)
        assert 0 == list(servers)[0].id
        patched.assert_called_once_with(
            method="get",
            url=f"{self.client.config.host}/nfs-servers",
            headers={"Authorization": f"Bearer {self.client.config.api_key}"},
        )

    @patch_request("nfs_server_200")
    def test_nfs_server(self, patched):
        server = self.client.get_nfs_server(nfs_server_id=0)
        assert 0 == server.id
        patched.assert_called_once_with(
            method="get",
            url=f"{self.client.config.host}/nfs-servers/0",
            headers={"Authorization": f"Bearer {self.client.config.api_key}"},
        )

    @patch_request("status_202")
    def test_update_nfs_server_ipv4(self, patched):
        data = UpdateNfsServerIpv4(address="198.51.100.2", netmask="255.255.254.0")
        result = self.client.update_nfs_server_ipv4(nfs_server_id=0, data=data)
        assert result is None
        patched.assert_called_once_with(
            method="post",
            url=f"{self.client.config.host}/nfs-servers/0/ipv4",
            headers={"Authorization": f"Bearer {self.client.config.api_key}", "content-type": "application/json"},
            data=data.model_dump_json(exclude_none=True).encode("utf-8"),
        )

    @patch_request("nfs_server_200")
    def test_update_nfs_server(self, patched):
        data = UpdateNfsServer(name="name_test", description="description_test")
        result = self.client.update_nfs_server(nfs_server_id=0, data=data)
        assert 0 == result.id
        patched.assert_called_once_with(
            method="put",
            url=f"{self.client.config.host}/nfs-servers/0",
            headers={"Authorization": f"Bearer {self.client.config.api_key}", "content-type": "application/json"},
            data=data.model_dump_json(exclude_unset=True).encode("utf-8"),
        )

    @patch_request("nfs_server_power_status_200")
    def test_get_nfs_server_power_status(self, patched):
        result = self.client.get_nfs_server_power_status(nfs_server_id=0)
        assert "power_on" == result.status
        patched.assert_called_once_with(
            method="get",
            url=f"{self.client.config.host}/nfs-servers/0/power-status",
            headers={"Authorization": f"Bearer {self.client.config.api_key}"},
        )
