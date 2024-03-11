import unittest
from unittest import mock

from click.testing import CliRunner

from vpsc.commands import vpsc


class TestCommandServer(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch("vpsc.commands.Client")
        self.addCleanup(patcher.stop)
        self.mock_client = patcher.start().return_value

        patcher = mock.patch("vpsc.commands._print")
        self.addCleanup(patcher.stop)
        self.mock_print = patcher.start()

        self.runner = CliRunner()

    def test_list(self):
        self.mock_client.get_servers.return_value = ["result"]
        result = self.runner.invoke(vpsc, ["server", "list"])
        assert 0 == result.exit_code
        self.mock_client.get_servers.assert_called()
        self.mock_print.assert_called_once_with("result")

    def test_list_id(self):
        self.mock_client.get_server.return_value = "result"
        result = self.runner.invoke(vpsc, ["server", "list", "-id", "12345"])
        assert 0 == result.exit_code
        self.mock_client.get_server.assert_called_once_with(server_id=12345)
        self.mock_print.assert_called_once_with("result")

    def test_update_server(self):
        self.mock_client.update_server.return_value = "result"
        result = self.runner.invoke(vpsc, ["server", "update", "-id", "12345", "-n", "name", "-d", "description"])
        assert 0 == result.exit_code
        self.mock_client.update_server.assert_called_once_with(server_id=12345, data=mock.ANY)
        self.mock_print.assert_called_once_with("result")

    def test_update_server_empty(self):
        self.mock_client.update_server.return_value = "result"
        result = self.runner.invoke(vpsc, ["server", "update", "-id", "12345", "-n", "", "-d", ""])
        assert 0 == result.exit_code
        self.mock_client.update_server.assert_called_once_with(server_id=12345, data=mock.ANY)
        self.mock_print.assert_called_once_with("result")

    def test_update_server_error(self):
        result = self.runner.invoke(vpsc, ["server", "update"])
        assert 2 == result.exit_code

        result = self.runner.invoke(vpsc, ["server", "update", "-id"])
        assert 2 == result.exit_code

    def test_get_power_status(self):
        self.mock_client.get_server_power_status.return_value = "result"
        result = self.runner.invoke(vpsc, ["server", "power-status", "-id", "12345"])
        assert 0 == result.exit_code
        self.mock_client.get_server_power_status.assert_called_once_with(server_id=12345)
        self.mock_print.assert_called_once_with("result")

    def test_get_power_status_error(self):
        result = self.runner.invoke(vpsc, ["server", "power-status", "-id"])
        assert 2 == result.exit_code

    def test_power_on_server(self):
        patcher = mock.patch("vpsc.commands.sleep")
        self.addCleanup(patcher.stop)
        patcher.start()

        self.mock_client.get_server_power_status.return_value = "result"
        result = self.runner.invoke(vpsc, ["server", "power-on", "-id", "12345"])
        assert 0 == result.exit_code
        self.mock_client.power_on_server.assert_called_once_with(server_id=12345)
        self.mock_client.get_server_power_status.assert_called_once_with(server_id=12345)
        self.mock_print.assert_called_once_with("result")

    def test_power_on_server_error(self):
        result = self.runner.invoke(vpsc, ["server", "power-on", "-id"])
        assert 2 == result.exit_code

    def test_shutdown_server(self):
        patcher = mock.patch("vpsc.commands.sleep")
        self.addCleanup(patcher.stop)
        patcher.start()

        self.mock_client.get_server_power_status.return_value = "result"
        result = self.runner.invoke(vpsc, ["server", "shutdown", "-id", "12345"])
        assert 0 == result.exit_code
        self.mock_client.shutdown_server.assert_called_once_with(server_id=12345, force=False)
        self.mock_client.get_server_power_status.assert_called_once_with(server_id=12345)
        self.mock_print.assert_called_once_with("result")

    def test_shutdown_server_force(self):
        patcher = mock.patch("vpsc.commands.sleep")
        self.addCleanup(patcher.stop)
        patcher.start()

        self.mock_client.get_server_power_status.return_value = "result"
        result = self.runner.invoke(vpsc, ["server", "shutdown", "-id", "12345", "-f"])
        assert 0 == result.exit_code
        self.mock_client.shutdown_server.assert_called_once_with(server_id=12345, force=True)
        self.mock_client.get_server_power_status.assert_called_once_with(server_id=12345)
        self.mock_print.assert_called_once_with("result")

    def test_shutdown_server_error(self):
        result = self.runner.invoke(vpsc, ["server", "shutdown", "-id"])
        assert 2 == result.exit_code

    def test_update_server_ptr_record_ipv4(self):
        self.mock_client.get_server.return_value = "result"

        result = self.runner.invoke(vpsc, ["server", "ptr-record", "-id", "12345", "-t", "ipv4", "-h", "example.jp"])
        assert 0 == result.exit_code
        self.mock_client.update_server_ipv4_ptr.assert_called_once_with(server_id=12345, data=mock.ANY)
        self.mock_client.get_server.assert_called_once_with(server_id=12345)
        self.mock_print.assert_called_once_with("result")

        self.mock_client.update_server_ipv4_ptr.reset_mock()
        result = self.runner.invoke(vpsc, ["server", "ptr-record", "-id", "12345", "-t", "IPv4", "-h", "example.jp"])
        assert 0 == result.exit_code
        self.mock_client.update_server_ipv4_ptr.assert_called_once_with(server_id=12345, data=mock.ANY)

    def test_update_server_ptr_record_ipv6(self):
        self.mock_client.get_server.return_value = "result"

        result = self.runner.invoke(vpsc, ["server", "ptr-record", "-id", "12345", "-t", "ipv6", "-h", "example.jp"])
        assert 0 == result.exit_code
        self.mock_client.update_server_ipv6_ptr.assert_called_once_with(server_id=12345, data=mock.ANY)
        self.mock_client.get_server.assert_called_once_with(server_id=12345)
        self.mock_print.assert_called_once_with("result")

        self.mock_client.update_server_ipv6_ptr.reset_mock()
        result = self.runner.invoke(vpsc, ["server", "ptr-record", "-id", "12345", "-t", "IPV6", "-h", "example.jp"])
        assert 0 == result.exit_code
        self.mock_client.update_server_ipv6_ptr.assert_called_once_with(server_id=12345, data=mock.ANY)

    def test_update_server_ptr_record_error(self):
        result = self.runner.invoke(vpsc, ["server", "ptr-record", "-id", "-t", "ipv6", "-h", "example.jp"])
        assert 2 == result.exit_code
        result = self.runner.invoke(vpsc, ["server", "ptr-record", "-id", "12345", "-t", "-h", "example.jp"])
        assert 2 == result.exit_code
        result = self.runner.invoke(vpsc, ["server", "ptr-record", "-id", "12345", "-t", "ipv7", "-h", "example.jp"])
        assert 2 == result.exit_code
        result = self.runner.invoke(vpsc, ["server", "ptr-record", "-id", "12345", "-t", "ipv6", "-h"])
        assert 2 == result.exit_code
