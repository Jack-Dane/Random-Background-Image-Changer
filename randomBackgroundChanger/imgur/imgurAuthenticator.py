
import requests
import webbrowser
import json


class ImgurAuthenticator:

    def __init__(self, clientId, clientSecret, credsFile="creds.json"):
        self._clientId = clientId
        self._clientSecret = clientSecret
        self._credsFile = credsFile
        self._accessToken = None
        self._refreshToken = None
        self._pin = None
        self.startAuthentication()

    @property
    def accessTokenURL(self):
        return "https://api.imgur.com/oauth2/token"

    @property
    def pinAuthenticationURL(self):
        return f"https://api.imgur.com/oauth2/authorize?client_id={self._clientId}&response_type=pin"

    @property
    def _authPostData(self):
        return {
            "client_id": self._clientId,
            "client_secret": self._clientSecret
        }

    @property
    def _accessTokens(self):
        return {
            "access_token": self._accessToken,
            "refresh_token": self._refreshToken
        }

    @property
    def accessToken(self):
        if not self._accessToken:
            self.startAuthentication()
        return self._accessToken

    def _updateTokens(self, response):
        self._accessToken = response["access_token"]
        self._refreshToken = response["refresh_token"]
        self._saveTokensToDisk()

    def refreshToken(self):
        postData = {
            **self._authPostData,
            "refresh_token": self._refreshToken,
            "grant_type": "refresh_token"
        }
        response = requests.post(self.accessTokenURL, data=postData)
        response.raise_for_status()
        self._updateTokens(response.json())

    def _saveTokensToDisk(self):
        with open(self._credsFile, "w") as credsFile:
            json.dump(self._accessTokens, credsFile)

    def startAuthentication(self):
        try:
            with open(self._credsFile, "r") as credsFile:
                creds = json.load(credsFile)
                self._accessToken = creds["access_token"]
                self._refreshToken = creds["refresh_token"]
        except (FileNotFoundError, KeyError) as exception:
            if isinstance(exception, KeyError):
                self._clearCredsFile()
            self._pinBasedAuthentication()

    def _clearCredsFile(self):
        with open(self._credsFile, "w") as credsFile:
            credsFile.truncate(0)

    def _pinBasedAuthentication(self):
        webbrowser.open(self.pinAuthenticationURL)

    def addPin(self, pin):
        self._pin = pin
        self._getAccessTokenFromPin()

    def _getAccessTokenFromPin(self):
        postData = {
            **self._authPostData,
            "grant_type": "pin",
            "pin": self._pin
        }
        response = requests.post(self.accessTokenURL, data=postData)
        response.raise_for_status()
        self._updateTokens(response.json())
