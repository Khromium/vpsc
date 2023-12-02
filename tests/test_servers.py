import unittest

from vpsc.client import Client, APIConfig
from .request_loader import request_loader


class TestServers(unittest.TestCase):
    def setUp(self):
        self.client = Client(config=APIConfig(api_key="test"))

    @request_loader("server_200")
    def test_server(self, patched):
        server = self.client.get_server(server_id=1)
        assert server.id == 0
        patched.assert_called_once_with(
            method="get",
            url=f"{self.client.config.host}/servers/1",
            headers={"Authorization": f"Bearer {self.client.config.api_key}"},
        )

    @request_loader("servers_200")
    def test_servers(self, patched):
        servers = self.client.get_servers()
        assert len(servers) == 1
        assert list(servers)[0].id == 0
        patched.assert_called_once_with(
            method="get",
            url=f"{self.client.config.host}/servers",
            headers={"Authorization": f"Bearer {self.client.config.api_key}"},
        )
