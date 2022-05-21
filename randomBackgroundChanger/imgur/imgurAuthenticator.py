
import requests
import webbrowser
import json


class ImgurAuthenticator:

    def __init__(self, clientId, clientSecret):
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.accessToken = None
        self.refreshToken = None
        self.pin = None

    @property
    def accessTokenURL(self):
        return "https://api.imgur.com/oauth2/token"

    @property
    def pinAuthenticationURL(self):
        return f"https://api.imgur.com/oauth2/authorize?client_id={self.clientId}&response_type=pin"

    @property
    def authPostData(self):
        return {
            "client_id": self.clientId,
            "client_secret": self.clientSecret
        }

    @property
    def _accessTokens(self):
        return {
            "access_token": self.accessToken,
            "refresh_token": self.refreshToken
        }

    def updateTokens(self, response):
        self.accessToken = response["access_token"]
        self.refreshToken = response["refresh_token"]
        self._saveTokensToDisk()

    def refreshToken(self):
        postData = {
            **self.authPostData,
            "refresh_token": self.refreshToken,
            "grant_type": "refresh_token"
        }
        response = requests.post(self.accessTokenURL, data=postData)
        response.raise_for_status()
        self.updateTokens(response.json())

    def _saveTokensToDisk(self):
        with open("creds.json", "w") as credsFile:
            json.dump(self._accessTokens, credsFile)

    def startAuthentication(self):
        try:
            with open("creds123.json", "r") as credsFile:
                creds = json.load(credsFile)
                self.accessToken = creds["access_token"]
                self.refreshToken = creds["refresh_token"]
        except FileNotFoundError:
            self._pinBasedAuthentication()

    def _pinBasedAuthentication(self):
        webbrowser.open(self.pinAuthenticationURL)
        self.pin = input("Enter Imgur Pin: ")
        self._getAccessTokenFromPin()

    def _getAccessTokenFromPin(self):
        postData = {
            **self.authPostData,
            "grant_type": "pin",
            "pin": self.pin
        }
        response = requests.post(self.accessTokenURL, data=postData)
        response.raise_for_status()
        self.updateTokens(response.json())
