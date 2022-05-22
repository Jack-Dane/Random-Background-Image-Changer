
from unittest import TestCase
from unittest.mock import patch, MagicMock

from randomBackgroundChanger.imgur.imgurAuthenticator import ImgurAuthenticator

MODULE_PATH = "randomBackgroundChanger.imgur.imgurAuthenticator."


@patch(f"{MODULE_PATH}requests")
@patch.object(ImgurAuthenticator, "_saveTokensToDisk")
class Test_ImgurAuthenticator_refreshToken(TestCase):

    def test_correct_post_parameters(self, ImgurAuthenticator_saveTokensToDisk, requests):
        requests.post.return_value = MagicMock()
        requests.post.return_value.json.return_value = {
            "refresh_token": "refresh_token234",
            "access_token": "access_token234"
        }
        imgurAuthenticator = ImgurAuthenticator("client_id123", "client_secret123")
        imgurAuthenticator._refreshToken = "refresh_token123"

        imgurAuthenticator.refreshToken()

        requests.post.assert_called_once_with(
            imgurAuthenticator.accessTokenURL,
            data={
                "client_id": "client_id123",
                "client_secret": "client_secret123",
                "refresh_token": "refresh_token123",
                "grant_type": "refresh_token"
            }
        )
        self.assertEqual("refresh_token234", imgurAuthenticator._refreshToken)
        self.assertEqual("access_token234", imgurAuthenticator._accessToken)
        ImgurAuthenticator_saveTokensToDisk.assert_called_once_with()


@patch(f"{MODULE_PATH}open")
class Test_ImgurAuthentictor_startAuthentication(TestCase):

    @patch(f"{MODULE_PATH}json")
    def test_valid_creds_file(self, json, open):
        open.return_value = MagicMock()
        json.load.return_value = {
            "access_token": "access_token123",
            "refresh_token": "refresh_token123"
        }
        imgurAuthenticator = ImgurAuthenticator("client_id123", "client_secret123")

        imgurAuthenticator.startAuthentication()

        self.assertEqual("access_token123", imgurAuthenticator._accessToken)
        self.assertEqual("refresh_token123", imgurAuthenticator._refreshToken)

    @patch.object(ImgurAuthenticator, "_pinBasedAuthentication")
    def test_no_creds_file(self, _pinBasedAuthentication, open):
        open.side_effect = FileNotFoundError
        imgurAuthenticator = ImgurAuthenticator("client_id123", "client_secret123")

        imgurAuthenticator.startAuthentication()

        _pinBasedAuthentication.assert_called_once_with()
        self.assertIsNone(imgurAuthenticator._accessToken)
        self.assertIsNone(imgurAuthenticator._refreshToken)


@patch(f"{MODULE_PATH}requests")
@patch.object(ImgurAuthenticator, "_saveTokensToDisk")
class Test_ImgurAuthentictor__getAccessTokenFromPin(TestCase):

    def test_correct_post_parameters(self, ImgurAuthenticator_saveTokensToDisk, requests):
        requests.post.return_value = MagicMock()
        requests.post.return_value.json.return_value = {
            "refresh_token": "refresh_token234",
            "access_token": "access_token234"
        }
        imgurAuthenticator = ImgurAuthenticator("client_id123", "client_secret123")
        imgurAuthenticator._refreshToken = "refresh_token123"
        imgurAuthenticator._pin = "pin123"

        imgurAuthenticator._getAccessTokenFromPin()

        requests.post.assert_called_once_with(
            imgurAuthenticator.accessTokenURL,
            data={
                "client_id": "client_id123",
                "client_secret": "client_secret123",
                "pin": "pin123",
                "grant_type": "pin"
            }
        )
        self.assertEqual("refresh_token234", imgurAuthenticator._refreshToken)
        self.assertEqual("access_token234", imgurAuthenticator._accessToken)
        ImgurAuthenticator_saveTokensToDisk.assert_called_once_with()
