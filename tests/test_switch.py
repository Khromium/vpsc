import unittest

from vpsc.models import CreateSwitch, UpdateSwitch
from vpsc.client import Client, APIConfig
from .patch_request import patch_request


class TestServers(unittest.TestCase):
    def setUp(self):
        self.client = Client(config=APIConfig(api_key="test"))

    @patch_request("switch_201")
    def test_create_switch(self, patched):
        data = CreateSwitch(name="string", description="string", zone_code="tk2")
        result = self.client.create_switch(data=data)
        assert 0 == result.id
        assert "tk2" == result.zone.code
        assert "石狩第1" == result.zone.name
        assert "string" == result.name
        assert "string" == result.description
        patched.assert_called_once_with(
            method="post",
            url=f"{self.client.config.host}/switches",
            headers={"Authorization": f"Bearer {self.client.config.api_key}", "content-type": "application/json"},
            data=data.model_dump_json(exclude_none=True).encode("utf-8"),
        )

    @patch_request("switches_200")
    def test_get_switches(self, patched):
        switches = self.client.get_switches()
        assert 1 == len(switches)
        assert 0 == list(switches)[0].id
        patched.assert_called_once_with(
            method="get",
            url=f"{self.client.config.host}/switches",
            headers={"Authorization": f"Bearer {self.client.config.api_key}"},
        )

    @patch_request("switch_200")
    def test_get_switch(self, patched):
        switch = self.client.get_switch(switch_id=0)
        assert 0 == switch.id
        patched.assert_called_once_with(
            method="get",
            url=f"{self.client.config.host}/switches/0",
            headers={"Authorization": f"Bearer {self.client.config.api_key}"},
        )

    @patch_request("switch_200")
    def test_update_switch(self, patched):
        data = UpdateSwitch(name="string", description="string")
        result = self.client.update_switch(switch_id=0, data=data)
        assert 0 == result.id
        patched.assert_called_once_with(
            method="put",
            url=f"{self.client.config.host}/switches/0",
            headers={"Authorization": f"Bearer {self.client.config.api_key}", "content-type": "application/json"},
            data=data.model_dump_json(exclude_unset=True).encode("utf-8"),
        )

    @patch_request("status_204")
    def test_delete_switch(self, patched):
        result = self.client.delete_switch(switch_id=0)
        assert result is None
        patched.assert_called_once_with(
            method="delete",
            url=f"{self.client.config.host}/switches/0",
            headers={"Authorization": f"Bearer {self.client.config.api_key}", "content-type": "application/json"},
        )
