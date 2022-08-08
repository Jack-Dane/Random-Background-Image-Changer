
from unittest import TestCase
from unittest.mock import patch, MagicMock

from randomBackgroundChanger.imgur.imgurAuthenticator import PinImgurAuthenticator, _ImgurAuthenticator

MODULE_PATH = "randomBackgroundChanger.imgur.imgurAuthenticator."


class AuthenticatorTest(_ImgurAuthenticator):

    def _startAuthentication(self):
        pass


@patch(f"{MODULE_PATH}requests")
@patch.object(AuthenticatorTest, "_saveTokensToDisk")
@patch.object(AuthenticatorTest, "_startAuthentication", return_value=MagicMock())
class Test_ImgurAuthenticator_refreshToken(TestCase):

    def test_correct_post_parameters(
            self, ImgurAuthenticator_startAuthentication, ImgurAuthenticator_saveTokensToDisk, requests
    ):
        requests.post.return_value = MagicMock()
        requests.post.return_value.json.return_value = {
            "refresh_token": "refresh_token234",
            "access_token": "access_token234"
        }
        imgurAuthenticator = AuthenticatorTest("client_id123", "client_secret123")
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
        imgurAuthenticator = AuthenticatorTest("client_id123", "client_secret123")

        imgurAuthenticator.startAuthentication()

        self.assertEqual("access_token123", imgurAuthenticator._accessToken)
        self.assertEqual("refresh_token123", imgurAuthenticator._refreshToken)

    @patch.object(AuthenticatorTest, "_startAuthentication")
    @patch.object(_ImgurAuthenticator, "_clearCredsFile")
    def test_no_creds_file(self, _clearCredsFile, _startAuthentication, open):
        open.side_effect = FileNotFoundError

        imgurAuthenticator = AuthenticatorTest("client_id123", "client_secret123")

        _startAuthentication.assert_called_once_with()
        _clearCredsFile.assert_not_called()
        self.assertIsNone(imgurAuthenticator._accessToken)
        self.assertIsNone(imgurAuthenticator._refreshToken)

    @patch(f"{MODULE_PATH}json")
    @patch.object(AuthenticatorTest, "_clearCredsFile")
    @patch.object(AuthenticatorTest, "_startAuthentication")
    def test_no_access_token(self, _startAuthentication, _clearCredsFile, json, open):
        json.load.return_value = {
            "other data": "other data 123"
        }

        imgurAuthenticator = AuthenticatorTest("client_id123", "client_secret123")

        _clearCredsFile.assert_called_once_with()
        _startAuthentication.assert_called_once_with()
        self.assertIsNone(imgurAuthenticator._accessToken)
        self.assertIsNone(imgurAuthenticator._refreshToken)


@patch(f"{MODULE_PATH}requests")
@patch.object(PinImgurAuthenticator, "_saveTokensToDisk")
@patch.object(PinImgurAuthenticator, "_startAuthentication", return_value=MagicMock())
class Test_PinImgurAuthenticator__getAccessTokenFromPin(TestCase):

    def test_correct_post_parameters(
            self, ImgurAuthenticator_pinBasedAuthentication, ImgurAuthenticator_saveTokensToDisk, requests
    ):
        requests.post.return_value = MagicMock()
        requests.post.return_value.json.return_value = {
            "refresh_token": "refresh_token234",
            "access_token": "access_token234"
        }
        imgurAuthenticator = PinImgurAuthenticator("client_id123", "client_secret123")
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
