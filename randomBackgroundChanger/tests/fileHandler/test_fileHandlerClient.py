
from werkzeug.exceptions import NotFound
from unittest import TestCase
from unittest.mock import patch, call, MagicMock

from randomBackgroundChanger.fileHandler.fileHandlerClient import FileHandlerClient

MODULE_PATH = "randomBackgroundChanger.fileHandler.fileHandlerClient."


class AuthTestCommon(TestCase):

    def setUp(self):
        self.jsonMock = MagicMock()
        self.jsonMock.json.return_value = {"token": "token"}
        self.fileHandlerClient = FileHandlerClient(
            3000, "clientId", "clientSecret"
        )

    @staticmethod
    def postJson():
        return {
            "clientId": "clientId",
            "clientSecret": "clientSecret"
        }

    @staticmethod
    def deleteJson():
        deleteJson = AuthTestCommon.postJson()
        deleteJson.update(
            {"token": "token"}
        )
        return deleteJson


@patch(MODULE_PATH + "requests")
class Test_FileHandlerClient_nextBackgroundImage(AuthTestCommon):

    def test_ok(self, requests):
        requests.post.return_value = self.jsonMock

        self.fileHandlerClient.nextBackgroundImage()

        self.assertEqual(
            [
                call.post("http://localhost:3000/token", json=AuthTestCommon.postJson()),
                call.post().json(),
                call.post(
                    "http://localhost:3000/change-background",
                    json={},
                    headers={"Authorization": f"Bearer: token"}
                ),
                call.post().raise_for_status(),
                call.delete("http://localhost:3000/token", json=AuthTestCommon.deleteJson())
            ],
            requests.mock_calls
        )


@patch(MODULE_PATH + "requests")
class Test_FileHandlerClient_addPin(AuthTestCommon):

    def test_ok(self, requests):
        requests.post.return_value = self.jsonMock

        self.fileHandlerClient.addPin("abc123")

        self.assertEqual(
            [
                call.post("http://localhost:3000/token", json=AuthTestCommon.postJson()),
                call.post().json(),
                call.post(
                    "http://localhost:3000/imgur-pin",
                    json={"pin": "abc123"},
                    headers={"Authorization": f"Bearer: token"}
                ),
                call.post().raise_for_status(),
                call.delete("http://localhost:3000/token", json=AuthTestCommon.deleteJson())
            ],
            requests.mock_calls
        )


@patch(MODULE_PATH + "requests")
class Test_FileHandlerClient__sendRequest(AuthTestCommon):

    def test_ensure_token_deleted(self, requests):
        requests.post.side_effect = [self.jsonMock, NotFound]

        with self.assertRaises(NotFound):
            self.fileHandlerClient._sendRequest("url")

        requests.assert_has_calls(
            [
                call.post("http://localhost:3000/token", json=AuthTestCommon.postJson()),
                call.post('url', json={}, headers={'Authorization': 'Bearer: token'}),
                call.delete("http://localhost:3000/token", json=AuthTestCommon.deleteJson())
            ]
        )
